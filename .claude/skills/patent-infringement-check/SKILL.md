---
name: patent-infringement-check
description: Detect whether a given patent is being used (infringed) by other organizations. Use this skill whenever the user provides a patent file path (PDF or markdown, e.g. "专利集/CN114531405B.pdf"), or asks to check / 排查 / 检测 a patent for unauthorized use, infringement (侵权 / 违约), or third-party usage. Triggers on requests like "检测这个专利有没有被其他公司使用", "排查 CN... 的侵权情况", "看看谁在用这个专利". Produces a sequenced set of analysis documents (专利介绍、潜在应用场景、潜在使用组织、潜在违约、违约列表) next to the input patent file.
---

# Patent Infringement Check (专利侵权检测)

You are running a six-step analytical pipeline that takes one patent and produces a chain of markdown reports investigating whether other organizations have used that patent without authorization.

## Inputs

The user will provide a patent file path, e.g. `专利集/CN114531405B.pdf`, `专利集/CN114531405B.md`, or `专利集/CN114531405B/CN114531405B.pdf`. Treat the filename stem (e.g. `CN114531405B`) as the **patent ID**.

**All work for one patent lives in its own per-patent subfolder**: `专利集/<patent_id>/`. This folder holds the input PDF/MD, all generated reports, and a `.cache/` subdirectory for downloaded helper PDFs (vendor whitepapers, conference papers, etc).

If the user's input PDF is still at `专利集/<patent_id>.pdf` (i.e. not yet inside its own folder), Step 1 must first create `专利集/<patent_id>/` and move the input file in before producing any reports.

> Example layout for `CN114531405B`:
> ```
> 专利集/CN114531405B/
>   ├── CN114531405B.pdf                   ← input (moved here from 专利集/ if needed)
>   ├── CN114531405B.md                    ← Step 1 output (Google Patents text)
>   ├── CN114531405B"专利介绍".md          ← Step 2
>   ├── CN114531405B"潜在应用场景".md      ← Step 3
>   ├── CN114531405B"潜在使用组织".md      ← Step 4
>   ├── CN114531405B"潜在违约".md          ← Step 5
>   ├── CN114531405B"违约列表".md          ← Step 6
>   └── .cache/                            ← downloaded PDFs used during research
>       ├── triton_sigcomm24.pdf
>       └── ...
> ```

## The Six-Step Pipeline

Execute each step in order. After each step, write the output markdown file to disk before continuing — the next step reads it back. Use `TodoWrite` to track the six steps.

---

### Step 1 — Acquire patent text

**Pre-step (folder normalization)**: If the input file is at `专利集/<patent_id>.pdf` (or `.md`) — i.e. directly under `专利集/` — first create `专利集/<patent_id>/` and move the input there. All subsequent reads / writes use the subfolder. If the input is already inside `专利集/<patent_id>/`, skip this normalization.

**If the input file extension is `.md`:** read it directly, skip to Step 2.

**If the input is `.pdf` (or any non-markdown):**

1. Construct the Google Patents URL: `https://patents.google.com/patent/<PATENT_ID>/zh` (use `/zh` for Chinese-language patents whose ID starts with `CN`; use `/en` otherwise).
2. Use `WebFetch` with a prompt asking for: title, abstract, claims (权利要求), background, technical solution, embodiments, figures captions, applicant, inventors, filing date, publication date, grant date, legal status, and IPC/CPC classifications.
3. If `WebFetch` is blocked or returns thin content, fall back to **local PDF text extraction**:
   - Prefer the `pdf` skill (which wraps `pdfplumber` / `pypdf`). Run a short script like:
     ```python
     import pdfplumber, sys, io
     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # Windows console fix
     with pdfplumber.open(r'<path>') as p:
         for i, page in enumerate(p.pages, 1):
             print(f'--- page {i} ---'); print(page.extract_text() or '')
     ```
     This handles Chinese / multi-page patent PDFs cleanly. The naive `Read` tool on a PDF only works for very short / page-bounded reads (and requires explicit `pages=` for >10 pages); on a typical 50-page CN patent it returns truncated or unstructured text.
   - For scanned / image-only PDFs (no embedded text), use the `pdf` skill's OCR path (`pytesseract` + `pdf2image`).
4. Save the cleaned, well-structured Markdown to `专利集/<patent_id>/<patent_id>.md` so future runs skip the fetch.

Do **not** invent fields. If a field is missing, write `（未获取到）`.

---

### Step 2 — Patent introduction → `<patent_id>"专利介绍".md`

Read the markdown produced in Step 1 carefully, then write a structured introduction. Use this template:

```markdown
# <patent_id> 专利介绍

## 基本信息
- 专利号：
- 标题：
- 申请人 / 专利权人：
- 发明人：
- 申请日 / 公开日 / 授权日：
- 法律状态（截至检索日 <YYYY-MM-DD>）：
- 主分类号（IPC/CPC）：

## 一句话概括
（用一句话讲清楚这个专利在解决什么问题、用什么手段、得到什么效果。）

## 解决的技术问题
## 核心技术方案
（用 3–6 个要点讲清楚机制；如有公式 / 模块 / 流程，列清。）

## 关键权利要求解读
（重点解读独立权利要求 1，标注每个限定特征；再概述从属权利要求扩展了哪些特征。）

## 保护范围边界（重要）
- 必要技术特征清单（缺一不可）：
- 等同特征讨论（哪些替换方案可能仍落入保护范围）：
- 明显不在保护范围内的相邻方案：
```

权利要求是后续判定侵权的尺子，**必要技术特征清单一定要写全且写准**。如果某个特征模糊，宁可保守列出多个解读。

---

### Step 3 — Application scenarios → `<patent_id>"潜在应用场景".md`

基于专利介绍 + 当前社会与产业发展现状，推演这个专利在现实世界里**可能被使用**的场景。注意：今天是 `currentDate`（系统提供），结合最新行业动态思考，不要局限于专利文本里举的例子。

模板：

```markdown
# <patent_id> 潜在应用场景

## 推演方法
（说明你是从专利的哪些核心特征出发，结合什么产业趋势进行推演的。）

## 场景列表
对每一个场景给出：
### 场景 N：<场景名称>
- 场景描述：
- 该场景下使用专利的形式（产品 / 服务 / 内部流程 / SDK / 云服务 / ...）：
- 与权利要求的对应关系（哪些必要技术特征会被命中）：
- 商业价值 / 紧迫性（高 / 中 / 低 + 一句话理由）：
- 反例（看似相关其实不构成使用的情况）：
```

至少给 5 个场景；按"命中权利要求的可能性"由高到低排列。

---

### Step 4 — Potentially using organizations → `<patent_id>"潜在使用组织".md`

针对每个高优先级场景，列出**真实存在**的、有动机和能力使用该专利的组织。允许使用 `WebSearch` 进行联网验证。

要求：
- 不要瞎编公司名。每个组织都要能在公开信息中找到对应业务线。
- 排除专利权人自己及其明确授权的关联方。
- 区分"可能性高"（有公开产品 / 论文 / 招聘 / 专利布局命中相关方向）和"可能性中"（业务相邻但无直接证据）。

模板：

```markdown
# <patent_id> 潜在使用组织

## 排除清单
- 专利权人 / 申请人本身：
- 已知关联方 / 明确被授权方：

## 组织清单
对每一个组织：
### <组织名称>
- 类型：上市公司 / 独角兽 / 高校 / 研究院 / 创业公司 / 政府机构 / ...
- 主营业务相关产品线：
- 命中场景（引用 Step 3 的场景编号）：
- 使用该专利的合理性（为什么"它会去做这件事"）：
- 可能性等级：高 / 中 / 低
- 检索关键词建议（5–10 个，用于 Step 5 的联网检索）：
```

至少给 8 个组织，覆盖至少 3 个不同场景。

---

### Step 5 — Suspect publications → `<patent_id>"潜在违约".md`

> **重要时间约束**：只看 patent **授权日 / 公开生效日之后** 的发布内容。授权日之前的工作不构成侵权。

对 Step 4 列表里的每个组织，使用 `WebSearch` 检索其官方发布、产品文档、技术博客、白皮书、开源仓库 README、招股书 / 财报技术披露、学术论文、官方公众号文章等。

检索建议：
- query 模板：`<组织名> <技术关键词> after:<授权日>`
- 也尝试：`<组织名> <场景关键词> 白皮书 / 技术报告 / 专利`
- 优先官方一手信源；二手报道作为线索但需溯源。
- **从论文 / 白皮书 PDF 取证**：当 `WebFetch` 拉论文 PDF（例如 SIGCOMM / NSDI / OSDI / ATC / APNet 一手论文、厂商白皮书）只返回二进制流时，先把 PDF 下载到本地，再调用 `pdf` skill 用 `pdfplumber` 抽取全文文本，逐页扫描多 NIC / bond / LACP / flow table 同步等关键词。这是 SIGCOMM 论文层面取证的主要手段。
- **反向专利墙比对（强烈推荐用于实现细节型专利）**：对于通信 / 芯片 / 算法等"细节不在产品文档里公开"的专利，直接搜厂商在授权日之后申请的同主分类专利，是更稳定的强证据来源。
  - query 模板：`<组织名> 申请人 IPC <主分类号> after:<授权日>`
  - 推荐渠道：[Google Patents Advanced](https://patents.google.com/advanced)（assignee + cpc + after:），IncoPat、智慧芽、Patentscope、CNIPA 检索系统。
  - 重点关注权利要求文本中是否出现与目标专利**相同的必要技术特征组合**；如果命中即作为该候选的"专利墙佐证"加入证据链（标注："虽未在产品文档披露，但 <组织名> 已就同一发明点申请了 CNxxx / USxxx / WOxxx，权利要求 N 与本专利 F1-Fk 高度重合"）。

判断"是否落入保护范围"的标准（**全部满足才记为可疑命中**）：
1. 时间上晚于专利授权日；
2. 描述中能比对到独立权利要求的**全部必要技术特征**（或等同替换）；
3. 是该组织"自己在用"，而不是评论 / 引用 / 学术综述他人方法。

模板：

```markdown
# <patent_id> 潜在违约（初筛）

## 检索范围与时间
- 专利授权日：<YYYY-MM-DD>
- 检索截止日：<currentDate>
- 检索方式：WebSearch（说明使用的核心 query 模板）

## 候选清单
### 候选 N
- 涉嫌组织：
- 来源链接（必须可点）：
- 来源类型（官网 / 技术博客 / 论文 / 招股书 / 公众号 / GitHub / ...）：
- 发布日期：
- 专利墙佐证（如 Step 5 反向检索拿到，列出其专利号 + 权利要求摘录；否则写"未检索到"）：
- 与专利保护范围的逐特征对比表：
  | 必要技术特征 | 候选发布中的对应描述 | 字面命中（是/否/疑似） | 等同命中（是/否/疑似） | 证据片段（原文摘录） |
  - **字面命中**：候选材料的描述是否能直接逐词对应到该必要技术特征。
  - **等同命中**：是否以"基本相同的手段，实现基本相同的功能，达到基本相同的效果"，且替换对本领域技术人员显而易见。当字面=否、等同=是时，需简述等同理由。
- 初步结论：可疑命中（全部字面=是 或 字面+等同合并=是）/ 疑似（部分要件待证）/ 排除（任一要件字面+等同均=否）
- 备注与需要进一步核实的点：
```

如某个组织联网检索找不到任何相关公开内容，就在文末"未发现可疑发布的组织"小节列出，并保留方便后续复查。

---

### Step 6 — Final infringement list → `<patent_id>"违约列表".md`

仔细复核 Step 5 中所有"可疑命中 / 疑似"项。对每一项做以下三项核查后再决定保留或剔除：

1. **来源真实性**：链接是否可访问？是否官方一手？必要时再次 `WebFetch` 确认原文。
2. **特征完整性**：是否真的命中**所有**必要技术特征？只要缺一个就降级为"疑似"或剔除。
3. **时间合规性**：发布日期确实晚于授权日？

最终输出：

```markdown
# <patent_id> 违约列表（终筛）

## 核查标准
（说明本轮做了哪些再核查动作。）

## 高置信侵权候选
对每一项给：
### <组织名>
- 来源链接：
- 发布日期：
- 命中的独立权利要求：
- 命中类型：字面侵权 / 等同侵权（必须明确二选一或并列；纯等同侵权需说明等同三步法理由）。
- 完整特征对比表（同 Step 5 模板的"字面命中 / 等同命中"两栏；进入本节意味着每项要件至少在"字面"或"等同"中至少一栏=是，否则降级或剔除）：
- 专利墙佐证（如有）：
- 置信度（高 / 中），及置信理由：
- 建议的下一步动作（发函取证 / 购买产品测试 / 律师函 / 暂缓观察）：

## 已剔除候选
| 组织 | 来源 | 剔除原因 |

## 检索盲区与局限性声明
（说明哪些组织 / 场景没能拿到一手证据，哪些是技术细节不公开导致无法判断，提醒用户本报告仅为线索性分析，不构成法律意见。）
```

---

## 全局约束

- **永远不要伪造引用**。每条来源必须是 `WebSearch` / `WebFetch` 实际拿到的链接；拿不到就如实写"未检索到公开来源"。
- **永远不要替用户下结论说"已构成侵权"**。专利侵权判定是法律结论，本 skill 输出的是**线索与证据链**，最终结论应交由专业律师。文末必须包含免责声明。
- **保留中间产物**。Step 1 抓取下来的 `.md`、每一步的报告都要落盘，方便用户翻查与复算。所有产物落到 `专利集/<patent_id>/`；研究过程中下载的辅助 PDF（论文、白皮书）落到 `专利集/<patent_id>/.cache/`。
- **TodoWrite 跟踪六个步骤**，每完成一步立即 mark completed，方便用户看到进度。
- 中文专利用中文输出；英文专利用英文输出，以专利原文语言为准。
- 输出文件名严格使用用户指定的全角引号格式：`<patent_id>"<阶段>".md`，引号是 **U+201C / U+201D**（不是 ASCII `"`，不是中文标点 `「」` 或 `《》`）。
- **写入全角引号文件名的固定流程（Windows 重要）**：`Write` 工具直接传含 `"..."` 的路径会报 `ENOENT`（宿主把它当成 ASCII `"` 处理），必须按下面两步：
  1. 先用 `Write` 把内容写到临时文件 `<patent_id>_stepN_temp.md`（同目录，不带引号）。
  2. 再用 `PowerShell` 通过 `[char]0x201C` / `[char]0x201D` 拼路径并 `[System.IO.File]::Move(...)` 改名，例如：
     ```powershell
     $src = '<dir>\<patent_id>_stepN_temp.md'
     $dst = '<dir>\<patent_id>' + [char]0x201C + '<阶段>' + [char]0x201D + '.md'
     [System.IO.File]::Move($src, $dst)
     ```
  注：不要用 `Move-Item -LiteralPath '...""...'`，PowerShell 5.1 在解析含 ASCII `"` 的字面量时会先报 `Illegal characters in path`。Linux/macOS 不受此限制，但跨平台建议统一走上面的流程。

## 触发示例

- 用户：`检测一下 专利集/CN114531405B.pdf 有没有被其他公司使用` → 触发，按六步走。
- 用户：`帮我看看 CN114531405B 这个专利的侵权情况` → 触发；如目录里已有 PDF 则按上面流程，否则先问用户文件位置。
- 用户：`这个专利讲的是什么？` → **不**触发完整六步，只跑 Step 1+2 即可（介绍）；如用户随后追问"谁可能在用 / 有没有人侵权"，再继续后续步骤。
