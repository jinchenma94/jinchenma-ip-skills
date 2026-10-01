#!/usr/bin/env python3
"""Resolve a read-only character/style selection from local manifests."""
import argparse
import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
BUILTIN = SKILL_ROOT / "assets/ip-packs/jinchenma"
STYLES = SKILL_ROOT / "assets/style-packs"

def read_json(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object: {path}")
    return value

def local_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("Resource path must be a nonempty relative POSIX path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Invalid resource path: {value}")
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"Missing or escaped resource: {value}")
    return str(target)

def resolve(ip_pack=BUILTIN, style=None, variant=None):
    pack = Path(ip_pack).resolve()
    manifest = read_json(pack / "manifest.json")
    if manifest.get("schemaVersion") not in (1, 2):
        raise ValueError("Unsupported IP schemaVersion")
    ip_id = manifest.get("id")
    if not isinstance(ip_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ip_id):
        raise ValueError("Invalid IP id")
    if ip_id != pack.name:
        raise ValueError("IP id must match the pack directory")
    for key in ("displayName", "license"):
        if not isinstance(manifest.get(key), str) or not manifest[key]:
            raise ValueError(f"Missing {key}")
    # A legacy IP manifest's style field never selects an illustration style.
    catalog = read_json(STYLES / "catalog.json")
    style_id = style or catalog["defaultStyle"]
    aliases = {"3d": "jinchenma-3d", "2d": "jinchenma-surrealism", "legacy": "jinchenma-surrealism"}
    style_id = aliases.get(style_id, style_id)
    if style_id not in catalog["styles"]:
        raise ValueError(f"Unknown illustration style: {style_id}")
    style_path = Path(local_file(STYLES, catalog["styles"][style_id]))
    style_manifest = read_json(style_path)
    if style_manifest.get("schemaVersion") != 1 or style_manifest.get("id") != style_id:
        raise ValueError("Invalid style manifest")
    variants = manifest.get("variants", {})
    if not isinstance(variants, dict):
        raise ValueError("IP variants must be an object")
    chosen_variant = variant
    if chosen_variant is None and variants:
        chosen_variant = (style_manifest["defaultCharacterVariant"] if pack == BUILTIN.resolve()
                          else manifest.get("defaultVariant"))
    if chosen_variant is not None:
        if chosen_variant not in variants:
            raise ValueError(f"IP does not provide variant: {chosen_variant}")
        character = variants[chosen_variant]
    else:
        character = manifest
    assets = character.get("assets")
    if not isinstance(assets, dict):
        raise ValueError("Missing character assets")
    reference = local_file(pack, assets.get("turnaround"))
    if Path(reference).suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
        raise ValueError("Unsupported character reference image format")
    style_root = style_path.parent
    result = {
        "ip_id": ip_id, "display_name": manifest["displayName"],
        "character_variant": chosen_variant, "illustration_style": style_id,
        "character_reference": reference,
        "character_spec": local_file(pack, character.get("characterSpec")),
        "style_spec": local_file(style_root, style_manifest.get("styleSpec")),
        "prompt_template": local_file(style_root, style_manifest.get("promptTemplate")),
        "style_examples": [local_file(style_root, p) for p in style_manifest.get("examples", [])],
    }
    if "reference" in assets:
        result["character_supplement"] = local_file(pack, assets["reference"])
    if "palette" in style_manifest:
        result["palette"] = local_file(style_root, style_manifest["palette"])
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ip-pack", type=Path, default=BUILTIN)
    parser.add_argument("--style", help="Style id or alias: 3d, 2d, legacy")
    parser.add_argument("--variant", choices=("3d", "2d"), help="Explicit character reference variant")
    args = parser.parse_args()
    try:
        result = resolve(args.ip_pack, args.style, args.variant)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Visual selection failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
