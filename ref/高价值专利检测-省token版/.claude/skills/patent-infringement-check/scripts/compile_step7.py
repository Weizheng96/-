"""Step 7 helper — compile the final "违约列表.md" by aggregating every
candidate's `_verdict.md` + `_meta.json` into one status table.

This is purely template-based — no LLM call. Sub-agents in Step 6 have already
done the per-candidate reasoning; Step 7 just sorts + tabulates.

Verdict classification: scans each `_verdict.md` for a "## 最终判定" / "##最终落档"
heading, then reads the next non-empty line to detect one of:
    第 1 档 / 第 2 档 / 第 3 档 / 第 4 档 / 第 5 档
    确认侵权 / 公开资料不足 / 已排除 / 待评估

Usage:
    python compile_step7.py <PATENT_ID>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LQ = "“"
RQ = "”"

RANK_RE = re.compile(r"第\s*([1-5])\s*档")
LABEL_RE = re.compile(r"(确认侵权|公开资料不足|已排除|待评估)")


def _find_repo_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__)).resolve()
    for parent in [p, *p.parents]:
        if (parent / "专利集").exists():
            return parent
    raise FileNotFoundError("专利集/ not found")


CANONICAL_LABEL = {
    1: "确认侵权（高）",
    2: "确认侵权（中）",
    3: "公开资料不足（强候选）",
    4: "公开资料不足（弱候选）",
    5: "已排除",
}


def _classify_verdict(text: str) -> tuple[int, str]:
    """Return (rank, label). rank: 1-5; 9 = 待评估; 8 = unknown.

    Label is ALWAYS the canonical label corresponding to rank — never抽
    sub-agent verdict 文件里随手写的自定义短语（"已排除"、"弱嫌疑"等可能
    出现在五档定义复述段里，干扰 regex 抽取）。
    """
    # Find the "最终判定" section
    m = re.search(r"##+\s*(?:最终判定|最终落档|最终\s*verdict)\s*\n+(.*?)(?=\n##|\Z)",
                  text, re.DOTALL)
    chunk = m.group(1) if m else text
    rank_match = RANK_RE.search(chunk)
    if rank_match:
        rank = int(rank_match.group(1))
        return rank, CANONICAL_LABEL.get(rank, "未识别")

    # Fallback when no "第 N 档" found — sniff the bare label
    label_match = LABEL_RE.search(chunk)
    label_text = label_match.group(1) if label_match else None
    if label_text == "确认侵权":
        return 2, CANONICAL_LABEL[2]
    if label_text == "公开资料不足":
        return 4, CANONICAL_LABEL[4]
    if label_text == "已排除":
        return 5, CANONICAL_LABEL[5]
    return 9, "待评估"


def _one_line_summary(text: str) -> str:
    m = re.search(r"##+\s*总结一句话\s*\n+(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", m.group(1).strip())[:180]
    # fallback: last non-empty paragraph
    for p in reversed([p.strip() for p in text.split("\n\n") if p.strip()]):
        if not p.startswith("#"):
            return re.sub(r"\s+", " ", p)[:180]
    return ""


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("patent_id")
    args = ap.parse_args(argv)

    repo = _find_repo_root()
    pdir = repo / "专利集" / args.patent_id
    cand_root = pdir / "候选"
    if not cand_root.exists():
        print(f"[step7] {cand_root} not found — run init_candidates.py first", file=sys.stderr)
        return 2

    rows = []
    for cdir in sorted(cand_root.iterdir()):
        if not cdir.is_dir():
            continue
        meta_path = cdir / "_meta.json"
        verdict_path = cdir / "_verdict.md"
        evidence_path = cdir / "关键证据.md"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        vtext = verdict_path.read_text(encoding="utf-8") if verdict_path.exists() else ""
        rank, label = _classify_verdict(vtext) if vtext else (9, "待评估")
        summary = _one_line_summary(vtext)
        rel_evidence = (Path("候选") / cdir.name / "关键证据.md").as_posix() if evidence_path.exists() else ""
        rel_verdict = (Path("候选") / cdir.name / "_verdict.md").as_posix()
        rows.append({
            "nn": meta.get("nn", cdir.name.split("-", 1)[0]),
            "slug": cdir.name,
            "type": meta.get("type", ""),
            "name": meta.get("name", ""),
            "org": meta.get("organization", ""),
            "hits": meta.get("hit_features_initial", ""),
            "rank": rank,
            "label": label,
            "summary": summary,
            "rel_evidence": rel_evidence,
            "rel_verdict": rel_verdict,
        })

    # Sort: rank ASC (1 best, 5 排除, 9 待评估 last);
    # within rank by 初判 F# count DESC (more hits = more concerning);
    # within same F# count by nn ASC (stable).
    def _hits_count(s: str) -> int:
        return len([t for t in re.split(r"[,，;；\s]+", s or "") if t.strip()])
    rows.sort(key=lambda r: (
        r["rank"],
        -_hits_count(r["hits"]),
        int(r["nn"]) if str(r["nn"]).isdigit() else 999,
    ))

    out = []
    out.append(f"# {args.patent_id} 违约列表（终筛）\n")
    out.append("> 自动汇总自每个候选的 `_verdict.md`。本报告仅为线索性分析，不构成法律意见。\n")
    out.append("\n## 状态总表（按 5 档技术判定排序）\n")
    out.append("| 序号 | 类型 | 名称 | 组织 | 初判命中 F# | 技术判定 | 关键证据 | verdict |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i, r in enumerate(rows, 1):
        ev = f"[关键证据]({r['rel_evidence']})" if r["rel_evidence"] else "（无）"
        out.append(
            f"| {i} | {r['type']} | {r['name']} | {r['org']} | {r['hits']} | "
            f"**第 {r['rank']} 档：{r['label']}** | {ev} | [_verdict.md]({r['rel_verdict']}) |"
        )

    # Per-candidate detail
    out.append("\n## 候选明细（按上表顺序）\n")
    for i, r in enumerate(rows, 1):
        out.append(f"### {i}. {r['slug']} — {r['name']}")
        out.append(f"- 组织：{r['org']}")
        out.append(f"- 初判命中 F#：{r['hits']}")
        out.append(f"- 技术判定：**第 {r['rank']} 档：{r['label']}**")
        if r["summary"]:
            out.append(f"- 总结：{r['summary']}")
        out.append(f"- [verdict]({r['rel_verdict']}){' · ' + ev if r['rel_evidence'] else ''}\n")

    # Statistics
    by_rank: dict[int, int] = {}
    for r in rows:
        by_rank[r["rank"]] = by_rank.get(r["rank"], 0) + 1
    out.append("## 统计")
    rank_names = {r: f"第 {r} 档（{CANONICAL_LABEL[r].replace('（', '·').replace('）', '')}）"
                  for r in (1, 2, 3, 4, 5)}
    rank_names.update({8: "未识别", 9: "待评估"})
    for rank in sorted(by_rank):
        out.append(f"- {rank_names.get(rank, str(rank))}：{by_rank[rank]} 个")
    out.append(f"- 合计：{len(rows)} 个候选")

    out.append("\n## 免责声明\n")
    out.append("本报告基于公开资料的自动检索 + sub-agent 合议，**不构成法律意见**。"
               "侵权判定为法律结论，应由律师 / 法院依据完整证据链与权利要求字面解释作出。")

    out_path = pdir / f"{args.patent_id}{LQ}违约列表{RQ}.md"
    out_path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"[step7] wrote {out_path}  ({len(rows)} candidates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
