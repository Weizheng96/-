---
name: patent-infringement-check
description: Detect whether a given patent is being used (infringed) by other organizations. Use this skill whenever the user provides a patent ID or path, or asks to check / 排查 / 检测 / 调查 a patent for unauthorized use, infringement (侵权 / 违约), or third-party usage. Triggers on phrases like "检测这个专利有没有被其他公司使用", "排查 X 的侵权情况", "看看谁在用这个专利". Produces a 7-step chain of analysis reports next to the input patent file (潜在应用场景及侵权特征 → 潜在使用组织 → 潜在侵权产品初选 → 潜在侵权产品-全 → 候选/*/_verdict.md → 违约列表). Step 1 / init / Step 7 are Python scripts (no LLM); Steps 2-5 run as Claude's main agent; Step 6 spawns one general-purpose sub-agent per candidate in react mode for evidence collection + verdict.
---

# Patent Infringement Check — 7-step pipeline

每一步要么落一份 markdown 报告到 `专利集/<PATENT_ID>/`，要么填充 `候选/<slug>/` 子目录。**所有 LLM 推理由 Claude 完成**——主 agent 负责 Steps 2-5，sub-agent 负责 Step 6 每候选独立的取证+判定。Python 脚本仅做 HTTP 抓取、文件切片、模板汇总三类无 LLM 工作。

**职责分工**：

| 工种 | 哪些步骤 |
|---|---|
| Python 脚本（无 LLM） | Step 1 (`fetch_patent.py`) · Step 2 切片 (`slice_patent.py`) · Step 6 候选目录初始化 (`init_candidates.py`) · Step 7 (`compile_step7.py`) · 全角引号文件写入 (`write_report.py`) |
| Claude 主 agent | Steps 2-5 推理 + Step 6 sub-agent 编排 + 全程复核 |
| Claude sub-agent（general-purpose, react 模式） | Step 6 每候选独立的 WebSearch + WebFetch 迭代 + 直接写 `_verdict.md` |

**依赖**：

```bash
pip install requests beautifulsoup4 lxml pdfplumber pypdf
```

---

## 0. 输入与落盘约定

- **输入**：patent ID（`<PATENT_ID>`，如 `XX1234567A` 形式的公开号）或路径 `专利集/<PATENT_ID>.pdf`
- **工作目录**：`专利集/<PATENT_ID>/`——若 PDF 在 `专利集/` 根，先建子目录并把 PDF 移进去
- **文件名规约**（全角引号 = U+201C `"` + U+201D `"`，**不是** ASCII `"`）：

```
专利集/<PATENT_ID>/
├── <PATENT_ID>.pdf                              ← 输入（可选）
├── <PATENT_ID>.md                                ← Step 1
├── <PATENT_ID>"潜在应用场景及侵权特征".md       ← Step 2
├── <PATENT_ID>"潜在使用组织".md                  ← Step 3
├── <PATENT_ID>"潜在侵权产品初选".md              ← Step 4
├── <PATENT_ID>"潜在侵权产品-全".md               ← Step 5
├── <PATENT_ID>"违约列表".md                      ← Step 7
└── 候选/NN-<slug>/
    ├── _meta.json                                ← init 脚本写
    ├── _sources.md                               ← sub-agent 写（query 留痕）
    ├── _pruned.txt (可选)                        ← sub-agent 粗筛 0 信号时写
    ├── _verdict.md                               ← sub-agent 直接写（含"第 N 档"标签）
    └── <下载的证据 PDF / HTML>
```

**Windows 全角引号写法**：Claude 的 `Write` 工具直接写全角引号路径会 `ENOENT`。所有 Step 2-5 输出按下述流程：
1. Claude 用 `Write` 写到 ASCII 临时名 `_scratch_stepN.md`
2. Claude 调 `python <scripts>/write_report.py <PATENT_ID> <stage_name> _scratch_stepN.md` 完成 rename + 删源

---

## Step 1 — 取专利原文 → `<PATENT_ID>.md`

```bash
python .claude/skills/patent-infringement-check/scripts/fetch_patent.py <PATENT_ID>
```

抓 `https://patents.google.com/patent/<PATENT_ID>/zh`（CN 用 `/zh`，其他用 `/en`），BeautifulSoup 直抽所有权利要求 verbatim + 说明书全文 + 基本信息（含**公开/授权日**——Step 6 时间窗判定的关键字段）。

**退出码**：`0` 成功；`2` 失败 → Claude 回退 `WebFetch`（prompt 须强调 `Output ALL claims verbatim, do not summarize`）或 `pdf` skill 本地解析 PDF。结果都落到 `<PATENT_ID>.md`。

---

## Step 2 — 应用场景 + 独权 + 侵权特征 → `<PATENT_ID>"潜在应用场景及侵权特征".md`

**避免读全文**：先用 slice 脚本把 `<PATENT_ID>.md` 削成仅含基本信息 + 摘要 + 背景技术 + 所有独立权的精简版（典型 1.5-4k 字符，原文常超过 30k）：

```bash
python .claude/skills/patent-infringement-check/scripts/slice_patent.py <PATENT_ID> --out /tmp/<PATENT_ID>_slice.md
```

Claude `Read` 这个切片（**不要再 Read 原 `<PATENT_ID>.md`**——浪费 token），按下方模板写到 `_scratch_step2.md`，再 `write_report.py` 重命名为带全角引号的最终文件。

**模板**：

````markdown
# <PATENT_ID> 潜在应用场景及侵权特征

## 基本信息
- 专利号：
- 标题：
- 当前权利人：
- 申请日 / 公开（授权）日：           ← 后续 Step 6 时间窗用此字段

## 一、潜在应用场景（严格来自背景技术 — 不外扩）

### 场景 1：<场景简名>
- **背景技术 verbatim 依据**：> "<原文引文>"
- **场景说明**：1-2 句话，谁在用、用来干什么
- **使用本专利的典型形式**：（如 SDK / 内嵌算法 / 工艺步骤 / 配方组分 等——仅基于背景技术明示，**不外扩**）

### 场景 2 / 场景 3 ...
（按背景技术实际描述的场景数列；若只描述 1 个就只写 1 个——**宁少勿编**。）

## 二、独立权利要求 + 侵权特征 F1-Fk

### 权 1 verbatim
> <整段引自切片中权 1 的原文>

### F1-Fk 清单
- **F1（<特征简名>）**：<verbatim 引自权 1 的对应句>
- **F2（...）**：<...>
- ...

**拆分规则**：权 1 字面中"包括 / 其特征在于 / 所述 ... 包括"后面的每个并列限定 / 动作步骤 / 关键参数拆成一个 F#。禁止合并多步、禁止意译。

### 其他独立权（仅当存在多条独立权时填）
- 权 N（<形式：方法/装置/介质/.../混合>）：<verbatim 简述与权 1 的差异部分>

### 关键限定词与隐含约束
- <整数限定（如 N ≥ 2）/ 多层结构 / 时间窗 / 默认 vs 可选 / 配方比例 / 工艺次序 等——每条一行>
````

**Step 2 自检**：F# 数量是否覆盖权 1 所有并列动作？整数限定 / 多层结构 / 时间窗有没有漏？

---

## Step 3 — 潜在使用组织 → `<PATENT_ID>"潜在使用组织".md`

**Claude 主 agent 直接做**。基于 Step 2 的场景列表，按场景分组列出**真实存在**的组织。**只收录两类组织，其余一律不列**：

- (i) **知名组织**——在本领域有公认知名度的头部 / 主流主体（公众或行业内广泛知晓的大型企业、上市公司、头部机构）
- (ii) **独角兽公司**——私募估值 ≥10 亿美元、尚未上市的高成长创业公司

**排除**：默默无闻的中小企业、纯政府试点 / 行业协会成员 / 标准化参与方、无公开知名度的实验室或个人项目——这些即便沾边也不列（避免 Step 4/6 把预算耗在无从取证的长尾主体上）。判断"是否知名 / 是否独角兽"以可公开核实的信号为准（主流媒体报道、上市状态、知名榜单 / 融资披露）。

**精简输出**——每个组织只需 1 行，并标注其属于 (i) 还是 (ii)：

```markdown
### 场景 N：<场景名>

- **<组织名>**（类型；i 知名 / ii 独角兽）— 1 句定位（含知名度 / 独角兽依据）— 代表性**已商用**产品/项目：<P1, P2, P3>
- ...
```

候选数量按需要——背景技术只描述 1 个场景的，组织少 4-5 个也合理；多场景的可以 10+。**Step 3 不深挖产品**——Step 4 才展开到具体产品族。

不确定 vendor 真实性 / 是否够"知名或独角兽"时跑 1 条 `WebSearch` 验证；查不到、或核实后既非知名也非独角兽的，不要列。

写到 `_scratch_step3.md` → `write_report.py <PATENT_ID> 潜在使用组织 _scratch_step3.md`。

---

## Step 4 — 潜在侵权产品初选 → `<PATENT_ID>"潜在侵权产品初选".md`

**Claude 主 agent 直接做**。基于 Step 3 的组织 × Step 2 的 F1-Fk，列出**有具体名字**的产品 / SDK / 服务 / 模块 / 工艺。表头**严格**：

| NN | 类型 | 名称 | vendor | 命中场景 | 初判命中 F# | 公开度 | candidate_slug |
| --- | --- | --- | --- | --- | --- | --- | --- |

**类型**取值：`产品` / `技术`（技术类是 Step 5 归并后才会出现，Step 4 默认全填"产品"）。

**要求**：

- **只收录 Step 3 已列组织已经"开始应用"的产品**——即已上市 / 已商用 / 已公开发布并提供给客户或公众使用的产品、服务、SDK。**不考虑技术原型**：研究 demo、概念验证（PoC）、实验室样机、内部测试版、论文里的方法实现、未发布的预研项目一律**不列**（这些无从在 Step 6 取到可公开核实的应用证据）。判断"是否已开始应用"以可公开核实的信号为准（产品页 / 发布公告 / 商用案例 / 客户落地新闻 / 应用商店或仓库的正式 release）。
- vendor 必须是 Step 3 收录的某个组织（知名组织或独角兽）；不要在 Step 4 引入 Step 3 之外的新主体
- 产品名是 vendor 公开使用的具体名（**不要泛指**——禁止 "<vendor> 云平台"、"<vendor> 解决方案"类）
- 同一组织允许多个产品族（各自独立成行）
- 若候选与 F1-Fk 概念上不在同一抽象层（如专利讲算法 / 候选是物理硬件 ODM），**不要列**（避免浪费 Step 6 预算）
- **NN 是两位整数前缀，从 01 起**——后续 init 脚本按此创建 `候选/NN-<slug>/`
- 公开度 = vendor 对该产品技术细节的对外公开程度（文档 / 论文 / 开源等），高 / 中 / 低
- `candidate_slug` 形如 `NN-<vendor-product>`（ASCII 小写连字符）

数量按需要。**宁缺毋滥**——若某场景下的知名 / 独角兽组织均无已商用产品（只有原型），该场景可少列或不列，不要为凑数纳入原型。写到 `_scratch_step4.md` → `write_report.py`。

---

## Step 5 — 技术词驱动的长尾扩展 + 归并 → `<PATENT_ID>"潜在侵权产品-全".md`

**Claude 主 agent 直接做（含 WebSearch）**。两阶段。

### 5.1 长尾扩展（技术词驱动）

从 Step 2 的 F1-Fk 抽 **2-3 个核心技术词组合**——必须是技术术语，不是 vendor / 业务定位词。**每条 query 都把召回锚定到 Step 3/4 两道闸**（知名组织 / 独角兽 + 已商用），从源头减少随后会被剔除的无效召回。跑下表 5 条 `WebSearch`，每条至少 1 次（行 2a / 2b 必须**双轨并行**，不能只跑一条）：

| # | query 模板 | 召回意图 |
|---|---|---|
| 1 | `<核心技术词组合> 龙头 OR 头部 OR 上市公司 商用` | 知名头部 / 上市公司（中文披露主导，已落地） |
| 2a | `<核心技术词组合 EN> (NASDAQ OR NYSE) company product` | 海外上市 / 英文披露主导的知名厂商（已发布产品） |
| 2b | `<核心技术词组合 中文> 中概股 OR 美股上市 OR 港股 商用` | 海外上市但中文 PR 主导的知名中概（已落地） |
| 3 | `<核心技术词组合> 独角兽 OR 估值十亿 落地` | 已商用落地的独角兽 |
| 4 | `<核心技术词组合> 正式发布 OR 商用 OR 落地案例 OR GA release` | 已发布 / 已商用的产品或开源实现（**排除** demo / PoC / 预研原型） |

**为什么 2a / 2b 必须双轨并行**：海外上市 ≠ 英文披露。部分知名中概 / 港股厂商的某条业务线对外披露主要走中文 PR 渠道（综合门户 / 行业垂直媒体 / 财经资讯站等），英文资料几乎空白；只跑英文 query 会系统性漏检这一子集。反向亦然——海外原生的知名厂商在中文媒体往往不可见。两条 query 用同一组核心技术词，仅语言 / 关键词不同，召回成本可控。

**纪律**：0 命中也明示"0 命中"；引用 URL 必须 `WebSearch` 实际返回；召回的 vendor 主业完全偏离本专利领域、仅关键词碰撞的——剔除，**不要进入归并**。query 已锚定两道闸，但仍须在归并前做一次终筛兜底，剔除漏网的：(a) 既非知名组织也非独角兽的主体，(b) 仍处技术原型阶段（demo / PoC / 实验室实现 / 未发布预研、无公开商用或发布信号）的候选——这两类不进入候选总表。

**不要写中间 `长尾扩展.md` 文件**——直接在主 agent 上下文中保留 5-15 条非冗余的新候选，下一节合并。

### 5.2 归并 + 去重（直接写 `潜在侵权产品-全.md`）

合并 Step 4 初选 + 5.1 长尾结果，应用 **产品 vs 技术二元归并规则**：

- **一个产品命中多项 F#** → 该**产品**作一个条目（"命中 F#" 列多项）
- **多个产品共用一项技术，且该技术本身就实现了 F1-Fk**（如某 SDK / 协议 / 开源库 / 算法实现 / 配方 / 工艺规范——技术本体即侵权主体，下游产品只是集成） → 该**技术**作一个条目（"应用案例" 列下游产品）
- 若技术只是被集成、下游有独立二次创新 → 保留产品分别成行

**输出文件必须严格按下述结构**（init 脚本依此解析；偏离会导致解析失败但脚本退出码仍为 0——*静默失败*！自检表头列名 + 简介标题层级）：

````markdown
# <PATENT_ID> 潜在侵权产品-全

> 合并 Step 4 初选 + Step 5.1 长尾扩展，并按"产品 / 技术二元归并规则"去重。
> 序号 NN 即为后续 `候选/NN-<slug>/` 子文件夹的前缀。

## 候选总表

| NN | 类型 | 名称 | 组织 | 命中 F#（初判） | 公开度 | candidate_slug |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | 技术 | <技术名> | <宿主组织 / 主 maintainer> | F1, F2, F4 | 高 | `01-tech-<slug>` |
| 02 | 产品 | <产品名> | <vendor> | F1, F3, F5 | 中 | `02-<vendor>-<product>` |
| ... | ... | ... | ... | ... | ... | ... |

## 各候选简介

### 01-tech-<slug>
- 类型：技术
- 名称：
- 组织：
- 命中 F#（初判）：
- 公开度：
- 一句话定位：
- 应用案例（仅"技术"类条目）：<下游产品列表>

### 02-<vendor>-<product>
- 类型：产品
- 名称：
- vendor：
- 命中 F#（初判）：
- 公开度：
- 一句话定位：

### 03-...
````

写到 `_scratch_step5.md` → `write_report.py <PATENT_ID> 潜在侵权产品-全 _scratch_step5.md`。

---

## Step 6 — 逐候选 react 模式取证 + 直接写 verdict

### 6.0 初始化候选文件夹

```bash
python .claude/skills/patent-infringement-check/scripts/init_candidates.py <PATENT_ID>
```

按 Step 5 候选总表为每个候选建 `候选/NN-<slug>/`，写 `_meta.json`（slug / type / name / organization / hit_features_initial / publicity / blurb）+ 占位 `_verdict.md`。幂等；`--force` 覆盖。

### 6.1 Sub-agent react 协议（每候选一个独立 agent）

主 agent **批量并行 spawn** `subagent_type: general-purpose` agent（建议每批 3-5 个；不要一次 spawn 几十个——工具并发会被节流）。

**关键：每批 spawn 完后等待该批全部返回再启动下一批**——否则 Step 6 没完成就跑 Step 7 会读到空 `_verdict.md`。Step 7 不能在 Step 6 全部 sub-agent 返回前启动。

**Sub-agent prompt 装配**：把下面的协议作为模板，替换其中所有 `{PATENT_ID}` 和 `{SLUG}` 为本候选的实际值。**展开方式**——主 agent 用 Python 字符串格式化或手工替换：

例：候选 `03-acme-widget` 在专利 `XX1234567A` 下，sub-agent prompt 模板里 `{PATENT_ID}` → `XX1234567A`、`{SLUG}` → `03-acme-widget`。

**Sub-agent 协议模板**（verbatim 嵌入，仅替换占位符；本协议是 sub-agent 的 user message，不要外加包装）：

```
你是某具体候选的证据收集 + 判定 sub-agent。一次性完成 react 模式搜索 + 证据合议 + 直接产出 _verdict.md。**禁止替专利权人下"已构成侵权"的法律结论**——只给"第 N 档"技术档位。

【上下文 — 必须先读】

1. 读候选元数据：`Read 专利集/{PATENT_ID}/候选/{SLUG}/_meta.json`
2. 读专利的 F# 特征：`Read 专利集/{PATENT_ID}/{PATENT_ID}"潜在应用场景及侵权特征".md`
3. 从该文件抽出"公开（授权）日"——作为时间窗判定基准

【Phase 1 — react 模式粗筛（预算 ≤4 WebSearch）】

**强制 react**：每次只发 **1 条** WebSearch，看完返回结果后再决定下一条。**禁止在一条消息内并行多条 WebSearch**。

起步建议：
  - query 1：`<vendor / 技术名> <产品 / 主仓库名> <Step 2 第一个核心技术词>`
  - query 1 命中无关 → query 2 换 `site:` 限定或换语言
  - query 1 命中相关 → query 2/3 用 `<vendor> <某个 F# 技术词>` 缩到具体特征
  - 累计 4 条仍无信号 → 走"早剪枝"

【早剪枝】

满足任一立即停止：
  (i) 4 条 query 全 0 命中 / 命中 URL 全部与候选无关
  (ii) 所有命中材料发布日期 < 专利公开（授权）日 — 现有技术，不构成侵权证据
  (iii) 命中材料显示候选实际架构层级与 F# 概念上不同（非同一抽象层）

此时**只**做三件事：
  - 写 `专利集/{PATENT_ID}/候选/{SLUG}/_pruned.txt`：一句话剪枝原因
  - 写 `专利集/{PATENT_ID}/候选/{SLUG}/_sources.md`：跑过的 query + 0 命中声明
  - 用下方 PRUNED VERDICT 模板写 `_verdict.md`，返回主 agent

【Phase 2 — react 模式深抓（仅当 Phase 1 未剪枝；预算 ≤6 WebFetch）】

对 Phase 1 中信号最强的 2-4 个 URL，逐个 `WebFetch`。每次 WebFetch 完读完再决定下一个——**禁止一次并行多个 WebFetch**。

抓取重点：
  - F# 中含**整数限定 / 多层结构 / 时间窗 / 配方比例**的，**主动找** vendor 文档中描述的实际拓扑 / 配比——如果 vendor 文档默认描述的是下界以下的形态（例：F# 要求 N ≥ 2，vendor 只描述 N=1），**verbatim 摘录**该单实例描述（这是反向证据信号）
  - **优先找候选 vendor 自己的专利**：若候选 vendor 在本专利公开（授权）日**之后**自己申请了同主题专利，去 Google Patents / 专利检索站抓它的权利要求全文做机制比对。竞品自有专利往往直接、verbatim 地披露其真实实现路径（用了什么手段、跳过/替换了哪一步），是判定"相同 / 等同 / 反向"质量最高的单一证据源——常常一步定档。这是与领域无关的通用取证动作（无论专利属于何种技术领域都适用）。
  - 抓 PDF 用 `curl -ksSL -o 专利集/{PATENT_ID}/候选/{SLUG}/<name>.pdf <url>`
  - 抓长 HTML 同样落盘到候选目录
  - 每条命中证据，记录其**发布日期**用于时间窗判定

**WebFetch 失败兜底**（强制规则）：WebFetch 单次失败（403 / SPA 壳 / 超时 / 反爬）→ **必须**用 curl 带浏览器 UA 再试一次：
`curl -ksSL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -o 专利集/{PATENT_ID}/候选/{SLUG}/<basename> <url>`
curl 仍失败再放弃。抓到的本地 PDF 用 `pdf` skill 读，本地 HTML 用 `Read` 读。一手论文 / 源码 / 标准 RFC / 招股书 这类 L1 级证据，**至少要尝试 curl 兜底一次再放弃**——否则容易停留在 vendor 营销摘要级别的二手信息，导致判定偏保守。

**SPA 官网兜底**（强制规则）：若 WebFetch / curl 抓到的 HTML 体积很小（<2KB）且正文几乎为空、只剩 `<title>`，多半是 JS 渲染的单页应用（SPA）——真正内容由它引用的脚本（常见命名如 `*.Body.js` / `app.*.js` / `*.html.Body.js`，多挂在 CDN 域名下）二次加载。此时**不要**直接判"无内容"：从抓到的 HTML 里提取这些脚本 URL，用同样的 curl UA 把脚本抓下来落盘，再用 `Read` / `Grep` 在脚本里核验关键词。抓不到再放弃，并在 `_sources.md` 注明"SPA 渲染、已尝试脚本兜底"。

【证据真实性 — 严格反向 vs 限定语区分】

| sub-agent 看到的措辞 | 是反向证据还是限定语？ |
|---|---|
| "Y does NOT do X" / "Y 不支持 X" / "Y 仅支持 Z（不支持 X）" / "Y explicitly excludes X" | ✅ **真反向证据** |
| "X is out of scope" / "X is future work" / "X can work with Y" / "X 不在本文范围" | ⚠️ **作用域限定语**（**不是**反向证据） |
| "Y achieves X via different mechanism" | ❌ **不是**反向证据——这是等同命中信号 |

**F# 实现路径分歧的判定规则**（防 sub-agent 过保守）：

- **中间变量省略**：F# 描述为多步流程 `输入 → 中间变量 → 决策`，候选直接做 `输入 → 决策`（跳过中间变量但用了同样的输入、达成同样的决策效果）→ **等同命中**，不是不命中。示例（跨领域类比，仅说明 schema）：(a) 药物专利写"配料 → 中间合成物 → 终产物"，仿制药用"一锅法"跳过中间合成物但终产物一致 → 等同命中；(b) 机械专利写"工件 → 装夹定位 → 加工"，竞品用自适应夹具跳过显式定位步骤但加工结果一致 → 等同命中；(c) UI 交互专利写"输入事件 → 状态机 → 视图"，reactive 框架直接绑定"输入事件 → 视图"跳过显式状态机但终态一致 → 等同命中。
- **开放枚举推定**：F# 用"包括"/"如"/"例如"列出方法清单，候选用清单外但效果等价的方法 → **等同命中**（"包括"通常是开放枚举；封闭枚举须 F# 明示如"仅限"/"only"/"exactly"，否则不能反向解读）。
- **方向**：只有候选**明示拒绝** F# 要求的输入或效果（如"我们不使用 X / X is explicitly excluded"）才升级为反向证据；实现路径不同 ≠ 反向证据；连续参数替代离散枚举 ≠ 反向证据。

【输出 — 直接写 _verdict.md】

把下面整个模板 verbatim 写入 `专利集/{PATENT_ID}/候选/{SLUG}/_verdict.md`（替换 `<…>` 占位符）。最终判定**必须**含字面字符串 `第 N 档`（N ∈ {1,2,3,4,5}），否则 Step 7 解析失败。

  # {SLUG} verdict

  ## 候选基本信息
  - 名称：<from _meta.json name>
  - 组织：<from _meta.json organization>
  - 类型：<from _meta.json type>
  - 初判命中 F#：<from _meta.json hit_features_initial>
  - 专利公开（授权）日：<from Step 2 输出>

  ## F# 命中表

  | F# | 判定 | 证据 verbatim | URL | 备注 |
  | --- | --- | --- | --- | --- |
  | F1 | 字面命中 / 等同命中 / 公开资料不足 / 反向证据 | "<verbatim 引文>" 或"未找到" | <URL> | 等同时简述同手段/同功能/同效果 |
  | F2 | ... | ... | ... | ... |
  | ... | ... | ... | ... | ... |

  ## 已检查文档清单
  - <文档 1 1-行摘要> — <URL>
  - ...

  ## 最终判定

  **第 N 档：<标签>**

  五档定义：
    - 第 1 档：确认侵权（高）— F1-Fk 全部字面命中
    - 第 2 档：确认侵权（中）— F1-Fk 全部命中，含 ≥1 等同命中
    - 第 3 档：公开资料不足（强候选）— ≥60% F# 命中，剩余公开资料不足且无反向证据
    - 第 4 档：公开资料不足（弱候选）— <60% F# 命中
    - 第 5 档：已排除 — 仅当：(a) ≥1 条 F# 有真反向证据，或 (b) 全部证据 < 专利公开日（现有技术），或 (c) 架构层级不同

  **第 5 档的硬门槛——必须是"针对该候选产品的正向事实"，不是推断也不是缺失**：
    - (a) 真反向证据 = 针对**该候选**的、verbatim 的正向否定或正向不同机制描述（"该产品仅做 X、不做 Y" / 该候选自有文档或自有专利写明用的是另一套手段）。**行业通用机制反推、"同类产品一般都这样"、"公开资料未提及" 一律不算反向证据**——那只是公开资料不足。
    - (c) 架构层级不同 = 有**该候选自身**的架构事实（具体型号 / 规格 / 自有文档原文）证明它与 F# 不在同一抽象层；不能仅凭"它没披露这个特征"或"通用实现一般是另一种形态"推定。
    - 若候选与专利**属于同一抽象层**、只是缺少某个 F# 的正向证据、又拿不到针对它本身的反向事实 → 落 **第 4 档（公开资料不足）**，并填升级路径，**不得**判第 5 档。

  **0 命中 ≠ 已排除**。无正向证据但也无反向证据（含"未提及" / "通用机制反推"）→ "公开资料不足"（第 3 或 4 档），**不是**第 5 档。

  判定依据（1-3 句话，基于上表 F# 命中分布）：
  <理由>

  ## 升级路径（仅当落第 3-4 档时填）
  - <如何补取证：反向工程 / NDA 渠道 / 论文深读 / 招股书披露 / 客户访谈 等>

  ## 总结一句话

  <≤120 字，必须含"落第 N 档"字样>

【PRUNED VERDICT 模板 — 仅 Phase 1 早剪枝时用】

  # {SLUG} verdict

  ## 候选基本信息
  <同上>

  ## 最终判定

  **第 5 档：已排除（粗筛阶段）**

  排除原因（粗筛后立判）：

  > <一句话原因，含 (i)/(ii)/(iii) 字样指明触发条件>

  ## 已跑 query 留痕
  - query 1: `<query>` → 0 命中 / <命中要点>
  - query 2: ...

  ## 总结一句话

  候选 {SLUG} 在 Phase 1 粗筛被剪枝（落第 5 档）：<原因>

【纪律】
- 不要替候选下"已构成侵权"的法律结论
- 不要伪造 URL 或 verbatim 引文（主 agent 会抽样验证，伪造会被发现）
- 不要在 Phase 1 / Phase 2 内并行多个工具调用 — 必须 react 模式串行
- 整数限定外推禁令：F# 含 N ≥ 2 等限定时，若 vendor 文档只描述下界以下形态 → 不能写"理论上可扩展 → 字面命中"，应判"公开资料不足"或视具体引文情况判"反向证据"
- 工具能力受限（付费墙 / 登录墙）时，在 `_sources.md` 明示原因，不要凭印象写
```

### 6.2 主 agent 复核（必做 — 抽样验证 sub-agent 不脑补）

每批 sub-agent 全部返回后，`Read` 抽样 2-3 个 `_verdict.md`：

1. "第 1 / 2 档" verdict 是否真有 F1-Fk 全套 verbatim 引文？必要时 `WebFetch` 一次验证某个引文 URL
2. "第 5 档" verdict 是否真满足 (a)/(b)/(c) 硬条件？（防 "0 命中 → 误标已排除"——sub-agent 经常犯）
3. F# 命中表的整数限定 / 多层结构如有命中，是否真的有多实例 / 多层引文？还是 sub-agent 用单实例引文外推了？

**纠错路径**：
- 发现 sub-agent 明显走偏 → 删 `_verdict.md` + 重 spawn 该候选的 sub-agent（传入额外指令"请注意 XX 之前误判 YY"）
- 仅档位轻微偏移、F# 表正确 → 直接 `Edit` `_verdict.md` 改"第 N 档"字样（**保留** `## 最终判定` 标题 + `第 N 档` anchor——Step 7 解析依赖）

---

## Step 7 — 终筛 → `<PATENT_ID>"违约列表".md`

```bash
python .claude/skills/patent-infringement-check/scripts/compile_step7.py <PATENT_ID>
```

无 LLM 调用——读所有 `_verdict.md` + `_meta.json`，按"最终判定"段的"第 N 档"标签排序输出状态总表 + 候选明细 + 统计 + 免责声明。

**排序规则（按技术判定程度从严到松）**：
1. 主键：rank 升序（第 1 档 → 第 5 档 → 待评估 9 末尾）
2. 同档内二级键：初判命中 F# 数量**降序**（命中越多 = 越值得关注，靠前）
3. 同档同 F# 数三级键：NN 升序（稳定回退）

**Step 7 前置条件**：所有 `候选/NN-<slug>/_verdict.md` 必须含"第 N 档"字样（不能停留在 init 时的占位"待评估"）。如有任一候选 verdict 为"第 9 档：待评估"，回 Step 6 补跑该候选后再 compile。

**主 agent 交付**：`Read` 输出确认；最终给用户 3 个数字——
- 第 1+2 档候选数 = 高置信侵权候选
- 第 3 档数 = 建议法务深查
- 第 5 档数 = 已排除

### 法律状态 caveat

如 Step 1 抓到的 `<PATENT_ID>.md` 显示专利法律状态为 **未授权 (Pending)** / **失效 (Expired)** / **无效宣告进行中**，在 `违约列表.md` 末尾追加一段说明（Pending → "确认侵权"档候选只构成"临时保护期主张追溯许可费"依据，不能直接起诉；Expired → 全部已排除；无效进行中 → 列出风险）。**法律状态不影响技术档位排序**——状态机判的是"技术上是否落入保护范围"。

---

## 全局约束

1. **永远不要伪造引用**：每条来源必须是 `WebSearch` / `WebFetch` / `curl` 实际拿到的 URL；拿不到写"未检索到公开来源"
2. **永远不要替用户下"已构成侵权"结论**：本 skill 输出的是**线索与证据链**；结论交给律师 / 法院。`违约列表.md` 末尾自动含免责声明
3. **保留中间产物**：所有报告 + 候选文件夹都落盘，不要中途清理
4. **报告语言**：默认中文，无论专利原文语言（仅 `<PATENT_ID>.md` 保留专利原文）
5. **检索不要自治**：所有 WebSearch / WebFetch 都由 Claude（主 agent 或 sub-agent）显式发起，并由主 agent 抽样复核证据真实性。不依赖任何全自动 RAG 黑盒。
6. **TodoWrite 跟踪 7 步**：每步完成立即 mark done；脚本退出码 ≠ 0 不要默默跳过
7. **0 命中 ≠ 已排除**：状态机硬约束。0 命中只能落"公开资料不足"档，不能升"已排除"——这条规则在 Step 6 sub-agent prompt 内强化了一次

---

## 主动改进建议

执行中如发现规则 / 模板 / sub-agent prompt 不够好——**先把当前任务跑完**，然后在最终回复里明确提出建议（观察到的问题 + 修改方式 + 预计好处）。**等用户确认后再编辑** SKILL.md / scripts/。

---

## 触发示例

- `检测一下 XX1234567A 有没有被其他公司使用` → 触发，按 7 步走（Step 1 直接调 fetch_patent.py）
- `专利集/<PATENT_ID>.pdf 排查侵权` → 触发；Step 1 先 fetch_patent.py，失败回退 WebFetch / 本地 PDF
