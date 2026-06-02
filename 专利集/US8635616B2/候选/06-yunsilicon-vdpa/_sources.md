# 06-yunsilicon-vdpa — 检索留痕 _sources.md

## Phase 1 — react 粗筛 query 留痕
1. WebSearch: `云豹智能 Yunsilicon DPU virtio vDPA 轻量虚拟化 卸载`
   → 命中：云豹支持标准 virtio-net/virtio-blk，virtio 后端在 DPU 上做硬化，可基于 vDPA 实现热迁移；vDPA = 数据面在硬件、控制面在软件分离（RedHat 提出）。有信号。
2. WebSearch: `云豹智能 DPU virtio 后端 硬化 vDPA 热迁移 数据面 控制面 架构`
   → 命中：云豹采用用户态 vDPA 框架，在 DPU 上实现 virtio 后端；数据面硬件加速 + 控制面软件管理分离；同站点资源池需统一 virtio feature 以实现热迁移。
3. WebSearch: `云豹智能 专利 virtio DPU 数据面 卸载 SR-IOV VF 虚拟机 patent Yunsilicon`
   → 未检索到云豹自有专利公开文本；命中产业文「DPU 与 CPU 互联接口之争：Virtio 还是 SR-IOV」——确认 Virtio(vDPA) 与 SR-IOV 直通是两条并列路线。

## Phase 2 — react 深抓（WebFetch / curl 落盘）
- WebFetch https://blog.csdn.net/weixin_60347558/article/details/124996167 （龙蜥 virtio+DPU 实践 Q&A）— 只给高层概念，无数据面实现细节。
- WebFetch https://www.cnblogs.com/kevin-jun-2022/p/16890840.html （vDPA = virtio 半硬件虚拟化）— 关键架构源；已 curl 落盘 `cnblogs-vdpa-16890840.html`。
- WebFetch https://community.aijishu.com/a/1060000000228117 （Virtio vs SR-IOV 接口之争）— 已 curl 落盘 `aijishu-virtio-vs-sriov-228117.html`。
- WebFetch https://xie.infoq.cn/article/b420dbaeb67a60d3beaa133b8 （龙蜥 virtio 趋势+云豹解读）— 正文为空，无可用文本。

## 落盘文件
- cnblogs-vdpa-16890840.html — vDPA 架构原理（数据面硬件直通、控制面软件、无 SR-IOV VF 中转后端）
- aijishu-virtio-vs-sriov-228117.html — Virtio(vDPA) 与 SR-IOV 两路线区别 + 性能对比

## 受限说明
- 未检索到云豹智能自有专利公开文本，无法逐字比对其 virtio 后端是否采用本专利"BE 绑定空闲 VF 软件实例"结构。
- 云豹官方仅披露到"vDPA / virtio 后端硬化 / 热迁移"层级，未公开数据面 DMA 地址下发的内部实现细节（属"公开资料不足"）。
- 龙蜥 InfoQ 镜像正文抓取为空。
