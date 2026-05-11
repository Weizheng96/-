# Verdict — 05 QUIC + FEC IETF

> 候选：C4 QUIC + FEC 实验性扩展（lsquic / quiche / msquic / PQUIC FEC plugin）
> 适用独立权：权 1
> 主体类型：T4 核心技术；Priority P1

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | QUIC stream 区分 application data | — | **公开资料不足** — QUIC 核心 RFC 不含业务感知 |
| F2 | QUIC 核心不含 FEC；draft-michel-quic-fec 实验性 | — | **公开资料不足** |
| F3 | QUIC PTO (probe timeout) 隐含 deadline | 等同 | **等同命中** |
| F4 | QUIC packet pacing | 等同 | **等同命中** |
| F5 | QUIC 实现已广泛部署（Cloudflare / Google / MS / Apple）| — | **字面命中** |

字面 1/5 + 等同 2/5 + 资料不足 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 4 档 公开资料不足（弱）** | 1. 等同三步法 F3/F4 成立；2. 反向脑补禁令 F1/F2 不过宽读；3-7 同 01 | **第 4 档 公开资料不足（弱）** |

## 关键证据 URL

- [datatracker.ietf.org](https://datatracker.ietf.org/) — IETF QUIC WG drafts
- draft-michel-quic-fec — 实验性 FEC extension
- [github.com/google/quiche](https://github.com/google/quiche) — Google quiche
- [github.com/microsoft/msquic](https://github.com/microsoft/msquic) — Microsoft msquic
- [github.com/litespeedtech/lsquic](https://github.com/litespeedtech/lsquic) — lsquic

## 总结一句话

QUIC 核心 RFC 9000/9001/9002 不强制 FEC；FEC 实验性 draft 尚未广泛部署；落第 4 档（公开资料不足弱）。
