# Verdict — FD.io VPP upstream（核心技术候选 CT-2）

> 主体类型：S1（上游开源）；权 1 / 9；**P0**（依据：上游开源核心技术 / R-OPENSOURCE 双层激活）

## 核心组织
**Linux Foundation Networking / FD.io 项目宿主** + **Cisco（NASDAQ: CSCO）—— VPP 主要贡献者** + **Intel（NASDAQ: INTC）**

## F1-F5 命中表
| F# | 证据 | 命中 |
|---|---|---|
| F1 | VPP 文档：是用户态多线程 vSwitch / vRouter | **字面命中** |
| F2 | VPP `vlib_worker` 多线程模型，可通过 `cpu` 配置块设置 worker 线程数与 CPU 集合 | **字面命中** |
| F3 | VPP NUMA-aware 端口绑定；状态采集存在但不如 OVS auto-LB 明确 | **字面命中候选 / 部分公开资料不足** |
| F4 | VPP 主线 auto rebalance 机制相对有限——主要靠 admin 手动 / 启动时分配 | **公开资料不足**（auto-LB 在 VPP 中没有 OVS 那样明确的 feature） |
| F5 | VPP 支持 worker handoff 机制 — 流可以在 worker 间迁移 | **字面命中候选**（worker handoff = 端口服务的 worker 改变） |

## 时间线：VPP 17.04+（2017+），post-grant 主导

## 状态机三栏
| 权 | 原始 | 调整 | 最终 |
|---|---|---|---|
| 权 1 / 9 | **第 3 档：公开资料不足（强候选）** | F4 auto trigger 弱；F5 worker handoff 等同命中 | 第 3 档 |

## 总结
VPP F1/F2/F5 字面或等同命中；F3/F4 公开资料不足（无明确 auto-LB feature）；落第 3 档强候选——比 OVS upstream 弱一档。
