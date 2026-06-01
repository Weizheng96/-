# 30-pico-connect 检索留痕

## Phase 1 WebSearch（≤4 起步 + 2 扩展）

| # | Query | 命中数 | 关键链接 |
|---|---|---|---|
| q1 | `Pico Connect VR streaming FEC packet loss adaptive` | 0（仅泛 FEC 学术文献，无 Pico 内部实现） | https://arxiv.org/pdf/2001.07852（DeepRS，与 Pico 无关）|
| q2 | `字节 Pico 串流 抗丢包` | 0（仅产品介绍 / 用户社区 setup 教程，无技术细节） | https://www.picoxr.com/cn/software/pico-link |
| q3 | `site:patents.google.com Pico ByteDance VR streaming` | 0（结果全部为 Magic Leap / 三星 / 高通无关专利） | — |
| q4 | `PICO 串流 FEC 冗余 自适应 业务类型 ByteDance` | 0（仅返回 HelpCenter 入口与 WebRTC 通用 FEC 简书） | https://pico-connect-guide.bytedance.com/docs/help_center/5yu1udgb |
| q5 | `"PICO Connect" OR "PICO 互联" streaming protocol UDP FEC redundancy implementation` | 0（同上，无 Pico 自家技术披露） | — |
| q6 | `Pico VR streaming reverse engineering protocol packet loss` | 0（无 Pico 协议逆向公开资料） | — |

## Phase 2 WebFetch（≤6）

| # | URL | 工具 | 结果 |
|---|---|---|---|
| f1 | https://www.picoxr.com/cn/software/pico-link | WebFetch | 仅产品介绍 + 系统要求，0 技术细节 |
| f2 | https://zhuanlan.zhihu.com/p/1973735004694651695（PICO 企业串流 v2.1 知乎专栏） | WebFetch → 403；curl 兜底 → 仅返回 694B 反爬桩 | 内容获取失败（站点封禁） |
| f3 | https://pico-connect-guide.bytedance.com/docs/help_center/5yu1udgb | WebFetch | 仅标题渲染（"串流游戏 能玩吗"），正文 JS 渲染未抓到 |
| f4 | https://www.ithome.com/0/755/095.htm | WebFetch | 仅营销话术："全新的跨端连接技术架构"、"超低延迟连接"、"画面超分"；**0 FEC / 冗余 / 业务类型自适应**披露 |

## 工具受限说明
- 知乎专栏（最可能含 Pico 企业串流 v2.1 技术 deep-dive）对未登录爬虫 403；curl 兜底亦只拿到反爬桩；当前 sub-agent 无 zhihu 登录态。
- Pico 帮助中心为 SPA，正文 JS 渲染，WebFetch（基于 HTML→Markdown）无法触发动态加载。
- 字节跳动开发者门户（developer-cn.picoxr.com）首页内容超过 10MB 限制，无法整体抓取；按主题深入需具体子页 URL，但搜索引擎未暴露相关子页。

## 结论
Pico Connect 的传输层（编码 / FEC / 冗余 / 调度 / 业务类型识别）公开文档为零；现有公开材料仅营销层（"超低延迟"、"跨端连接技术架构"），无法定位 F1-F5 中任一特征是否实际命中。
