"""Step 1 helper — fetch a patent's full text from Google Patents and write
`专利集/<patent_id>/<patent_id>.md`.

Why a script: WebFetch tends to summarize long claims sections — making Step 2's
feature extraction unreliable. Direct HTML scrape + BeautifulSoup gives verbatim
claims/description for free.

Usage:
    python fetch_patent.py <PATENT_ID> [--lang zh|en] [--force]

Exit codes:
    0 — wrote `<patent_id>.md`
    2 — HTTP / parse failure; caller should fall back to WebFetch
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def _find_repo_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__)).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found above script")


def _text(el) -> str:
    """Collapse whitespace inside an element to a clean string."""
    if el is None:
        return ""
    txt = el.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", txt).strip()


def fetch_html(patent_id: str, lang: str = "zh") -> str:
    url = f"https://patents.google.com/patent/{patent_id}/{lang}"
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": f"{lang},en"}, timeout=60)
    r.raise_for_status()
    # Google Patents serves UTF-8 but doesn't always advertise it correctly
    r.encoding = "utf-8"
    return r.text


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # Title
    title_meta = soup.find("meta", attrs={"name": "DC.title"})
    title = (title_meta or {}).get("content") if title_meta else None
    if not title:
        t = soup.find("h1", attrs={"itemprop": "pageTitle"}) or soup.find("span", attrs={"itemprop": "title"})
        title = _text(t)

    # Patent number / publication info
    pub_num = _text(soup.find(attrs={"itemprop": "publicationNumber"}))

    # Dates
    def _date(prop):
        el = soup.find(attrs={"itemprop": prop})
        if el and el.get("datetime"):
            return el["datetime"]
        return _text(el)

    filing_date = _date("filingDate")
    priority_date = _date("priorityDate")
    publication_date = _date("publicationDate")

    # Applicants / Inventors
    inventors = [_text(x) for x in soup.find_all(attrs={"itemprop": "inventor"})]
    assignees = [_text(x) for x in soup.find_all(attrs={"itemprop": "assigneeOriginal"})]
    current_assignees = [_text(x) for x in soup.find_all(attrs={"itemprop": "assigneeCurrent"})]

    # Legal status
    legal_event_rows = soup.select('tr[itemprop="events"]')
    legal_events = []
    for row in legal_event_rows[:15]:
        d = _text(row.find(attrs={"itemprop": "date"}))
        title_ev = _text(row.find(attrs={"itemprop": "title"}))
        if d or title_ev:
            legal_events.append((d, title_ev))

    # Classifications
    cpc = []
    for c in soup.select('span[itemprop="Code"]'):
        code = _text(c)
        if code and code not in cpc:
            cpc.append(code)

    # Abstract
    abstract_el = soup.find(attrs={"itemprop": "abstract"})
    abstract = _text(abstract_el) if abstract_el else ""

    # Claims — verbatim, one per "claim" div
    claims = []
    claims_section = soup.find(attrs={"itemprop": "claims"})
    if claims_section:
        for cl_div in claims_section.select("div.claim[num]"):
            num = cl_div.get("num", "").lstrip("0") or "?"
            parts = [_text(p) for p in cl_div.select("div.claim-text")]
            body = "\n".join(p for p in parts if p)
            if body:
                claims.append((num, body))

    # Description — split by paragraphs / headings
    desc_section = soup.find(attrs={"itemprop": "description"})
    desc_md = ""
    if desc_section:
        content = desc_section.find(attrs={"itemprop": "content"}) or desc_section
        lines = []
        for child in content.descendants:
            if getattr(child, "name", None) == "heading":
                lines.append("\n### " + _text(child) + "\n")
            elif getattr(child, "name", None) in ("p",):
                t = _text(child)
                if t:
                    lines.append(t)
        if not lines:
            for p in content.find_all(["p", "div"]):
                t = _text(p)
                if t and len(t) > 20:
                    lines.append(t)
        desc_md = "\n\n".join(lines)

    return {
        "title": title,
        "publication_number": pub_num,
        "filing_date": filing_date,
        "priority_date": priority_date,
        "publication_date": publication_date,
        "inventors": inventors,
        "assignees_original": assignees,
        "assignees_current": current_assignees,
        "legal_events": legal_events,
        "cpc": cpc[:20],
        "abstract": abstract,
        "claims": claims,
        "description": desc_md,
    }


def render_md(data: dict, patent_id: str, source_url: str) -> str:
    out = []
    out.append(f"# {patent_id} — {data['title'] or '(未获取到标题)'}\n")
    out.append(f"> 来源：[{source_url}]({source_url})\n")
    out.append("\n## 基本信息\n")
    out.append(f"- 公开号：{data['publication_number'] or patent_id}")
    out.append(f"- 申请日：{data['filing_date'] or '（未获取到）'}")
    out.append(f"- 优先权日：{data['priority_date'] or '（未获取到）'}")
    out.append(f"- 公开/授权日：{data['publication_date'] or '（未获取到）'}")
    if data["assignees_original"]:
        out.append(f"- 原始申请人：{'; '.join(data['assignees_original'])}")
    if data["assignees_current"]:
        out.append(f"- 当前权利人：{'; '.join(data['assignees_current'])}")
    if data["inventors"]:
        out.append(f"- 发明人：{'; '.join(data['inventors'])}")
    if data["cpc"]:
        out.append(f"- 分类号（CPC）：{', '.join(data['cpc'])}")
    if data["legal_events"]:
        out.append("\n### 法律状态事件（前 15 条）")
        for d, t in data["legal_events"]:
            out.append(f"- {d}：{t}")

    if data["abstract"]:
        out.append("\n## 摘要\n")
        out.append(data["abstract"])

    out.append(f"\n## 权利要求（共 {len(data['claims'])} 项 — verbatim）\n")
    for num, body in data["claims"]:
        out.append(f"### 权 {num}\n")
        out.append(body)
        out.append("")

    out.append("\n## 说明书（含背景技术 / 发明内容 / 具体实施方式）\n")
    out.append(data["description"] or "（未获取到说明书正文）")

    return "\n".join(out).rstrip() + "\n"


def detect_lang(patent_id: str) -> str:
    return "zh" if patent_id.upper().startswith("CN") else "en"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("patent_id", help="patent publication number, e.g. CN1234567A / US9876543B2 / EP3456789A1 / WO2024123456A1")
    ap.add_argument("--lang", choices=["zh", "en"], default=None)
    ap.add_argument("--force", action="store_true", help="overwrite existing .md")
    args = ap.parse_args(argv)

    repo = _find_repo_root()
    lang = args.lang or detect_lang(args.patent_id)
    out_dir = repo / "专利集" / args.patent_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.patent_id}.md"
    if out_path.exists() and not args.force:
        print(f"[fetch_patent] {out_path} already exists; use --force to overwrite", file=sys.stderr)
        return 0

    url = f"https://patents.google.com/patent/{args.patent_id}/{lang}"
    try:
        html = fetch_html(args.patent_id, lang)
    except Exception as e:
        print(f"[fetch_patent] HTTP error for {url}: {e}", file=sys.stderr)
        return 2

    try:
        data = parse(html)
    except Exception as e:
        print(f"[fetch_patent] parse error: {e}", file=sys.stderr)
        return 2

    if not data["claims"]:
        print(f"[fetch_patent] no claims extracted (page may be blocked or pattern changed); "
              f"caller should fall back to WebFetch", file=sys.stderr)
        return 2

    md = render_md(data, args.patent_id, url)
    out_path.write_text(md, encoding="utf-8")
    print(f"[fetch_patent] wrote {out_path}  ({len(data['claims'])} claims, "
          f"{len(data['description'])} chars of description)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
