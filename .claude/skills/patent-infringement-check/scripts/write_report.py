"""Helper to write Step 2/3/4/5 markdown reports with Chinese full-width quotes
(U+201C / U+201D) in the filename.

Background: on Windows the Claude `Write` tool cannot write to a path containing
full-width quotes directly (ENOENT). The workaround is: Claude writes content to
a temp file with ASCII name, then runs this helper which moves it to the proper
quoted name using Python's native file IO (which handles U+201C / U+201D fine).

Usage:
    python write_report.py <PATENT_ID> <STAGE_NAME> <SCRATCH_PATH>
    # → writes 专利集/<PATENT_ID>/<PATENT_ID>"<STAGE_NAME>".md
    # → deletes the scratch file on success (pass --keep-source to keep)

The `stage_name` is the bracketed-quote-inner-text (no quote characters, no .md
suffix). The destination file format is always:
    专利集/<patent_id>/<patent_id>"<stage_name>".md
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

LQ = "“"   # U+201C
RQ = "”"   # U+201D


def _find_repo_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("patent_id")
    ap.add_argument("stage_name", help="text between the full-width quotes, e.g. 潜在应用场景及侵权特征")
    ap.add_argument("source", help="path to the markdown file Claude wrote")
    ap.add_argument("--keep-source", action="store_true",
                    help="do not delete the source after copying")
    args = ap.parse_args(argv)

    repo = _find_repo_root()
    pdir = repo / "专利集" / args.patent_id
    if not pdir.exists():
        print(f"[write_report] {pdir} does not exist", file=sys.stderr)
        return 2
    src = Path(args.source)
    if not src.is_absolute():
        src = repo / src
    if not src.exists():
        print(f"[write_report] source {src} not found", file=sys.stderr)
        return 2

    dst = pdir / f"{args.patent_id}{LQ}{args.stage_name}{RQ}.md"
    shutil.copyfile(src, dst)
    if not args.keep_source:
        src.unlink()
    print(f"[write_report] wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
