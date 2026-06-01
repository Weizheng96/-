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
    p = (start or Path(__file__)).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found")


def _section(md: str, names: list[str]) -> str:
    for name in names:
        m = re.search(rf"(?:^|\n)#+\s*{re.escape(name)}[^\n]*\n(.*?)(?=\n#+\s|\Z)",
                      md, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def _basic_info(md: str) -> str:
    lines = []
    for line in md.splitlines()[:60]:
        if line.startswith("# "):
            lines.append(line)
        elif line.startswith("- "):
            lines.append(line)
        elif line.startswith("## 摘要") or line.startswith("## 权利要求"):
            break
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
    # All claims in the file
    pattern = re.compile(r"\n###\s*权\s*(\d+)\s*\n(.*?)(?=\n###\s*权\s*\d|\Z)", re.DOTALL)
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

    if args.out:
        Path(args.out).write_text(sliced, encoding="utf-8")
        print(f"[slice] wrote {args.out}  ({len(sliced)} chars; original {len(md)} chars)",
              file=sys.stderr)
    else:
        sys.stdout.buffer.write(sliced.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
