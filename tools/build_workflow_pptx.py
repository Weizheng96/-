from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from textwrap import wrap
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape


OUT = Path("Patent_Infringement_Check_Workflow.pptx")

SLIDE_W = 12192000
SLIDE_H = 6858000
EMU = 914400


def e(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def rid(i: int) -> str:
    return f"rId{i}"


def sp(
    sid: int,
    name: str,
    x: int,
    y: int,
    w: int,
    h: int,
    text: str = "",
    fill: str = "FFFFFF",
    line: str = "A6B3C2",
    font: str = "2438",
    color: str = "14213D",
    bold: bool = False,
    shape: str = "roundRect",
    align: str = "ctr",
    valign: str = "mid",
    margin: int = 91440,
) -> str:
    body = tx_body(text, font=font, color=color, bold=bold, align=align, margin=margin)
    return f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="{sid}" name="{e(name)}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
          <a:prstGeom prst="{shape}"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>
          <a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>
        </p:spPr>
        {body.replace('<a:bodyPr', f'<a:bodyPr anchor="{valign}"', 1)}
      </p:sp>"""


def tx_body(
    text: str,
    font: str = "2438",
    color: str = "14213D",
    bold: bool = False,
    align: str = "l",
    margin: int = 91440,
) -> str:
    paras = []
    for raw_para in text.split("\n"):
        if raw_para == "":
            paras.append("<a:p/>")
            continue
        # Manual wrapping keeps text from overflowing in PowerPoint without relying on autosize.
        lines = []
        for line in raw_para.split("|BR|"):
            if len(line) > 44:
                lines.extend(wrap(line, width=44, break_long_words=False, replace_whitespace=False))
            else:
                lines.append(line)
        runs = []
        for idx, line in enumerate(lines):
            br = "<a:br/>" if idx else ""
            runs.append(
                f"""{br}<a:r><a:rPr lang="zh-CN" sz="{font}" {'b="1"' if bold else ''}>
                     <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
                     <a:latin typeface="Microsoft YaHei"/><a:ea typeface="Microsoft YaHei"/>
                   </a:rPr><a:t>{e(line)}</a:t></a:r>"""
            )
        paras.append(f'<a:p><a:pPr algn="{align}"/>' + "".join(runs) + "</a:p>")
    return f"""<p:txBody>
        <a:bodyPr wrap="square" lIns="{margin}" tIns="{margin}" rIns="{margin}" bIns="{margin}"/>
        <a:lstStyle/>
        {''.join(paras)}
      </p:txBody>"""


def title(text: str, subtitle: str | None = None) -> str:
    sub = f"\n{subtitle}" if subtitle else ""
    return sp(2, "Title", 457200, 228600, 11277600, 731520, text + sub, "FFFFFF", "FFFFFF", "3200", "0F172A", True, "rect", "l")


def footer(num: int) -> str:
    return sp(90, "Footer", 10134600, 6507480, 1600200, 228600, f"{num}", "FFFFFF", "FFFFFF", "1200", "64748B", False, "rect", "r")


def slide_xml(num: int, shapes: list[str]) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="F8FAFC"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes)}
      {footer(num)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def empty_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>"""


def slide_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""


def content_types(n: int) -> str:
    slides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slides}
</Types>"""


def presentation_xml(n: int) -> str:
    ids = "\n".join(f'<p:sldId id="{255+i}" r:id="{rid(i)}"/>' for i in range(1, n + 1))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{n+1}"/></p:sldMasterIdLst>
  <p:sldIdLst>{ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle/>
</p:presentation>"""


def presentation_rels(n: int) -> str:
    rels = [
        f'<Relationship Id="{rid(i)}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, n + 1)
    ]
    rels.append(f'<Relationship Id="rId{n+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>')
    rels.append(f'<Relationship Id="rId{n+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"


def master_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
  </p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""


def layout_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Workflow">
  <a:themeElements>
    <a:clrScheme name="Workflow">
      <a:dk1><a:srgbClr val="0F172A"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="334155"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="2563EB"/></a:accent1><a:accent2><a:srgbClr val="0F766E"/></a:accent2>
      <a:accent3><a:srgbClr val="B45309"/></a:accent3><a:accent4><a:srgbClr val="BE123C"/></a:accent4>
      <a:accent5><a:srgbClr val="7C3AED"/></a:accent5><a:accent6><a:srgbClr val="475569"/></a:accent6>
      <a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Microsoft YaHei"><a:majorFont><a:latin typeface="Microsoft YaHei"/><a:ea typeface="Microsoft YaHei"/></a:majorFont><a:minorFont><a:latin typeface="Microsoft YaHei"/><a:ea typeface="Microsoft YaHei"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="Workflow"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/><a:extraClrSchemeLst/>
</a:theme>"""


def package_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""


def doc_props(n: int) -> tuple[str, str]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>专利侵权检测工作流</dc:title><dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""
    app = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex OOXML Generator</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>{n}</Slides>
</Properties>"""
    return core, app


def make_slides() -> list[str]:
    slides: list[str] = []

    slides.append(slide_xml(1, [
        sp(3, "Hero", 457200, 914400, 11277600, 3200400, "专利侵权检测工作流\n从单件专利到可审计证据链", "0F172A", "0F172A", "4000", "FFFFFF", True, "rect", "l"),
        sp(4, "Sub", 914400, 3886200, 9144000, 914400, "目标：快速定位高价值侵权线索，并保留每一步的输入、判断、证据 URL 与盲区声明，供领导汇报和法务复核。", "F8FAFC", "CBD5E1", "2400", "334155", False, "rect", "l"),
        sp(5, "Pill1", 914400, 5143500, 2468880, 548640, "CN107634908B 示例", "DBEAFE", "93C5FD", "1900", "1E3A8A", True),
        sp(6, "Pill2", 3657600, 5143500, 2468880, 548640, "测试集命中 START 云游戏", "CCFBF1", "5EEAD4", "1900", "134E4A", True),
        sp(7, "Pill3", 6400800, 5143500, 2926080, 548640, "权 1 F1-F5 逐项证据", "FEF3C7", "FCD34D", "1900", "78350F", True),
    ]))

    # Flow chart.
    x0, y0, bw, bh, gap = 381000, 1524000, 2057400, 1600200, 228600
    labels = [
        ("1 领域分析", "抽取 IPC/CPC、独权主题、F# 必要特征\n映射产业链主体：RTC、云游戏、直播、开源、OEM\n输出 R-* 风险标志：开源、配置、标准、招标、专利墙"),
        ("2 场景分析", "从 F# 反推高命中场景\n识别正例：低时延、丢包恢复、业务差异化\n识别反例：接收端 NACK、固定 FEC、TCP 重传"),
        ("3 潜在组织", "三视角扩展候选：产业全景、资本市场、标准/协会\n按中国/海外/上游开源分层\n避免只搜熟悉厂商的认知偏差"),
        ("4 对应产品", "组织拆成产品族、SDK、协议栈、OEM 设备\n区分发送端/接收端/中转节点\n绑定适用独权：方法权、设备权"),
        ("5 相关证据", "19 类来源穿透：论文、文档、代码、配置、演讲、招标\n每条 F# 要有 URL 或 0 命中声明\n落盘关键证据、verdict、最终列表"),
    ]
    shapes = [title("主流程图：领域分析 → 场景分析 → 潜在组织 → 对应产品 → 相关证据", "每一阶段都产出可复核 Markdown，而不是只给最终判断")]
    for i, (head, body) in enumerate(labels):
        x = x0 + i * (bw + gap)
        shapes.append(sp(10 + i, head, x, y0, bw, bh, f"{head}\n{body}", ["DBEAFE","CCFBF1","EDE9FE","FEF3C7","FFE4E6"][i], ["60A5FA","2DD4BF","C4B5FD","FBBF24","FB7185"][i], "1650", "0F172A", False, "roundRect", "l"))
        if i < 4:
            shapes.append(sp(30 + i, "Arrow", x + bw - 68580, y0 + 548640, 365760, 365760, "", "64748B", "64748B", shape="rightArrow"))
    shapes.append(sp(50, "AuditBar", 685800, 5486400, 10820400, 571500, "审计线贯穿全流程：输入文件、检索 query、候选扩展理由、F# 命中证据、降级/排除原因、法务待核事项全部留痕", "FFFFFF", "CBD5E1", "1900", "334155", True, "rect", "ctr"))
    slides.append(slide_xml(2, shapes))

    slides.append(slide_xml(3, [
        title("实现思路：把“找侵权”拆成可执行的数据流水线"),
        sp(3, "Patent", 685800, 1371600, 2971800, 1143000, "专利解析\n• PDF/MD 提取权利要求\n• 独权优先，拆 F# 要件\n• 记录法律状态与时间窗", "DBEAFE", "93C5FD", "1800", "1E3A8A", True, "roundRect", "l"),
        sp(4, "Domain", 4419600, 1371600, 2971800, 1143000, "领域适配\n• IPC/CPC → 技术赛道\n• 产业链主体类型\n• R-* 触发器决定检索深度", "CCFBF1", "5EEAD4", "1800", "134E4A", True, "roundRect", "l"),
        sp(5, "Candidate", 8153400, 1371600, 2971800, 1143000, "候选生成\n• 组织 → 产品族 → 版本/SKU\n• 上游开源与商业 fork 分层\n• 发送端主体过滤", "FEF3C7", "FCD34D", "1800", "78350F", True, "roundRect", "l"),
        sp(6, "Evidence", 685800, 3200400, 2971800, 1371600, "证据收集\n• 官方文档、论文、GitHub、配置、演讲、招标\n• verbatim 引文 + URL\n• 0 命中也记录 query", "FFE4E6", "FDA4AF", "1800", "881337", True, "roundRect", "l"),
        sp(7, "Verdict", 4419600, 3200400, 2971800, 1371600, "状态机判定\n• F# 全命中 → 确认侵权\n• 缺要件 → 公开资料不足\n• 主体/反向证据 → 排除\n• 标准/豁免另行标记", "EDE9FE", "C4B5FD", "1800", "4C1D95", True, "roundRect", "l"),
        sp(8, "Outputs", 8153400, 3200400, 2971800, 1371600, "汇报输出\n• 状态总表\n• 单候选关键证据\n• 盲区与升级路径\n• 高 ROI 维权建议", "FFFFFF", "CBD5E1", "1800", "334155", True, "roundRect", "l"),
        sp(9, "Trace", 914400, 5486400, 10363200, 594360, "核心原则：先用权利要求限定技术事实，再找产品实现证据；所有推断都要能回到 F#、来源 URL 和落档规则。", "0F172A", "0F172A", "2000", "FFFFFF", True, "rect", "ctr"),
    ]))

    slides.append(slide_xml(4, [
        title("解决的问题：从“凭经验搜索”变成“可复核筛查”"),
        sp(3, "Problem1", 685800, 1371600, 3124200, 1371600, "问题 1\n候选遗漏\n\n用主体类型 + 三视角扩展，覆盖头部厂商、上游开源、下游产品和 OEM。", "DBEAFE", "93C5FD", "1800", "1E3A8A", True, "roundRect", "l"),
        sp(4, "Problem2", 4419600, 1371600, 3124200, 1371600, "问题 2\n证据不可追溯\n\n每个候选保留 _sources、关键证据、verdict，证据必须有 URL 或明确 0 命中。", "CCFBF1", "5EEAD4", "1800", "134E4A", True, "roundRect", "l"),
        sp(5, "Problem3", 8153400, 1371600, 3124200, 1371600, "问题 3\n误判成本高\n\n强制记录反例：接收端逻辑、固定 FEC、TCP 重传、标准相邻但不重合。", "FEF3C7", "FCD34D", "1800", "78350F", True, "roundRect", "l"),
        sp(6, "Problem4", 685800, 3429000, 3124200, 1371600, "问题 4\n领导难以理解\n\n用“领域→场景→组织→产品→证据”展示为什么会找到该产品。", "FFE4E6", "FDA4AF", "1800", "881337", True, "roundRect", "l"),
        sp(7, "Problem5", 4419600, 3429000, 3124200, 1371600, "问题 5\n法务难以接手\n\n输出高 ROI 候选、待核事项、反向专利墙/SEP/取证升级路径。", "EDE9FE", "C4B5FD", "1800", "4C1D95", True, "roundRect", "l"),
        sp(8, "Problem6", 8153400, 3429000, 3124200, 1371600, "问题 6\n无法复跑\n\n所有中间产物落盘，可重新审阅 query、候选池和每个 F# 的降级原因。", "FFFFFF", "CBD5E1", "1800", "334155", True, "roundRect", "l"),
    ]))

    slides.append(slide_xml(5, [
        title("CN107634908B 测试集示例：成功找到正确侵权产品 START 云游戏"),
        sp(3, "PatentCard", 685800, 1371600, 3581400, 3657600, "专利对象\nCN107634908B\n一种数据传输的方法和设备\n\n核心发明点\n发送端根据业务类型、网络状态、传输成功率、时延要求，自适应确定冗余包数量、传输总时间和调度方法。\n\n法律状态\nActive；授权日 2021-06-08；预期失效 2036-07-19。", "FFFFFF", "CBD5E1", "1750", "0F172A", True, "roundRect", "l"),
        sp(4, "ResultCard", 4724400, 1371600, 6400800, 3657600, "测试结果\n正确答案：腾讯 START 云游戏\n工作流输出：候选 01-tencent-start-cloudgaming，技术判定第 1 档：确认侵权（高）\n\n为什么能命中\n• 领域分析把本专利定位到“实时音视频传输 + 自适应 FEC + 业务感知 QoS”\n• 场景分析将云游戏/远程渲染列为最高命中场景之一\n• 潜在组织扩展到腾讯 START、先游、GameMatrix\n• 证据收集找到 NSDI 2024 三项 START 网络团队成果：Hairpin、Pudica、AUGUR\n• verdict 表显示权 1 F1-F5 字面命中 5/5", "DBEAFE", "93C5FD", "1800", "1E3A8A", True, "roundRect", "l"),
        sp(5, "Path", 914400, 5486400, 10210800, 594360, "示例链路：CN107634908B → 云游戏低时延传输场景 → 腾讯 START / GameMatrix → Hairpin + Pudica + AUGUR → 权 1 逐项证据表", "0F172A", "0F172A", "1900", "FFFFFF", True, "rect", "ctr"),
    ]))

    slides.append(slide_xml(6, [
        title("权 1 对应证据（一）：F1-F3"),
        sp(3, "F1", 685800, 1257300, 10424100, 1143000, "F1 根据数据流特征变量获取业务类型\n证据：腾讯文章称“为了满足云游戏对于画质、延迟、卡顿极为苛刻的要求”；业务类型即 cloud gaming / 低延迟视频流，并可区分视频帧、音频、控制信令。\n链接：https://ur.tencent.com/article/1481", "DBEAFE", "93C5FD", "1700", "1E3A8A", True, "roundRect", "l"),
        sp(4, "F2", 685800, 2743200, 10424100, 1371600, "F2 根据网络状态变量、传输成功率、业务类型获取冗余包数量\n证据：Hairpin 对数据包、重传和冗余包进行多轮传输最优组合；实时监测 RTT 和丢包事件，动态调整 FEC 参数，以适应网络条件快速变化。\n链接：https://ur.tencent.com/article/1481  |  https://github.com/hkust-spark/hairpin", "CCFBF1", "5EEAD4", "1700", "134E4A", True, "roundRect", "l"),
        sp(5, "F3", 685800, 4457700, 10424100, 1257300, "F3 根据时延要求获取冗余数据包传输总时间\n证据：Pudica 面向 cloud gaming 严格时延场景，以零排队为目标；AUGUR 围绕实时流媒体长尾时延和 frame stall rate 优化，体现 frame-level deadline。\n链接：https://www.usenix.org/conference/nsdi24/presentation/wang-shibo  |  https://www.usenix.org/conference/nsdi24/presentation/zhou-yuhan", "FEF3C7", "FCD34D", "1600", "78350F", True, "roundRect", "l"),
    ]))

    slides.append(slide_xml(7, [
        title("权 1 对应证据（二）：F4-F5 与结论"),
        sp(3, "F4", 685800, 1257300, 10424100, 1371600, "F4 根据网络状态变量、传输总时间、冗余数据包数量获取调度方法\n证据：Hairpin 的多轮传输最优组合对应冗余包调度方法；Pudica 的 zero-queuing pacing 对应在时延预算内安排发送时机。\n链接：https://github.com/hkust-spark/hairpin  |  https://www.usenix.org/conference/nsdi24/presentation/wang-shibo", "EDE9FE", "C4B5FD", "1700", "4C1D95", True, "roundRect", "l"),
        sp(4, "F5", 685800, 2971800, 10424100, 1143000, "F5 根据冗余数据包调度方法发送冗余数据包\n证据：Pudica abstract 说明该方案已部署在大规模云游戏平台，服务数百万玩家；START 官网证明对应商业产品持续运营。\n链接：https://www.usenix.org/conference/nsdi24/presentation/wang-shibo  |  https://start.qq.com", "FFE4E6", "FDA4AF", "1700", "881337", True, "roundRect", "l"),
        sp(5, "Conclusion", 685800, 4686300, 10424100, 1028700, "结论\n权 1 必要技术特征 F1-F5 均有公开证据对应；测试集正确答案 CN107634908B → 腾讯 START 云游戏被工作流排在第 1 档“确认侵权（高）”。", "0F172A", "0F172A", "2100", "FFFFFF", True, "rect", "ctr"),
    ]))

    slides.append(slide_xml(8, [
        title("可审计交付物：领导看路径，法务看证据"),
        sp(3, "Artifacts", 685800, 1371600, 5257800, 2743200, "本示例已落盘文件\n• CN107634908B“领域适配”.md\n• CN107634908B“潜在应用场景”.md\n• CN107634908B“违约列表”.md\n• 候选/01-tencent-start-cloudgaming/关键证据.md\n• 候选/01-tencent-start-cloudgaming/_sources.md\n• 候选/01-tencent-start-cloudgaming/_verdict.md", "FFFFFF", "CBD5E1", "1750", "0F172A", True, "roundRect", "l"),
        sp(4, "Audit", 6400800, 1371600, 4800600, 2743200, "审计口径\n• 每条 F# 证据有原文和 URL\n• 反例与已排除项单独列出\n• 标准合规/SEP/patent pledge 标为法务待核\n• 公开资料不足不硬判侵权\n• 最终列表按落档排序并给升级路径", "DBEAFE", "93C5FD", "1750", "1E3A8A", True, "roundRect", "l"),
        sp(5, "Next", 914400, 4800600, 10210800, 800100, "对外汇报建议：先用第 2 页解释流程，再用第 5-7 页展示 CN107634908B 如何在测试集中找到 START 云游戏，并逐项回到权 1 证据。", "0F172A", "0F172A", "1900", "FFFFFF", True, "rect", "ctr"),
    ]))

    return slides


def build() -> None:
    slides = make_slides()
    core, app = doc_props(len(slides))
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(len(slides)))
        z.writestr("_rels/.rels", package_rels())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("ppt/presentation.xml", presentation_xml(len(slides)))
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels(len(slides)))
        z.writestr("ppt/slideMasters/slideMaster1.xml", master_xml())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>""")
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout_xml())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", empty_rels())
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, xml in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels())


if __name__ == "__main__":
    build()
