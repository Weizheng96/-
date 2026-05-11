# Verdict — 10 Microsoft Teams + Skype

> 候选：T1-07 Microsoft Teams + Skype Calling + Teams Rooms 硬件
> 适用独立权：权 1 + 权 8（Teams Rooms 硬件 OEM 出厂固化）
> 主体类型：T1 RTC SDK；Priority P0

## F# 命中表

| F# | 字面 | 等同 | 综合 |
| --- | --- | --- | --- |
| F1 | Teams 区分 audio / video / screen-share — Satin codec 仅用于 audio | — | **字面命中** |
| F2 | "FEC is used dynamically when there's packet loss... Satin's bitrate savings allows for sending more redundant data to increase resistance to packet loss" | — | **字面命中**（动态 FEC）|
| F3 | Azure 网络 + adaptive bandwidth | 等同 deadline-aware | **等同命中** |
| F4 | FEC 周期性发冗余 — 与 Pacer 协同 | 等同 uniform 调度 | **等同命中** |
| F5 | Teams + Skype Calling 全平台部署 | — | **字面命中** |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | 第 2 档 | 1. 等同三步法 F3/F4 4 行成立；2-7 同 01；MS 与华为无明确 patent grant；Satin 非 SEP | **第 2 档 确认侵权（中）** |
| 权 8 | 第 2 档 — Teams Rooms (Logitech Rally Bar / Poly Studio / Yealink MeetingBar) 硬件 OEM 出厂固化 | 同上 | **第 2 档 确认侵权（中）** |

## 关键证据 URL

- [techcommunity.microsoft.com/.../satin-microsoft-s-latest-ai-powered-audio-codec.../2141382](https://techcommunity.microsoft.com/t5/microsoft-teams-blog/satin-microsoft-s-latest-ai-powered-audio-codec-for-real-time/ba-p/2141382) — **FEC 动态启用 + Satin 冗余**
- [learn.microsoft.com/.../network-requirements](https://learn.microsoft.com/en-us/skypeforbusiness/plan-your-deployment/network-requirements/network-requirements) — Video FEC included
- [techcommunity.microsoft.com/.../new-microsoft-teams-features-improve-call-and-meeting-quality/2884341](https://techcommunity.microsoft.com/blog/microsoftteamsblog/new-microsoft-teams-features-improve-call-and-meeting-quality/2884341)
- [en.wikipedia.org/wiki/Satin_(codec)](https://en.wikipedia.org/wiki/Satin_(codec)) + [mspoweruser.com/microsoft-satin-ai-powered-audio-codec-teams](https://mspoweruser.com/microsoft-satin-ai-powered-audio-codec-teams/)

## 总结一句话

Microsoft Teams + Satin codec 官方文档明示"动态启用 FEC、随丢包发送更多冗余"，正面命中 F2；落第 2 档（确认侵权中）。
