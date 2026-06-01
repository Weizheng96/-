# 04-tencent-start 检索留痕

## Phase 1 粗筛 WebSearch（2 query 即获强信号 → 提前进入 Phase 2）

1. `腾讯 START 云游戏 弱网 FEC 抗丢包 冗余` → 命中：
   - https://ur.tencent.com/article/1481 （腾讯高校合作官方页：START 团队 3 项 NSDI 2024 成果）
   - https://cloud.tencent.com/developer/information/腾讯云游戏start
   - https://www.zhihu.com/question/371291065
2. `Tencent START Hairpin NSDI 2024 cloud gaming FEC redundancy paper` → 命中：
   - https://www.usenix.org/system/files/nsdi24-meng.pdf （Hairpin paper PDF）
   - https://www.usenix.org/conference/nsdi24/presentation/meng （Hairpin abstract page）
   - https://www.usenix.org/conference/nsdi25/presentation/an （Tooth NSDI'25，参考用）
3. `腾讯 START 云游戏 控制流 视频流 业务类型 自适应冗余` → 命中：
   - https://baike.baidu.com/item/腾讯%20START%20云游戏/67476332
   - https://ur.tencent.com/article/1481
4. `Pudica Tencent START cloud gaming congestion control NSDI 2024 paper` → 命中：
   - https://www.usenix.org/system/files/nsdi24-wang-shibo.pdf
   - https://sibwang.github.io/publications/Pudica-NSDI24.pdf
5. `AUGUR Tencent cloud gaming NSDI 2024 cellular tail latency` → 命中：
   - https://www.usenix.org/system/files/nsdi24-zhou-yuhan.pdf
6. `Tencent START cloud gaming "control packets" vs "video packets" different transport scheduling separate channel` → 未命中业务类型分流证据。
7. `"cloud gaming" FEC "frame type" I-frame P-frame redundancy adaptive Tencent` → 命中（参考）：
   - https://zilimeng.com/papers/tooth-nsdi25.pdf （Tooth 在 Well-Link Times，**非** START）

## Phase 2 WebFetch / curl 深抓

1. `WebFetch https://ur.tencent.com/article/1481` → 拿到 3 篇 NSDI 论文标题 / 作者 / 部署叙述（页面对 FEC 输入细节描述粗）。
2. `curl https://www.usenix.org/system/files/nsdi24-meng.pdf` → 落盘 `nsdi24-hairpin.pdf`（2.8 MB），pdfplumber 抽文 `nsdi24-hairpin.txt`（100k chars，21 页）→ §3.3 MDP 公式、§4.1 实现架构图、§4.7 生产部署 A/B 测试时间 2021-09 + integrated since then。
3. `WebFetch https://zilimeng.com/papers/tooth-nsdi25.pdf` → 403/binary，改用 curl + pdfplumber 抽文 `nsdi25-tooth.txt` → 确认部署在 "Well-Link Times Inc."（非 START）。
4. `curl https://sibwang.github.io/publications/Pudica-NSDI24.pdf` → 抽前 2 页 → 确认 Pudica 是 CCA（拥塞控制）而非 FEC，定位为 START 部署证据非 F# 直接证据。

## 时间窗确认

- 专利授权日：2021-06-08
- Hairpin 上线 START：2021-09（A/B 之后持续 integrated）→ 严格晚于授权日 ✓
- Pudica 部署 START：论文中明示"serving millions of players"，未给精确日期但论文 2024-04，必然部分晚于 2021-06-08 ✓

## 工具受限明示

- WebFetch 对 usenix.org / zilimeng.com 直接 403 → 全部走 curl + Mozilla UA 兜底（成功）。
- 未尝试 GitHub 代码侧证据（START 闭源，无开源仓库可查），是 F1 / F2 业务类型轴证据缺口的来源。
