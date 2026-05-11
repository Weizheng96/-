# 候选：Marvell OCTEON 10 DPU

## 候选标识
- candidate_slug: `21-marvell-octeon10`
- 主体类型：B. DPU 芯片厂
- 适用独立权：权 35 + 权 23

## §A 主流来源摘要

| # | 源 | URL | 引文 |
| --- | --- | --- | --- |
| 1 | Marvell OCTEON 10 product page | https://www.marvell.com/products/data-processing-units.html | OCTEON 10 软件栈含 vSwitch / Open vSwitch；VPP 插件含 LACP |
| 2 | OCTEON 10 CN102/CN103 announcement | https://www.marvell.com/company/newsroom/two-new-marvell-octeon-10-processors-for-networking-devices.html | 2023-12 发布；用于 routers / firewalls / 5G small cells / SD-WAN |
| 3 | Asterfusion Helium DPU (基于 OCTEON) | https://cloudswit.ch/blogs/marvell-octeon-devices-power-edge-computing/ | Helium DPU 集成 OCTEON CN9670 |

## §D 状态机三栏判定

| 独立权 | 状态机原始判定 | 后置调整记录 | 最终 verdict |
| --- | --- | --- | --- |
| 权 23 / 35 | **公开资料不足（第 4 档弱候选）** | OCTEON 10 软件栈包含 vSwitch + LACP，但 Marvell 自身公开材料中**0 命中**"多卡 + sync flow"具体实现 | **公开资料不足（第 4 档弱候选）** |

### 最终 verdict

**公开资料不足**：Marvell OCTEON 10 提供 vSwitch + LACP 软件 building blocks，但无公开多 NIC 同步流表具体实现。

## 总结一句话

Marvell OCTEON 10 软件栈含 vSwitch+LACP building blocks 但无具体多 NIC sync flow 实现公开，**落第 4 档公开资料不足弱候选**。
