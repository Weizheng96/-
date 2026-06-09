# 证据索引 — 13-baidu-browser（_sources.md / 检索留痕）

候选：百度浏览器 / 百度 App 内嵌浏览内核（T7 内核）
专利公开（授权）日基准：2023-08-30

## Phase 1 — react 粗筛 WebSearch（串行）
1. `百度浏览器 内核 渲染 加载 优化 原理`
   - 命中：T7 内核（百度手机浏览器自研，基于 Blink 深度定制）；首屏优先加载/视觉焦点识别；ResourceScheduler；六重加速。
   - 关键 URL：
     - https://baike.baidu.com/item/T7%E5%86%85%E6%A0%B8/19857712 （T7内核 百度百科）
     - https://zh.wikipedia.org/zh-hans/百度浏览器
2. `百度 T7内核 首屏 优先加载 渲染管线 资源调度 算法`
   - 命中关键 URL（最相关机制源）：
     - https://xie.infoq.cn/article/ea042747d8863f882d249aa41 （百度APP浏览内核资源加载优化实践 -- ResourceScheduler 调优机制，InfoQ）
     - https://juejin.cn/post/7052633261402488868 （同文掘金镜像）
3. `百度浏览器 停更 下线 百度App 内嵌浏览 内核 现状`
   - 命中：PC 百度浏览器 2019-09-30 正式停止网页浏览基础功能（已下线，且早于时间窗）；
     T7 内核（移动端）截至 2023 已迭代至第四代架构，仍在用（百度手机浏览器 / 百度 App 内嵌浏览）。
   - 关键 URL：
     - https://www.williamlong.info/archives/5843.html （百度浏览器正式停止服务）

## Phase 2 — react 深抓 WebFetch / curl（串行）
- WebFetch https://xie.infoq.cn/article/ea042747d8863f882d249aa41 → SPA 空壳，正文未取到。
- WebFetch https://juejin.cn/post/7052633261402488868 → 成功取到 ResourceScheduler 机制正文（用于 F2/F3/F4/F7 判定）。
- WebFetch https://baike.baidu.com/item/T7%E5%86%85%E6%A0%B8/19857712 → 403。
- curl -A 兜底取得 baike T7 页 HTML（本地 t7-baike.html），脚本抽取关键段（_t7_extract.txt）。

## 证据索引表
| # | 时间 | 类型 | URL / 本地路径 | 命中要点 |
| --- | --- | --- | --- | --- |
| 1 | 2015→2023(第4代) | 百科 | https://baike.baidu.com/item/T7%E5%86%85%E6%A0%B8/19857712 | T7内核基于Blink深度定制；网页渲染优化=首屏关键路径拆解+渲染引擎布局算法优化；仍在用 |
| 2 | 技术博客 | 机制源 | https://juejin.cn/post/7052633261402488868 | ResourceScheduler：按资源类型给初始加载优先级(High/Medium/Low)+按场景调整+importance属性(high/low/auto)；作用于IMG/CSS/JS/link 4类资源；为网络请求调度，非DOM子树、无固定延迟 |
| 3 | 2019-09-30 | 公告 | https://www.williamlong.info/archives/5843.html | PC 百度浏览器停止网页浏览基础功能（已下线，早于时间窗；与移动端T7区分） |

## 工具受限说明
- InfoQ 原文为 SPA，WebFetch 仅得空壳；以掘金同文镜像取正文，机制描述一致。
- 百度百科 WebFetch 403；改用 curl -A 兜底取得 HTML 后本地抽取。
- 候选闭源（公开度低），F4/F5/F7 的内核内部实现以公开技术博客 / 百科为最高可得证据级别。
