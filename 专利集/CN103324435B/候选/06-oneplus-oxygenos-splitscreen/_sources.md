# 证据索引 — 06-oneplus-oxygenos-splitscreen

## Phase 1 react 粗筛 WebSearch（串行）
1. `OxygenOS split screen enter swipe gesture how to OnePlus`
   → 命中 F1 信号：三指上滑进入分屏（Settings > Accessibility & convenience > Split View > "Swipe up with 3 fingers to enter Split view"）。来源 TechWiser / MashTips / OnePlus 官方手册摘要。
2. `OxygenOS split screen swap two apps switch positions drag divider OnePlus`
   → 命中 F3/F4 信号：OnePlus Open（折叠屏）可"by dragging and dropping the app view to change the order"互换两窗口位置；普通机型另有三点菜单 Switch App（属替换非互换）。来源 Android Central / Pocket-lint。

## Phase 2 react 深抓 WebFetch（串行）
- Pocket-lint《How multitasking works on the OnePlus Open》(发布 2023-11-03，晚于公开日 2017.02.08)
  verbatim："You can even switch app positions by dragging and dropping the app view to change the order."
  → F3（窗口间拖动手势）+ F4（双向互换两窗口位置）核心证据。
- XDA《4 OxygenOS features...OnePlus Open multitasking》(发布 2023-10-25)：讲分屏创建与全屏切换，未述互换手势（无反据，仅未提及）。
- Huawei Central tri-split-screen 文：WebFetch 403 Forbidden（工具受限，未采信）。

## 落盘证据文件
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2023-11-03 | HTML | pocketlint-oneplus-open-multitasking.html（已 grep 确认含 swap verbatim，第 3233 行）/ https://www.pocket-lint.com/how-multitasking-works-on-the-oneplus-open/ | F3+F4：拖放互换两窗口位置 |
| 2 | — | HTML | androidcentral-oneplus-splitscreen.html / https://www.androidcentral.com/how-enable-split-screen-multitasking-oneplus-phone | F1 三指上滑进入分屏 |

## 工具受限说明
- huaweicentral.com WebFetch 返回 403，未作为证据采信。
- 一加官方手册 PDF（service.oneplus.com）通过 WebSearch 摘要交叉印证"三指上滑进入分屏"，已有 TechWiser/MashTips 第二来源印证。
