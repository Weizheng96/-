# 23-xiaomi-cyberdog _sources.md

## Phase 1 WebSearch（粗筛 — 4 query 串行）

1. `Xiaomi CyberDog communication protocol ROS2 DDS FEC redundancy`
   - hit: https://github.com/MiRoboticsLab/cyberdog_ros2/blob/main/README.md
   - hit: https://github.com/MiRoboticsLab/cyberdog_ros2/blob/main/README_EN.md
   - hit: https://arxiv.org/pdf/2508.11366 (Optimizing ROS 2 Communication for Wireless Robotic Systems — 不涉 CyberDog)
   - 关键发现：DDS 中间件 = Cyclone DDS（ROS 2 Galactic），无 FEC 描述

2. `site:github.com MiRoboticsLab cyberdog communication`
   - hit: https://github.com/MiRoboticsLab/cyberdog_motor_sdk/blob/main/README_EN.md
   - hit: https://github.com/MiRoboticsLab/cyberdog_ws
   - hit: https://github.com/MiRoboticsLab/cyberdog_vision
   - hit: https://github.com/MiRoboticsLab/cyberdog_mivins
   - 关键发现：motor SDK 用 LCM；bridges 模块用 gRPC + CAN；无任何 FEC / 冗余 / 业务类型自适应描述

3. `CyberDog cloud control adaptive redundancy packet loss business type`
   - 0 实质命中（返回均为通用 cloud redundancy 概念文 / 非 CyberDog）

4. `小米 CyberDog 通信 冗余 自适应 FEC 业务类型 传输成功率`
   - hit: https://matheecs.tech/study/2021/09/23/cyberdog.html （测评，未提 FEC）
   - hit: https://www.oschina.net/news/253785 （CyberDog 2 开源率新闻）
   - hit: https://www.zhihu.com/question/617282032 （评论性文章）
   - hit: https://blog.csdn.net/u010178611/article/details/82656838 （通用 FEC 算法详解，非 CyberDog）
   - 关键发现：无任何中文资料把 CyberDog 与 FEC / 业务类型自适应冗余关联

## Phase 2 WebFetch（深抓 — 2 url）

1. https://github.com/MiRoboticsLab/cyberdog_ros2/blob/main/README_EN.md
   - 确认：只声明 `Cyclone DDS`；无 QoS / FEC / 冗余 / 业务类型 / 自适应调度任一描述

2. https://github.com/MiRoboticsLab/cyberdog_motor_sdk/blob/main/README_EN.md
   - 确认：LCM + multicast；README 自承 "difficult to ensure real-time LCM communication when running on the user PC" — 即无 proactive FEC 层补偿；无 UDP / 重传 / FEC / 冗余 / 业务类型描述

## 工具限制说明

- WebSearch 与 WebFetch 均成功，无需 curl 兜底
- 未深入分析 CyberDog 1/2 闭源云端控制路径（小米云）—— 该路径不开源，公开资料零；按"未检索到公开来源"处理
