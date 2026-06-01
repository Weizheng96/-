# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Not a software codebase — a **patent-infringement analysis workspace**. There is no build, lint, or test toolchain. The "logic" lives in a single Claude skill; everything else is input data and generated reports.

Directory layout:

- `专利集/` — root for all patent work. Each patent gets its own subfolder named with the patent ID (`专利集/<PATENT_ID>/`). The subfolder contains the input PDF (optional), all generated reports (`<PATENT_ID>.md`, `<PATENT_ID>"潜在应用场景及侵权特征".md`, etc.), and `候选/NN-<slug>/` per-候选 evidence folders (created by Step 6's init script).
- Per-候选 evidence folders hold downloaded materials (PDFs / scraped HTML / GitHub raws), an `_sources.md` index (sub-agent query 留痕), a `_verdict.md` (sub-agent 直接写入的合议结果), and `_meta.json` (candidate metadata written by `init_candidates.py`). May also contain `_pruned.txt` if Phase 1 粗筛 returned no signal.
- `.claude/skills/patent-infringement-check/SKILL.md` — the main "code". A 7-step pipeline that turns one input patent into a chain of analysis reports.
- `.claude/skills/patent-infringement-check/scripts/` — Python helper scripts (all **no-LLM** — pure file IO / HTTP / parsing):
  - `fetch_patent.py` — Step 1: Google Patents HTML → `<PATENT_ID>.md`
  - `slice_patent.py` — Step 2 helper: slice `<PATENT_ID>.md` to background + 独立权利要求 only (95%+ char reduction for Claude reading)
  - `init_candidates.py` — Step 6.0: parse Step 5's candidate table → create `候选/NN-<slug>/` folders + `_meta.json` + placeholder verdict
  - `compile_step7.py` — Step 7: aggregate every `_verdict.md` by "第 N 档" tag → `违约列表.md`
  - `write_report.py` — helper: Claude writes ASCII-named scratch file; this script renames to the full-width-quote filename (workaround for Claude `Write` ENOENT bug on full-width quote paths)

  Design rule: **all LLM work is Claude's own** — main agent for Steps 2-5, react-mode sub-agent for Step 6 per-candidate. No external LLM dependency.
- `.claude/skills/patent-infringement-check-高消耗版本/` — **archived** early heavy-reference version (kept for diffing only; not auto-triggered).
- `.claude/skills/pdf/` — supporting skill for PDF text/table extraction (wraps `pdfplumber` / `pypdf`). Used by Step 1 as a fallback when Google Patents `fetch_patent.py` / `WebFetch` is blocked. Run `pip install requests beautifulsoup4 lxml pdfplumber pypdf` once.

## How work gets done here

When the user provides a patent ID / path or asks to check a patent for unauthorized use / 侵权 / 违约, the `patent-infringement-check` skill auto-triggers. It runs 7 sequenced steps, each writing one markdown report **into the same directory as the input patent**:

1. `<PATENT_ID>.md` — patent verbatim text (via `scripts/fetch_patent.py`; fallback `WebFetch` / local PDF)
2. `<PATENT_ID>"潜在应用场景及侵权特征".md` — Claude reads the **sliced** patent (via `scripts/slice_patent.py` — saves 95%+ tokens vs reading full patent), writes scenarios anchored verbatim to background + all independent claims + F1-Fk
3. `<PATENT_ID>"潜在使用组织".md` — Claude lists orgs per scenario, 1 line per org (lean)
4. `<PATENT_ID>"潜在侵权产品初选".md` — Claude lists specific named products per org
5. `<PATENT_ID>"潜在侵权产品-全".md` — Claude runs tech-word-driven `WebSearch`es for long-tail and applies product↔tech merge rule, written directly (no intermediate notes file)
6. `候选/NN-<slug>/_verdict.md` (one per candidate) — Claude spawns one general-purpose **sub-agent in react mode** per candidate; each sub-agent iterates `WebSearch` → read → refine `WebSearch` → `WebFetch` → write `_verdict.md` directly. Sub-agent may early-prune with `_pruned.txt`. Folders are pre-created by `scripts/init_candidates.py`.
7. `<PATENT_ID>"违约列表".md` — final ranked list (via `scripts/compile_step7.py`, pure template aggregation by "第 N 档" tag)

Each step reads the previous step's output from disk, so they must be written before moving on. Use `TodoWrite` to track the 7 steps.

**Where each LLM is used**: Claude does **all** LLM reasoning. Main agent handles Steps 2-5; one react-mode sub-agent per candidate handles Step 6. Step 1 / Step 6.0 init / Step 7 are pure Python. Token-efficiency design: Step 2 uses a slice helper to feed Claude only ~3k chars (background + independent claims) instead of the full ~100k patent; Step 5 writes the merged candidate list directly without a separate long-tail-notes intermediate file; Step 6 sub-agents have isolated contexts so per-candidate tool returns don't pollute the main agent.

## Conventions that are easy to get wrong

- **Filename format uses Chinese full-width quotes** — specifically **U+201C (`"`) + U+201D (`"`)**, not ASCII `"` (U+0022), not 「」 (U+300C/U+300D), not 《》, not `''` (U+2018/U+2019). The displayed glyphs `"`/`"` and `"` look almost identical in many fonts; if you copy-paste a filename, eyeball isn't enough — verify the code points.
- **Writing these filenames on Windows**: The new pipeline avoids the old `Write` ENOENT bug because **all reports with full-width quotes are written by Python scripts** (native `Path.write_text(..., encoding="utf-8")` handles U+201C/U+201D fine). Claude only needs `Read` / `Edit` on these files — both of which support full-width quote paths. If you ever need to write a new full-quote file from inside Claude, do `Write` to a temp name first, then `PowerShell` `[System.IO.File]::Move` using `[char]0x201C` / `[char]0x201D` to rename — but in normal operation this should be unnecessary.
- Reports always go **inside the patent's own subfolder** (`专利集/<patent_id>/`), never at repo root or directly under `专利集/`. If the input PDF is still at `专利集/<patent_id>.pdf`, the skill creates the subfolder and moves the input in before generating reports.
- Output language follows the patent's original language (CN patents → Chinese reports).
- Time gate for infringement candidates: only material **published after the patent's grant date** counts. Prior art is irrelevant here.
- Never output a definitive "已构成侵权" conclusion — this skill produces leads and evidence chains, not legal opinions. Every final report must include a disclaimer.
- Never fabricate citations. If `WebSearch` / `WebFetch` returns nothing, write "未检索到公开来源" and move on.

## Modifying the skill

The skill's behaviour is defined by two surfaces:

1. [.claude/skills/patent-infringement-check/SKILL.md](.claude/skills/patent-infringement-check/SKILL.md) — the 7-step pipeline overview, trigger phrases (in frontmatter `description`), templates for Steps 2-5, the sub-agent protocol for Step 6, and global constraints. **Almost all behavioural rules live here** since LLM work is now all Claude's.
2. [.claude/skills/patent-infringement-check/scripts/*.py](.claude/skills/patent-infringement-check/scripts/) — Python helpers (no LLM). Logic changes here are mechanical: HTML parsing schema (`fetch_patent.py`), patent section detection (`slice_patent.py`), candidate table schema (`init_candidates.py`), verdict tag detection (`compile_step7.py`), filename quote rename (`write_report.py`). Edits take effect on the next invocation.

When iterating: most rule changes (Step templates, sub-agent prompt, global constraints) go in SKILL.md. Script edits are reserved for parsing / schema / Python-level concerns.

**主动提出改进建议**：在执行 skill 的过程中，如果你发现某个步骤有更优的执行方法（例如更准确的检索 query 模板、更可靠的 PDF 解析方式、漏掉的常见判定标准、模板里冗余或缺失的字段、可以并行化的环节、容易让模型走偏的措辞等），**先把当前任务跑完**，然后在最终回复里向用户**明确提出改进建议**——说明：1) 你观察到的问题；2) 建议如何修改 [.claude/skills/patent-infringement-check/SKILL.md](.claude/skills/patent-infringement-check/SKILL.md)；3) 预计带来的好处。**等用户确认后再实际编辑 SKILL.md**，不要静默修改。这样 skill 会随着每次实战逐步进化。

### 改进 skill 时的"标准答案隔离与一致性"硬约束（**最先满足 — 否则 dogfood 失效**）

`正确答案.md` 保存了若干评测专利的"标准答案"——它是用来**事后**评估 SKILL / 主 agent 表现的基准，不允许被 SKILL 内化。SKILL 必须对评测专利和其他专利**表现一致**——否则 SKILL 等于针对评测集作弊，dogfood 信号失效。

**强制规则**：

1. **任何形式的标准答案都不允许出现在 SKILL.md / CLAUDE.md / 任何被 skill 加载的辅助文档中**——包括正确候选名、其代表性产品名、生态相关 keyword、代表性 vendor 名、典型论文 / 上游项目名 / 配置参数 / commit 关键词等任何可让主 agent 跳 1–2 步链到标准答案的辅助信息。

2. **不允许任何"针对评测用例的暗示性文字"**——即便用了"某 X 类专利"形式的占位符也属于暗示，因为如果占位符里的领域恰好对应评测集中存在的专利，就会泄露评测集的领域分布。**领域 / 场景 / 主分类号 / 标准号 / 标志性技术词**等任何能在概率上把读者引向评测专利的信息一律禁止。同一约束也适用于 `scripts/*.py` 的 docstring / argparse help / 例子——这些文本会被开发者读到、也可能被 Claude 在 Read 脚本时加载，等同于 SKILL.md 的扩展面。

3. **不允许写"实测案例 / 实测教训 / 曾发生 / 本规则源自……失误"等案例锚点**——SKILL 是机制层文档，规则的正确性必须由其内在逻辑独立成立，而非靠引用过去的失败案例做正当性背书。把案例叙事写入 SKILL 会带来 3 个问题：(a) 把评测集的失败模式作为默认前提，导致过拟合；(b) 让 SKILL 在评测集和非评测集表现不一致；(c) 每次新失败都倾向再加一条案例锚点，文档膨胀且越发偏置。**正确做法是把案例中提炼出的抽象原则编进流程本身**，去掉案例叙事。

4. **跨领域示例必须 ≥ 3 个并列领域**，且每个领域**与项目下任何评测专利无显然语义关联**。示例的作用是教 schema 而非教答案；如果 3 个示例都集中在一个看似跟评测集相邻的领域，就要重选。

5. **改动后必须做一致性核查**：脑测把规则套到一个完全无关的新领域（生物制药 / UI 交互 / 机械工艺 / 金融风控等）专利上是否仍合理；如果规则需要大量重新解释才能适用，就该改写为条件激活规则（R-* flag），而不是硬编码当前领域的特征。

**为什么这条最先满足**：如果 SKILL 内化了标准答案或暗示了评测集分布，后续所有"防过拟合自检"都形同虚设——主 agent 在跑评测专利时会通过 SKILL 内置的 hint 直接锁定方向，dogfood 信号失效。

**审计动作**（每次修改 SKILL 或 scripts/*.py 后必跑）：grep SKILL.md **以及** scripts/*.py 是否出现：(a) `正确答案.md` 中任何候选名或其相关 keyword；(b) `专利集/` 下任一评测专利号或其领域 / 主分类号 / 关键术语；(c) "实测案例 / 实测教训 / 曾发生 / 本规则源自" 等案例锚点。任一命中先清理再提交。

### 改进 skill 时的"防过拟合"硬约束（**重要 — 与上节配合使用**）

每次迭代 SKILL 时，**必须先做这套防过拟合自检**——否则 SKILL 会逐渐被某个领域 / 某个产品 / 某个厂商绑架，丧失跨领域适用性。

**改 SKILL 前的 5 条强制自检**：

1. **本次改动是"机制层"还是"示例层"？** —— 机制层（流程、判定规则、状态机）大胆改；示例层（具体厂商名、具体产品族、具体 query 模板）必须**至少给 3 个不同领域的并列示例**，不能只列触发本次迭代的那个领域。

2. **新加的规则在另一个完全不同领域是否还成立？** —— 写入 SKILL 前先脑测：把改动套到一个完全不同领域的专利上（例如生物制药 / UI 交互 / 机械工艺 / 金融风控），如果该规则要么"明显不适用"要么"需要大量重新解释"，就改成**条件激活规则**（在 sub-agent prompt 中按候选 metadata 字段触发，而非硬编码为流程默认动作）。

3. **是否在用案例叙事变相硬编码？** —— 不允许写"实测案例 / 实测教训"括注；规则文本必须独立成立。规则源于过去某次失败这件事**自己知道就好**，文档里只留下从失败中抽象出来的机制改进。

4. **新加的"必跑清单"是不是某个领域的产业全景图？** —— 如果是某个具体领域的主体清单 / 厂商清单 / 论文集，**必须让 Step 3 / Step 4 由 Claude 主 agent 现场构造**（SKILL 仅描述"如何构造"的元规则），不要硬编码到 SKILL 文档或 scripts/*.py。

5. **跑过非触发领域的 dogfood 验证了吗？** —— 任何超过 3 条改进的迭代后，跑一个完全不同领域的专利做一次 dogfood，验证 SKILL 没被新一轮迭代再次绑架。

**额外提示：sub-agent 给的 verdict 不是真理** —— 主 agent 在采纳 sub-agent 判定前必须**至少抽样复核**：(a) `_verdict.md` 的"检索粗筛"段是否真有 query 留痕（防止 sub-agent 跳过 Phase 1 直接脑补）；(b) "已排除"档是否真满足硬条件（0 命中 ≠ 已排除——必须有真反向证据 / 时间不合规 / 领域无关之一）；(c) "确认侵权"档的 F# 引文是否真出现在引用 URL（必要时 `WebFetch` 抽样验证）。**反向证据 vs 限定作用域语必须严格区分**："X 可以与 Y 配合"、"X 是 future work"、"X 不在本工作范围"——都不是反向证据，仅是限定作用域语。这条已写入 SKILL.md Step 6 的 sub-agent 协议中。
