"""Step 2 helper — slice a patent's full markdown to only the sections Claude
needs for Step 2 (scenario extraction + claim 1 + features), so Claude reads
~3k chars instead of ~100k.

Output goes to stdout (Claude can capture via Bash) OR --out <path>.
Sections extracted:
  - 基本信息 (title / dates / assignee / classifications)
  - 摘要 (if present)
  - 背景技术 (the primary anchor for scenario extraction)
  - 所有独立权利要求 (auto-detected — typically 权 1 plus any other claim
    starting with "一种 ..." or "A method/system/apparatus/...")

Usage:
    python slice_patent.py <PATENT_ID>                 # prints slice to stdout
    python slice_patent.py <PATENT_ID> --out FILE      # writes to FILE
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _find_repo_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found")


# Optional heading prefix: Chinese-numeral ("四、"), parenthesised ("（一）"),
# or arabic ("4." / "4、") — CN patents often number sections this way.
_HEADING_PREFIX = (
    r"(?:[一二三四五六七八九十百零]+[、.\s]"
    r"|（[一二三四五六七八九十百零]+）"
    r"|\d+[.、]?\s*)?\s*"
)


def _section(md: str, names: list[str]) -> str:
    for name in names:
        m = re.search(
            rf"(?:^|\n)#+\s*{_HEADING_PREFIX}{re.escape(name)}[^\n]*\n(.*?)(?=\n#+\s|\Z)",
            md, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


_BASIC_INFO_STOP = re.compile(rf"^#+\s*{_HEADING_PREFIX}(?:摘要|权利要求|Abstract|Claims)")


def _basic_info(md: str) -> str:
    lines = []
    for line in md.splitlines()[:60]:
        if _BASIC_INFO_STOP.match(line):
            break
        if line.startswith("# ") or line.startswith("- "):
            lines.append(line)
    return "\n".join(lines).strip()


_INDEP_STARTERS_ZH = ("一种", "一组", "一类", "一台", "一套")
_INDEP_STARTERS_EN_RE = re.compile(
    r"^\d+\.?\s*(?:A|An)\s+(?:method|system|apparatus|device|computer|"
    r"machine|chip|medium|composition|process)\b",
    re.IGNORECASE,
)


def _is_independent(body: str) -> bool:
    """Heuristic: claim body starts with a kind-of-noun (CN) or 'A method/...' (EN);
    not 'according to claim N' (从属权利要求)."""
    head = body.lstrip().lstrip("0123456789. ").strip()
    if head.startswith("根据权利要求") or head.startswith("根据权要求"):
        return False
    if "according to claim" in head.lower()[:80]:
        return False
    if any(head.startswith(s) for s in _INDEP_STARTERS_ZH):
        return True
    if _INDEP_STARTERS_EN_RE.match(head):
        return True
    return False


def _independent_claims(md: str) -> list[tuple[str, str]]:
    """Yield (num, body) for each independent claim. Always include claim 1
    regardless of heuristic (it is always independent by patent-law convention)."""
    out = []
    # All claims in the file. Headers vary: "### 权 1", "### 权利要求 1",
    # "### 权利要求 1（独立权 — 方法 …）" (annotation before the newline).
    # Match "权" or "权利要求" + number, then consume the rest of the header line.
    claim_head = r"###\s*权(?:利要求)?\s*(\d+)"
    pattern = re.compile(
        rf"\n{claim_head}[^\n]*\n(.*?)(?=\n###\s*权(?:利要求)?\s*\d|\Z)", re.DOTALL)
    matches = pattern.findall(md)
    if not matches:
        return out
    for num, body in matches:
        body = body.strip()
        if num == "1" or _is_independent(body):
            out.append((num, body))
    return out


def slice_md(md: str) -> str:
    parts = []
    parts.append(_basic_info(md))
    abstract = _section(md, ["摘要", "Abstract"])
    if abstract:
        parts.append("\n## 摘要\n\n" + abstract)
    background = _section(md, ["背景技术", "Background", "技术领域"])
    parts.append("\n## 背景技术（Step 2 应用场景定锚）\n\n" +
                 (background or "（原文未划分独立的背景技术章节；请用说明书前 1/3 段）"))
    indep = _independent_claims(md)
    if indep:
        parts.append(f"\n## 独立权利要求（共检出 {len(indep)} 项）\n")
        for num, body in indep:
            parts.append(f"\n### 权 {num}\n\n{body}")
    else:
        parts.append("\n## 独立权利要求\n\n（未能自动检出；请直接读原文 `<patent_id>.md`）")
    return "\n".join(parts).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("patent_id")
    ap.add_argument("--out", help="output file path; defaults to stdout")
    args = ap.parse_args(argv)

    repo = _find_repo_root()
    md_path = repo / "专利集" / args.patent_id / f"{args.patent_id}.md"
    if not md_path.exists():
        print(f"[slice] {md_path} not found", file=sys.stderr)
        return 2

    md = md_path.read_text(encoding="utf-8")
    sliced = slice_md(md)

    # Detect auto-extraction failure so the caller can fall back to reading the
    # full patent instead of silently trusting a near-empty slice (exit 0 + a
    # placeholder is a silent failure — return a non-zero code instead).
    bg_failed = "（原文未划分独立的背景技术章节" in sliced
    claims_failed = "（未能自动检出" in sliced

    if args.out:
        Path(args.out).write_text(sliced, encoding="utf-8")
        print(f"[slice] wrote {args.out}  ({len(sliced)} chars; original {len(md)} chars)",
              file=sys.stderr)
    else:
        sys.stdout.buffer.write(sliced.encode("utf-8"))

    if bg_failed or claims_failed:
        missing = ", ".join(
            x for x, f in [("背景技术", bg_failed), ("独立权利要求", claims_failed)] if f)
        print(f"[slice] WARNING auto-detect failed for: {missing} — "
              f"fall back to Reading the full 专利集/{args.patent_id}/{args.patent_id}.md "
              f"for the missing section(s).", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
