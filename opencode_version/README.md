# opencode_version — 专利侵权检测 skill 的 opencode 测试沙盒

用来测试 **opencode（VS Code 插件）** 跑 `patent-infringement-check` skill 的效果。与仓库根的 Claude Code 版本对照。

```
opencode_version/
├── AGENTS.md                 # opencode 工作区规则（= Claude 版的 CLAUDE.md，opencode 自动加载）
├── opencode.json             # opencode 配置：模型、权限、general subagent
├── .opencode/
│   └── skills/
│       └── patent-infringement-check/
│           ├── SKILL.md       # 7 步流水线（已按 opencode 工具名/subagent 调用适配）
│           └── scripts/*.py    # 5 个无-LLM Python 脚本
└── 专利集/                    # 待测专利，每个只含输入 PDF，报告由 skill 现场生成
```

---

## 1. 配置

### 1.1 下载安装

- **opencode CLI**（VS Code 扩展只是前端，必须装本机 CLI）：
  ```powershell
  npm install -g opencode-ai
  ```
  装完**重启终端 / VS Code**让 PATH 生效，验证：
  ```powershell
  opencode --version
  ```
- **VS Code 扩展**：在扩展市场搜索 `opencode` 安装。
- **Python 依赖**（skill 的脚本用）：
  ```powershell
  pip install requests beautifulsoup4 lxml pdfplumber pypdf
  ```

### 1.2 登录模型（opencode Zen）

opencode 默认没有任何凭证，必须先登录一个 provider，否则扩展打开后**没有输入框**（无法开会话）。

```powershell
opencode auth login
```

按提示选 **opencode (Zen)** → 跟随浏览器登录 → 完成后验证：

```powershell
opencode auth list   # 应显示 1 credential
```

> 选 Zen 的好处：联网搜索工具 `websearch`（走 Exa AI）**自动启用、免费、无需 API key**；用自带 key 才需要额外设 `OPENCODE_ENABLE_EXA=1`。模型按 token 计费（见 opencode Zen 价目）。

### 1.3 选择模型

登录后，在 opencode 界面里**自己选一个 Zen 模型**（配置文件刻意不写死 `model`，由你按需挑选，选一次会被记住）：

- **VS Code 扩展**：用对话框上方/旁边的模型选择器下拉，选一个 `opencode/...` 模型。
- **TUI/CLI**：输入 `/models` 命令，从列表里选。

推荐 `opencode/claude-sonnet-4-5`（性价比好）；要更强判定可选 `opencode/claude-opus-4-5`，省钱可选 `opencode/claude-haiku-4-5` 或某个 `*-free` 免费模型。

### 1.4 打开当前项目

用 opencode（VS Code 扩展 / CLI）**把 `opencode_version` 这个目录作为项目根打开** —— skill、`opencode.json`、`AGENTS.md` 都按本目录为根发现。

```powershell
opencode --port 18839     # 或直接在 VS Code 里打开本目录并启动扩展
```

---

## 2. 使用

在 opencode 对话框里**直接用自然语言**说要检测哪个专利，skill 会自动触发并按 7 步生成报告到该专利自己的文件夹内。例如：

- `检测一下 CN103324435B 有没有被其他公司使用`
- `专利集/EP3937484B1/EP3937484B1.pdf 排查侵权`
- `排查 US8635616B2 的侵权情况`

触发后无需人工干预，skill 会用 `todowrite` 跟踪 7 步进度：抓取专利原文 → 提炼侵权特征 → 列潜在使用组织 → 产品初选 → 产品全集 → 逐候选取证合议 → 汇总违约列表。Step 6 会为每个候选派一个 `general` subagent 独立检索取证。

> 时间门槛：只有**专利授权日之后**公开的材料才算侵权候选，先行技术不计。skill 不会输出"已构成侵权"的法律定论，只产出线索与证据链，每份最终报告都带免责声明。

---

## 3. 结果文档说明

所有报告生成在 `专利集/<专利号>/` 目录内，按 7 步依次产出：

| 文件 | 步骤 | 内容 |
|---|---|---|
| `<专利号>.md` | 1 | 专利原文（抓自 Google Patents，或本地 PDF 兜底） |
| `<专利号>"潜在应用场景及侵权特征".md` | 2 | 从背景 + 独立权利要求提炼的应用场景，逐条锚定到原文，给出侵权特征 F1–Fk |
| `<专利号>"潜在使用组织".md` | 3 | 每个场景下可能使用该技术的组织清单（1 行 1 个） |
| `<专利号>"潜在侵权产品初选".md` | 4 | 每个组织名下的具体产品名 |
| `<专利号>"潜在侵权产品-全".md` | 5 | 技术词驱动的长尾检索 + 产品↔技术合并后的候选全集 |
| `候选/NN-<slug>/_verdict.md` | 6 | **每个候选一份**：subagent 检索取证后写的合议结果，按"第 N 档"分级 |
| `<专利号>"违约列表".md` | 7 | 最终排名清单，按档位聚合所有 `_verdict.md` |

**`候选/NN-<slug>/` 文件夹内**还有：
- `_sources.md` — subagent 的检索 query 留痕
- `_meta.json` — 候选元数据（由 `init_candidates.py` 写入）
- `_pruned.txt` — 若粗筛无信号、提前剪枝时写入

> 文件名用的是**中文全角引号**（U+201C `"` + U+201D `"`），由 Python 脚本写入，不是 ASCII 引号。

**判定档位**（`_verdict.md` / 违约列表里的"第 N 档"）从高到低代表侵权可能性，第 1 档最高。读结果时优先看违约列表，再回到对应候选的 `_verdict.md` 看证据链与引用 URL。

---

## 已做的 opencode 适配（相对 Claude 版）

- skill 放到 opencode 原生位置 `.opencode/skills/`，脚本路径相应改为 `.opencode/...`。
- SKILL.md 顶部加了"opencode 运行说明"：工具名映射表（`WebSearch`→`websearch` 等）+ subagent 经 `task` 工具调用内置 `general`。
- `opencode.json` 为 `general` subagent 开启 `bash`（opencode 默认对 subagent 禁用 bash，而 Step 6 取证需要 curl / 读本地 PDF / 写候选目录），并设为 `mode: subagent`。
- 工作区规则用 `AGENTS.md`（opencode 原生），不含 Claude 版 `CLAUDE.md` 里关于"标准答案隔离 / 防过拟合"的开发期 meta（那是改 skill 时用的；本沙盒无 `正确答案.md`）。
