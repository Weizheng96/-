# Verdict — Microsoft Hyper-V Virtual Switch + Azure AccelNet

> S1+S2；权 1/11；**P1**

F1（vSwitch + 双 NIC HA + VM）字面命中（Azure VM 支持双 NIC）；F2-F5 Hyper-V vSwitch + AccelNet + Catapult FPGA / Azure Boost SmartNIC 闭源；NSDI 2018 "Azure Accelerated Networking" 论文公开部分架构但未涉及跨卡 LACP HW offload 同步。**第 3 档（公开资料不足强候选）**。
