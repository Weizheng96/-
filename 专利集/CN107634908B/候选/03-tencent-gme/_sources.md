# 证据索引 — 03-tencent-gme

## Phase 1 — WebSearch query 留痕

| # | Query | 主要命中 |
| --- | --- | --- |
| 1 | `Tencent GME 游戏多媒体引擎 抗丢包 FEC` | CSDN 腾讯 GME 官方博客（FEC 4+1/4+4 信道编码原理）；腾讯云 GME 产品页 |
| 2 | `腾讯云 GME 网络自适应 业务场景 战斗 闲聊 FEC 冗余` | SegmentFault 镜像「腾讯云GME之网络编解码」（房间类型↔策略映射）；ydwlcloud 评测；知乎 p/96091331 |
| 3 | `腾讯 GME 房间类型 流畅 标准 高清 业务类型 SDK 配置` | 腾讯云官方文档「实时语音」（房间类型 enum）；新手指引；Cocos GME 接入 |
| 4 | `GME Tencent SetAudioCategory SetRoomType FEC adaptive packet loss` | 多为通用 FEC / TRTC 资料，未拿到 SDK 级新增证据 |

## Phase 2 — WebFetch / curl 留痕

| # | URL | 工具 | 结果 |
| --- | --- | --- | --- |
| 1 | https://blog.csdn.net/Tencentgme/article/details/103857430 | WebFetch | 部分付费墙，仅获取公开摘要 |
| 2 | https://cloud.tencent.com/developer/article/2649149 | WebFetch | 营销/产品概览，无技术细节 |
| 3 | https://segmentfault.com/a/1190000021501763 | WebFetch | **核心命中** — FEC 4+4 上限、按房间类型选 FEC/ARQ/UDT、动态加降冗余的 verbatim |
| 4 | https://zhuanlan.zhihu.com/p/96091331 | WebFetch + curl 兜底 | WebFetch 403；curl 仅 694 字节登录墙 → 工具受限 |
| 5 | https://cloud.tencent.com/document/product/607/15232 | WebFetch | 官方接口文档：房间类型由 SDK 调用方 `ITMG_ROOM_TYPE_FLUENCY` 显式设置；监控 weight/loss/delay |
| 6 | https://cloud.tencent.com/document/product/607/18522 | WebFetch | 官方音质选择文档：流畅/标准/高清三档场景说明（开黑、休闲、音乐互动）verbatim |
| 7 | https://segmentfault.com/a/1190000021233052 | WebFetch | 技术方案，FEC 仅一句"信道编码处理网络抗抖动抗丢包"，无策略细节 |
| 8 | https://zhuanlan.zhihu.com/p/1997251979970363729 | WebFetch + curl 兜底 | WebFetch 403；curl 694 字节登录墙 → 工具受限 |

## 本地落盘文件

- `zhihu_p96091331.html` — 694 字节登录墙 placeholder
- `zhihu_ydwlcloud.html` — 694 字节登录墙 placeholder
