# 15-antgroup-oceanbase verdict

## 候选基本信息
- 名称：OceanBase（partition Paxos 副本 + RootService 均衡 + Zone） / 组织：Ant Group / 类型：产品 / 初判F#：F0,F1,F2,F3 / 专利公开日：2017-12-01

## F# 命中表
| F# | 判定 | 证据 verbatim | URL | 备注 |
| --- | --- | --- | --- | --- |
| F0 | 等同 | "每个分区数据在物理上存储多份，每一份叫做分区的一个副本"；"leader提供读写，follower可非一致性读"；"它可以随时快速切换为 leader 对外提供服务" | https://www.bookstack.cn/read/oceanbase-1.4-zh/1522fe8ff850a576.md | 多节点+每分区多副本，leader=主副本对外服务、follower=备副本容错→对应 F0"每主分区对应至少一个备分区，主副本对外服务"。差异：OceanBase 经 Paxos 选举产生 leader（动态），专利为静态主副本；主备语义对应→记等同，触发全候选封顶第2档 |
| F1 | 等同 | "主均衡策略解决的整体思路为：在某个均衡组中，根据副本的分布情况，实时挑选主，挑选主的结果为：primary_zone 上资源单元上分布的主的数量均衡"；"在同一优先级的 Zone 间将 Leader 打散在不同的机器上" | https://www.bookstack.cn/read/OceanBase-3.1.1-zh/c0c7037ce0b5914c.md | leader（主副本）在 server/资源单元间数量均衡=F1"主分区在各节点均匀分布"。OceanBase 以"主数量均衡"实现，不字面用"差值<阈值"，但目标=任意节点主数量趋同→等同 |
| F2 | 等同 | "副本根据负载和特定的策略，由系统自动调度分散在多个 Server上"；"副本的分布情况称为 Locality，这里的副本分布情况指各 Zone 内包含的副本数量以及副本类型"；（三副本分别分布在不同 Zone 的不同节点上） | https://www.bookstack.cn/read/oceanbase-1.4-zh/1522fe8ff850a576.md | 同一分区的多个副本分散在不同 Zone/不同 Server（不同节点）=F2 反亲和"备副本排除主副本所在节点/分组"（Zone≈分组/可用区）；副本在多 Server 间均衡=F2 均匀。OceanBase 以 Locality+Zone 实现反亲和，非专利字面"第一类/第二类节点"措辞→等同 |
| F3 | 等同 | "分区组内的均衡算法是，首先通过个数均衡使得分区在资源单元间个数分布均匀，然后计算各个资源单元的负载，交换负载最高、负载最低的两个资源单元上的分区"；"随着数据持续写入分区，资源单元的负载会动态变化，会持续触发迁移，使得硬盘持续均衡" | https://www.bookstack.cn/read/OceanBase-2.2.77-zh/d1e167e910d90924.md | RootService 把分区/unit 从负载最高资源单元(高负载节点)迁到负载最低资源单元(低负载节点)=F3"高负载节点备分区移到低负载节点"。OceanBase 以"交换/迁移负载最高最低资源单元上的分区"实现，对应高低负载二次均衡→等同 |

## 已检查文档清单
- 《OceanBase v3.1.1 官方教程》数据均衡（主均衡、RootService 负载均衡因素、分区组均衡算法）— https://www.bookstack.cn/read/OceanBase-3.1.1-zh/c0c7037ce0b5914c.md
- 《OceanBase v1.4 官方教程》数据分区-副本（leader/follower 语义、多副本、Locality/Zone 分布）— https://www.bookstack.cn/read/oceanbase-1.4-zh/1522fe8ff850a576.md
- 《OceanBase v2.2.77 官方教程》数据均衡（高低负载资源单元分区交换、持续迁移）— https://www.bookstack.cn/read/OceanBase-2.2.77-zh/d1e167e910d90924.md
- （取数失败）OceanBase 学习指南 分区副本概述 — http://www.oceanbase.wiki/...（证书错误+Empty reply，F2 已由 v1.4 文档覆盖）

## 最终判定
**第 2 档：全特征命中（含等同），封顶第 2 档**

五档：1=全字面；2=全命中含≥1等同；3=≥60%无反向；4=<60%；5=已排除。
判定依据：F0–F3 四项全部正向命中且无任何反向证据；OceanBase 以 partition 多副本 Paxos 组、leader/follower 主备语义、Locality/Zone 反亲和分布、RootService 把高低负载资源单元上的分区互迁三段式，逐项对应专利 F0–F3。因 leader 为 Paxos 选举式（动态主副本）而专利为静态主副本，且 OceanBase 用"主数量均衡 / 资源单元负载交换"实现而非专利字面"差值<阈值 / 第一类第二类节点"措辞，多项构成等同而非字面，依规则封顶第 2 档。

## 升级路径（第3-4档）：不适用（已落第2档，方向为下调风险而非升档）。下调触发：若取得蚂蚁自有同主题中国专利原文，证明其副本放置/选主算法与本专利在"按主分区为单位、整数阈值<1 的强约束均匀"上存在机制性差异，则部分特征可由等同降为不命中。

## 总结一句话：OceanBase 以 partition 多副本 Paxos 组（leader 主副本/follower 备副本）、Zone 级 Locality 反亲和分布、RootService 把高低负载资源单元上的分区互迁，逐项对应专利 F0–F3 且无反向证据，因 Paxos 选举式主副本等同（非字面）落第2档。
