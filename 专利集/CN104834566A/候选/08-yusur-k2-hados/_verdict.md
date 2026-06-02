# 08-yusur-k2-hados verdict

## 候选基本信息
- 名称：中科驭数 K2/K2Pro DPU + HADOS 软件栈 / 组织：中科驭数 Yusur（独角兽）
- 类型：产品 / 初判命中 F#：F1,F2,F3 / 专利公开日：2015-08-12

## 检索粗筛（react，4 WebSearch）
- 已执行 4 条 WebSearch（留痕见 `_sources.md`），有信号（YUSUR 确实做 vSwitch / OVS 转发面卸载），未早剪枝，进入深抓。
- 结论：公开材料只到「OVS 硬件卸载 / 流表卸载 / 流调度与隔离」层，缺转发线程级负载驱动端口再分配细节；且架构方向与本专利相反。

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测 K 个转发处理线程状态属性） | 公开资料不足/架构不匹配 | "flow table matching... offloaded:yes / dp:tc... avoiding the use of host CPU resources"（YUSUR 把流表匹配卸载到硬件，绕过宿主机 CPU） | https://kube-ovn.readthedocs.io/zh-cn/latest/en/advance/offload-yusur/ | YUSUR 卸载后转发由硬件 TC/eSwitch 执行，CPU 软件转发线程退出热路径；无「检测 K 个转发线程状态」机制公开 |
| F2（状态满足预设触发条件） | 公开资料不足/架构不匹配 | 未找到 | — | K2-Pro 仅「精细的流调度与隔离机制」（硬件流调度），无「按转发线程状态触发再分配」表述 |
| F3（调整≥1 线程所服务的交换端口） | 公开资料不足/架构不匹配 | "shorten the data path without modifying the OVS control plane"（仅数据面下沉硬件，不改控制面端口↔线程映射逻辑） | https://kube-ovn.readthedocs.io/zh-cn/latest/en/advance/offload-yusur/ | 公开实现是流表硬件卸载，非软件「端口↔转发线程运行时再分配」；未检索到端口迁移机制 |
| F4（K 为正整数，多核线程↔CPU 一一对应） | 公开资料不足 | "支持高通量多队列 DMA"「KPU 异构计算核 数据流驱动」 | https://www.yusur.tech/dpu/K2-Pro | 有多队列/多核硬件，但非「K 软件转发线程绑 K CPU + 按负载迁移端口」的专利形态 |

## 已检查文档清单
- YUSUR K2-Pro 产品页（虚拟交换二层交换 / 200Gbps 线速 / NP 可编程 L2~L7）— https://www.yusur.tech/dpu/K2-Pro
- YUSUR/CSDN K2-Pro 技术博客（KPU 架构 / 数据流驱动 / 80Mpps / 精细流调度与隔离）— https://blog.csdn.net/yusur/article/details/140042733
- Kube-OVN 官方「Offload with YUSUR」文档（决定性：OVS 流表硬件卸载 offloaded:yes/dp:tc，绕过宿主机 CPU）— https://kube-ovn.readthedocs.io/zh-cn/latest/en/advance/offload-yusur/
- Google Patents 搜中科驭数同主题自有专利 — 未检索到署名匹配专利

## 最终判定
**第 5 档：已排除（架构层级不同）**

判定依据：本专利核心是**软件 vSwitch 多核转发线程**（每线程绑 1 CPU）按线程负载状态在运行时**再分配交换端口↔线程映射**（F1 检测线程状态→F2 触发条件→F3 迁移端口）。YUSUR 公开的卸载模型恰恰相反——把 OVS 流表匹配/转发**下沉到 DPU 硬件**（`offloaded:yes`/`dp:tc`，eSwitch/TC flower），缩短数据路径并**绕过宿主机 CPU 转发线程**，使软件转发线程退出热路径。这是把「软件多核转发线程」整体卸载/消解，而非在其内部实现专利的「按线程负载再分配端口」机制——属架构层级不同（criterion iii），构成真排除依据（非 0 命中排除）。

## 升级路径（第3-4档填）
（不适用——已落第 5 档）
若日后 YUSUR 公开 HADOS 软件转发面（DPDK/PMD 形态）内部存在「按转发线程实时负载动态迁移 rxq/端口到不同 CPU」的实现细节，则可重启评估并升档。

## 总结一句话
YUSUR DPU/HADOS 走 OVS 流表硬件卸载、绕过宿主机 CPU 转发线程，与本专利「软件多核转发线程按负载再分配端口」架构层级相反，落第 5 档（已排除）。
