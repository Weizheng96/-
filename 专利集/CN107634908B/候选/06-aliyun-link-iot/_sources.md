# 06-aliyun-link-iot 检索留痕

## Phase 1 — WebSearch query 留痕

1. `阿里云 Link IoT Kit SDK 弱网 重传 冗余 FEC`
   - 命中：阿里云 Link SDK 帮助中心文档（接入、SDK 集成、断线重连）
   - 关键发现：Link SDK 在 MQTT 连接断开时的"reconnection mechanism"为指数退避；未提及 FEC / 主动冗余

2. `Aliyun Link IoT MQTT QoS reliability retransmission mechanism`
   - 命中：阿里云 Message Queue for MQTT (https://partners-intl.aliyun.com/vodafone/products/mqtt) + 标准 MQTT QoS 解释
   - 关键发现：阿里云 MQTT 服务提供 QoS 0/1/2 三档；QoS 1 重传机制 = "publisher 发 → 等 ACK → 未收到则重发"（ARQ）；"message retransmission only happens on client reconnection"

3. `site:help.aliyun.com 物联网平台 消息 QoS 重传 离线`
   - 命中：消息通信 FAQ / MQTT 连接 FAQ / 离线消息处理
   - 关键发现："aiot_mqtt_process function sends heartbeat packets to the server to maintain long connection status and resends unanswered QoS=1 packets" —— 标准 ACK-based 重传；离线缓存 = QoS 0 ≤1 天 / QoS 1 ≤7 天

4. `阿里云 物联网平台 业务类型 自适应 冗余包 主动 前向纠错`
   - 命中：物联网平台功能特性页 / 技术白皮书 / 企业版实例对比
   - 关键发现：未检索到任何"业务类型自适应"、"主动冗余包"、"前向纠错"相关功能

## Phase 1 补充 — WebSearch（用于 Phase 2 衔接）

5. `阿里云 IoT Link Live 视频 推流 FEC 抗丢包 弱网`
   - 命中：阿里云视频直播（CDN-Live）相关文档，**与 IoT 平台 / Link SDK 无关**
   - 关键发现：阿里云"视频直播"和"物联网平台/Link IoT Kit"是分立产品；未见 IoT 侧的 FEC 推流模块

6. `aliyun link kit github SDK source FEC redundancy adaptive`
   - 命中：https://github.com/aliyun/iotkit-embedded （C-SDK）+ https://github.com/aliyun/alibabacloud-linkkit-python-sdk
   - 关键发现：定位到 SDK 仓库地址，进入 Phase 2 抓 src 结构

## Phase 2 — WebFetch / curl 留痕

7. `https://help.aliyun.com/zh/iot/product-overview/features`
   - 抓取结果：官方对"不稳定无线网络下的通信不可靠"的解决方案为 **"设备影子缓存机制"**（device shadow，云端缓存最新状态、设备重连后同步），**而非 packet-level 主动 FEC**
   - 原文 verbatim："设备影子缓存机制，将设备与应用解耦，解决不稳定无线网络下的通信不可靠痛点"
   - 数据压缩特性原文："对设备与物联网平台之间的数据传输进行压缩处理，达到节约设备流量和提高传输速度的效果"
   - **无 FEC / 主动冗余 / 业务类型自适应 任何提及**

8. `https://help.aliyun.com/zh/iot/support/technical-whitepaper`
   - 抓取结果：页面是技术白皮书目录索引，未含具体技术细节段落

9. `https://help.aliyun.com/zh/iot/developer-reference/link-sdks`
   - 抓取结果：Link SDK 全模块清单 = 设备连接认证 / 消息通信（MQTT/CoAP/HTTP）/ 物模型 / 网关子设备 / OTA / 远程登录 / 日志上报 / 远程配置 / NTP / 文件管理
   - **无 FEC / 业务类型 / 主动冗余 / 自适应调度 任何模块**
   - 抓取结论："SDK 多协议接入（MQTT/CoAP/HTTP）；MQTT 走标准 QoS；无定制冗余机制"

10. `https://help.aliyun.com/zh/iot/developer-reference/overview-5`
    - 抓取结果：C Link SDK 仅暴露 `MQTT接入 / HTTPS接入 / CoAP接入` 三种接入；无任何 packet-level redundancy / adaptive retransmission / traffic classification / burst handling / arrival interval analysis API

11. `https://raw.githubusercontent.com/aliyun/iotkit-embedded/master/README.md` (curl)
    - 抓取结果：README 仅 20 行，仅描述 "C-SDK 简介 + 移植说明"，无 FEC / redundancy 提及
    - 本地落盘：`iotkit-embedded-readme.md`

12. `https://api.github.com/repos/aliyun/iotkit-embedded/contents/src?ref=v3.0.1` (curl)
    - 抓取结果：src 顶层子目录 = `atm, coap, dev_bind, dev_model, dev_reset, dev_sign, dynamic_register, http, http2, infra, mqtt, ota, wifi_provision`
    - **完整列出 SDK 全部 13 个功能子目录，无 FEC / redundancy / scheduler / classifier 子目录**
    - 本地落盘：`iotkit-embedded-src-modules.md`

13. `https://github.com/aliyun/alibabacloud-linkkit-python-sdk` (WebFetch)
    - 抓取结果：GitHub 页面 JS 渲染失败，未拿到内容；但 Python SDK 仅是 IoT 平台 OpenAPI 包装（云端管理 API，非设备端传输栈），与 F1-F5 无关

## 工具受限明示
- GitHub Code Search API 需要认证（`api.github.com/search/code` 返回 401），无法对 iotkit-embedded 全代码做 FEC/redundancy 关键词 grep；但目录结构（13 个子目录全清单）+ 官方文档全模块清单两路一致，已足以判定。
