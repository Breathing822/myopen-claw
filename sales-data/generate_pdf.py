#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程新能源商用车 车型培训手册 PDF生成器 v3
按照 微卡→小卡→轻卡→VAN→冷藏车 结构
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 颜色
C_GREEN   = HexColor('#1a5f2a')
C_LGREEN  = HexColor('#e8f5e9')
C_BGREEN  = HexColor('#a5d6a7')
C_ALT     = HexColor('#f1f8f1')
C_DARK    = HexColor('#333333')
C_GRAY    = HexColor('#666666')
C_BLUE    = HexColor('#1565C0')
C_LBLUE   = HexColor('#E3F2FD')
C_ORANGE  = HexColor('#E65100')
C_LORANGE = HexColor('#FFF3E0')

# 字体
FONT_MED = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_LIT = '/System/Library/Fonts/STHeiti Light.ttc'
pdfmetrics.registerFont(TTFont('Heiti-Medium', FONT_MED))
pdfmetrics.registerFont(TTFont('Heiti-Light', FONT_LIT))
FN = 'Heiti-Light'   # normal
FB = 'Heiti-Medium'  # bold

PAGE_W, PAGE_H = A4

# ─── 样式工厂 ───────────────────────────────────────────────
def mkstyle(n, **kw):
    d = {'name': n, 'fontName': FN, 'fontSize': 9, 'textColor': C_DARK, 'leading': 13}
    for k, v in kw.items():
        if k in d:
            d[k] = v
    return ParagraphStyle(**d)

S = {
    'title':    mkstyle('T',  fontName=FB, fontSize=20, textColor=C_GREEN,
                   alignment=TA_CENTER, spaceAfter=4, leading=26),
    'sub':      mkstyle('Sub', fontSize=11, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=18, leading=14),
    'h1':        mkstyle('H1', fontName=FB, fontSize=13, textColor=white,
                   backColor=C_GREEN, spaceAfter=8, spaceBefore=14,
                   leftIndent=-10, rightIndent=-10,
                   padding=(6, 10, 6, 10), leading=17),
    'h2':        mkstyle('H2', fontName=FB, fontSize=11, textColor=C_GREEN,
                   spaceAfter=4, spaceBefore=10, leading=14),
    'h3':        mkstyle('H3', fontName=FB, fontSize=9, textColor=HexColor('#2e7d32'),
                   spaceAfter=3, spaceBefore=6, leading=12),
    'body':      mkstyle('B',  fontSize=8.5, leading=12, spaceAfter=3),
    'bullet':    mkstyle('BU', fontSize=8.5, leading=11, spaceAfter=2,
                   leftIndent=12, bulletIndent=2),
    'note':      mkstyle('N',  fontSize=7.5, textColor=C_GRAY, alignment=TA_CENTER, leading=10),
    'tag_g':     mkstyle('TG', fontSize=8, textColor=C_GREEN, backColor=C_LGREEN,
                    alignment=TA_CENTER, leading=10),
    'tag_b':     mkstyle('TB', fontSize=8, textColor=C_BLUE, backColor=C_LBLUE,
                    alignment=TA_CENTER, leading=10),
    'tag_o':     mkstyle('TO', fontSize=8, textColor=C_ORANGE, backColor=C_LORANGE,
                    alignment=TA_CENTER, leading=10),
}

def p(txt, k='body'):     return Paragraph(txt, S[k])
def sp(h=0.2):            return Spacer(1, h*cm)
def hr():                 return HRFlowable(width='100%', thickness=0.5, color=C_GRAY)

# ─── 表格工具 ────────────────────────────────────────────────
def ts(data, widths, header_color=C_GREEN):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  header_color),
        ('TEXTCOLOR',    (0,0), (-1,0),  white),
        ('FONTNAME',     (0,0), (-1,0),  FB),
        ('FONTNAME',     (0,1), (-1,-1), FN),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('ALIGN',        (0,0), (0,-1),  'LEFT'),
        ('ALIGN',        (1,0), (-1,-1), 'LEFT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',         (0,0), (-1,-1), 0.5, C_BGREEN),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [white, C_ALT]),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def ts2(data, cw):
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('FONTNAME',     (0,0), (-1,-1), FN),
        ('FONTSIZE',     (0,0), (-1,-1), 8),
        ('TEXTCOLOR',    (0,0), (0,-1),  C_GREEN),
        ('ALIGN',        (0,0), (0,-1),  'LEFT'),
        ('ALIGN',        (1,0), (-1,-1), 'LEFT'),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',         (0,0), (-1,-1), 0.5, C_BGREEN),
        ('ROWBACKGROUNDS',(0,0),(-1,-1), [white, C_ALT]),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def tag(txt, k='tag_g'):
    return Paragraph(txt, S[k])

# ─── 页码 ────────────────────────────────────────────────────
def page_num(canvas, doc):
    canvas.saveState()
    canvas.setFont(FN, 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawCentredString(PAGE_W/2, PAGE_H - 1.2*cm,
                             "远程新能源商用车 车型培训手册")
    canvas.drawCentredString(PAGE_W/2, 1.0*cm, f"第 {doc.page} 页")
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════
def build_pdf():
    out = '/Users/breathing/.openclaw/workspace/sales-data/二网车型培训手册.pdf'
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=1.4*cm, rightMargin=1.4*cm,
                            topMargin=1.6*cm, bottomMargin=1.4*cm,
                            title="远程新能源商用车 车型培训手册")
    story = []
    cwA = [3*cm, 13*cm]      # 两列参数表
    cwB = [2.5*cm, 4*cm, 9.5*cm]  # 推荐车型表
    cwC = [2.2*cm, 2.2*cm, 2*cm, 2.2*cm, 2*cm, 1.8*cm, 1.8*cm]  # 轻卡对比
    cwD = [2.2*cm, 1.8*cm, 2*cm, 1.8*cm, 1.8*cm, 2*cm, 1.8*cm]  # VAN对比

    # ═══════════════════════════════════════════
    # 封面
    # ═══════════════════════════════════════════
    story += [sp(2), p("远程新能源商用车", 'sub'), p("车型培训手册", 'title'), sp(0.3),
              p("适用于：二网经销商 / 销售顾问", 'sub'), sp(0.8)]
    ct = Table([['更新时间', '2026年5月'],['车型覆盖','微卡·小卡·轻卡·VAN·冷藏车'],['版本','内部培训版 V2.0']],
               colWidths=[3.5*cm, 8*cm])
    ct.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),FN),('FONTSIZE',(0,0),(-1,-1),9),
        ('TEXTCOLOR',(0,0),(0,-1),C_GREEN),
        ('ALIGN',(0,0),(0,-1),'RIGHT'),
        ('ALIGN',(1,0),(1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
    ]))
    story += [ct, PageBreak()]

    # ═══════════════════════════════════════════
    # 一、产品线总览
    # ═══════════════════════════════════════════
    story.append(p("一、产品线总览", 'h1'))
    story.append(ts([
        ['级别', '代表车型', '货厢', '电池', '续航', '核心优势'],
        ['微卡', 'F1E', '3.3-3.5m³\n栏板/厢式', '玄武35-51kWh\n智芯46kWh', '260-305km', '灵活配送·最后1公里'],
        ['小卡', 'F3E / F5E', '3.7-3.8m³\n栏板/厢式', '玄武65-73kWh\n宁德71kWh\n智芯62kWh', '280-400km', '承载升级·城市重载'],
        ['轻卡', 'H8E / H9E / T9E', '4.0-4.2m³\n栏板/厢式', '智芯/玄武/宁德\n81-154kWh', '200-400km', '长途城配·重载主力'],
        ['轻卡-醇氢', 'H8M / H9M', '4.0m³+', '醇氢21/81kWh', '1000km+', '甲醇增程·里程无忧'],
        ['VAN-微客', 'V6E / V7E / V8E', '6-8.5m³\n盲仓/明窗', '玄武35-65kWh\n宁德50kWh', '300-460km', '客货两用·乘用体验'],
        ['冷藏车', '各系列冷藏版', '原厂冷藏厢', '各型号对应', '200-400km', '冷链运输·多温区'],
    ], [2*cm, 2.5*cm, 2.8*cm, 3.2*cm, 1.8*cm, 2.7*cm]))

    # ═══════════════════════════════════════════
    # 二、微卡 F1E
    # ═══════════════════════════════════════════
    story.append(p("二、微卡系列 — F1E", 'h1'))
    story.append(p("真能载 · 真能跑 · 真能赚", 'h2'))

    # 车型矩阵
    story.append(p("车型配置矩阵", 'h3'))
    story.append(ts([
        ['车型', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '快充', '电池质保'],
        ['F1E', '平板', '玄武', '35 / 41 / 51', '~305', '30min', '10年/80万'],
        ['F1E', '高栏', '玄武', '51', '~305', '30min', '10年/80万'],
        ['F1E', '厢式', '玄武', '35 / 41 / 51', '~305', '30min', '10年/80万'],
        ['F1E', '冷藏车', '智芯/宁德', '46 / 53', '~260', '支持', '8年/40万'],
    ], [1.8*cm, 2*cm, 2.5*cm, 3*cm, 1.8*cm, 1.8*cm, 3.1*cm]))

    story.append(p("核心卖点话术", 'h3'))
    for b in [
        '✅ <b>同级最大载质量</b>：核定载荷2.5t，载质量领先竞品30%',
        '✅ <b>超长质保</b>：电池最高10年/80万公里，创富无忧',
        '✅ <b>大方量货厢</b>：最大9.7m³（高栏），装得多赚得多',
        '✅ <b>快充+外放电</b>：30分钟补能，支持220V外放电，移动商铺',
        '✅ <b>越级宽体驾舱</b>：轻卡级空间，躺平休息，舒适创富',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("销售话术", 'h3'))
    story.append(p(
        '"这台F1E，10年80万质保、9方大货厢、2.5吨载质量，'
        '城里配送一趟能多拉200斤货，充电30分钟就跑一天，'
        '还有220V外放电摆摊用，算下来比油车一年省2万多。"', 'body'))

    # ═══════════════════════════════════════════
    # 三、小卡 F3E / F5E
    # ═══════════════════════════════════════════
    story.append(p("三、小卡系列 — F3E / F5E", 'h1'))
    story.append(p("城市重载配送首选，介于微卡和轻卡之间", 'h2'))

    story.append(p("F3E 车型配置矩阵", 'h3'))
    story.append(ts([
        ['车型', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['F3E', '平板', '玄武', '65 / 73', '~350', '10年/80万'],
        ['F3E', '平板', '宁德', '71', '~380', '8年/60万'],
        ['F3E', '高栏', '玄武', '65 / 73', '~350', '10年/80万'],
        ['F3E', '厢式', '玄武', '65 / 73', '~350', '10年/80万'],
        ['F3E', '厢式', '宁德', '71', '~380', '8年/60万'],
    ], [1.8*cm, 2*cm, 2.5*cm, 3*cm, 1.8*cm, 3.9*cm]))

    story.append(p("F5E 车型配置矩阵", 'h3'))
    story.append(ts([
        ['车型', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['F5E', '平板', '智芯', '62', '~320', '8年/40万'],
        ['F5E', '厢式', '智芯', '62', '~320', '8年/40万'],
    ], [1.8*cm, 2*cm, 2.5*cm, 3*cm, 1.8*cm, 3.9*cm]))

    story.append(p("核心卖点话术", 'h3'))
    for b in [
        '✅ <b>160mm直通大梁</b>：610L高强钢，1.5t/3t额定载荷，重载无忧',
        '✅ <b>免维护前后桥</b>：前后桥免维护轮端，降低维护成本',
        '✅ <b>乘用化座舱</b>：电子怀挡、无钥匙进入、电动冷暖空调',
        '✅ <b>超长质保</b>：玄武电池10年/80万公里',
        '✅ <b>智慧辅助驾驶</b>：FCW/LDW/AEB/ACC/PEB全方位保护',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("销售话术", 'h3'))
    story.append(p(
        '"F3E小卡比微卡能多拉1吨货，比轻卡更灵活好停车，'
        '160大梁+3吨后桥，建材、仓储配送全拿下，'
        '玄武电池10年80万质保，买回去放心用。"', 'body'))

    # ═══════════════════════════════════════════
    # 四、轻卡 H系列 / T系列
    # ═══════════════════════════════════════════
    story.append(p("四、轻卡系列 — H8E / H9E / T9E / H8M / H9M", 'h1'))

    # H8E
    story.append(p("H8E 中体轻卡 配置矩阵", 'h2'))
    story.append(ts([
        ['货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['平板', '智芯', '101', '~280', '8年/40万'],
        ['平板', '玄武', '133', '~350', '10年/80万'],
        ['高栏', '智芯', '81 / 101', '~250/280', '8年/40万'],
        ['高栏', '玄武', '133', '~350', '10年/80万'],
        ['高栏', '宁德', '120', '~300', '8年/60万'],
        ['厢式', '智芯', '81 / 101', '~250/280', '8年/40万'],
        ['厢式', '玄武', '133', '~350', '10年/80万'],
        ['厢式', '宁德', '120', '~300', '8年/60万'],
    ], [2.5*cm, 2.5*cm, 3*cm, 2*cm, 3*cm]))

    story.append(sp(0.2))

    # H9E
    story.append(p("H9E 宽体轻卡 配置矩阵", 'h2'))
    story.append(ts([
        ['货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保', '备注'],
        ['平板', '玄武(2C)', '133', '~350', '10年/80万', '2C快充'],
        ['高栏', '宁德', '120 / 140', '~300/360', '8年/60万', ''],
        ['高栏', '玄武', '133 / 154', '~350/400', '10年/80万', ''],
        ['厢式', '宁德', '120 / 140', '~300/360', '8年/60万', ''],
        ['厢式', '玄武', '133 / 154', '~350/400', '10年/80万', ''],
    ], [2.2*cm, 2.2*cm, 2.8*cm, 1.8*cm, 2.5*cm, 2.5*cm]))

    story.append(sp(0.2))

    # T9E
    story.append(p("T9E 平板轻卡 配置矩阵", 'h2'))
    story.append(ts([
        ['货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['平板', '宁德', '120 / 140', '~300/360', '8年/60万'],
        ['平板', '玄武', '133 / 154', '~350/400', '10年/80万'],
        ['高栏', '宁德', '120 / 140', '~300/360', '8年/60万'],
        ['高栏', '玄武', '133 / 154', '~350/400', '10年/80万'],
        ['厢式', '宁德', '120 / 140', '~300/360', '8年/60万'],
        ['厢式', '玄武', '133 / 154', '~350/400', '10年/80万'],
    ], [2.2*cm, 2.2*cm, 2.8*cm, 1.8*cm, 2.8*cm, 2.2*cm]))

    story.append(sp(0.2))
    story.append(p("轻卡核心卖点话术", 'h3'))
    for b in [
        '✅ <b>H9E宽体驾驶室</b>：+100mm宽度，乘坐空间更宽敞',
        '✅ <b>多种电池选择</b>：智芯/玄武/宁德，按需选配',
        '✅ <b>2C快充版</b>：H9E平板133度2C，充电更快',
        '✅ <b>气刹制动</b>：60km/h下比液刹短7米，长下坡更安全',
        '✅ <b>EPB躺平赚钱</b>：电子驻车，座椅间无凸起可躺平休息',
        '✅ <b>B端专属服务</b>：0息金融、管家服务、备用车',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("销售话术", 'h3'))
    story.append(p(
        '"这台H9E宽体，154度玄武电池跑400公里没问题，'
        '气刹+EPB，开高速下坡都安全，EPB还能躺平休息，'
        '10年80万质保，零息金融只要X万就能开走。"', 'body'))

    # 醇氢轻卡
    story.append(sp(0.3))
    story.append(p("H8M / H9M 醇氢轻卡（甲醇增程）配置矩阵", 'h2'))
    story.append(ts([
        ['车型', '货厢类型', '电池/醇箱', '电量(kWh)', '综合续航', '电池质保'],
        ['H8M', '高栏', '醇氢21', '~21', '1000km+', '—'],
        ['H8M', '厢式', '醇氢21', '~21', '1000km+', '—'],
        ['H9M', '高栏', '醇氢81', '~81', '1000km+', '—'],
        ['H9M', '厢式', '醇氢81', '~81', '1000km+', '—'],
    ], [1.8*cm, 2.2*cm, 2.5*cm, 2.5*cm, 2.5*cm, 3.5*cm]))

    story.append(p("醇氢卖点话术", 'h3'))
    for b in [
        '⛽ <b>超长续航</b>：甲醇+纯电综合续航1000km+，无里程焦虑',
        '⛽ <b>燃料灵活</b>：可醇可电，甲醇补给方便，续航无忧',
        '⛽ <b>寒区适用</b>：H9M 81度大醇箱，满足寒区长途运营',
        '⛽ <b>成本优势</b>：甲醇燃料成本低，综合运营成本优于纯电',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("销售话术", 'h3'))
    story.append(p(
        '"醇氢版跑长途再也不担心充电问题了，'
        '加注甲醇几分钟跑1000公里，成本比纯电还省，'
        'H9M 81度醇箱，寒区长途配送首选。"', 'body'))

    # ═══════════════════════════════════════════
    # 五、VAN V6E / V7E / V8E
    # ═══════════════════════════════════════════
    story.append(p("五、VAN系列 — V6E / V7E / V8E", 'h1'))

    # V6E
    story.append(p("V6E — 6方大空间，同级最大", 'h2'))
    story.append(ts([
        ['版别', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['功能版', '盲仓', '玄武', '41 / 51', '~300/325', '10年/80万'],
        ['明盲窗26款', '盲仓', '玄武', '41 / 51', '~300/325', '10年/80万'],
        ['明盲窗26款', '明窗', '玄武', '35 / 41 / 51', '~280/300/325', '10年/80万'],
    ], [2.5*cm, 2.5*cm, 2.5*cm, 2.8*cm, 1.8*cm, 2.9*cm]))

    story.append(p("V6E 核心卖点话术", 'h3'))
    for b in [
        '✅ <b>6方大空间</b>：同级最大货厢，座椅可折叠/挂起',
        '✅ <b>270度对开尾门</b>：方便开启固定，不占空间',
        '✅ <b>超长质保</b>：玄武电池10年/80万公里',
        '✅ <b>灵活空间</b>：第二/三排连体座椅可侧翻挂起，扩展货舱',
        '✅ <b>功能版性价比</b>：价格友好，创业首选',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))

    # V7E
    story.append(p("V7E — 7方大空间，拉得多赚得多", 'h2'))
    story.append(ts([
        ['版别', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['载货版', '盲仓', '玄武', '51', '~375', '10年/80万'],
        ['载货版', '盲仓', '宁德', '50', '~365', '8年/60万'],
        ['载货版', '明窗', '玄武', '51', '~375', '10年/80万'],
        ['功能版', '明窗', '玄武', '51', '~375', '10年/80万'],
        ['功能版', '明窗', '宁德', '50', '~365', '8年/60万'],
    ], [2.2*cm, 2.2*cm, 2.2*cm, 2.5*cm, 1.8*cm, 3.1*cm]))

    story.append(p("V7E 核心卖点话术", 'h3'))
    for b in [
        '✅ <b>7.5m³大空间</b>：买7方送半方，货厢2870mm可拓4100mm',
        '✅ <b>1.5吨额定载重</b>：同级最强，多拉350kg≈29箱矿泉水',
        '✅ <b>2C液冷超充</b>：15分钟补能200km，充电10分钟跑2小时',
        '✅ <b>OneBox制动</b>：满载80km/h刹停仅28米',
        '✅ <b>乘用化座舱</b>：怀挡+座椅通风加热+语音交互+360影像',
        '✅ <b>V2L外放电</b>：货厢支持220V取电，多场景拓展',
        '✅ <b>功能版</b>：5/6/7/9座可选，座椅全平放倒，拉人载货两用',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))

    # V8E
    story.append(p("V8E — 8方大空间，承载担当", 'h2'))
    story.append(ts([
        ['版别', '货厢类型', '电池品牌', '电量(kWh)', '续航(km)', '电池质保'],
        ['载货版', '盲仓', '玄武', '51 / 65', '~350/460', '10年/80万'],
        ['载货版', '明窗', '玄武', '51 / 65', '~350/460', '10年/80万'],
        ['功能版', '明窗(营运版)', '玄武', '51 / 65', '~350/460', '10年/80万'],
        ['冷藏车', '冷藏版', '玄武', '51', '~340', '10年/80万'],
    ], [2.2*cm, 2.2*cm, 2.2*cm, 2.5*cm, 1.8*cm, 3.1*cm]))

    story.append(p("V8E 核心卖点话术", 'h3'))
    for b in [
        '✅ <b>8.5m³大空间</b>：货厢内长3280mm，可拓展4500mm',
        '✅ <b>1.61吨额定载重</b>：同级最强承载',
        '✅ <b>双侧滑门</b>：最大1100mm侧门开度，支持1×1.2m托盘',
        '✅ <b>2C液冷超充</b>：65度电池跑460km，充电10分钟跑2小时',
        '✅ <b>功能版</b>：6/7/9座可选，座椅翻折，拉人载货都方便',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("VAN全系列销售话术", 'h3'))
    story.append(p(
        '"V8E拉8方货、1.61吨，城里建材、商超配送全够用，'
        '65度电跑460公里，2C快充15分钟就能再跑200公里，'
        '还有360影像、语音交互、座椅加热，'
        '乘用车一样的体验 but 能拉货能拉人！"', 'body'))

    # ═══════════════════════════════════════════
    # 六、冷藏车
    # ═══════════════════════════════════════════
    story.append(p("六、冷藏车系列", 'h1'))
    story.append(p("原厂冷藏厢 · 多温区控温 · 冷链首选", 'h2'))

    story.append(ts([
        ['适配车型', '货厢尺寸参考', '电池', '电量(kWh)', '续航参考', '冷机温度'],
        ['V8E 冷藏版', '原厂冷藏厢', '玄武', '51', '~340km', '-18℃以下'],
        ['F1E 冷藏版', '原厂冷藏厢', '智芯/宁德', '46 / 53', '~260km', '-18℃以下'],
        ['F5E 冷藏版', '原厂冷藏厢', '智芯', '62', '~300km', '-18℃以下'],
        ['H8E 冷藏版', '原厂冷藏厢', '宁德', '100 / 140', '~280/380km', '-29℃以下'],
        ['H9E 冷藏版', '原厂冷藏厢', '玄武', '132 / 154', '~350/400km', '-29℃以下'],
        ['H8M 冷藏版', '原厂冷藏厢', '醇氢21', '~21', '800km+', '-29℃以下'],
        ['H9M 冷藏版', '原厂冷藏厢', '醇氢81', '~81', '1000km+', '-29℃以下'],
    ], [2.8*cm, 3*cm, 2.2*cm, 2.2*cm, 2*cm, 2.8*cm]))

    story.append(p("冷藏车核心卖点话术", 'h3'))
    for b in [
        '❄️ <b>原厂冷藏厢</b>：标配原厂冷藏厢体，品质有保障',
        '❄️ <b>极速降温</b>：30℃降至0℃仅需20分钟（比油车快一倍）',
        '❄️ <b>多区控温</b>：冷藏/常温/冷冻多模式，满足不同货物需求',
        '❄️ <b>防锈材质</b>：玻璃钢+聚氨酯，符合FDA食品级认证',
        '❄️ <b>超低油耗/电耗</b>：纯电冷藏成本低，醇氢版续航无忧',
        '❄️ <b>轻卡冷藏版</b>：H9E 154度跑400公里，H8M醇氢版跑1000公里',
    ]:
        story.append(p(b, 'bullet'))

    story.append(sp(0.2))
    story.append(p("销售话术", 'h3'))
    story.append(p(
        '"冷藏车选我们，H9E配154度玄武电池，跑400公里全程冷链不停机，'
        '-29℃超低温，医药、冻肉、海鲜全搞定；'
        '如果跑长途选H9M醇氢版，1000公里续航，甲醇加注快，冷链不间断。"', 'body'))

    # ═══════════════════════════════════════════
    # 七、选装包汇总
    # ═══════════════════════════════════════════
    story.append(p("七、选装包汇总", 'h1'))
    story.append(ts([
        ['选装包', 'V6E', 'V7E', 'V8E', '说明'],
        ['补能包', '—', '✅', '✅', '6.6kW慢充 + V2L车内/车外对外放电'],
        ['科技降险运维包', '—', '✅', '✅', 'DVR + DMS + 流量包 + 双向实时通话'],
        ['智享包2', '—', '—', '✅', '大屏线束 + 高清倒车摄像头 + 电调后视镜(带加热)'],
        ['尊享包', '—', '✅', '—', '铝合金花纹地板 + 货厢顶棚 + 隔断观察窗'],
        ['集成ADAS', '✅(26款)', '—', '—', 'LDW+FCW+AEB+DMS+ESC+胎压(V6E明盲窗26款标配)'],
    ], [3.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 7.1*cm]))

    # ═══════════════════════════════════════════
    # 八、快速对比
    # ═══════════════════════════════════════════
    story.append(p("八、产品快速对比", 'h1'))

    story.append(p("轻卡对比（H8E / H9E / T9E）", 'h2'))
    story.append(ts([
        ['车型', '宽度', '轴距', '电量', '续航', '快充', '峰值功率'],
        ['H8E 中体', '窄体', '3360', '81-133kWh', '250-350km', '2C/20min', '81-155kW'],
        ['H9E 宽体', '+100mm', '3360', '120-154kWh', '300-400km', '2C/20min', '100-155kW'],
        ['T9E', '2120mm', '3360/3600', '120-154kWh', '300-400km', '18min', '235kW'],
        ['H8M 醇氢', '窄体', '3360', '醇氢21', '1000km+', '甲醇', '100kW'],
        ['H9M 醇氢', '宽体', '3360', '醇氢81', '1000km+', '甲醇', '100kW'],
    ], cwC))

    story.append(sp(0.2))
    story.append(p("VAN对比（V6E / V7E / V8E）", 'h2'))
    story.append(ts([
        ['车型', '货厢', '电量', '续航', '载质量', '快充', '质保'],
        ['V6E 盲仓', '6m³', '41/51kWh', '300-325km', '—', '35min', '10年/80万'],
        ['V6E 明窗', '6m³', '35/41/51kWh', '280-325km', '—', '36min', '10年/80万'],
        ['V7E 盲仓', '7.5m³', '51kWh', '375km', '1.5吨', '15min', '10年/80万'],
        ['V7E 明窗', '7.5m³', '51kWh', '375km', '1.5吨', '15min', '10年/80万'],
        ['V8E 盲仓', '8.5m³', '51/65kWh', '350-460km', '1.61吨', '15min', '10年/80万'],
        ['V8E 明窗', '8.5m³', '51/65kWh', '350-460km', '1.61吨', '15min', '10年/80万'],
    ], cwD))

    story.append(sp(0.2))
    story.append(p("微卡/小卡对比", 'h2'))
    story.append(ts([
        ['车型', '级别', '电量', '续航', '载质量', '电池质保'],
        ['F1E', '微卡', '35-51kWh', '~305km', '1.0-1.6吨', '10年/80万'],
        ['F3E', '小卡', '65-73kWh', '~350-380km', '1.5-3.0吨', '10年/80万'],
        ['F5E', '小卡', '62kWh', '~320km', '1.5-3.0吨', '8年/40万'],
    ], [2*cm, 2*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.6*cm]))

    # ═══════════════════════════════════════════
    # 九、客户需求推荐
    # ═══════════════════════════════════════════
    story.append(p("九、客户需求推荐", 'h1'))
    story.append(ts([
        ['客户需求', '推荐车型', '核心卖点'],
        ['最后一公里配送', 'F1E', '灵活通过、35度小电池够用、性价比最高'],
        ['商超/社区团购配送', 'F1E / V6E', 'F1E能拉1.6吨+V6E 6方空间'],
        ['城市重载配送', 'F3E', '160mm大梁+3吨后桥，载质量比微卡高30%'],
        ['工厂/仓储物流', 'V7E / H8E', 'V7E 7.5方拉得多，H8E重载长续航'],
        ['长途城配/专线', 'H9E / T9E', '154度跑400公里，2C快充效率高'],
        ['冷链-城市配送', 'V8E冷藏 / F1E冷藏', 'V8E 51度跑340公里，H9E 154度跑400公里'],
        ['冷链-长途运输', 'H9E冷藏 / H9M冷藏', 'H9E 154度400km，H9M醇氢1000km不间断'],
        ['建材/重载运输', 'F3E / H8E', 'F3E小卡3吨后桥，H8E 133度重载版'],
        ['甲醇增程-长途', 'H9M 醇氢', '81度醇箱，1000km+续航，甲醇成本低'],
        ['客货两用/营运', 'V7E/V8E功能版', '5-9座可选，座椅全平放倒，拉人拉货两相宜'],
    ], cwB))

    # ═══════════════════════════════════════════
    # 十、质保服务
    # ═══════════════════════════════════════════
    story.append(p("十、质保与服务体系", 'h1'))
    story.append(ts2([
        ['服务项目', '内容'],
        ['三电质保', '玄武电池：最高10年/80万公里 | 宁德电池：8年/60万公里 | 智芯电池：8年/40万公里'],
        ['底盘免维护', '5年/30万km（轻卡）'],
        ['B端专属服务', '0息金融、长周期、管家服务、备用车、停运补偿'],
        ['金融方案', '可租可售可回购，多样化金融产品'],
    ], [3*cm, 13*cm]))

    story += [sp(0.8), hr(),
              p('📌 声明：具体配置以实车为准。远程新能源商用车保留对所有参数和配置修改的权力，如有变更，恕不另行通知。', 'note')]

    doc.build(story, onFirstPage=page_num, onLaterPages=page_num)
    print(f"PDF生成成功: {out}")
    return out

if __name__ == '__main__':
    build_pdf()
