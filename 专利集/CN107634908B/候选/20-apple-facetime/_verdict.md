# Verdict — 20 Apple FaceTime + iMessage Call

> 候选：T1-08；适用权 1 + 权 8（iPhone/iPad/Mac/Apple Watch/Apple Vision Pro 设备 OEM）；T1 RTC SDK + T5；P0

## F# 命中表

| F# | 综合 |
| --- | --- |
| F1 | 字面命中（FaceTime 区分 audio / video / SharePlay / Persona） |
| F2 | 字面命中（"FaceTime employs FEC techniques to mitigate packet loss" — UMA Technology + WWDC）|
| F3 | 等同命中（实时通话 deadline + WirelessInsights 预测性 networking） |
| F4 | 等同命中（adaptive bitrate + FEC + WWDC 2025 WirelessInsights） |
| F5 | 字面命中（FaceTime 全平台部署） |

字面 3/5 + 等同 2/5。

## 状态机三栏

| 权 | 原始 | 后置 | 最终 |
| --- | --- | --- | --- |
| 权 1 | **第 3 档 公开资料不足（强）**（Apple 闭源生态使具体参数难取证） | 等同 F3/F4 4 行成立；3-7 同 01；建议先评估 PCT 同族在 US 的执行力 | **第 3 档 公开资料不足（强）** |
| 权 8 | **第 3 档**（iPhone / Mac / iPad / Vision Pro 设备 OEM 出厂固化） | 同上 | **第 3 档** |

## 关键证据 URL

- [umatechnology.org/facetime-audio-quality-how-to-enhance-it-on-iphone/](https://umatechnology.org/facetime-audio-quality-how-to-enhance-it-on-iphone/) — **FEC 字面命中**
- [developer.apple.com/videos/play/wwdc2019/712/](https://developer.apple.com/videos/play/wwdc2019/712/) — WWDC 2019 networking
- [developer.apple.com/videos/play/wwdc2020/10111/](https://developer.apple.com/videos/play/wwdc2020/10111/) — WWDC 2020 networking
- [medium.com/@p.akhrameev/apples-wirelessinsights-predictive-networking-44c8578c42c7](https://medium.com/@p.akhrameev/apples-wirelessinsights-predictive-networking-44c8578c42c7) — WWDC 2025 WirelessInsights
- [tidbits.com/2022/04/22/use-apples-networkquality-tool-to-test-internet-responsiveness/](https://tidbits.com/2022/04/22/use-apples-networkquality-tool-to-test-internet-responsiveness/)
- [en.wikipedia.org/wiki/FaceTime](https://en.wikipedia.org/wiki/FaceTime)

## 总结一句话

Apple FaceTime 公开材料明示"使用 FEC 缓解丢包" + adaptive bitrate + WWDC 多场涉及；闭源栈无具体参数披露；落第 3 档（公开资料不足强）；维权 Apple 全闭源生态可行性受限。
