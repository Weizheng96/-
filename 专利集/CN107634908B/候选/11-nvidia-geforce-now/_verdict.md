# Verdict — 11 NVIDIA GeForce NOW + CloudXR

> 候选：T2-02 NVIDIA GeForce NOW + CloudXR SDK；适用权 1 + 权 8（NVIDIA SHIELD 硬件）；P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | GFN 区分 video frame / 控制信令 / 音频 | — | **字面命中** |
| F2 | adaptive bitrate 显式；FEC 在 CloudXR forum 提问但官方未给定答 | — | **公开资料不足**（硬约束 3 反向脑补禁令）|
| F3 | 严格 deadline cloud gaming 隐含 | 等同 deadline-aware | **等同命中** |
| F4 | adaptive bitrate scaling | 等同 | **等同命中** |
| F5 | GFN / CloudXR 全平台部署 | — | **字面命中** |

字面 2/5 + 等同 2/5 + 资料不足 1/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）** | 1. 等同三步法 F3/F4 4 行成立；2. 反向脑补禁令 F2 不过宽读；3. Active；4-7 同 01；建议反向工程升级 | **第 3 档 公开资料不足（强）** |
| 权 8 | 同上 — NVIDIA SHIELD TV / Tablet 设备 OEM 命中 | 同上 | **第 3 档** |

## 关键证据 URL

- [nvidia.custhelp.com/.../how-do-i-use-the-custom-streaming-quality.../5340](https://nvidia.custhelp.com/app/answers/detail/a_id/5340/~/how-do-i-use-the-custom-streaming-quality-settings-on-geforce-now)
- [docs.nvidia.com/cloudxr-sdk/latest/release_notes/release_notes.html](https://docs.nvidia.com/cloudxr-sdk/latest/release_notes/release_notes.html)
- [nvidia.com/en-us/design-visualization/solutions/cloud-xr/](https://www.nvidia.com/en-us/design-visualization/solutions/cloud-xr/)
- [web.cs.wpi.edu/~claypool/mqp/ga-adaptive/paper.pdf](https://web.cs.wpi.edu/~claypool/mqp/ga-adaptive/paper.pdf) — 学术分析
- [forums.developer.nvidia.com/t/.../177503](https://forums.developer.nvidia.com/t/force-minimum-bandwidth-bitrate/177503) — FEC 提问无官方答

## 总结一句话

NVIDIA GFN/CloudXR adaptive bitrate 明确字面命中 F2 部分；FEC 公开度低、F3 时延约束未明示；落第 3 档（公开资料不足强）；建议法务通过反向工程 + NDA 渠道升级。
