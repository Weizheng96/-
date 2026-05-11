# Verdict — 22 SRT Haivision Upstream

> 候选：C2 SRT 协议 + libsrt (Haivision 主导)
> 适用独立权：权 1 + 权 8
> 主体类型：T4 上游开源协议（R-OPENSOURCE）
> Priority：P0（含反向证据 — 已排除）

## F# 命中表（基于 §A.4 官方文档深读）

| F# | 字面 | 反向证据 | 综合 |
| --- | --- | --- | --- |
| F1 业务类型 | 0 命中 — SRT 协议 layer 之下不含业务感知 | — | **公开资料不足** |
| F2 冗余包数量 自适应 | — | **"FEC is purely static — it does not adapt to network conditions" + "Both connection endpoints must agree on parameters"** | **真反向证据**（"Y supports only Z (not X)" 模式，对应 §D 状态机硬约束第 4 条 (a) 真反向证据）|
| F3 时延要求 → 总时间 | `latency` 参数显式设置时间预算 | — | **字面命中** |
| F4 调度方法 自适应 | — | **FEC 矩阵 (cols, rows, layout) 全为 static 配置；arq=always/onreq/never 也是 static** | **真反向证据** |
| F5 实际发送 | libsrt 发送 | — | 字面命中 |

字面 2/5 + 反向 2/5 + 资料不足 1/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 5 档 已排除（反向证据 — F2/F4 不自适应）** | 1. 等同三步法 N/A（有真反向证据，不可走等同）；2. 反向 vs 限定语区分：上表第 2 行模式 "Y supports only Z (not X)" 真反向 ✅；3. Active；4. SRT 2017 年开源，早于本专利申请日 2016-07-19 — 部分 SRT 早期实现可能构成现有技术抗辩；5. R-STANDARD = false；6. §5.0 豁免：硬条件 (a) 反向证据 ✅；7. patent pledge：Haivision 是 SRT Alliance 维护方但与华为无 patent grant 关系 | **第 5 档 已排除（反向证据）** |
| 权 8 | 同上 — Haivision Makito X 等编码器只搭载 static FEC 时同档已排除；但**若 Haivision 商业版在 SRT 之上加了自适应层，则需单独评估** | 同上 + 升级路径 | **第 5 档 已排除（反向证据）+ 保留下游 Makito X 商业版作 4 档弱候选** |

## 关键证据 URL

- [github.com/Haivision/srt/blob/master/docs/features/packet-filtering-and-fec.md](https://github.com/Haivision/srt/blob/master/docs/features/packet-filtering-and-fec.md) — **官方明示 FEC is purely static**
- [haivision.github.io/srt-rfc/draft-sharabayko-srt.html](https://haivision.github.io/srt-rfc/draft-sharabayko-srt.html) — SRT Protocol RFC draft
- [srtlab.github.io/srt-cookbook/apps/ffmpeg.html](https://srtlab.github.io/srt-cookbook/apps/ffmpeg.html) — FFmpeg SRT 用法
- [github.com/Haivision/srt](https://github.com/Haivision/srt) — libsrt 主仓库

## 总结一句话

SRT 上游 libsrt 官方文档明示"FEC 纯静态，不随网络条件自适应"，对应 F2/F4 真反向证据；落第 5 档已排除。但下游 Haivision Makito X 等商用编码器可能在 SRT 之上加自适应层——保留作 4 档弱候选待进一步证据。
