# Step 1 — Acquire Patent Text

Convert the input patent (PDF or MD) into a clean, complete `<patent_id>.md` with all claim text verbatim. Step 2 depends on the full claim text — do not silently proceed with truncated content.

## Pre-step: Folder normalization

If the input file is at `专利集/<patent_id>.pdf`（or `.md`） — i.e. directly under `专利集/` — first create `专利集/<patent_id>/` and move the input there. All subsequent reads/writes use the subfolder. Skip if input is already inside `专利集/<patent_id>/`.

## If input is `.md`

Read it directly, skip to Step 2.

## If input is `.pdf` (or any non-markdown)

### 1. Try Google Patents WebFetch (cheapest path)

URL pattern: `https://patents.google.com/patent/<PATENT_ID>/zh` (use `/zh` for CN patents, `/en` otherwise).

Initial WebFetch prompt should ask for: title, abstract, all 权利要求 (claims) verbatim, background, technical solution, embodiments, figure captions, applicant, inventors, filing/publication/grant dates, legal status, IPC/CPC classifications.

### 2. WebFetch 汇总输出诊断与 narrow-prompt-per-claim 补救（强制）

WebFetch 底层使用快速小模型，对"抓取所有权利要求"这类长跨度任务**倾向于压缩为汇总**而非逐条 verbatim 输出。

**识别汇总信号**：返回文本中出现"权 N 至 M 涉及 / 包括 / 等"、"具体实现方式"、"涵盖"等概括用语，或某条权利要求短到与汇总后文字相当、与从属权常见 100-500 字的规模严重不符。

一旦命中汇总输出，**不要把汇总当作 verbatim 写入 Step 1 输出文件**——立即按下述补救流程：

1. 对**每一条从属权**单独发一次 narrow WebFetch，prompt 严格限定为：
   ```
   Output ONLY the verbatim <语言> text of <claim N> from this patent. Do not summarize.
   Format: "<claim N>：<full verbatim text>"
   ```
2. 对**每一条独立权**也单独做 verbatim 抓取——独立权同样容易被压成一句话。
3. 抓取完毕后把每条权利要求 verbatim 合并写入 `<patent_id>.md`，并在文件头注明"按权利要求逐条 verbatim 抓取"。
4. 若 Google Patents 返回的总权利要求数（在第一次汇总输出末尾）多于已抓到的条目数，对未抓的条目继续 narrow 抓取直到完整。

跨领域适用性：本规则对任何专利语言（CN / US / EP / JP / KR / WO）、任何 IPC 主分类都适用，无领域依赖。

### 3. WebFetch 受阻 / 内容稀薄时：本地 PDF 提取

Prefer the `pdf` skill (which wraps `pdfplumber` / `pypdf`)：

```python
import pdfplumber, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # Windows console fix
with pdfplumber.open(r'<path>') as p:
    empty = 0
    for i, page in enumerate(p.pages, 1):
        txt = page.extract_text() or ''
        if not txt.strip(): empty += 1
        print(f'--- page {i} ---'); print(txt)
    print(f'EMPTY_PAGES={empty}/{len(p.pages)}')
```

The naive `Read` tool on a PDF only works for very short / page-bounded reads; on a typical 50-page CN patent it returns truncated or unstructured text.

### 4. Scanned-PDF 自动检测

If `EMPTY_PAGES` ≥ 80% of pages, do **not** retry pdfplumber with different settings — switch immediately to one of:

1. **Re-run Google Patents `WebFetch` with a stricter prompt** demanding full claim text verbatim (often the cheapest path; CN patents almost always have indexed text on Google Patents even when their PDF is scanned).
2. **`pdf` skill OCR path** (`pytesseract` + `pdf2image` + `tesseract -l chi_sim+eng`) — only when WebFetch is blocked AND the patent is critical enough to warrant OCR cost.

Do not silently proceed past Step 1 with empty patent text — Step 2's "必要技术特征清单" depends on the full claim text.

### 5. Save

Save the cleaned, well-structured Markdown to `专利集/<patent_id>/<patent_id>.md` so future runs skip the fetch.

## Do not invent fields

If a field is missing, write `（未获取到）`.
