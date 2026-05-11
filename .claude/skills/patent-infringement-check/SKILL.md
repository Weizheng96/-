---
name: patent-infringement-check
description: Detect whether a given patent is being used (infringed) by other organizations. Use this skill whenever the user provides a patent file path (PDF or markdown, e.g. "专利集/CN12345678A.pdf"), or asks to check / 排查 / 检测 a patent for unauthorized use, infringement (侵权 / 违约), or third-party usage. Triggers on requests like "检测这个专利有没有被其他公司使用", "排查 CN... 的侵权情况", "看看谁在用这个专利". Produces a sequenced set of analysis documents (专利介绍、领域适配、潜在应用场景、潜在使用组织、潜在违约、违约列表 + per-candidate verdict/关键证据) next to the input patent file.
---

# Patent Infringement Check (专利侵权检测)

You are running a six-step analytical pipeline that takes one patent and produces a chain of markdown reports investigating whether other organizations have used that patent without authorization.

**Reference docs**：本 SKILL 是流程总览。每一步的**详细模板、硬规则、跨领域示例**都在对应的 `reference/*.md` 文档中——执行该步骤时按链接读取，不要凭记忆套用模板。

---

## Inputs

用户会提供专利文件路径（PDF 或 MD），如 `专利集/<patent_id>.pdf`。**filename stem 即 patent ID**。

**所有工作都在 per-patent 子文件夹内**：`专利集/<patent_id>/`。子文件夹布局：

```
专利集/<patent_id>/
  ├── <patent_id>.pdf                   ← input
  ├── <patent_id>.md                    ← Step 1 输出
  ├── <patent_id>"专利介绍".md          ← Step 2
  ├── <patent_id>"领域适配".md          ← Step 3a（领域分类 + R-* 标志 + 必跑清单）
  ├── <patent_id>"潜在应用场景".md      ← Step 3b（轻量场景推演）
  ├── <patent_id>"潜在使用组织".md      ← Step 4
  ├── <patent_id>"潜在违约".md          ← Step 5（候选总索引）
  ├── <patent_id>"违约列表".md          ← Step 6（终筛，状态总表）
  ├── 候选/<slug>/                       ← 每候选独立子文件夹（Step 5+6）
  │   ├── _sources.md                    ← 已抓取证据索引
  │   ├── _verdict.md                    ← 状态机三栏判定
  │   ├── 关键证据.md                    ← Step 6 per-candidate 两小节文档
  │   └── <下载的证据文件>
  └── .cache/                            ← 研究过程中下载的辅助 PDF
```

输出文件名严格使用全角引号格式：`<patent_id>"<阶段>".md`，引号是 **U+201C / U+201D**——Windows 路径写入有固定流程，见 [reference/operational_quirks.md](./reference/operational_quirks.md)。

---

## The Six-Step Pipeline

Execute each step in order. After each step, write the output markdown file to disk before continuing — the next step reads it back. Use `TodoWrite` to track the six steps.

### Step 1 — Acquire patent text → `<patent_id>.md`

把输入专利（PDF / MD）转成完整 verbatim 的 markdown。Step 2 依赖完整 claim 文本——**不允许带截断或汇总内容进入 Step 2**。

主要路径：
1. 输入 `.md` → 直接读，跳到 Step 2
2. 输入 `.pdf` → 先试 Google Patents WebFetch（CN 用 `/zh`，其他用 `/en`）
3. WebFetch 返回**汇总输出**（识别信号："权 N 至 M 涉及"、"包括"、"等"等概括用语）→ 必须按 narrow-prompt-per-claim 逐条 verbatim 重抓
4. WebFetch 受阻 / 内容稀薄 → 本地 `pdfplumber` 提取；若 EMPTY_PAGES ≥ 80%（扫描 PDF）→ 切到 OCR 或回到 WebFetch stricter prompt

→ 详细流程 / WebFetch 汇总诊断信号 / narrow-prompt 模板 / PDF 提取脚本 / 扫描 PDF 处置：**[reference/step1_acquire_patent_text.md](./reference/step1_acquire_patent_text.md)**

### Step 2 — Patent introduction → `<patent_id>"专利介绍".md`

把 Step 1 的 markdown 解析成结构化介绍：基本信息 / 一句话概括 / 解决的技术问题 / 核心技术方案 / **独立权利要求总览（含侵权主体映射）** / **必要技术特征清单 F1-Fk** / **每条 F# 的 satisfaction paths（独立权字面 / 从属权 alt / 等同）**。

关键约束：
- **逐条列出**所有独立权（不只权 1）+ 每条对应的侵权主体类型
- 多条独立权共享同一组核心特征时明示"以下 N 条独立权共享 F1-Fk"
- 每条 F# 至少列 3 类 satisfaction path——**避免漏读从属权 alt**

→ 完整模板 + 主体映射表（方法 / 装置 / 整机 / 芯片 / 介质五件套）+ F# satisfaction paths 规则：**[reference/step2_patent_introduction.md](./reference/step2_patent_introduction.md)**

### Step 3 — Domain Adaptation + Application Scenarios + R-STANDARD Subprocess

按 3a → 3b 顺序执行；3c 仅在 R-STANDARD = true 时执行。

- **3a 领域适配** → `<patent_id>"领域适配".md`：把本专利分类到一个具体领域，**现场构造**：(i) 5 大主体类型清单 + 必跑参考清单（**强制 3 视角覆盖**：产业全景 / 金融市场 / 政府名录）；(ii) **本领域研究阵地清单**（≥ 3 个，含主域名——Step 5 §A.2 / §A.5 / §A.15 按此清单逐家跑 query）；(iii) 6 个 R-* 标志（R-OPENSOURCE / R-CONFIG / R-PARTNER / R-PATENTWALL / R-PROCURE / R-STANDARD）
- **3b 应用场景** → `<patent_id>"潜在应用场景".md`：轻量场景推演，每个场景必须列**具名产品列表**（防 niche / 子品牌漏检），且每个 named product 必须在 Step 4 候选清单中以独立产品族条目出现
- **3c R-STANDARD 子流程**：仅当 R-STANDARD = true。判定 SEP / GB / 行业准入三类，影响 Step 4 候选清单处置

→ 完整模板 + 多视角强制要求 + R-* 标志判定标准 + 研究阵地清单推演方法 + 3c 标准合规判定矩阵：**[reference/step3_domain_and_scenarios.md](./reference/step3_domain_and_scenarios.md)**

### Step 4 — Potentially using organizations → `<patent_id>"潜在使用组织".md`

按 Step 3 给出的 5 大主体类型分组展开候选；至少 8 个组织、覆盖至少 3 个场景。

七条硬规则（按优先级顺序应用）：
1. **R-1 按"产品族"而非"公司"展开**：每个组织 ≥ 2 个产品族，独立成行
2. **R-2 拓扑变体细分**（条件激活——独立权字面含 N ≥ 2 / K ≥ 1 / 多层结构等整数限定）：必须按拓扑变体拆成多个候选条目分别 verdict
3. **R-3 R-OPENSOURCE 双层激活**：上游开源项目 + 商业发行版**双层独立 P0**
4. **R-4 主体覆盖检查**：按 5 大主体类型逐条 check，不允许默默跳过
5. **R-5 长尾覆盖检查**（技术词驱动 query，非业务定位 query）+ 用户驱动反向兜底 + 领域过拟合自检
6. **R-6 核心技术候选归并**：多个产品共享同一核心技术 → 归并为"核心技术 + 原创组织"一行；下游使用方作为该候选 verdict 的"应用案例"
7. **R-7 架构层级不符的预排除**：F1 概念上都不构成的候选直接预排除，保留在 Step 6 状态总表"第 5 档：已排除（架构层级不符）"以保证审计可追溯

→ 完整模板 + 七条硬规则的详细判定准则 + 跨领域示例：**[reference/step4_organizations.md](./reference/step4_organizations.md)**

### Step 5 — 全候选证据协议 → `<patent_id>"潜在违约".md` + `候选/<slug>/_verdict.md`

对 **Step 4 列出的所有候选 × 它们各自适用的所有独立权**强制执行。**找到一个高置信侵权候选后不得提前终止**。

协议四段：

- **§A 19 类源穿透**：所有候选必跑前 9 类主流来源；"公开资料不足"档候选必续跑 10-19 类非主流来源；第 20 类反向工程视成本启用。每类源跑过 0 命中也要明示"<类> 检索 0 命中"，不能默默跳过。
  - **检索单元构造（3×2 矩阵）**：每条 query 至少跨 **2 个 identifier 维度**（vendor 本地名 / 国际名 / 邮箱域）× **2 种语言**（vendor 主营市场语言 / 研究阵地主导语言）—— 防止"vendor 中文名 + 中文 topic" 单一组合的系统性漏检
  - **执行纪律 — verifiable 证据强制**：每条 query 必须留 URL 或 0-hit 显式声明；**不允许**写"建议法务深读 / 据悉 / 通常 / 推测"等推测性断言代替实际 query 执行；主 agent §A 收尾必须 grep 自检，命中推测性词汇必须返回去补跑
- **§B 本地化证据归档**：每候选 `候选/<slug>/` 子文件夹 + `_sources.md` 索引 + 每条命中资料本地落盘
- **§C 子 agent 逐文档审阅**（P0 必跑；P1 / P2 可选）：每份证据**独立 spawn** general-purpose agent；禁止合并多份文档到同一 agent；并行 spawn
- **§D 状态机判定 + 三栏 verdict**：投票汇总 F# → 三档状态（确认侵权 / 已排除 / 公开资料不足）→ 5 档细化排名 → 三栏 verdict（状态机原始 ↔ 后置调整 ↔ 最终）+ 7 条后置调整逐条核查

  状态机四条硬约束（机制层 — 防偏倚）：
  1. **等同回避偏倚**（禁止）：等同命中与字面命中同档，不得潜意识降级
  2. **法律不确定性回流**（禁止）：法律解读由律师 / 法院做，写入"建议下一步"字段，不回流降低状态机判定
  3. **反向脑补过宽读**（与硬约束 1 对偶 — 同样禁止）：vendor 文档只覆盖 F# 子集时，未覆盖 F# 不得直接标"字面命中"；**整数限定的拓扑外推禁令** — 不能用 vendor 单实例文档推 N ≥ 2 多实例命中（应回到 Step 4 R-2 拆拓扑变体）
  4. **已排除门槛硬约束**：**0 命中 ≠ 已排除**——必须满足真反向证据 / 时间不合规 / 领域无关 / 架构错位 / 重复 5 条硬条件之一才能判已排除

- **§E 穷尽性证明**：所有"公开资料不足"档候选必须在 verdict 末尾列 19 类源逐类已跑 query

→ 完整 §A 19 类源清单 + 3×2 矩阵 query 构造规则 + 执行纪律 verifiable 证据规则 + 7 条后置调整 + §D 状态机 4 条硬约束 + 三栏 verdict 格式 + §E 穷尽性证明模板：**[reference/step5_evidence_collection.md](./reference/step5_evidence_collection.md)**

### Step 6 — Final infringement list → `<patent_id>"违约列表".md` + `候选/<slug>/关键证据.md`

仔细复核 Step 5 中所有 verdict（来源真实性 / 特征完整性 / 时间合规性）+ 执行专利法律状态后置调整。

输出包含：

- **状态总表**：按 5 档技术判定排序；同档内按子排序键 6.1-6.4（核心技术 → 权属人自营 → 第三方集成 → 仅引用方）。"一行一产品 OR 核心技术"模型；"组织"列允许列多个；**"关键证据"列**指向每候选独立的 `关键证据.md`
- **每个候选独立的 `关键证据.md`**（强制两小节）：
  - **一、基于被侵犯独权的 F# 证据原文 + 网页链接**：对适用独权的每条 F#，给出 verbatim 引文 + 可点击 URL（无字面引文时明示"未找到字面引文"或"公开资料不足"）
  - **二、已检查文档清单**：逐条列出 Step 5 §A 实际跑过的资料——文档名 / 内容摘要 / URL / 简要评价（"字面命中" / "信号命中" / "无相关内容" / "未深抓取" 等）

法律状态后置调整：
- **Active**：标准流程
- **Pending**：所有"确认侵权"候选标"等待授权 — 临时保护期"+ 在状态总表下方加 4 项紧凑模板（临时保护起算日 / 可执行性 / 追溯许可费基础 / 审查风险点）；**不影响排序位置**（排序只看技术判定）
- **Expired / 无效宣告**：相应降级

→ 状态总表完整模板 + 7 个列定义 + 排序规则 + per-candidate `关键证据.md` 两小节模板 + Pending 紧凑模板 + 标准合规候选清单 + 检索盲区声明：**[reference/step6_final_list.md](./reference/step6_final_list.md)**

---

## 全局约束

### ★ 隔离与一致性硬约束

SKILL 是机制层文档，规则的正确性由其内在逻辑独立成立。**禁止**在 SKILL 中写入任何能让主 agent 跳 1-2 步推理到具体评测答案的信息——包括但不限于：

- 任何评测专利号、领域分类、主分类号、关键术语
- 评测答案候选名、其代表性产品 / 论文 / 上游项目 / 配置参数 / 关键 commit / 代表性 vendor 名
- "实测案例 / 实测教训 / 曾发生 / 本规则源自……失误"等案例叙事
- 用占位符暗示评测集分布的语言（如"某 X 类专利"反向暗示评测集中存在该领域专利）
- 任何"避开 / 不要用"列表（写 avoid list 等于反向告诉读者哪些是评测集）

从过去案例中提炼出的抽象原则**直接写进流程本身**（而非作为案例括注挂在规则旁边）。**每次修改 SKILL 后必须 grep 自查**，命中先清理再提交。

### 其他全局约束

- **永远不要伪造引用**：每条来源必须是 `WebSearch` / `WebFetch` 实际拿到的链接；拿不到就如实写"未检索到公开来源"
- **永远不要替用户下结论说"已构成侵权"**：专利侵权判定是法律结论，本 skill 输出的是**线索与证据链**，最终结论应交由专业律师。文末必须包含免责声明
- **保留中间产物**：Step 1-6 的报告都要落盘到 `专利集/<patent_id>/`；研究过程中下载的辅助 PDF 落到 `专利集/<patent_id>/.cache/`
- **TodoWrite 跟踪六步**：每完成一步立即 mark completed
- **报告语言**：默认中文输出，无论专利原文语言（CN / US / EP / JP / KR / WO 任一）。文件名也统一中文。仅 Step 1 抓取的专利原文 verbatim 文本 (`<id>.md`) 保留专利原文语言
- **改进建议主动提出 + 等用户确认再编辑 SKILL**：执行过程中发现 SKILL 有改进空间，先跑完当前任务，然后在最终回复里明确提出建议（问题 / 修改方案 / 预计好处），等用户确认后再实际编辑

→ Windows 全角引号文件名固定写入流程 / 中文路径 PowerShell 选择 / 403 fallback：**[reference/operational_quirks.md](./reference/operational_quirks.md)**

---

## 触发示例

- 用户：`检测一下 专利集/<patent_id>.pdf 有没有被其他公司使用` → 触发，按六步走
- 用户：`帮我看看 <patent_id> 这个专利的侵权情况` → 触发；如目录里已有 PDF 则按上面流程，否则先问用户文件位置
