# 20-tesla-cloud 检索 + 抓取留痕

## Phase 1 WebSearch (4 次)

1. `Tesla vehicle cloud telemetry OTA protocol reliability redundancy`
   - 命中信号：OTA "multiple network paths" 冗余（指网络通路冗余，不是 packet-level FEC）+ "intelligent retry mechanisms"（reactive 重传，非 proactive 冗余）
   - https://bnxt.ai/blog/tesla-app-architecture-live-telemetry-ota-updates-vehicle-cloud-sync
   - https://arxiv.org/html/2510.22024v1
2. `Tesla MQTT WebSocket vehicle protocol reverse engineering`
   - 命中：官方 Fleet Telemetry（WebSocket + Protobuf/Flatbuffers），社区 TeslaMate（MQTT 转发，非传输层）
   - https://github.com/teslamotors/fleet-telemetry
   - https://docs.teslamate.org/docs/integrations/mqtt/
3. `Tesla fleet telemetry adaptive FEC redundancy packet loss`
   - 关键反向证据：Tesla 公开机制是「断连缓冲 5000 条消息（≥2500 秒），重连后全部投递」—— 典型 reactive ARQ/store-and-forward，非 proactive FEC
   - https://github.com/teslamotors/fleet-telemetry/issues/319
4. `Tesla vehicle cloud "redundant packets" OR "forward error correction" telemetry`
   - 命中：Fleet Telemetry 支持 reliable_ack（ack-based），无 FEC / redundant packets 字样
   - https://github.com/teslamotors/fleet-telemetry

补 1：`"fleet-telemetry" tesla github websocket reconnect buffer reliability`
- 进一步证实"车端 buffer + exponential backoff reconnect (max 30s) + 重发未 ack 数据 (delivery policy = latest)"的纯 ARQ 形态
- https://github.com/teslamotors/fleet-telemetry/blob/main/README.md

## Phase 2 WebFetch (3 次成功，1 次 403)

- https://github.com/teslamotors/fleet-telemetry — README 仅描述 reliable_ack 机制；无 FEC / 冗余 / 业务类型分类
- https://developer.tesla.com/docs/fleet-api/fleet-telemetry — HTTP 403（dev portal 拒绝匿名抓取）；curl 兜底亦 403
- https://bnxt.ai/blog/tesla-app-architecture-live-telemetry-ota-updates-vehicle-cloud-sync — 仅"intelligent retry mechanisms"模糊措辞，无 FEC / 业务类型差分
- https://raw.githubusercontent.com/teslamotors/fleet-telemetry/main/protos/vehicle_data.proto — proto schema 中**无任何** FEC / redundancy / QoS / 业务类型字段

## 工具受限说明

- developer.tesla.com 全局 403（WebFetch + curl 兜底均失败），Tesla 的私有协议规格无法独立验证；但官方开源 fleet-telemetry 实现已覆盖车端 → 云的 1st-mile 传输路径，足以判定**该公开通道是否存在权 1 的 F1-F5 五要素**
- Tesla 车机内部协议栈不公开；本判定仅基于「Tesla 官方对外公开的车-云通道」证据。Tesla 是否在内部 OTA 下行通道或 CAN 网关里使用 FEC，无公开证据可证可证否 — 故不纳入命中
