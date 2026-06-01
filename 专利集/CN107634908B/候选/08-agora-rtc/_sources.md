# 08-agora-rtc 检索留痕

## Phase 1 WebSearch（4 query）
1. `Agora SD-RTN packet-level FEC redundancy scheduling algorithm`
   - 命中：SegmentFault SD-RTN 演进文 / Agora WP / 通用 FEC 论文
   - 关键 URL：
     - https://segmentfault.com/a/1190000040725941/en
     - https://hello.agora.io/rs/096-LBH-766/images/Agora_WP_SD-RTN-Delivers-RealTime-Internet-Advantages.pdf
2. `Agora SIGCOMM OR NSDI paper SD-RTN real-time communication network`
   - 命中：Agora Networking Medium 标签页、LinkedIn、Whitepaper PDF
   - 关键 URL：
     - https://medium.com/agora-io/tagged/networking
     - https://hello.agora.io/rs/096-LBH-766/images/Agora_WP_SD-RTN-Delivers-RealTime-Internet-Advantages.pdf
   - 说明：未检索到公开的 SIGCOMM / NSDI 同行评审论文（招股书 S-1 也未公开 FEC 内部算法）
3. `site:docs.agora.io FEC redundancy packet loss recovery video SDK`
   - 命中：3.x interactive-live-streaming release notes / video-calling release notes / configure-video-encoding 等
   - 关键 URL：
     - https://docs.agora.io/en/3.x/interactive-live-streaming/introduction/release-notes
     - https://docs.agora.io/en/video-calling/enhance-call-quality/configure-video-encoding
     - https://docs.agora.io/en/video-calling/overview/release-notes
4. `Agora SDK channel profile audio scenario AUDIO_SCENARIO traffic type FEC`
   - 命中：setAudioProfile / setChannelProfile 文档
   - 关键 URL：
     - https://docs.agora.io/en/3.x/interactive-live-streaming/basic-features/audio-profiles
     - https://docs.agora.io/en/help/integration-issues/profile_difference

## Phase 2 WebFetch（5 fetch）
1. https://hello.agora.io/rs/096-LBH-766/images/Agora_WP_SD-RTN-Delivers-RealTime-Internet-Advantages.pdf
   - WebFetch 返回二进制，已 PowerShell `Copy-Item` 落盘为 `agora_sd-rtn_whitepaper.pdf`（7.3MB）
   - 本地 `_extract_pdf.py` (pdfplumber) 提取到 `_whitepaper_text.txt`
2. https://segmentfault.com/a/1190000040725941/en — 拿到 "FEC or multi-channel redundancy ... based on the network link assessment status and the required qos level" verbatim
3. https://docs.agora.io/en/3.x/interactive-live-streaming/basic-features/audio-profiles — 确认 `setAudioProfile` 由开发者设置
4. https://docs.agora.io/en/help/integration-issues/profile_difference — 确认 `setChannelProfile` 由开发者设置 + 该 profile 文档未提及 FEC
5. https://docs.agora.io/en/3.x/interactive-live-streaming/introduction/release-notes — 全文仅 1 处 FEC 提及（"slightly reduces CPU usage by optimizing the FEC codec"）

## Phase 2 补充 WebSearch（1 query — 确认 "FEC 自适应" 出处）
- `"Agora" "FEC" "adaptive" "frame rate" "video packets" 4K release notes`
- 命中 Agora docs 中 "improved FEC algorithm enables adaptive switches according to the frame rate and number of video frame packets" 的官方表述

## 工具受限
- WebFetch 对 PDF 返回二进制 → 改走 PowerShell + pdfplumber 本地提取（已成功）
- 未发现 Agora 公开过 SD-RTN 内部 FEC 算法的同行评审论文 / 招股书技术附录
