# 18-cloudmosa-puffin verdict

## 候选基本信息
- 名称：Puffin Browser（云端渲染 / Cloud Rendering）
- 组织：CloudMosa, Inc.
- 类型：产品
- 初判命中 F#（from _meta.json）：F1, F2, F5, F6
- 专利公开（授权）日：2023-08-30（时间窗基准）
- 一句话定位：远程浏览器——网页渲染（含 DOM 解析）在云端服务器完成（约 95% 工作量），端侧仅做"显示光栅化 / 绘制渲染结果"（约 5%）。核心技术名 Network Vector Rendering (NVR)，端侧重建的是服务器下发的矢量绘制指令流（vector graphic drawing commands），而非端侧解析 DOM 后按元素优先级错峰显示。

## F# 命中表

| F# | 判定（三态） | 证据 verbatim | URL | 备注 |
|---|---|---|---|---|
| F1（接收含多元素的标记语言文档） | 未在端侧命中 / 架构层级不同 | "Those heavy works before painting are done in the data center level, and then server will send the rendering result to client, so client just need to draw the page."；"the server handles DOM parsing and other processing tasks" | tigercosmos.xyz/post/2018/09/puffin/ ; medium.com/coding-neutrino-blog/how-the-puffin-browser-works | 标记文档的接收/解析发生在云端服务器，非权 1 所限定的 "mobile device" 端侧。端侧拿到的是已渲染结果，不接收/解析 markup document。 |
| F2（基于规则集给元素分配优先级值） | 未命中（端侧无 DOM 元素，无从赋元素级优先级） | "Display Rasterization on the client side ... accounting for only 5% of the total workload, while HTML rendering requires massive computing resources, accounting for 95%"；"client just need to draw the page" | cloudmosa.com/overview ; tigercosmos.xyz | 端侧不持有 DOM 元素集合，仅绘制服务器下发的矢量指令/图像，无"对多元素按规则赋优先级"动作。公开资料未见 Puffin 端侧做元素级优先级赋值。 |
| F3（≥2 规则 / ≥2 优先级值 / ≥2 元素子集） | 未命中 | 同 F2（端侧无元素子集） | cloudmosa.com/overview | 端侧无元素子集结构，F3 整数/结构限定无从满足。 |
| F4（元素子集含父元素及其嵌套元素 — DOM 父子结构定优先级） | 未命中 | "The Remote Browser Graphics Language uses hierarchical layers and vector-based drawing commands ... generic web contents defined by content layers with the vector-based drawing commands"（端侧组织单位是 content layers/矢量绘制指令，非 DOM 父子嵌套子集） | windowsforum.com/threads/...393588/（Phase1 检索摘要）；cloudmosa.com/overview | 端侧的层级是"绘制层(layers)+矢量指令"，与权 1 所要求的"DOM 父元素+其嵌套子元素子集"非同一对象。 |
| F5（基于优先级值确定元素显示顺序） | 未命中 / 架构层级不同 | "client just need to draw the page"；"Once rendering has done, Mango will send rendered data to Puffin" | tigercosmos.xyz | 显示顺序由服务器渲染结果决定并下发，端侧不基于"元素优先级值"在本地排序元素。 |
| F6（按该顺序显示各元素对应渲染内容） | 未命中 / 架构层级不同 | "client just need to draw the page"（端侧绘制的是整页渲染结果，非逐元素按本地确定顺序上屏） | tigercosmos.xyz ; medium.com/coding-neutrino-blog | 端侧绘制对象是云端渲染结果（图像/矢量流），非权 1 的"按元素顺序逐元素显示对应渲染内容"。 |
| F7（相邻元素显示间预定延迟时间 — 关键区分特征） | 未命中（无证据 + 与架构不兼容） | 三个来源均无端侧"元素间预定延迟错峰显示"描述："The document does not explicitly address element prioritization, element ordering, or delayed element-by-element display on the client side." | tigercosmos.xyz ; medium.com/coding-neutrino-blog | 端侧不做元素级显示调度，更无"上一元素显示后延迟固定时长再显示下一元素"机制。无任何正向证据。 |

## 已检查文档清单
- https://www.cloudmosa.com/overview （CloudMosa 官方架构总览，verbatim：95%/5% 工作量分割、NVR、HTML Rendering on server / Display Rasterization on client）
- https://medium.com/coding-neutrino-blog/how-the-puffin-browser-works-440c91cece8f （独立技术拆解，verbatim：heavy works before painting in data center, client just draws）
- https://tigercosmos.xyz/post/2018/09/puffin/ （同文独立镜像，verbatim：server send rendering result, client just draw the page；明确无元素优先级/排序/延迟显示）
- Phase 1 检索摘要：windowsforum 远程浏览器线程（NVR/矢量绘制指令、Blink/Chromium 在服务器侧）

## 最终判定 **第 5 档：已排除（架构层级不同 (c)）**

判定依据：
1. 权 1 限定 "a computer-implemented method for web browsing on a **mobile device**"，其核心三步（对端侧标记文档的多元素按规则赋优先级 → 按优先级确定元素显示顺序 → 相邻元素间以预定延迟错峰显示）均发生在**端侧设备**。
2. Puffin 是远程浏览器：针对该候选自身的 verbatim 架构事实表明，**HTML 渲染与 DOM 解析在云端服务器完成（约 95% 工作量），端侧仅做"显示光栅化 / 绘制服务器下发的渲染结果（矢量绘制指令流，NVR）"（约 5%）**。端侧不持有 DOM 元素集合、不在本地对元素赋优先级、不在本地按元素优先级排序并错峰延迟显示。
3. 故 F1-F7 所要求的端侧元素级机制在 Puffin 端侧整体缺位且与其架构不兼容——属"架构层级不同"的正向反据（第 5 档 (c)），并非仅"0 命中"。

（注：本判定为技术档位，不构成"已/未构成侵权"的法律结论。）

## 升级路径
不适用（第 5 档）。
- 反向监控点：若 CloudMosa 未来推出"端侧 DOM 重建 + 本地按元素优先级错峰显示"的变体（如 RemoteMojo 系若公开资料证实端侧重建 DOM 并在本地做元素级优先调度 + 预定延迟显示），则需重新核查 F1-F7，可能脱离第 5 档。当前公开资料未见此类端侧元素级延迟显示证据。

## 总结一句话
Puffin 为远程浏览器，网页渲染与 DOM 解析在云端服务器完成、端侧仅绘制服务器下发的矢量渲染结果，权 1 所限定的端侧"元素优先级赋值→按序→相邻元素预定延迟错峰显示"机制在端侧整体缺位且与其架构不兼容，**落第 5 档（已排除，架构层级不同）**。
