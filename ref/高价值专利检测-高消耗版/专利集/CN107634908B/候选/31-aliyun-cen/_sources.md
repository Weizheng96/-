# 31-aliyun-cen 检索留痕

## Phase 1 — WebSearch (4 次, react 串行)

### q1 `阿里云 CEN 全球加速 GA FEC 主动冗余`
返回结果均为 GA / CEN 通用产品介绍页, **无任何 FEC / 主动冗余字段命中**. 代表性链接:
- https://help.aliyun.com/zh/ga/product-overview/select-and-purchase-ga-resources
- https://help.aliyun.com/zh/ga/getting-started/get-started
- https://help.aliyun.com/zh/ga/support/faq-about-global-accelerator
- https://help.aliyun.com/zh/ga/

### q2 `Aliyun Alibaba Global Accelerator packet-level redundancy FEC forward error correction`
返回结果以学术 / 第三方 (F5, Springer, IEEE) FEC 通用资料为主, **阿里云官方资料中未出现 packet-level FEC 描述**. 代表性链接:
- https://www.alibabacloud.com/product/ga
- https://www.alibabacloud.com/help/en/ga/product-overview/what-is-global-accelerator/
- https://static-aliyun-doc.oss-cn-hangzhou.aliyuncs.com/download/pdf/153125/User_Guide_intl_en-US.pdf

### q3 `阿里云 GA 全球加速 弱网 丢包 优化 原理`
官方文档**自述机制**: 依托 BGP 带宽 + 全球传输网络 + 就近接入 + 多节点智能调度 + 跨域专线回源; **未出现 "冗余包 / FEC / 前向纠错 / 主动冗余" 任何字面**. 代表性链接:
- https://help.aliyun.com/zh/ga/product-overview/what-is-global-accelerator/
- https://help.aliyun.com/zh/ga/use-cases/optimize-remote-o-m-access-to-bastion-machines-through-global-acceleration-ga
- https://help.aliyun.com/zh/ga/use-cases/configure-global-acceleration-1

### q4 `"全球加速" GA 阿里云 冗余包 FEC 前向纠错`
返回的均为**阿里云开发者社区 / 第三方博客的 FEC 通用原理科普**, 没有任何一条说 "GA 产品内置 FEC". 代表性链接:
- https://developer.aliyun.com/article/243543  (通用 FEC 科普, 与 GA 产品无关)
- https://developer.aliyun.com/article/1238122  (FEC 在 VOIP 的应用, 与 GA 无关)
- https://help.aliyun.com/zh/ga/user-guide/overview-of-standard-ga-instances/

## Phase 2 — WebFetch (2 次, react 串行)

### f1 `https://help.aliyun.com/zh/ga/product-overview/what-is-global-accelerator/`
官方 "什么是全球加速" 页. 提取结论:
- (1) **未提及** FEC / 冗余包 / 主动冗余;
- (2) **未提及** 按数据流特征 (包长 / 到达间隔 / 突发性) 做业务类型识别;
- (3) 自述机制是 "可以根据监听路由类型定义的转发方式将流量分配到后端服务", "优质 BGP 带宽和全球传输网络", "TCP 协议就近终结和 SSL 证书就近卸载".

### f2 `https://www.alibabacloud.com/help/zh/ga/product-overview/what-is-global-accelerator/`
国际版同名页交叉验证:
- TCP 协议就近终结 + SSL 证书就近卸载;
- 四层 TCP/UDP 与七层 HTTP/HTTPS 协议加速;
- 跨地域和多终端节点流量管理;
- **不**提及 packet-level FEC, UDP 包重传 / 复制, 按流特征分类业务类型.

## 工具受限明示
- 未抽样 CEN (云企业网) 专属文档. 但 CEN 定位是企业级 VPC 互联 / SD-WAN 路由产品 (路由 / BGP / 专线), 就产品定位而言比 GA 离 packet-level FEC 更远; 本判定以 GA 官方文档为反向证据中心, 并已对 GA 做 2 份独立官方页交叉验证.
- 阿里云开发者社区 (developer.aliyun.com) 上的 FEC 科普文章并非产品文档, 不构成 "GA / CEN 产品内置 FEC" 的证据.
