"""Step 6 setup helper — parse Step 5's "潜在侵权产品-全.md" candidate table
and create one `候选/NN-<slug>/` folder per candidate with starter files.

Each starter folder contains:
  - `_meta.json` — candidate metadata (NN, slug, type, name, org, hit_features,
    publicity, one-liner, applications) for sub-agents to read
  - `_verdict.md` — placeholder verdict that sub-agents will overwrite
  - `_sources.md` — placeholder evidence index

Idempotent: skips existing folders unless --force is passed.

Usage:
    python init_candidates.py <PATENT_ID> [--force]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LQ = "“"
RQ = "”"


def _find_repo_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found")


def _parse_candidate_table(md: str) -> list[dict]:
    """Pull rows from the '候选总表' table."""
    rows = []
    in_table = False
    headers: list[str] = []
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not headers:
            # Expect header row containing "NN" or "类型" or "名称"
            if any(h in cells[0] for h in ("NN", "序号")) or "类型" in s:
                headers = cells
                in_table = True
                continue
        if in_table:
            if set(cells[0].replace("-", "").replace(":", "").strip()) <= {"-", " ", ":"}:
                continue  # separator row
            if len(cells) < len(headers):
                cells = cells + [""] * (len(headers) - len(cells))
            row = dict(zip(headers, cells))
            # Skip rows where NN isn't a number
            nn_raw = row.get(headers[0], "").strip("`").strip()
            if not re.fullmatch(r"\d{1,3}", nn_raw):
                continue
            rows.append(row)
    return rows


def _parse_blurbs(md: str) -> dict[str, str]:
    """Map slug → '## 各候选简介' block text for that slug."""
    blurbs = {}
    m = re.search(r"##\s*各候选简介\s*\n(.+)\Z", md, re.DOTALL)
    if not m:
        return blurbs
    body = "\n" + m.group(1)  # ensure leading newline so re.split works on first heading
    parts = re.split(r"\n###\s+", body)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        slug = lines[0].strip().strip("`").strip()
        blurbs[slug] = "\n".join(lines[1:]).strip()
    return blurbs


def _norm_slug(raw: str) -> str:
    return raw.strip().strip("`").strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("patent_id")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing _meta.json / _verdict.md / _sources.md")
    args = ap.parse_args(argv)

    repo = _find_repo_root()
    pdir = repo / "专利集" / args.patent_id
    src = pdir / f"{args.patent_id}{LQ}潜在侵权产品-全{RQ}.md"
    if not src.exists():
        print(f"[init] {src} not found — run merge_step5.py first", file=sys.stderr)
        return 2
    md = src.read_text(encoding="utf-8")

    rows = _parse_candidate_table(md)
    blurbs = _parse_blurbs(md)
    if not rows:
        print("[init] could not parse any candidate rows from 候选总表", file=sys.stderr)
        return 2

    cand_root = pdir / "候选"
    cand_root.mkdir(exist_ok=True)

    created = 0
    skipped = 0
    for r in rows:
        headers = list(r.keys())
        nn = r[headers[0]].strip("` ")
        kind = r[headers[1]] if len(headers) > 1 else ""
        name = r[headers[2]] if len(headers) > 2 else ""
        org = r[headers[3]] if len(headers) > 3 else ""
        hits = r[headers[4]] if len(headers) > 4 else ""
        publicity = r[headers[5]] if len(headers) > 5 else ""
        slug_raw = r[headers[6]] if len(headers) > 6 else ""
        slug = _norm_slug(slug_raw)
        if not slug:
            slug = f"{nn}-unnamed"
        if not slug.startswith(f"{nn}-"):
            slug = f"{nn}-{slug.lstrip('0123456789-')}"

        cdir = cand_root / slug
        meta_path = cdir / "_meta.json"
        verdict_path = cdir / "_verdict.md"
        sources_path = cdir / "_sources.md"

        if cdir.exists() and not args.force:
            skipped += 1
            continue

        cdir.mkdir(exist_ok=True)
        meta = {
            "nn": nn,
            "slug": slug,
            "type": kind,
            "name": name,
            "organization": org,
            "hit_features_initial": hits,
            "publicity": publicity,
            "blurb": blurbs.get(slug, "").strip(),
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        verdict_path.write_text(
            f"# {slug} — 待评估\n\n"
            f"> 候选 NN: {nn} · 类型: {kind} · 名称: {name} · 组织: {org}\n"
            f"> 公开度: {publicity} · 初判命中 F#: {hits}\n\n"
            "## 状态\n\n**待评估** — 等待 Step 6 sub-agent 输出最终 verdict。\n\n"
            "## 检索粗筛（sub-agent 填写）\n\n（待填）\n\n"
            "## F# 比对（sub-agent 填写 — 仅在粗筛通过时）\n\n（待填）\n\n"
            "## 最终判定\n\n**待评估**\n",
            encoding="utf-8",
        )
        sources_path.write_text(
            f"# 证据索引 — {slug}\n\n"
            "| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |\n"
            "| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
        )
        created += 1

    print(f"[init] created {created} candidate folders, skipped {skipped} existing "
          f"(use --force to overwrite). Root: {cand_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
