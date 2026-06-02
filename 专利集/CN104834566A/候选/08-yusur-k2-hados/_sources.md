# 证据索引 — 08-yusur-k2-hados

## Phase 1 — react 粗筛（WebSearch 留痕）
1. `中科驭数 Yusur HADOS DPU vSwitch 转发 卸载 负载均衡 多核`
   - 命中 yusur.tech 产品/方案页 + CSDN「网络功能卸载」。信号：HADOS 做 vSwitch 硬件卸载、网络/存储/安全/管理卸载、SDA/KPU 架构。→ 相关，继续。
2. `中科驭数 K2 DPU 转发线程 端口 调度 流表 OVS 卸载 数据面`
   - 命中 K2-Pro 产品页 + CSDN 技术博客。信号：K2-Pro「精细的流调度与隔离机制」「网络卸载/表项卸载/存储卸载/RDMA 卸载」「OVN/OVS 做转发面，网络 I/O 由 DPU 卸载」。→ 硬件卸载引擎方向。
3. `中科驭数 K2 DPU 多核 转发线程 负载均衡 端口 队列 绑核 动态调整`
   - 仅得 K2-Pro 端口/多队列 DMA、80Mpps、KPU 架构等芯片规格；明确「未找到转发线程/负载均衡/绑核/动态调整的微观实现细节」。
4. `Yusur 中科驭数 HADOS vSwitch dataplane forwarding thread port queue rebalance offload`
   - 命中 Kube-OVN 官方「Offload with YUSUR」文档（最强架构证据）。
   - 补：Google Patents `中科驭数 Yusur 专利 转发 线程 端口 队列 负载 调度 DPU` —— 未检索到中科驭数署名的同主题自有专利。

## Phase 2 — react 深抓（WebFetch 留痕）

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | K2-Pro 产品页(2024) | 厂商产品页 | https://www.yusur.tech/dpu/K2-Pro | 仅「虚拟交换二层交换 / 200Gbps 线速交换 / NP 可编程 L2~L7」；无转发线程↔端口动态再分配细节 |
| 2 | 2024-07 | 厂商技术博客 | https://blog.csdn.net/yusur/article/details/140042733 | K2-Pro「KPU 架构 / 数据流驱动 / 80Mpps / 200G / 精细流调度与隔离」；无线程级实现 |
| 3 | Kube-OVN 文档(>2015) | 第三方集成文档(决定性) | https://kube-ovn.readthedocs.io/zh-cn/latest/en/advance/offload-yusur/ | YUSUR CONFLUX-2200E 把 OVS 流表匹配/隧道封装卸载到硬件，`offloaded:yes`/`dp:tc`，缩短数据路径绕过宿主机 CPU 转发线程；不改 OVS 控制面，数据面下沉硬件 |

## 关键判断
YUSUR 公开卸载模型 = OVS 硬件卸载（流表下沉 DPU 硬件 TC/eSwitch，CPU 转发线程退出热路径）。
本专利核心 = 软件 vSwitch 多核转发线程（每线程绑 1 CPU）按线程负载状态运行时再分配交换端口（F1 检测线程状态→F2 触发条件→F3 迁移端口↔线程映射）。
二者架构层级相反：硬件引擎卸载 vs 软件线程级端口再均衡。未检索到任何 F1-F3 的转发线程负载驱动端口再分配公开证据。
