# 画风选择与加载

本文件只负责选择，不混写各套画风规则。入口为 `assets/style-packs/catalog.json`，所有运行资源都在当前 Skill 内，安装后不依赖仓库根目录的设计资料。

## 默认与明确选择

| 本次用户要求 | 插图画风 | 内置人物版本 |
| --- | --- | --- |
| 未指定、默认、3D、新画风 | `jinchenma-3d` | `3d` |
| 旧版、2D 风格、旧超现实隐喻风格 | `jinchenma-surrealism` | `2d` |
| 明确分别指定人物和画风 | 按指定画风 | 按指定人物版本 |

普通的“概念图”“有隐喻”或“让物件悬浮”不表示切换旧版，仍使用默认 3D。只说“2D 人物”时改人物参考版本，插图画风仍为默认；只说“2D 风格”时选择完整旧组合。

每次新任务没有明确指定时使用默认 3D。不要持久化上次的旧版选择，不从旧人物 manifest 的 `style` 字段隐式激活旧画风。自定义 IP 保留已选身份，画风按本次要求选择。

## 独立资源

各风格包位于 `assets/style-packs/<style-id>/`，只读取本次选定包的 `manifest.json`：

- `styleSpec`：画风完整规则。
- `promptTemplate`：该画风的提示模板。
- `palette`：存在时读取该包配色；缺失时不套用另一个风格包的配色。
- `examples`：可按需查看的画风样图，只参考材质和布局原则，不复制人物身份、姿势和具体构图。
- `defaultCharacterVariant`：只为内置人物决定未明确指定的参考版本。

从各 manifest 所在目录解析相对路径。只加载一个风格包，不拼接两套模板；人物身份只来自当前 IP 的本次版本。

## 可核验解析

有 Python 时从 Skill 根目录运行：

```sh
python3 scripts/resolve_visuals.py
python3 scripts/resolve_visuals.py --style legacy
python3 scripts/resolve_visuals.py --style jinchenma-3d --variant 2d
```

自定义人物传入已验证的 `--ip-pack <人物包目录>`。解析器只读，不写配置、人物或配色。未指定时输出默认 3D；未知风格或损坏路径报告错误，不静默改成另一套风格。没有 Python 时按本文件与 manifest 手动解析。

解析结果给出人物参考、角色规范、画风规范、提示模板和可选配色的实际路径。只把本次选中风格的完整规则与模板用于生成。公开资料与生成记录仍使用仓库内相对路径。

## 模式边界

文章插图使用所选包完整画风。截图 IP 讲解继续读取 `references/screenshot-ip-mode.md`，保护原截图，仅让当前人物按选定版本和画风出现；原界面不接受 3D 重绘、白底替换或旧版超现实关系。
