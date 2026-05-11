# Verdict — Cilium / Isovalent（被 Cisco 2024 收购）

> 主体类型：S1 + S5；权 1 / 9；**P1**

## 核心组织
**Cisco Systems（NASDAQ: CSCO）—— Isovalent 2024 收购**；上游 Linux Foundation / CNCF Cilium 项目

## F1-F5 命中表
| F# | 证据 | 命中 |
|---|---|---|
| F1 | Cilium 是 eBPF dataplane CNI；不严格是 vSwitch 形态——与本专利"虚拟交换机 vSwitch"措辞存在解读差异 | **作用域限定 / 等同命中候选**（Cilium 在数据面承担虚拟交换功能，等同；但 F1 字面"vSwitch"措辞需走等同三步法）|
| F2 | Cilium eBPF 不是传统多线程 PMD 模型——eBPF 是内核数据路径，由内核 softirq / NAPI 驱动 | **公开资料不足 / 等同弱**（"K 个转发处理线程"在 eBPF 模型下 mapping 到内核 RX queue + softirq；等同度需个案判断） |
| F3-F5 | Cilium 提供端口与 service mesh 重映射（k8s service / endpoint），但触发条件 / 调整动作与本专利方法权措辞差异较大 | **公开资料不足** |

## 等同三步法（F1）
- 同手段：Cilium eBPF kernel datapath vs vSwitch user-space PMD —— 不同手段
- 同功能：都做虚拟网络转发 —— ✅
- 同效果：性能等价（取决于硬件）——部分等价
- 显而易见性：本领域熟知 eBPF 是 vSwitch 的相邻替代 —— ✅
- **等同命中存疑**（手段差异较大，但功能 / 效果 / 显而易见性都成立）

## 状态机三栏
| 权 | 原始 | 调整 | 最终 |
|---|---|---|---|
| 权 1 / 9 | **第 4 档：公开资料不足（弱候选）** | F1 等同度弱；F2-F5 与 eBPF 模型 fit 度低 | 第 4 档 |

## 总结
Cilium / Isovalent：eBPF dataplane 与本专利 vSwitch + PMD 多线程模型差异较大，F1-F2 等同度弱，F3-F5 公开资料不足；落第 4 档（公开资料不足弱候选）。
