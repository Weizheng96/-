# 02-tencent-meeting sources

## Phase 1 — WebSearch（react，串行 3 条）
- q1: `腾讯会议 自适应抗丢包 FEC 弱网` → 强相关命中 7 条（华万 / 视频会议官网 / 腾讯天籁白皮书 / 网易云信对比 / 知乎弱网音质 / 云巴巴），确认腾讯会议确有 FEC + 自适应抗丢包技术
- q2: `腾讯会议 网络优化 业务类型 冗余 自适应` → 6 条命中（cnblogs 腾讯会议视频传输算法 / 腾讯天籁实验室 / 知乎 / CSDN QUIC），缩到架构层文档；但"业务类型"具体输入未明示
- q3: `腾讯会议 FEC 冗余率 算法 丢包率 自适应调整` → 8 条命中（华万系列 / 腾讯云 2018 内容关键性 FEC 论文 / CSDN FEC 原理），找到最接近 F1 的"内容关键性级别"概念

## Phase 2 — WebFetch / curl（react，串行 5 次，含 1 次 curl 兜底 + 1 次 SSL fail）
- WebFetch https://www.cnblogs.com/ccloud/p/12951047.html → 仅泛述"时延 vs 带宽 vs 冗余"取舍，未披露 F1-F4 具体算法
- WebFetch https://cloud.tencent.com.cn/developer/article/1020364 → 关键发现：
  - 发布日期 2018-01-15（早于专利授权日 2021-06-08，但腾讯会议产品 2019-12 上线，材料是腾讯云体系内的算法研究，并非直接说明腾讯会议实现）
  - "内容关键性"是 codec / 帧级别静态分级（语音/非语音、LSP/PITCH/GAIN），非从"包长度/到达间隔/突发性"等数据流特征变量得到 → F1 关键限定未证实
  - "发送端根据网络状况反馈结果配置 FEC 冗余率以及关键性级别"——支持 F2 部分（网络状态 + 类业务类型联合），但"传输成功率"是否单独输入未明示
  - 节省 FEC 带宽 55%-100%，但未公开具体公式
- curl https://zhuanlan.zhihu.com/p/180055363 → 受限（694 字节响应，疑似反爬）；未能获取知乎正文
- WebFetch https://blog.csdn.net/QcloudCommunity/article/details/130256708 → 发布日 2023-04-19；内容是 QUIC 方向（连接迁移、登录耗时优化、抗 80% 丢包），不涉及 packet-level FEC 算法
- WebFetch https://source.meeting.qq.com/news/tianlai.html → 发布日 2020-12-31；披露"cFEC + cPLC"联合信源信道编码，但未公开 FEC 冗余率适配的具体数据流特征输入、调度方式
- WebFetch https://www.yun88.com/news/571.html → SSL 证书校验失败，未能抓取

## 工具受限说明
- 知乎 zhuanlan curl 抓取被反爬（response < 1KB）
- yun88.com SSL 证书校验失败
- 上述受限源未影响最终判定——其他源（华万系列 + 腾讯云 + 腾讯天籁官网 + CSDN + cnblogs）已构成对腾讯会议公开技术披露的多源交叉验证
