# aliyun/iotkit-embedded （Link Kit C-SDK） src/ 顶层模块清单

来源：https://api.github.com/repos/aliyun/iotkit-embedded/contents/src?ref=v3.0.1
抓取时间：2026-05-26

## src/ 子目录全清单

| 目录 | 说明 |
|---|---|
| `atm` | AT modem 相关（串口模组接入） |
| `coap` | CoAP 协议接入 |
| `dev_bind` | 设备绑定 |
| `dev_model` | 物模型（TSL） |
| `dev_reset` | 设备重置 |
| `dev_sign` | 设备签名认证 |
| `dynamic_register` | 一型一密动态注册 |
| `http` | HTTP 接入 |
| `http2` | HTTP/2 接入（含文件上传） |
| `infra` | 基础设施（日志、JSON、HAL 适配等） |
| `mqtt` | **MQTT 协议（标准实现）** |
| `ota` | OTA 升级 |
| `wifi_provision` | Wi-Fi 配网 |

## 关键反向证据

- **无 FEC / redundancy / forward error correction 相关模块**
- **无 traffic classifier / business type / adaptive scheduling 相关模块**
- **无 packet-level proactive redundancy 相关模块**
- 传输可靠性完全依赖 `mqtt` 子目录内的标准 MQTT 协议（QoS 0/1/2 = ARQ）
