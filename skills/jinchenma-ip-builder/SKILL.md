---
name: jinchenma-ip-builder
description: 从一张清晰人物照片或已有角色三视图创建、校验并保存可携带的个人 IP 包，生成统一的正面、侧面、背面三视图和 character-spec.md。适用于创建个人 IP、角色设定、三视图、character turnaround、IP pack、avatar builder、character consistency 等任务。
---

# Jinchenma 个人 IP 构建器

## 开始前

完整读取以下文件：

- `references/turnaround-workflow.md`：输入要求、三视图生成和一致性检查。
- `references/ip-pack-format.md`：可携带包的目录、字段、安全和非覆盖规则。

将 `assets/ip-pack-template/` 作为新建包的结构模板；替换模板值，不原样保留尖括号占位符。

## 确认输入和目标

1. 接受一张清晰人物照片，或一张已经完成的角色三视图。
2. 收集缺失的关键信息：IP 显示名称、标志性服装、配件、必须固定的特征、允许变化和禁止出现的特征。
3. 将人物唯一标识 `ip-id` 规范化为简短的英文小写 kebab-case。
4. 使用固定目录 `~/.agents/jinchenma-ip-builder` 保存个人 IP 包。目录不可写时报告错误并停止写入。
5. 同一 `ip-id` 的包已存在时不覆盖；默认使用下一个可用的 `-v2`、`-v3` 版本，用户也可以指定新的 `ip-id`。

只询问真正影响身份一致性的缺失信息。已有三视图和文字设定足够时直接继续。

## 保护真人照片

- 只把原始真人照片作为当前生成过程的视觉参考。
- 不复制、移动或保存原始照片到 IP 包、Skill、文章图片目录或其他长期目录。
- 不在 `manifest.json`、`character-spec.md`、生成提示词或最终报告中记录原始照片的本机路径。
- 不从照片推断或记录姓名、住址、联系方式、证件、单位等无关隐私。
- 若输入是已完成的卡通三视图，可在用户确认后将其作为包内唯一角色视觉资产。

## 创建三视图

按照 `references/turnaround-workflow.md` 构建同一角色的正面、侧面和背面视图。三视图是一个角色的多角度参考，不是三名角色。

- 有图像生成能力时，直接生成一张统一画布上的三视图，并使用输入照片或已有三视图作为参考。
- 没有图像生成能力时，输出可以交给生图工具直接使用的完整三视图 brief；明确说明尚未创建可用 IP 包，不伪造文件。
- 用户提供的已有三视图符合规范时，不强制重画；先检查一致性，再请用户确认。
- 用户确认后，将最终图保存为包内 `assets/turnaround.png`。不要保存到 `.jinchenma-assets/`。

## 生成角色规范

只在用户确认三视图后生成 `references/character-spec.md`。至少包含：

- 角色定位。
- 固定身份特征。
- 标志性服装与配件。
- 允许变化。
- 禁止漂移。
- 可复用的生图提示词片段。
- 一致性检查清单。

以三视图中可见且用户确认的事实为准。不要把生成过程中的偶然细节升级为固定规则。

## 写入可携带 IP 包

1. 在 Builder 根目录创建 `packs/<ip-id>/assets/` 和 `packs/<ip-id>/references/`。
2. 写入确认后的 `assets/turnaround.png`。
3. 写入 `references/character-spec.md`。
4. 写入符合 `references/ip-pack-format.md` 的 `manifest.json`，自定义包的 `license` 默认为 `private`。
5. 验证包内相对路径、文件存在性和包目录边界。

写文件前检查目标。任何已有包、图片、规范或 manifest 都不得静默覆盖。

## 交付

报告以下结果：

- `ip-id` 和显示名称。
- 包目录的绝对路径。
- 三视图和角色规范的绝对路径。
- 仍需人工关注的一致性问题。
- 如需用于文章插图，提示用户在 `jinchenma-ip-article-illustrations` 首次初始化或切换人物时导入此包。

Builder 的交付结果是位于 Builder 根目录下的完整个人 IP 包。人物导入、当前人物选择和切换由 `jinchenma-ip-article-illustrations` 处理；`.jinchenma-assets/` 用于文章插图成品。
