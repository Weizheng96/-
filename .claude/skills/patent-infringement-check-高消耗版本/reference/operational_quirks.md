# Operational Quirks — Windows 路径、文件命名、抓取 fallback

跨平台 / Windows 特定的 SKILL 操作性细节。在执行 Step 1-6 任何步骤时遇到对应问题，按本文件流程处理。

---

## 全角引号文件名（U+201C / U+201D）

输出文件名严格使用：`<patent_id>"<阶段>".md`——引号是 **U+201C / U+201D**（不是 ASCII `"`，不是中文标点 `「」` 或 `《》`）。

**显示等价但 Unicode 不同**——`"`/`"` 看起来很像 ASCII `"`，必须验证 code point。

---

## 写入全角引号文件名的固定流程（Windows 重要）

`Write` 工具直接传含 `"..."` 的路径会报 `ENOENT`（宿主把它当成 ASCII `"` 处理），必须按下面两步：

1. 先用 `Write` 把内容写到临时文件 `<patent_id>_stepN_temp.md`（同目录，不带引号）
2. 再用 `PowerShell` 通过 `[char]0x201C` / `[char]0x201D` 拼路径并 `[System.IO.File]::Move(...)` 改名：

```powershell
$src = '<dir>\<patent_id>_stepN_temp.md'
$dst = '<dir>\<patent_id>' + [char]0x201C + '<阶段>' + [char]0x201D + '.md'
[System.IO.File]::Move($src, $dst)
```

注：不要用 `Move-Item -LiteralPath '...""...'`，PowerShell 5.1 在解析含 ASCII `"` 的字面量时会先报 `Illegal characters in path`。Linux/macOS 不受此限制，但跨平台建议统一走上面的流程。

---

## 路径含中文 / 全角字符时优先用 PowerShell（Windows 重要）

Git Bash / Cygwin 在 Windows 上对非 ASCII 路径的处理不稳定——`cd` 到含中文 / 全角引号的目录后续命令可能因编码错乱而 ENOENT，`python -c "open(r'<中文路径>')"` 也会因 stdin 编码而失败。

**研究阶段下载证据 / 抓 PDF / 调用本地 Python 脚本时优先用 `PowerShell` + `Invoke-WebRequest -OutFile <绝对路径>` 与 `& <python.exe> <script.py> <绝对路径>`**——PowerShell 原生 UTF-16 字符串能正确处理中文路径。Bash + `curl -o` 在仅含 ASCII 的 `.cache/` 目录里仍可用；但只要绝对路径中有中文，就走 PowerShell。

---

## 403 / anti-bot 站点的 fallback 路径

部分厂商官网 / vendor 社区页面 / 企业产品页对直接 HTTP GET 返回 403 / TLS 错误，但 Anthropic 的 `WebFetch` 工具能通过托管侧渲染拿到内容。

遇到 `curl` / `Invoke-WebRequest` 失败时：

1. 改用 `WebFetch` 抽取关键段落
2. 把抽取结果保存为 `<source-name>-webfetch.md`，文件头加 provenance：
   ```markdown
   > 来源 URL: <url>
   > 抓取时间: <YYYY-MM-DD HH:mm>
   > 抓取方式: WebFetch (Anthropic) — 直接 GET 被 403 拒绝；本文件是 AI 抽取的关键段落，非原始 HTML
   ```
3. 在子 agent 审阅时**显式提示这是二手摘要**，子 agent 应在 verdict 中标注降一级置信。WebFetch 已经过 LLM 抽取压缩，可能丢失原文中关键的 verbatim 措辞 / 配置参数 / 表格数据。
