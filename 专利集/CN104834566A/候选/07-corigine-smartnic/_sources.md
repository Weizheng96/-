# 07-corigine-smartnic 检索留痕（_sources.md）

候选：芯启源 Corigine 第四代 SmartNIC / DPU（NP-SoC 多线程处理）
专利公开（授权）日：2015-08-12

## Phase 1 — react 粗筛 WebSearch（串行）
1. `芯启源 Corigine DPU SmartNIC vSwitch 卸载 多线程 转发 负载均衡`
   → 命中第四代 SmartNIC 架构报道：NP-SoC + 多线程处理模式、Agilio 支持 OVS 卸载 / TC-Flower / RTE_FLOW、P4/C 可快速实现负载均衡/防火墙/云网关。营销层有信号，缺线程↔端口动态再分配细节。
   - http://www.chinaiol.com/News/Content/202204/42_37224.html
   - https://cloud.tencent.com/developer/article/1991201
2. `芯启源 DPU NP-SoC 转发线程 端口 队列 调度 OVS rxq 卸载 实现`
   → 仍只到架构层（NP 报文处理引擎 + 流处理器 + 多线程达 ASIC 性能；Agilio 支持 OVS/TC-Flower/RTE_FLOW/vRouter 卸载）。明确："关于具体的转发线程、端口队列调度、rxq 卸载等细节实现的技术文档未在搜索结果中出现。"
   - https://zhuanlan.zhihu.com/p/687666835
   - https://www.cnblogs.com/kevin-jun-2022/p/16875676.html
3. `Corigine 芯启源 patent forwarding thread port queue scheduling vSwitch load balance`
   → 浮出两件 USPTO 专利（见下，均非芯启源所有）+ Corigine OVS 产品页。
   - https://www.corigine.com/TechnologiesandApplications-201.html
4. `Corigine assignee patent vSwitch OVS offload forwarding thread queue load balancing SmartNIC`
   → Corigine 谱系自有专利方向 = OVS megaflow 硬件卸载（US20210144094 "EXTENSION OF OPENVSWITCH MEGAFLOW OFFLOADS TO HARDWARE"），即把流表 match-action 卸到网卡硬件，绕过主机 CPU 转发线程。
   - https://patents.justia.com/patent/20210144094
   - https://www.corigine.com.cn/UploadFiles/pdf/2021-08-04/152108157220105.pdf （Agilio OVS-TC 加速白皮书）

## Phase 2 — react 深抓 WebFetch（串行）
- https://patents.google.com/patent/US12452176B2/en
  「Load balancing method for multi-thread forwarding and related apparatus」
  → assignee = **Huawei Technologies**（非芯启源），priority 2021-06-10。是华为自己后续专利，不能作为芯启源实施本专利的证据。
- https://patents.google.com/patent/US11575620B2/en
  「Queue-to-port allocation」
  → assignee = **Intel**（非芯启源），priority 2019-03-29。且其触发机制是"端口不可用/拥塞"而非"转发线程负载状态"——机制不同。
- https://www.corigine.com/TechnologiesandApplications-201.html （Agilio OVS 应用页）
  → 仅"transparent offload architecture replicates the packet data fast path on SmartNIC，回收 80% CPU、吞吐 5X"。无任何"多转发线程负载检测 / rxq / port-to-thread 再分配"表述。
- https://www.corigine.com.cn/UploadFiles/pdf/2021-08-04/152108157220105.pdf （Agilio OVS-TC 白皮书 PDF，已落盘）
  → 机制 = 把 OVS 流表 match-action 卸载到网卡硬件、绕过主机 CPU 处理；非"软件 vSwitch 内按转发线程负载迁移端口/队列"。

## 关键结论
公开材料一致停在"OVS/megaflow 硬件卸载 + NP-SoC 多线程"营销/架构层；F2（转发线程状态满足预设触发条件）/F3（调整线程所服务交换端口）的判别性细节无公开来源。两件标题相近的 USPTO 专利分别属 Huawei / Intel，均非芯启源。无明示反向证据（0 命中≠反向）。
