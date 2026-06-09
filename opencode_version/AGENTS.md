# AGENTS.md

opencode 在本工作区的运行指引。本文件等价于 Claude Code 的 `CLAUDE.md`（opencode 同时存在 `AGENTS.md` 与 `CLAUDE.md` 时只读 `AGENTS.md`），由 opencode 自动加载进上下文。

## 这个工作区是什么

不是软件代码库，而是一个**专利侵权分析工作区**。没有 build / lint / test 工具链。全部"逻辑"集中在一个 opencode skill 里，其余都是输入数据（专利 PDF）和将要生成的分析报告。

这是用来**测试 opencode 跑 `patent-infringement-check` skill 效果**的沙盒：`专利集/<ID>/` 下目前**只有输入 PDF**，所有报告由 skill 现场生成。

目录布局：

- `专利集/` — 所有专利工作的根。每个专利一个子文件夹，以专利号命名（`专利集/<PATENT_ID>/`），当前各自只含一份 `<PATENT_ID>.pdf`（输入）。skill 运行后会在同一文件夹内生成 `<PATENT_ID>.md`（专利原文）、各阶段报告（`<PATENT_ID>"潜在应用场景及侵权特征".md` 等）和 `候选/NN-<slug>/` 每候选取证文件夹。
- `.opencode/skills/patent-infringement-check/SKILL.md` — 主"代码"。一条 7 步流水线，把一个输入专利转成一串分析报告。opencode 通过内置 `skill` 工具自动发现并按需加载。
- `.opencode/skills/patent-infringement-check/scripts/*.py` — Python 辅助脚本（全部**无 LLM**，纯文件 IO / HTTP / 解析）：`fetch_patent.py`（Step 1 抓原文）、`slice_patent.py`（Step 2 切片，省 95%+ token）、`init_candidates.py`（Step 6.0 建候选目录）、`compile_step7.py`（Step 7 汇总）、`write_report.py`（把 ASCII 临时名重命名成全角引号文件名）。
- `opencode.json` — opencode 配置。关键点：为内置 `general` subagent 开启了 `bash`（Step 6 取证必需，opencode 默认对 subagent 禁用 bash）。

## 工作如何完成

当用户给出专利 ID / 路径，或要求检测某专利是否被侵权（侵权 / 违约 / 排查 / 调查 / 检测 / 看看谁在用），`patent-infringement-check` skill 自动触发。它跑 7 个有序步骤，每步把一份 markdown 报告写进**输入专利所在的同一目录**：

1. `<PATENT_ID>.md` — 专利原文（`scripts/fetch_patent.py`；回退 `webfetch` / 本地 PDF 经 `pdf` 解析）
2. `<PATENT_ID>"潜在应用场景及侵权特征".md` — 读切片后的专利，写场景 + 独立权利要求 + 侵权特征 F1-Fk
3. `<PATENT_ID>"潜在使用组织".md` — 每场景列真实存在的知名 / 独角兽组织
4. `<PATENT_ID>"潜在侵权产品初选".md` — 每组织列具体已商用产品
5. `<PATENT_ID>"潜在侵权产品-全".md` — 技术词驱动 `websearch` 长尾扩展 + 产品/技术归并，按侵权可能性降序
6. `候选/NN-<slug>/_verdict.md`（每候选一份）— 用 `task` 工具为默认前 20 个候选各 spawn 一个 `general` subagent（react 模式：`websearch` → 读 → 精修 → `webfetch`/curl → 写 verdict）
7. `<PATENT_ID>"违约列表".md` — 按"第 N 档"标签排序的终筛清单（`scripts/compile_step7.py`，纯模板汇总）

每步从磁盘读上一步输出，所以必须先写盘再进下一步。用 `todowrite` 跟踪 7 步。

**LLM 分工**：所有 LLM 推理由模型自己做——主（primary）agent 跑 Steps 2-5，每候选一个 `general` subagent 跑 Step 6。Step 1 / Step 6.0 init / Step 7 是纯 Python。

## opencode 专属注意事项

- **工具名**：SKILL.md 正文沿用 Claude 习惯名（`WebSearch` / `WebFetch` / `Read` / `Write` / `Edit` / `Grep` / `TodoWrite`），对应 opencode 的 `websearch` / `webfetch` / `read` / `write` / `edit` / `grep` / `todowrite`，语义一致。SKILL.md 顶部"opencode 运行说明"有完整映射表。
- **subagent**：Step 6 用 `task` 工具，`subagent_type` / agent 名填 `general`。`opencode.json` 已为 `general` 开启 `bash`——这是 Step 6 能 curl 兜底、读本地 PDF、写候选目录的前提。
- **websearch**：opencode 的 `websearch` 走 Exa，需 opencode 侧已配置可用。若不可用，按全局约束写"未检索到公开来源"，**不要伪造**。
- 首次运行前装依赖：`pip install requests beautifulsoup4 lxml pdfplumber pypdf`。

## 容易踩错的约定

- **文件名用中文全角引号** — 具体是 **U+201C（`"`）+ U+201D（`"`）**，不是 ASCII `"`、不是「」/《》/`''`。字形在多数字体下几乎一样，靠肉眼分辨不可靠；所有带全角引号的报告一律由 Python 脚本（`write_report.py`）写出，模型只需对这些文件做 `read` / `edit`。
- 报告永远写在**专利自己的子文件夹内**（`专利集/<patent_id>/`），不在仓库根或 `专利集/` 根。若输入 PDF 在 `专利集/` 根，skill 先建子文件夹并把 PDF 移进去。
- 输出语言跟随专利原文语言（中文专利 → 中文报告；仅 `<PATENT_ID>.md` 保留专利原文）。
- 侵权候选的时间闸：只有发表于**专利授权日之后**的材料才算数；现有技术（prior art）无关。
- **永远不要下"已构成侵权"的确定结论** — 本 skill 产出线索与证据链，不是法律意见。每份终报告都要含免责声明。
- 永远不要伪造引用。`websearch` / `webfetch` 查不到就写"未检索到公开来源"，继续下一步。
- **0 命中 ≠ 已排除**：状态机硬约束。0 命中（及"手段不同 / 非互斥手段 / 文档没提"）只能落"公开资料不足（未确定）"档，不能升"已排除"。

## 修改 skill

行为由两个面定义：`.opencode/skills/patent-infringement-check/SKILL.md`（7 步流水线、触发词、模板、Step 6 subagent 协议、全局约束——几乎所有行为规则在此）与 `scripts/*.py`（无 LLM，机械的解析 / 模板 / 重命名逻辑）。改动下次调用即生效。

执行过程中若发现更优执行方式（更准的检索 query、漏掉的判定标准、冗余/缺失字段等），**先把当前任务跑完**，再在最终回复里明确提出改进建议（观察到的问题 + 建议改法 + 预计好处），**等用户确认后再编辑** SKILL.md / scripts。不要静默修改。
