# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Not a software codebase — a **patent-infringement analysis workspace**. There is no build, lint, or test toolchain. The "logic" lives in a single Claude skill; everything else is input data and generated reports.

Directory layout:

- `专利集/` — root for all patent work. Each patent gets its own subfolder named with the patent ID, e.g. `专利集/CN114531405B/`. The subfolder contains the input PDF, all generated reports (`<id>.md`, `<id>"专利介绍".md`, etc.), `.cache/` for unattributed helper PDFs, and `候选/<candidate_slug>/` per-候选 evidence folders (created by Step 5b). Patent ID = filename stem.
- Per-候选 evidence folders hold downloaded materials (PDFs / scraped HTML / GitHub raws), an `_sources.md` index, and `_verdict.md` with the per-document sub-agent合议结果. Local archival is required before any "已排除" or "确认侵权" verdict.
- `.claude/skills/patent-infringement-check/SKILL.md` — the main "code". A six-step pipeline skill that turns one input patent into a chain of analysis reports.
- `.claude/skills/pdf/` — supporting skill for PDF text/table extraction (wraps `pdfplumber` / `pypdf`). Used by Step 1 as a fallback when Google Patents `WebFetch` is blocked, and by Step 5 for extracting evidence from downloaded SIGCOMM / NSDI / vendor whitepaper PDFs. Requires `pip install pypdf pdfplumber` (already done locally; may need install elsewhere).

## How work gets done here

When the user provides a patent path (e.g. `专利集/CN114531405B.pdf`) or asks to check a patent for unauthorized use / 侵权 / 违约, the `patent-infringement-check` skill auto-triggers. It runs six sequenced steps, each writing one markdown report **into the same directory as the input patent**:

1. Acquire patent text → `<id>.md` (PDF → Markdown via Google Patents `WebFetch`, fallback to local PDF Read; skip if `.md` already present)
2. `<id>"专利介绍".md`
3. `<id>"潜在应用场景".md`
4. `<id>"潜在使用组织".md`
5. `<id>"潜在违约".md` (initial screen via `WebSearch`)
6. `<id>"违约列表".md` (re-verified shortlist)

Each step reads the previous step's output from disk, so they must be written before moving on. Use `TodoWrite` to track the six steps.

## Conventions that are easy to get wrong

- **Filename format uses Chinese full-width quotes** — specifically **U+201C (`"`) + U+201D (`"`)**, not ASCII `"` (U+0022), not 「」 (U+300C/U+300D), not 《》, not `''` (U+2018/U+2019). The displayed glyphs `"`/`"` and `"` look almost identical in many fonts; if you copy-paste a filename, eyeball isn't enough — verify the code points.
- **Writing these filenames on Windows**: the `Write` tool **cannot** open a path containing the full-width quotes directly (the host normalizes them and rejects with `ENOENT`). The required workaround:
  1. `Write` to a temp filename (no quotes), e.g. `<id>_stepN_temp.md`.
  2. Use `PowerShell` + `[System.IO.File]::Move` with `[char]0x201C` / `[char]0x201D` to rename. Avoid `Move-Item -LiteralPath '..."..."...'` — PowerShell 5.1 will reject it as "Illegal characters in path".
  Downstream steps look up files by exact name, so the rename must succeed before the next step reads them.
- Reports always go **inside the patent's own subfolder** (`专利集/<patent_id>/`), never at repo root or directly under `专利集/`. If the input PDF is still at `专利集/<patent_id>.pdf`, the skill creates the subfolder and moves the input in before generating reports.
- Output language follows the patent's original language (CN patents → Chinese reports).
- Time gate for infringement candidates: only material **published after the patent's grant date** counts. Prior art is irrelevant here.
- Never output a definitive "已构成侵权" conclusion — this skill produces leads and evidence chains, not legal opinions. Every final report must include a disclaimer.
- Never fabricate citations. If `WebSearch` / `WebFetch` returns nothing, write "未检索到公开来源" and move on.

## Modifying the skill

The skill's behaviour is defined entirely by [.claude/skills/patent-infringement-check/SKILL.md](.claude/skills/patent-infringement-check/SKILL.md). To change the pipeline (add steps, tweak templates, adjust trigger phrases), edit that file's frontmatter `description` (controls auto-trigger) or body (controls behaviour). No code generation or compilation step is involved — edits take effect on the next skill invocation.

**主动提出改进建议**：在执行 skill 的过程中，如果你发现某个步骤有更优的执行方法（例如更准确的检索 query 模板、更可靠的 PDF 解析方式、漏掉的常见判定标准、模板里冗余或缺失的字段、可以并行化的环节、容易让模型走偏的措辞等），**先把当前任务跑完**，然后在最终回复里向用户**明确提出改进建议**——说明：1) 你观察到的问题；2) 建议如何修改 [.claude/skills/patent-infringement-check/SKILL.md](.claude/skills/patent-infringement-check/SKILL.md)；3) 预计带来的好处。**等用户确认后再实际编辑 SKILL.md**，不要静默修改。这样 skill 会随着每次实战逐步进化。

### 改进 skill 时的"标准答案隔离与一致性"硬约束（**最先满足 — 否则 dogfood 失效**）

`正确答案.md` 保存了若干评测专利的"标准答案"——它是用来**事后**评估 SKILL / 主 agent 表现的基准，不允许被 SKILL 内化。SKILL 必须对评测专利和其他专利**表现一致**——否则 SKILL 等于针对评测集作弊，dogfood 信号失效。

**强制规则**：

1. **任何形式的标准答案都不允许出现在 SKILL.md / CLAUDE.md / 任何被 skill 加载的辅助文档中**——包括正确候选名、其代表性产品名、生态相关 keyword、代表性 vendor 名、典型论文 / 上游项目名 / 配置参数 / commit 关键词等任何可让主 agent 跳 1–2 步链到标准答案的辅助信息。

2. **不允许任何"针对评测用例的暗示性文字"**——即便用了"某 X 类专利"形式的占位符也属于暗示，因为如果占位符里的领域恰好对应评测集中存在的专利，就会泄露评测集的领域分布。**领域 / 场景 / 主分类号 / 标准号 / 标志性技术词**等任何能在概率上把读者引向评测专利的信息一律禁止。

3. **不允许写"实测案例 / 实测教训 / 曾发生 / 本规则源自……失误"等案例锚点**——SKILL 是机制层文档，规则的正确性必须由其内在逻辑独立成立，而非靠引用过去的失败案例做正当性背书。把案例叙事写入 SKILL 会带来 3 个问题：(a) 把评测集的失败模式作为默认前提，导致过拟合；(b) 让 SKILL 在评测集和非评测集表现不一致；(c) 每次新失败都倾向再加一条案例锚点，文档膨胀且越发偏置。**正确做法是把案例中提炼出的抽象原则编进流程本身**，去掉案例叙事。

4. **跨领域示例必须 ≥ 3 个并列领域**，且每个领域**与项目下任何评测专利无显然语义关联**。示例的作用是教 schema 而非教答案；如果 3 个示例都集中在一个看似跟评测集相邻的领域，就要重选。

5. **改动后必须做一致性核查**：脑测把规则套到一个完全无关的新领域（生物制药 / UI 交互 / 机械工艺 / 金融风控等）专利上是否仍合理；如果规则需要大量重新解释才能适用，就该改写为条件激活规则（R-* flag），而不是硬编码当前领域的特征。

**为什么这条最先满足**：如果 SKILL 内化了标准答案或暗示了评测集分布，后续所有"防过拟合自检"都形同虚设——主 agent 在跑评测专利时会通过 SKILL 内置的 hint 直接锁定方向，dogfood 信号失效。

**审计动作**（每次修改 SKILL 后必跑）：grep SKILL.md 是否出现：(a) `正确答案.md` 中任何候选名或其相关 keyword；(b) `专利集/` 下任一评测专利号或其领域 / 主分类号 / 关键术语；(c) "实测案例 / 实测教训 / 曾发生 / 本规则源自" 等案例锚点。任一命中先清理再提交。

### 改进 skill 时的"防过拟合"硬约束（**重要 — 与上节配合使用**）

每次迭代 SKILL 时，**必须先做这套防过拟合自检**——否则 SKILL 会逐渐被某个领域 / 某个产品 / 某个厂商绑架，丧失跨领域适用性。

**改 SKILL 前的 5 条强制自检**：

1. **本次改动是"机制层"还是"示例层"？** —— 机制层（流程、判定规则、状态机）大胆改；示例层（具体厂商名、具体产品族、具体 query 模板）必须**至少给 3 个不同领域的并列示例**，不能只列触发本次迭代的那个领域。

2. **新加的规则在另一个完全不同领域是否还成立？** —— 写入 SKILL 前先脑测：把改动套到一个完全不同领域的专利上（例如生物制药 / UI 交互 / 机械工艺 / 金融风控），如果该规则要么"明显不适用"要么"需要大量重新解释"，就改成**条件激活规则**（依赖 Step 3 的领域分类标志触发，如 R-OPENSOURCE / R-CONFIG / R-PARTNER / R-PATENTWALL / R-PROCURE / R-STANDARD）。

3. **是否在用案例叙事变相硬编码？** —— 不允许写"实测案例 / 实测教训"括注；规则文本必须独立成立。规则源于过去某次失败这件事**自己知道就好**，文档里只留下从失败中抽象出来的机制改进。

4. **新加的"必跑清单"是不是某个领域的产业全景图？** —— 如果是某个具体领域的 5 大主体清单 / 厂商清单 / 论文集，**必须挪到 Step 3 让主 agent 现场构造**，不要硬编码到 SKILL 文档；SKILL 文档只保留"如何构造"的元规则。

5. **跑过非触发领域的 dogfood 验证了吗？** —— 任何超过 3 条改进的迭代后，跑一个完全不同领域的专利做一次 dogfood，验证 SKILL 没被新一轮迭代再次绑架。

**额外提示：sub-agent 给的 verdict 不是真理** —— 主 agent 在采纳 sub-agent 判定前必须**重读独立权 + 从属权 verbatim 文本**复核（特别是从属权提供的 alternative 路径）；**反向证据 vs 限定作用域语必须严格区分**（"X 可以与 Y 配合"、"X 是 future work"、"X 不在本工作范围"——都不是反向证据，仅是限定作用域语）；**非字面命中的 F# 必须强制跑等同三步法**再下结论。这条已写入 SKILL.md Step 5b §D，但作为通用工程纪律也在此 CLAUDE.md 强调一次。
