# 09-aliyun-artc sources（检索留痕）

## Phase 1 — react 粗筛（WebSearch，串行）
1. query：`阿里云 RTC ARTC 弱网 FEC 冗余 抗丢包 自适应`
   - 命中（相关）：阿里云 RTC 弱网对抗系列、掘金/网易云信 RTC 冗余策略。摘要披露：阿里云 FEC 采用冗余传输提高容错率，关键帧 10% / 非关键帧 5% 冗余率，按丢包判断网络状况动态调整冗余度；定义抗丢包恢复时间 → 推导达到 99% 恢复率所需 FEC 比例 → 自适应冗余调整。→ 有信号，不剪枝。
2. query：`阿里云 RTC FEC 冗余 网络状态 业务类型 QoS 自适应 冗余包数量`
   - 命中：自适应 FEC 相比静态 FEC 根据网络状态动态调整冗余；XOR/RS 算法；QoS 按业务优先级。
3. query：`阿里巴巴 阿里云 专利 自适应 FEC 冗余 业务类型 时延 调度 数据传输`
   - 未检索到阿里自有同主题（自适应 FEC 冗余/业务类型/时延调度）专利公开来源；仅 HPN 白皮书泛提自适应路径 + FEC。
4. query：`阿里云 RTC QoS 弱网对抗 FEC NACK 自适应冗余 抗丢包恢复 site:developer.aliyun.com OR site:zhuanlan.zhihu.com`
   - 命中：阿里云 RTC QoS 系列（NACK 格式与发送策略 781573、变分辨率编码 783329、LTR 368041540、屏幕共享编码优化 781479）。披露：按网络条件动态决策抗丢包方法（NACK / FEC / Hybrid FEC）并分配 NACK/FEC 带宽。

## Phase 2 — react 深抓（WebFetch / curl，串行）
- WebFetch https://help.aliyun.com/document_detail/2664046.html （阿里云 RTC 网络监控与弱网策略，更新 2024-03-25）—— SPA，正文未在静态 HTML，无实质内容。
- WebFetch https://juejin.cn/post/7145069820956901390 （掘金「RTC 弱网对抗之冗余策略」，**字节跳动视频云团队**，2022-09-19）—— 非阿里云，作通用 RTC 机制背景：FEC 冗余度按 P(m,i,k) 概率模型 + 99% 恢复率计算；定义抗丢包恢复时间 resend_delay → 被动重传次数 k → 推导 FEC 比例；Pacer 优先发 RTX 重传再发媒体。
- WebFetch https://developer.aliyun.com/article/783329 （阿里云 RTC QoS 变分辨率编码，2021-04-02，视频云技术小编=阿里云）—— SPA，正文未渲染。
- curl 兜底 developer.aliyun.com/article/783329 → 86KB 但正文为 JS 渲染（关键词 0 命中），SPA 限制，落盘 aliyun-dev-783329.html。
- WebFetch + curl 兜底 https://zhuanlan.zhihu.com/p/361876006 （阿里云 RTC QoS 弱网对抗）—— 403 / 反爬仅返回 628B，**工具受限未取到正文**，落盘 aliyun-zhihu-361876006.html。
- WebFetch Google Patents assignee=Alibaba 检索（FEC redundancy business type delay scheduling，after=20210608）—— 检索 UI 为 JS 渲染，未取到结果，**工具受限**。

## 工具受限说明
- 阿里云官方帮助文档 / developer.aliyun.com 文章正文、知乎专栏、Google Patents 检索页均为 JS 渲染或反爬，curl + 浏览器 UA 兜底仍无正文。故 F1/F3/F4 的阿里云自有 verbatim 细节未能落实，判定依据来自 WebSearch 返回的阿里云文章摘要 + 通用 RTC 机制描述。
