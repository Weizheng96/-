# Sources — 22 SRT Haivision Upstream

| # | 类型 | URL | 时间档 | 命中 |
| --- | --- | --- | --- | --- |
| 1 | §A.4 官方文档（**反向证据**） | [github.com/Haivision/srt/blob/master/docs/features/packet-filtering-and-fec.md](https://github.com/Haivision/srt/blob/master/docs/features/packet-filtering-and-fec.md) | 持续维护 | **反向 F2/F4** — "FEC is purely static, does not adapt" |
| 2 | §A.5 协议规范 | [haivision.github.io/srt-rfc/draft-sharabayko-srt.html](https://haivision.github.io/srt-rfc/draft-sharabayko-srt.html) | 持续 | F3 — latency 字面 |
| 3 | §A.4 cookbook | [srtlab.github.io/srt-cookbook/apps/ffmpeg.html](https://srtlab.github.io/srt-cookbook/apps/ffmpeg.html) | 持续 | F4 — packetfilter 参数 |
| 4 | §A.7 上游仓库 | [github.com/Haivision/srt](https://github.com/Haivision/srt) | 2017+ | F5 |
| 5 | §A.4 旧版文档 | [github.com/Haivision/srt/blob/v1.4.3/docs/features/packet-filtering-and-fec.md](https://github.com/Haivision/srt/blob/v1.4.3/docs/features/packet-filtering-and-fec.md) | 2020+ | 同 #1 — 多版本一致 |
| 6 | §A.4 第三方实现 | [ossrs.net/lts/en-us/docs/v5/doc/srt](https://ossrs.net/lts/en-us/docs/v5/doc/srt) | 持续 | F4 — SRS SRT 集成 |

**注**：本候选状态 = 第 5 档 已排除（反向证据）。但 §A.6 联合案例 — Haivision Makito X 等商业编码器可能在 SRT 之上加自适应层 — 工具能力下未深查 — 建议法务做反向工程取证。
