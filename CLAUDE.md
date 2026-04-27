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
