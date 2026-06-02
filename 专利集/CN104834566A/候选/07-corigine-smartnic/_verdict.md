# 07-corigine-smartnic verdict

## 候选基本信息
- 名称：芯启源 Corigine 第四代 SmartNIC / DPU（NP-SoC 多线程处理）
- 组织：芯启源 Corigine
- 类型：产品
- 初判命中 F#：F1,F3,F4
- 专利公开日：2015-08-12

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F1（检测 K 个转发线程状态属性） | 公开资料不足 | 仅"NP-SoC 模式…多线程的处理模式，使其可以达到 ASIC 固化芯片的数据处理能力"——只证明存在多线程，未证明"检测各转发线程的状态属性（负载/亲和性/资源额度）" | http://www.chinaiol.com/News/Content/202204/42_37224.html | 多线程≠对线程状态做检测判据 |
| F2（线程状态满足预设触发条件） | 公开资料不足 | 未找到——公开材料无任何"按转发线程负载/亲和性触发再分配"表述；检索结果明确"转发线程、端口队列调度、rxq 卸载等细节实现的技术文档未出现" | https://zhuanlan.zhihu.com/p/687666835 | 判别性特征，无公开来源 |
| F3（调整线程所服务的交换端口） | 公开资料不足（机制疑似不同） | "transparent offload architecture replicates the packet data fast path on SmartNIC"（把 OVS 流表 match-action 卸载到网卡硬件、绕过主机 CPU 转发线程）；Corigine 谱系自有专利方向为 OVS megaflow 硬件卸载（US20210144094） | https://www.corigine.com/TechnologiesandApplications-201.html ; https://patents.justia.com/patent/20210144094 | 其卸载是"绕过主机转发线程"，与本专利"在软件 vSwitch 内按线程负载迁移端口/队列"架构层级/机制不同；但无明示反向证据 |
| F4（K 为正整数，多核多端口） | 字面 | "通用 ARM 架构结合…NP 芯片（RISC-V 内核）、多线程的处理模式" | http://www.chinaiol.com/News/Content/202204/42_37224.html | 仅证明多线程多核存在，弱命中 |

## 已检查文档清单
- 芯启源首次公开"SmartNIC 第四代架构"赋能 DPU 蓝海（NP-SoC + 多线程 + Agilio OVS/TC-Flower/RTE_FLOW/vRouter 卸载 + P4/C 负载均衡）— http://www.chinaiol.com/News/Content/202204/42_37224.html
- 可编程 DPU 加速容器云网络卸载（明确缺转发线程/端口队列调度细节）— https://zhuanlan.zhihu.com/p/687666835
- Corigine Open vSwitch Applications 产品页（transparent offload，回收 80% CPU、吞吐 5X，无线程负载再分配表述）— https://www.corigine.com/TechnologiesandApplications-201.html
- Corigine Agilio OVS-TC 加速白皮书 PDF（机制=流表 match-action 硬件卸载，绕过主机 CPU）— https://www.corigine.com.cn/UploadFiles/pdf/2021-08-04/152108157220105.pdf
- US12452176B2「Load balancing method for multi-thread forwarding」→ assignee=Huawei（非芯启源）— https://patents.google.com/patent/US12452176B2/en
- US11575620B2「Queue-to-port allocation」→ assignee=Intel，触发机制=端口不可用（非线程负载）— https://patents.google.com/patent/US11575620B2/en

## 最终判定
**第 4 档：F 命中不足（<60%，判别性特征公开资料不足）**

判定依据：4 个特征中仅 F4（多线程多核）字面弱命中；F1/F2/F3 这三个承载本专利发明核心（检测转发线程状态→满足预设触发条件→运行时迁移线程所服务的交换端口）的判别性特征，公开材料全部停在"OVS/megaflow 硬件卸载 + NP-SoC 多线程"营销/架构层，无任何"按线程负载动态再分配端口/队列"的披露。且其商用机制（把流表卸到网卡硬件、绕过主机 CPU 转发线程）与本专利"软件 vSwitch 内的线程↔端口动态再分配"在架构层级上疑似不同。鉴于无明示反向证据（0 命中≠反向，故不入第 5 档），仅凭"多线程"字面不可外推 F1/F2/F3 命中，落第 4 档。

## 升级路径（第3-4档填）
- 取得芯启源 Agilio OVS Software Architecture White Paper 全文 / Agilio 软件用户手册，核查其在 OVS-DPDK PMD 软件路径（非纯硬件卸载路径）是否存在"按 PMD 线程负载/亲和性动态再分配 rxq→PMD 线程"的机制（OVS 上游有 pmd-rxq-assign 类机制，需确认芯启源是否在其卸载方案中保留并由其控制）。
- 检索芯启源（上海）半导体科技有限公司在中国国家知识产权局 2015-08-12 之后申请的同主题专利（vSwitch 数据面转发线程↔端口负载再分配），竞品自有专利常 verbatim 披露真实实现路径。
- 若拿到移动云/天翼云/浙江移动 SD-WAN 商用部署的技术方案文档，核查数据面是否含 F2/F3。

## 总结一句话
芯启源 SmartNIC 公开材料仅到"OVS 硬件卸载 + NP-SoC 多线程"架构层，仅 F4 字面弱命中、F1/F2/F3 判别性特征公开资料不足且机制疑似为"绕过主机转发线程的硬件卸载"，无明示反向证据，落第 4 档。
