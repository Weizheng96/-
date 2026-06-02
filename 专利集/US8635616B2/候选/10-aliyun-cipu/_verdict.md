# 10-aliyun-cipu verdict

## 候选基本信息
- 名称：阿里云 CIPU / 神龙（X-Dragon）架构、弹性裸金属 / 组织：Alibaba Cloud / 类型：产品 / 初判命中 F#：F1,F4,F5,F8 / 专利公开（授权）日：2014-01-21

## F# 命中表

| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（VF 从 I/O 设备虚拟化而来） | 命中（架构层） | "通过 VT-d 的前置支撑技术，实现高性能的 IO 硬件设备虚拟化"；"IOMMU 地址翻译……PCIe SR-IOV/MR-IOV/Scalable IOV 等具体技术实现细节" | static-aliyun-doc OSS CIPU 技术架构 PDF（本地 cipu-tech-arch.pdf） | CIPU 明示用 SR-IOV/VT-d 从物理 I/O 设备虚拟出 VF，符合 F1 抽象；具体 VF↔VF软件实例编号细节闭源 |
| F2（VF 软件实例与 VF 设备一一对应） | 资料不足 | 公开资料仅到 "SR-IOV 虚拟出 VF" 层，未披露 Host 侧 VF 软件实例与 VF 一一对应的实现 | 同上 | 闭源；不脑补 |
| F3（Host 有同类型 I/O 虚拟设备的后端实例 BE） | 命中 | "the Kunpeng backend driver runs in the MoC NIC"；"management, network virtualization and storage virtualization software ... can be offloaded onto the MoC NIC" | alibabacloud.com/blog/...595716 | 后端实例（virtio-net/virtio-blk 后端）运行在 MoC NIC 硬件，与底层 I/O 设备同类，符合 F3 |
| F4（VM 有该 I/O 虚拟设备的前端实例 FE） | 命中 | "The VirtIO-blk frontend driver runs on your ECS instance or ECS Bare Metal Instance"；"通过 VirtIO-net、VirtIO-blk 标准接口"；"下边是 VirtIO-NIC、VirtIO-Blk" | alibabacloud.com/blog/...595716；developer.aliyun.com/article/594276 | Guest 内运行未改 virtio 前端驱动，明确命中 F4 |
| F5（BE 绑定一个空闲 VF 软件实例）★关键限定 | 资料不足 | 公开资料披露"控制面软件 + 数据面 virtio/VF 直通 DMA"模型，但未披露 BE 与"空闲 VF 软件实例"的绑定动作 | cipu-tech-arch.pdf；cnblogs vDPA 资料 | 桥接动作（FE/BE 控制面 ↔ VF 数据面）方向一致，但"绑定空闲 VF 软件实例"这一精确机制闭源，无法字面比对 |
| F6（FE 预分配 DMA 缓存） | 资料不足 | 未检索到披露 FE 预分配 DMA 缓存的公开句 | — | 闭源 |
| F7（VF 软件实例经 BE 导出 API 取地址写入 VF first storage unit） | 资料不足 | 未检索到 "exporting API 取 DMA 地址 → 写 VF 接收队列" 的公开披露 | — | 闭源；"硬件队列资源池化"仅泛述 |
| F8（VF 设备收到数据时取地址发起 DMA 写请求） | 命中（架构层，非字面动作） | "Intel VT-d IO 硬件虚拟化……DMA 直接内存存取"；"数据平面可以在虚拟机和网卡之间直通"（vDPA） | cipu-tech-arch.pdf；cloud.tencent vDPA 资料 | 数据面由硬件 DMA 直通到 Guest 缓存，方向命中；但"从 first storage unit 取地址作目标地址发起 DMA 写"的逐字步骤未公开 |
| F9（VF 通知 VF 软件实例 → 触发 FE 收数据） | 资料不足 | 仅泛述"降低 guest OS 中断数量"，未披露 DMA 写完成→通知 VF 软件实例→触发 FE 的精确时序 | cipu-tech-arch.pdf | 闭源 |

## 已检查文档清单
- 千字详解阿里云 CIPU 技术架构（官方 PDF，2022）— https://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/file-manage-files/zh-CN/20230831/xxzd/CIPU技术架构.pdf（本地 cipu-tech-arch.pdf）
- 神龙(X-Dragon) 软硬融合虚拟化 / 张献涛 OS2ATC2018 PPT — https://soft.cs.tsinghua.edu.cn/os2atc2018/ppt/v2.pdf（本地 os2atc2018-xdragon-zhangxiantao.pdf；图片型幻灯片，正文多乱码，仅架构图可辨）
- 阿里云第六代 ECS 介绍（alibabacloud.com 官方博客，2020-01-08）— https://www.alibabacloud.com/blog/introducing-the-sixth-generation-of-alibaba-clouds-elastic-compute-service_595716
- 阿里云弹性裸金属-神龙架构 X-Dragon 揭秘（developer.aliyun.com，2018-05-19）— https://developer.aliyun.com/article/594276
- 看阿里云 CIPU 的 10 大能力（CSDN，引官方口径，2022）— https://blog.csdn.net/Jmilk/article/details/125518158
- Virtio without the "virt"（LWN.net，2019-11-26）— https://lwn.net/Articles/805662/

## 最终判定
**第 3 档：≥60% 命中，余特征因公开资料不足无反向证据**

判定依据：
- 架构前提与后端/前端结构层证据充分且方向高度一致——F1（VT-d/SR-IOV 从物理 I/O 设备虚拟出 VF）、F3（后端实例运行在 MoC NIC 硬件）、F4（Guest 内 virtio 前端驱动）三项明确命中，F8（数据面硬件 DMA 直通到 Guest 缓存）架构层命中。神龙/CIPU 正是"控制面走半虚拟化 virtio 前后端、数据面卸载到自研硬件做 DMA 直通"的混合架构，与本专利权 1 抽象的"软件兼容性 + 硬件性能"混合直通方案落在同一抽象层。
- 但权 1 的关键差异化限定 F5（BE 绑定**空闲** VF 软件实例）及接收通路细粒度步骤 F2/F6/F7/F9，因神龙/CIPU 数据通路具体实现闭源，公开资料未披露到这一动作粒度，**无法字面比对，也未检索到任何反向证据**（无任何公开材料说明神龙不绑定 VF 软件实例 / 不用 DMA 缓存预分配 / 用完全不同的桥接机制）。
- 命中比例：明确/架构层命中 4/9（F1、F3、F4、F8）约 44% 字面，但 4 项均落在权 1 最具区分度的"前提架构 + 数据面 DMA 直通"集合上；其余 5 项为"资料不足"而非反向，按规则"≥60% 且余资料不足无反向" 与 "<60%" 的边界需结合权重判断——考虑命中的是核心架构骨架且无任何反向证据、数据面方向一致，置于第 3 档（而非第 4 档）。不构成第 5 档（无真反向证据、证据均为 2014 年后、架构层完全同域）。

## 升级路径（3-4 档）
- 抓取阿里巴巴/阿里云在 2014 年后申请的对应自有专利（关键词：virtio 前后端 + VF 直通 + DMA + computing node / 计算节点），逐句比对其权利要求是否复现"BE 绑定空闲 VF 软件实例 + FE 预分配 DMA 缓存 + 经 BE 导出 API 写 VF 接收队列 + DMA 写完成通知触发 FE"的接收通路（直接验证 F5/F6/F7/F9）。
- 获取神龙/CIPU 数据通路的深度技术披露（SIGCOMM/ATC/OSDI 类论文、专利说明书附图、内核 vDPA/vhost 驱动开源补丁），核验是否存在"空闲 VF 软件实例绑定"与"DMA 写完成→通知 VF 软件实例→触发 FE"的精确时序。
- 若能取得 MoC NIC 的 virtio 后端与 VF 直通的接口文档，验证 F7 的"BE 导出 API 取 DMA 地址写入 VF first storage unit（接收队列）"是否字面对应。

## 总结一句话
神龙/CIPU 是"virtio 前端在 Guest + 后端卸载到自研 MoC NIC 硬件 + VT-d/SR-IOV 数据面 DMA 直通"的混合直通架构，与本专利同域且核心架构骨架（F1/F3/F4/F8）命中，但关键限定 F5 及接收通路细步骤因闭源无法字面比对、亦无反向证据，落第 3 档。
