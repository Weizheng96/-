# 36-siasun-rtmw 检索留痕

## Phase 1 粗筛 query（4/4 用尽，无 WebFetch 深抓）

### q1
- query: 新松 SIASUN RobotMaster 远程运维 通信协议 抗丢包
- 命中：
  - https://docs.mech-mind.net/1.5/zh-CN/SoftwareSuite/RobotIntegrations/FullControlProgram/Siasun/Siasun.html （Mech-Mind 集成文档）
  - https://www.siasun.com/ （新松官网）
  - https://www.siasunagv.com/ （新松 AGV 子公司）
  - https://www.sd-siasun.com/ （山东新松工业软件）
- 评估：均为公司主页 / 集成文档，无传输层主动冗余技术披露

### q2
- query: 新松 工业机器人 云端 通信 FEC 前向纠错 冗余
- 命中：
  - https://blog.csdn.net/limengshi138392/article/details/142005631 （FEC 科普）
  - https://www.ebyte.com/news/2053.html （FEC 汉明码）
  - https://wiki.mbalib.com/wiki/前向纠错 （FEC 百科）
- 评估：全为 FEC 一般概念，与新松无关

### q3
- query: SIASUN robot teleoperation network protocol packet loss redundancy
- 命中：
  - https://link.springer.com/article/10.1007/s00170-025-16236-w （IIoT teleoperation + VR）
  - https://www.netmaker.io/resources/teleoperation （teleoperation 一般综述：MQTT/WebSocket/RTP/多链路冗余）
  - https://www.robotsusa.com/SIASUN-Intelligentdeployment-Recoveryrobot-Intelligent-Deployment-Recovery-Robot.htm （新松硬件产品介绍）
- 评估：通用 teleoperation 综述描述多链路冗余但非 packet-level 主动 FEC；新松硬件描述未含网络协议细节

### q4
- query: "新松" "RobotMaster" OR "远程通信" 协议 业务 自适应 冗余
- 命中：
  - https://blog.csdn.net/jiyanghao19/article/details/139914409 （新松机器人编程示例）
  - https://www.siasun.com/about.html （新松公司介绍）
  - https://zh.wikipedia.org/zh-hans/新松机器人 （维基百科）
- 关键发现：RobotMaster 实为 Jabez Technologies / Hypertherm 第三方离线编程软件，并非新松自有产品；候选产品名构造存在归属歧义

## Phase 2 深抓
未执行——Phase 1 已确认候选产品归属歧义 + 0 高相关命中，进入早剪枝。
