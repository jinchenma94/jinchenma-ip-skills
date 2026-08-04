# Builder IP 包格式与写入规则

## 默认根目录

固定使用 `~/.agents/jinchenma-ip-builder`。

目录结构：

```text
<builder-home>/
└── packs/
    └── <ip-id>/
        ├── manifest.json
        ├── assets/
        │   └── turnaround.png
        └── references/
            └── character-spec.md
```

Builder 根目录不可写时报告错误并停止写入。私人包保存在 Builder 固定目录，不写入当前代码仓库。

Builder 根目录保存可携带 IP 包；文章人物 IP 和当前人物配置保存在文章插图 Skill 的独立目录。

## `ip-id` 与版本

- 使用简短、稳定、可读的英文小写 kebab-case，例如 `alex-creator`。
- 不使用空格、绝对路径、`..`、斜杠或控制字符。
- `jinchenma` 是内置默认人物的保留 `ip-id`，自定义包不要使用该值。
- 同名目录不存在时使用原 `ip-id`。
- 同名目录已经存在时不要覆盖，依次尝试 `<ip-id>-v2`、`-v3`，直到找到未使用的 `ip-id`。
- 用户明确指定其他 `ip-id` 时遵循用户选择，并继续执行非覆盖检查。

## manifest.json

必须包含以下字段：

```json
{
  "schemaVersion": 1,
  "id": "alex-creator",
  "displayName": "Alex Creator",
  "style": "jinchenma-surrealism",
  "assets": {
    "turnaround": "assets/turnaround.png"
  },
  "characterSpec": "references/character-spec.md",
  "license": "private"
}
```

规则：

- `schemaVersion` 当前为 `1`。
- `id` 是人物的 `ip-id`，必须与包目录名一致。
- `style` 描述文章插图艺术风格，不是人物身份；自定义包默认使用 `jinchenma-surrealism`。
- `assets.turnaround` 和 `characterSpec` 只使用相对于当前包目录的路径。
- 拒绝绝对路径、`..` 路径穿越，以及解析后离开包目录的符号链接。
- `license` 对自定义包默认为 `private`；不得自动继承 Jinchenma 默认资产的 CC BY 4.0。
- 只有公开包确实需要署名时才增加可选的 `attribution` 字段。

## character-spec.md

使用以下固定章节：

```markdown
# <显示名称> 角色规范

## 角色定位
## 固定身份特征
## 标志性服装与配件
## 允许变化
## 禁止漂移
## 生图提示词片段
## 一致性检查清单
```

写入可观察、可执行且经过用户确认的视觉规则，不写原始照片路径、私人背景资料或未确认的推断。

## 完成验证

确认：

1. 包目录和 `manifest.json.id` 一致。
2. 三视图与角色规范都存在。
3. 两个相对路径解析后仍位于当前包目录内。
4. 三视图是图片文件，且包含同一角色的正面、侧面、背面。
5. 自定义包的许可没有被错误标为 CC BY 4.0。
6. Builder 输出目录符合本文件定义，只包含可携带 IP 包。
