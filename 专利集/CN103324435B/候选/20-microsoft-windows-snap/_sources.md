# 证据索引 — 20-microsoft-windows-snap

## Phase 1 react 粗筛 WebSearch query 留痕
1. `Windows 11 Snap split screen how to trigger mouse keyboard touch gesture`
   - 命中：Snap 触发=鼠标拖拽到屏幕边/角、键盘 Win+方向键、Win+Z 调出 Snap Layouts 浮层。触摸"支持"但官方描述为拖拽，非"滑动手势把单屏一分为二"。
2. `Windows 11 Snap swap two snapped windows positions swap apps left right`
   - 命中（关键反向事实）：Windows 11 **没有内置一键 swap 两个已贴靠窗口**的功能；只能各自拖拽 / 分别用 Win+方向键逐个挪位。无"窗口间滑动手势触发双向内容互换"。
3. `Surface Duo dual screen drag app between screens swap apps touch gesture span`
   - 命中：Surface Duo（触摸设备）上滑 app 拖到中缝可跨屏 span；可在 app 间拖拽文本/图片。
4. `Surface Duo move app from left screen to right screen swap positions drag handle`
   - 命中：上滑某 app 不松手、横移到另一屏、目标屏高亮后松手→把该 app **移到另一屏**（单向移动一个 app，非"两个已分屏窗口内容双向互换"）。

## Phase 2 react 深抓
- WebFetch `nngroup.com/articles/surface-duo/` 成功：Surface Duo 的"分屏"来自**两块物理屏幕（硬件）**，apps 各占一屏，非软件滑动把单屏一分为二；spine 物理中缝。文中未提两 app 位置可互换。
- WebFetch `support.microsoft.com/.../different-ways-to-use-surface-duo` 失败：unknown certificate verification error；curl 兜底亦失败（schannel: SSL/TLS handshake failed，环境 TLS 协商问题）。→ 采信 query 1 与 query 3/4 中 Microsoft 官方支持页正文摘要交叉印证，符合 SKILL "大厂帮助中心受限时可采信 WebSearch 官方页正文摘要" 兜底规则。

## 工具受限说明
- support.microsoft.com 在本环境 WebFetch（证书校验失败）与 curl（schannel TLS 握手失败）均无法直抓；判定依据其官方页面在 WebSearch 返回的正文摘要，并与 nngroup 第三方分析交叉印证。

| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 现行 | 官方支持 | https://support.microsoft.com/en-us/windows/snap-your-windows-885a9b1e-a983-a3b1-16cd-c531795e6241 | Win Snap 触发=拖拽/键盘/Win+Z；无窗口间滑动互换 |
| 2 | 现行 | 官方支持 | https://support.microsoft.com/en-us/surface/different-ways-to-use-surface-duo-2d8854da-a49f-ecaf-a99d-9f571a696d6e | Duo 上滑+横移把一个 app 移到另一屏（单向） |
| 3 | 现行 | 第三方分析 | https://www.nngroup.com/articles/surface-duo/ | Duo 分屏=两块物理屏（硬件），非软件滑动一分为二 |
