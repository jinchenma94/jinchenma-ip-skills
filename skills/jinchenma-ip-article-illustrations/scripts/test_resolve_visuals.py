"""Regression checks for defaults, legacy isolation and portable paths."""
import json
import tempfile
import unittest
from pathlib import Path
from resolve_visuals import BUILTIN, local_file, resolve

class VisualResolutionTests(unittest.TestCase):
    def test_default_and_legacy_are_independent(self):
        current = resolve()
        old = resolve(style="legacy")
        self.assertEqual((current["character_variant"], current["illustration_style"]), ("3d", "jinchenma-3d"))
        self.assertEqual((old["character_variant"], old["illustration_style"]), ("2d", "jinchenma-surrealism"))
        self.assertNotEqual(current["character_reference"], old["character_reference"])
        self.assertNotEqual(current["style_spec"], old["style_spec"])
        self.assertNotIn("palette", old)
        self.assertEqual(resolve(), current)  # Selecting old does not stick.

    def test_explicit_character_variant_is_separate(self):
        selected = resolve(style="3d", variant="2d")
        self.assertEqual(selected["character_variant"], "2d")
        self.assertEqual(selected["illustration_style"], "jinchenma-3d")

    def test_preserved_2d_reference_is_exact(self):
        original = BUILTIN / "assets/turnaround.png"
        legacy = Path(resolve(style="legacy")["character_reference"])
        self.assertEqual(legacy.read_bytes(), original.read_bytes())

    def test_old_custom_manifest_does_not_select_old_style(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = Path(directory) / "custom"
            pack.mkdir()
            (pack / "turnaround.png").write_bytes((BUILTIN / "assets/turnaround.png").read_bytes())
            (pack / "spec.md").write_text("A custom identity")
            (pack / "manifest.json").write_text(json.dumps({"schemaVersion": 1, "id": "custom", "displayName": "Custom", "license": "private", "style": "jinchenma-surrealism", "assets": {"turnaround": "turnaround.png"}, "characterSpec": "spec.md"}))
            selected = resolve(pack)
            self.assertEqual(selected["illustration_style"], "jinchenma-3d")
            self.assertIsNone(selected["character_variant"])
            self.assertEqual(Path(selected["character_reference"]).parent, pack.resolve())

    def test_unknown_style_and_variant_fail(self):
        with self.assertRaises(ValueError): resolve(style="missing")
        with self.assertRaises(ValueError): resolve(variant="missing")

    def test_resource_escape_and_missing_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "pack"
            root.mkdir()
            outside = Path(directory) / "outside.md"
            outside.write_text("outside")
            (root / "link.md").symlink_to(outside)
            for path in ("../outside.md", str(outside), "link.md", "missing.md"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    local_file(root, path)

if __name__ == "__main__":
    unittest.main()
