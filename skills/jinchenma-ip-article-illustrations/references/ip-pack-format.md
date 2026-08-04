# 文章人物 IP：初始化、导入与切换

## 独立目录

固定使用 `~/.agents/jinchenma-ip-article-illustrations` 作为文章人物主目录。

目录结构：

```text
<article-home>/
├── config.json
└── ips/
    └── <ip-id>/
        ├── manifest.json
        ├── assets/
        │   └── turnaround.png
        └── references/
            └── character-spec.md
```

内置默认 IP 位于 Skill 自身的 `assets/ip-packs/jinchenma/`，不需要复制到文章人物主目录。

运行时人物统一保存在文章 Skill 的 `ips/`。Builder 目录中的完整 IP 包经过用户选择后复制为文章人物 IP。Builder 和文章 Skill 都使用 `ip-id` 作为人物唯一标识。

## config.json

文章 Skill 独立维护：

```json
{
  "schemaVersion": 1,
  "activeIp": "jinchenma"
}
```

要求：

- `schemaVersion` 必须为 `1`。
- `activeIp` 必须是非空、无斜杠、无 `..` 的 `ip-id`。
- 只有人物 IP 已经复制并通过验证后，才将其 `ip-id` 写入 `activeIp`。
- 配置损坏时报告问题，不静默覆盖；本次任务使用内置金尘马。
- 配置指向缺失或损坏的自定义 IP 时提示错误，本次使用内置金尘马，但不自动修改配置。

## 首次初始化

当 `config.json` 不存在时：

1. 在可交互场景先提示：`当前默认使用 Jinchenma。是否要更换为你自己的 IP 形象？`
2. 用户选择更换时，询问人物来源。选择 Builder 生成的 IP 时执行“从 Builder 导入”；选择其他来源时执行“从外部文件导入”。
3. 用户选择不更换时使用内置金尘马；文章主目录可写时写入 `activeIp: jinchenma`。
4. 用户开始更换但没有完成导入时，本次使用内置金尘马。
5. 宿主无法交互时，本次直接使用内置金尘马，不强制创建配置。

不要因为初始化问题阻断文章分析或生成。

## 从 Builder 导入

Builder 主目录固定为 `~/.agents/jinchenma-ip-builder`。

导入流程：

1. 只扫描 `<builder-home>/packs/*/manifest.json`。
2. 按“人物 IP 验证”检查每个包；不读取原始照片或无关文件。
3. 没有完整包时说明情况，并引导用户先运行 `jinchenma-ip-builder`。
4. 即使只有一个完整包，也显示名称和 `ip-id` 并请用户确认；有多个包时列出全部有效包供用户选择。
5. 用户确认后，只复制 manifest、三视图和角色规范到文章 Skill 的 `ips/<ip-id>/`。
6. 复制后重新验证目标人物 IP，通过后再激活。

这是一次性导入。Builder 中的后续修改不会自动同步；用户需要明确重新导入。

## 从外部文件导入

要求用户同时提供：

- 一张包含同一角色正面、侧面、背面的三视图。
- 一份符合固定章节的 `character-spec.md`。
- IP 显示名称；据此生成英文小写 kebab-case `ip-id`。

缺少文字规范时停止导入，引导用户把现有三视图交给 `jinchenma-ip-builder` 补全为完整包。不要只凭三视图创建文章人物 IP。

文件齐全时：

1. 检查文件存在、可读，三视图是支持的图片格式，文字规范包含角色定位、固定身份、服装配件、允许变化、禁止漂移、提示词片段和检查清单。
2. 在文章 Skill 的目标人物 IP 中使用标准相对路径。
3. 创建 `manifest.json`，设置 `style: jinchenma-surrealism`。没有明确来源许可时使用 `license: private`；来源文件或用户明确提供有效许可与署名时如实保留，不把已有公开许可重新标记为 private。
4. 只复制三视图和文字规范，不复制原始照片、同目录其他文件或本机路径记录。
5. 验证目标人物 IP 后再激活。

## 同一 `ip-id`

- 目标 `ip-id` 不存在时直接导入。
- 目标 `ip-id` 已存在且三视图、角色规范及 manifest 核心字段一致时，复用已有人物 IP 并允许激活。
- 目标 `ip-id` 已存在但内容不同时，不覆盖；依次使用 `<ip-id>-v2`、`-v3`。
- 重新导入 Builder 更新包时同样执行此规则。

## 切换人物

用户明确要求查看或切换人物时：

1. 列出内置 `jinchenma` 和 `ips/` 下所有通过验证的人物 IP。
2. 显示 `displayName`、`ip-id` 和当前激活标记，不展示无关私人描述。
3. 用户选择已导入人物后，将其 `ip-id` 写入 `activeIp`。
4. 用户选择尚未导入的 Builder 包或外部人物时，先完成对应导入流程。
5. 不把人物切换描述成画风切换。

## 人物 IP 验证

`manifest.json` 必须包含：

```json
{
  "schemaVersion": 1,
  "id": "example-ip",
  "displayName": "Example IP",
  "style": "jinchenma-surrealism",
  "assets": {
    "turnaround": "assets/turnaround.png"
  },
  "characterSpec": "references/character-spec.md",
  "license": "private"
}
```

验证规则：

- 必需字段存在，类型正确，`schemaVersion` 为 `1`。
- `manifest.id` 是人物的 `ip-id`，必须与人物 IP 目录名一致。
- `style` 为 `jinchenma-surrealism`；它表示文章艺术风格，不表示人物身份。
- `assets.turnaround` 和 `characterSpec` 是相对于人物 IP 目录的路径。
- 拒绝绝对路径、`..` 路径穿越和解析后离开当前人物 IP 目录的符号链接。
- 两个目标文件必须存在且可读。
- 自定义 IP 在没有明确来源许可时默认 `license: private`，不自动继承内置包的 CC BY 4.0，也不覆盖外部素材已有的明确许可与署名。

## 解析与运行提示

每次任务只解析一个人物 IP：

1. 读取 `config.json.activeIp`。
2. 值为 `jinchenma` 时使用内置默认 IP。
3. 其他值只从 `<article-home>/ips/<activeIp>/` 读取。
4. 无效时提示并为本次任务回退到内置金尘马。

选定后只加载当前人物 IP 的三视图和角色规范。视觉生成工具支持参考图片时，直接传入 `assets.turnaround`；三视图中的三个人形是同一角色的三个角度。

在开始生成文章插图前输出中间提示：

```text
当前使用 IP：<displayName> (<ip-id>)
```

## 隔离与隐私

- 不把 Builder 包持续作为运行时依赖；导入后使用文章 Skill 自己的副本。
- 不把私人 IP 复制进 Skill 仓库或 `.jinchenma-assets/`。
- 不保存外部原始照片，也不把来源绝对路径写入 manifest 或角色规范。
- 不把自定义 IP 的身份规则合并进内置金尘马。
- 文章插图任务只读使用已导入的人物 IP，不修改其中的三视图和角色规范。
