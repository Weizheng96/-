# 证据索引 — 16-ctelecom-ctwing

## Phase 1 — WebSearch query 留痕

### q1: `CTWing 中国电信 天翼物联 IoT 平台 抗丢包 FEC 冗余`
- https://www.ctwing.cn/ —— CTWing 官网首页
- https://baike.baidu.com/item/CTWing/59070643 —— 百度百科 CTWing 词条
- http://www.sasac.gov.cn/n4470048/n22624391/n26705666/n26705673/n26705725/c26762120/content.html —— 国资委 CTWing OS 介绍
- https://www.impcia.net/news/details_1273.html —— CTWing OS 2.0 发布通稿
- https://www.emqx.com/en/customers/china-telecom —— EMQX 客户案例（中国电信 NB-IoT 用 EMQX 作 MQTT broker）
- http://www.chinatelecom.com.cn/news/02/202301/t20230104_72873.html —— 中国电信 CTWing OS 发布通稿
- https://blog.csdn.net/qq_36347513/article/details/123853163 —— CTWing 设备接入（TCP）笔记
- https://help.senthink.com/电信CTWING设备接入.html —— 利尔达对接 CTWING 说明
- 命中要素：T-Link（MQTT 改进）/ MQTT / LWM2M / HTTP(S) / TCP 协议接入。**无 FEC / 主动冗余相关描述**。

### q2: `CTWing MQTT NB-IoT 协议栈 主动冗余 业务类型 自适应`
- https://zhuanlan.zhihu.com/p/593972987 —— Air780E 模块接入 CTWING AT 命令
- https://blog.csdn.net/u010460625/article/details/108955059 —— CTWing 设备接入实战
- https://www.cnblogs.com/LJing21/p/15840525.html —— MQTT 应用场景对接
- https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m —— EMQX IoT 协议综述
- https://blog.csdn.net/CTWing_cn/article/details/127728306 —— CTWing AIoT 通用组件 http 数据推送
- https://www.cnblogs.com/429512065qhq/p/17275383.html —— MQTT 对接 CTWING 非透传
- 命中要素：CTWing MQTT broker 端口 1883、QoS 等级、MQTT-SN 轻量化、LWM2M for NB-IoT。**仍无主动冗余 / 业务类型自适应描述**。

### q3: `"天翼物联" OR "CTWing" "前向纠错" OR "FEC" OR "网络编码"`
- https://www.gigalight.com.cn/bbs/technical-3588.html —— 通用 FEC 科普
- https://zhuanlan.zhihu.com/p/563942987 —— 光模块 FEC 科普
- https://cloud.tencent.com/developer/article/2331769 —— 腾讯云音视频 FEC 原理
- https://blog.csdn.net/huntenganwei/article/details/126786393 —— 适合 IoT 的 FEC 纠错码（与 CTWing 无关）
- https://info.support.huawei.com/info-finder/encyclopedia/zh/自适应前向纠错.html —— 华为 A-FEC 百科（华为，非电信 CTWing）
- 命中要素：检索域里 "CTWing" 与 "FEC/前向纠错/网络编码" 不共现。返回结果均为通用 FEC 科普或华为/腾讯文档，**与 CTWing 无任何技术耦合**。

### q4: `CTWing 天翼物联 QoS 重传 可靠传输 协议 白皮书`
- https://blog.csdn.net/qq_36347513/article/details/123853163 —— CTWing TCP 接入笔记
- http://www.sasac.gov.cn/.../c26762120/content.html —— CTWing OS 国资委通稿（6 大能力均未涉 FEC）
- https://www.163.com/dy/article/GQU4PDPM05128AGA.html —— "元宇宙物语"通稿
- https://blog.csdn.net/u014608435/article/details/122028502 —— ctWing AutoObserver 对接
- https://www.ctwing.cn/cpkx/1314 —— 5G 专网产品页（412 拦截）
- https://www.ctwing.cn/czlks/11 —— 开发者向导（412 拦截）
- 命中要素：CTWing 公开技术体系以 MQTT QoS（ack/重传）与 TCP 重传保证可靠性，**无主动冗余包发送、无 packet-level FEC、无业务类型自适应调度**的公开白皮书。

## Phase 2 — WebFetch / curl 留痕

### WebFetch
- https://www.ctwing.cn/solution/ —— **HTTP 412 Precondition Failed（防爬虫拦截）**

### curl 兜底
- 命令：`curl -sL -A "Mozilla/5.0..." https://www.ctwing.cn/solution/`
- 落地：`ctwing_solution.html`（4428 字节）
- 结果：返回页面为 JS 防爬虫挑战页（反爬黑盒 + 极少 DOM），关键词命中均位于混淆 JS 字符串内，**无有效产品文案可摘录**。工具受限明示：CTWing 官网对未带浏览器指纹的请求一律返回挑战页，无法以 curl/WebFetch 取得真实产品技术细节。

## 已检查文档清单
1. `ctwing_solution.html` —— CTWing solution 页 curl 副本（防爬虫挑战页，无效内容，仅留痕用）

## 工具受限明示
- CTWing 官网（www.ctwing.cn）对 WebFetch 和无浏览器指纹的 curl 均返回 412 / JS 挑战页，本轮无法直接获取产品技术细节。
- Phase 1 公网检索覆盖了官网通稿、国资委通稿、EMQX 客户案例、利尔达 / 域格 / Air780E 等三方对接文档、CSDN 技术博客等多个独立信息源，结论一致指向"MQTT/MQTT-SN/LWM2M/HTTP/TCP + QoS/ARQ"的常规 IoT 接入协议栈，未见任何"主动冗余 / FEC / 业务类型自适应冗余调度"线索。综合多源一致性，判定可成立。
