#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程新能源商用车 车型培训手册 PDF生成器 v2
优化排版，减少空白页
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 颜色
PRIMARY_GREEN = HexColor('#1a5f2a')
LIGHT_GREEN = HexColor('#e8f5e9')
BORDER_GREEN = HexColor('#a5d6a7')
ALT_ROW = HexColor('#f1f8f1')
DARK_TEXT = HexColor('#333333')
GRAY_TEXT = HexColor('#666666')

# 字体
FONT_MEDIUM = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_LIGHT = '/System/Library/Fonts/STHeiti Light.ttc'
pdfmetrics.registerFont(TTFont('Heiti-Medium', FONT_MEDIUM))
pdfmetrics.registerFont(TTFont('Heiti-Light', FONT_LIGHT))
FONT_NORMAL = 'Heiti-Light'
FONT_BOLD = 'Heiti-Medium'

PAGE_WIDTH, PAGE_HEIGHT = A4

def S(name='Normal', **kw):
    """创建样式"""
    base = ParagraphStyle(name=name, fontName=FONT_NORMAL, fontSize=9,
                          textColor=DARK_TEXT, leading=13, **kw)
    return base

def make_styles():
    s = {}
    s['title'] = ParagraphStyle('Title2', fontName=FONT_BOLD, fontSize=20,
                               textColor=PRIMARY_GREEN, alignment=TA_CENTER,
                               spaceAfter=4, leading=26)
    s['subtitle'] = ParagraphStyle('Subtitle2', fontName=FONT_NORMAL, fontSize=11,
                                   textColor=GRAY_TEXT, alignment=TA_CENTER, spaceAfter=20, leading=14)
    s['h1'] = ParagraphStyle('H12', fontName=FONT_BOLD, fontSize=14,
                              textColor=white, backColor=PRIMARY_GREEN,
                              spaceAfter=8, spaceBefore=14, leftIndent=-10, rightIndent=-10,
                              padding=(7, 10, 7, 10), leading=18)
    s['h2'] = ParagraphStyle('H22', fontName=FONT_BOLD, fontSize=11,
                              textColor=PRIMARY_GREEN, spaceAfter=5, spaceBefore=10, leading=14)
    s['h3'] = ParagraphStyle('H32', fontName=FONT_BOLD, fontSize=9,
                              textColor=HexColor('#2e7d32'), spaceAfter=3, spaceBefore=6, leading=12)
    s['body'] = ParagraphStyle('Body2', fontName=FONT_NORMAL, fontSize=8.5,
                               textColor=DARK_TEXT, alignment=TA_LEFT, spaceAfter=3, leading=12)
    s['bullet'] = ParagraphStyle('Bullet2', fontName=FONT_NORMAL, fontSize=8.5,
                                 textColor=DARK_TEXT, spaceAfter=2, leading=11,
                                 leftIndent=12, bulletIndent=2)
    s['note'] = ParagraphStyle('Note2', fontName=FONT_NORMAL, fontSize=7.5,
                               textColor=GRAY_TEXT, alignment=TA_CENTER, spaceAfter=8, leading=10)
    return s

ST = make_styles()

def TS(col_widths=None):
    """标准表格样式"""
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), PRIMARY_GREEN),
        ('FONTNAME', (0,0), (-1,0), FONT_BOLD),
        ('FONTNAME', (0,1), (-1,-1), FONT_NORMAL),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GREEN),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, ALT_ROW]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ])
    if col_widths:
        ts._argW  = col_widths
    return ts

def TS2(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TS(col_widths))
    return t

def h1(txt):
    return Paragraph(txt, ST['h1'])

def h2(txt):
    return Paragraph(txt, ST['h2'])

def h3(txt):
    return Paragraph(txt, ST['h3'])

def body(txt):
    return Paragraph(txt, ST['body'])

def bullet(txt):
    return Paragraph(txt, ST['bullet'])

def sp(h=0.2):
    return Spacer(1, h*cm)

def page_num(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NORMAL, 8)
    canvas.setFillColor(GRAY_TEXT)
    canvas.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 1.2*cm,
                             "远程新能源商用车 车型培训手册")
    canvas.drawCentredString(PAGE_WIDTH/2, 1.0*cm, f"第 {doc.page} 页")
    canvas.restoreState()

def build_pdf():
    out = '/Users/breathing/.openclaw/workspace/sales-data/二网车型培训手册.pdf'
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=1.4*cm, rightMargin=1.4*cm,
                            topMargin=1.6*cm, bottomMargin=1.4*cm,
                            title="远程新能源商用车 车型培训手册")
    s = ST
    story = []

    # ========== 封面 ==========
    story.append(sp(2))
    story.append(Paragraph("远程新能源商用车", s['subtitle']))
    story.append(Paragraph("车型培训手册", s['title']))
    story.append(sp(0.3))
    story.append(Paragraph("适用于：二网经销商 / 销售顾问", s['subtitle']))
    story.append(sp(0.8))

    cover = [
        ['更新时间', '2026年5月'],
        ['车型覆盖', '微卡 · 轻卡 · 中卡 · 冷藏 · VAN'],
        ['版本', '内部培训版 V1.0'],
    ]
    ct = Table(cover, colWidths=[3.5*cm, 8*cm])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT_NORMAL),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), PRIMARY_GREEN),
        ('TEXTCOLOR', (1,0), (1,-1), DARK_TEXT),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ct)
    story.append(PageBreak())

    # ========== 一、产品线总览 ==========
    story.append(h1("一、产品线总览"))
    overview = [
        ['系列', '代表车型', '定位', '适用场景'],
        ['微卡', 'F1E', '最后一公里配送', '城乡快递、商超配送、社区团购'],
        ['轻卡', '星智T、星智H、星智T冷藏/甲醇', '城配物流、中长途', '商超配送、冷链运输、长途货运'],
        ['中卡', 'F3E', '重载城配', '工厂物流、仓储转运、建材运输'],
        ['轻客/VAN', 'V6E/V7E/V8E', '客货两用/城市配送', '多人通勤、商户运输、移动商铺'],
    ]
    story.append(TS2(overview, [2.2*cm, 5*cm, 3.2*cm, 5.6*cm]))

    # ========== 二、微卡 ==========
    story.append(h1("二、微卡系列"))
    story.append(h2("星智F1E —— 真能载·真能跑·真能赚"))
    story.append(h3("基本参数"))
    story.append(TS2([
        ['驾驶室外宽', '1730mm'], ['轴距', '2600 / 2995 / 3200mm'],
        ['总质量', '2995 / 3200kg'], ['额定载质量', '955~1600kg（同级最强）'],
        ['货厢容积', '7.7~9.7m³（最大3350×1700×1700）'], ['最高车速', '90~100km/h'],
    ], [3*cm, 13*cm]))

    story.append(h3("三电系统"))
    story.append(TS2([
        ['电池品牌', '玄武35.2/41.05/51.39kWh / 宁德41.86kWh / 智芯46.08kWh'],
        ['电池质保', '最高 10年/80万公里（玄武）'],
        ['快充', '20%~80%，30分钟'],
        ['对外放电', '支持220V外放电（移动综合体）'],
    ], [3*cm, 13*cm]))

    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>同级最大载质量</b>：核定载荷2.5t，载质量领先竞品30%',
        '✅ <b>超长质保</b>：电池最高10年/80万公里',
        '✅ <b>大方量货厢</b>：9.7m³，装得多赚得多',
        '✅ <b>越级宽体驾舱</b>：轻卡级驾舱，空间优于竞品4%~6%',
        '✅ <b>快充+外放电</b>：30分钟补能，支持多种电器取电',
    ]:
        story.append(bullet(b))

    # ========== 三、轻卡 ==========
    story.append(h1("三、轻卡系列"))

    # 3.1 星智H
    story.append(h2("星智H轻卡 —— 智优双全，安心赚钱"))
    story.append(TS2([
        ['驾驶室外宽', 'H8E中体（窄）/ H9E宽体（+100mm）'],
        ['轴距', '3360 / 4495mm'], ['总质量', '4495kg'],
        ['货厢类型', '厢式 / 仓栅 / 栏板'],
        ['电池容量', '60 / 70 / 120 / 140kWh'], ['续航', '200~400km'],
        ['快充', '1C≤40min / 2C≤20min'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>智芯自研三电</b>：电机效率97.86%，峰值扭矩400N·m',
        '✅ <b>超低能耗</b>：百公里32kWh，优于竞品3%~8%',
        '✅ <b>气刹制动</b>：60km/h下比液刹短7米制动距离',
        '✅ <b>可调节导流罩</b>：减少风阻，提高续航7%',
        '✅ <b>EPB躺平赚钱</b>：电子驻车替代手柄，座椅间无凸起可躺平',
        '✅ <b>B端专属服务</b>：0息金融、长周期、管家服务、备用车',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # 3.2 星智T
    story.append(h2("星智T纯电轻卡 —— 硬核承载，智驾未来"))
    story.append(TS2([
        ['驾驶室外宽', '2120mm'], ['轴距', '3360 / 3600mm'],
        ['电池容量', '玄武133/154kWh / 宁德120/140kWh'],
        ['快充', '18分钟（20%~80%）'],
        ['峰值功率', '智芯 235kW'], ['轮端扭矩', '16000N·m'],
        ['续航', '300~400km+'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>硬核动力</b>：峰值功率235kW，轮端扭矩16000N·m',
        '✅ <b>超低能耗</b>：IEM能量管理，能耗降低20%',
        '✅ <b>极速补能</b>：2C液冷超充，15分钟补能200km+',
        '✅ <b>硬核承载</b>：4吨前桥+8吨后桥，214mm幅高直通梁车架',
        '✅ <b>智驾顶配</b>：18项组合驾驶辅助，AEB标配',
        '✅ <b>超长质保</b>：三电最高10年/80万公里',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # 3.3 星智T冷藏
    story.append(h2("星智T冷藏轻卡 —— 冷链首选"))
    story.append(TS2([
        ['冷藏厢体', '原厂4080×2100×2100mm（单开门/聚氨酯/花纹玻璃钢底板）'],
        ['电池容量', '玄武110/133/154kWh / 宁德120/140kWh'],
        ['快充', '18分钟（20%~80%）'],
        ['冷机温度', '最低-29℃'],
        ['降温速度', '30℃降至0℃仅需20分钟（比油车快一倍）'],
    ], [3*cm, 13*cm]))
    for b in [
        '❄️ <b>极速降温</b>：30℃降至0℃仅需20分钟',
        '❄️ <b>多区控温</b>：冷藏/常温/冷冻多场景',
        '❄️ <b>防锈材质</b>：玻璃钢、VR板，符合FDA食品级认证',
        '❄️ <b>甲醇增程版</b>：续航超1500km（醇箱120+140L）',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # 3.4 星智T甲醇
    story.append(h2("星智T甲醇轻卡 —— 增程续航新选择"))
    story.append(TS2([
        ['动力类型', '甲醇增程'],
        ['增程器', '智芯2.0T，功率100kW'],
        ['醇箱容量', '120+140L（标配）/ 120+140+90L（寒区版）'],
        ['续航', '超1500km（甲醇+纯电）'],
    ], [3*cm, 13*cm]))

    # ========== 四、中卡 ==========
    story.append(h1("四、中卡系列"))
    story.append(h2("星智F3E中卡 —— 承重担当"))
    story.append(TS2([
        ['驾驶室外宽', '1820mm'], ['轴距', '3700mm'], ['总质量', '3495kg'],
        ['货厢尺寸', '3790/3820×1870/1900×360mm（栏板/厢式/仓栅）'],
        ['电池容量', '玄武65/73kWh / 宁德56/71kWh'],
        ['续航', '300~400km（CLTC）'], ['峰值功率', '105/110kW'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>重载设计</b>：1.5t/3.0t额定载荷，160mm直通大梁',
        '✅ <b>免维护前后桥</b>：降低维护成本',
        '✅ <b>乘用化配置</b>：电子怀挡、无钥匙进入启动、电动冷暖空调',
        '✅ <b>超长质保</b>：玄武电池10年/80万公里',
    ]:
        story.append(bullet(b))

    # ========== 五、VAN ==========
    story.append(h1("五、轻客/VAN系列"))

    # V6E
    story.append(h2("星享V6E —— 6方大空间，同级最大"))
    story.append(TS2([
        ['整车尺寸', '4845×1730×1985mm'], ['轴距', '3100mm'],
        ['货箱容积', '6m³（2800×1600×1320mm）'],
        ['续航', '300~355km（CLTC）'],
        ['电池质保', '最高10年/80万公里（玄武）'],
        ['快充', '35~36分钟（20%~80%）'], ['座位数', '6座'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>6方大空间</b>：同级最大',
        '✅ <b>超长质保</b>：电池最高10年/80万公里',
        '✅ <b>灵活空间</b>：座椅可折叠/挂起，270度对开尾门',
        '✅ <b>V6E明盲窗26款</b>：续航升级350km+，新增香草蓝配色',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # V7E
    story.append(h2("星享V7E —— 7方大空间，拉得多赚得多"))
    story.append(TS2([
        ['整车尺寸', '5000×1820×1985mm'], ['轴距', '3200mm'],
        ['货箱容积', '7.5m³（2870×1770×1475mm）'],
        ['额定载重', '1.5吨（同级最强）'],
        ['续航', '365~375km（CLTC）'],
        ['快充', '2C液冷，30%~80%仅需15分钟'],
        ['电耗', '13.8kWh/100km（行业最低）'],
    ], [3*cm, 13*cm]))
    story.append(h3("制动系统"))
    story.append(TS2([
        ['制动类型', 'OneBox线控制动 + 前后盘式'],
        ['满载80km/h刹停', '仅需28米'],
        ['驻车', 'EPB电子手刹 + AutoHold'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>7.5m³大空间</b>：买7方送半方',
        '✅ <b>1.5吨额定载重</b>：同级最强，多装350kg（≈29箱矿泉水）',
        '✅ <b>极速补能</b>：2C液冷，15分钟补能200km',
        '✅ <b>行业最低电耗</b>：13.8kWh/100km',
        '✅ <b>OneBox制动</b>：满载80km/h刹停仅28米',
        '✅ <b>乘用化体验</b>：怀挡、躺椅、语音交互、V2L外放电',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # V8E
    story.append(h2("星享V8E —— 8方大空间，承载担当"))
    story.append(TS2([
        ['整车尺寸', '5400×1820×1985mm'], ['轴距', '3605mm'],
        ['货箱容积', '8.5m³（3280×1770×1475mm，可拓展4500mm）'],
        ['额定载重', '1.61吨（同级最强）'],
        ['续航', '340~460km（CLTC）'],
        ['电池', '玄武65kWh（10年/80万公里）/ 宁德50.2kWh'],
        ['快充', '2C液冷超充'],
    ], [3*cm, 13*cm]))
    story.append(h3("核心卖点"))
    for b in [
        '✅ <b>8.5m³大同级半方</b>：货厢内长3280mm，可拓展4500mm',
        '✅ <b>1.61吨额定载重</b>：同级最强',
        '✅ <b>双侧滑门</b>：最大1100mm侧门开度，支持1×1.2m托盘',
    ]:
        story.append(bullet(b))

    story.append(sp(0.3))

    # 功能版说明
    story.append(h2("VAN功能版（乘用版）"))
    story.append(TS2([
        ['V7E功能版', '5/6/7/9座可选，后排座椅可等比例放倒/全平放倒，拉人载货两用'],
        ['V8E功能版', '6/7/9座可选，后排座椅可翻折收起，布局随心变'],
    ], [3*cm, 13*cm]))

    # ========== 六、选装包 ==========
    story.append(h1("六、VAN系列选装包汇总"))
    story.append(TS2([
        ['选装包', 'V6E', 'V7E', 'V8E', '说明'],
        ['补能包', '—', '✅', '✅', '6.6kW慢充 + V2L对外放电'],
        ['科技降险运维包', '—', '✅', '✅', 'DVR + DMS + 流量包 + 双向实时通话'],
        ['智享包2', '—', '—', '✅', '大屏线束 + 高清倒车摄像头 + 电调后视镜'],
        ['尊享包', '—', '✅', '—', '铝合金花纹地板 + 货厢顶棚 + 隔断观察窗'],
        ['集成ADAS', '✅', '—', '—', 'LDW+FCW+AEB+DMS+ESC+胎压（V6E明盲窗标配）'],
    ], [3.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 8*cm]))

    # ========== 七、对比表 ==========
    story.append(h1("七、产品快速对比表"))

    story.append(h2("轻卡对比"))
    story.append(TS2([
        ['车型', '驾驶室宽度', '轴距', '电池容量', '续航', '快充', '峰值功率'],
        ['星智H', '窄/宽', '3360/4495', '60-140kWh', '200-400km', '2C/20min', '81-155kW'],
        ['星智T', '2120mm', '3360/3600', '120-154kWh', '300-400km+', '18min', '235kW'],
    ], [2.2*cm, 2.2*cm, 2*cm, 2.2*cm, 2*cm, 1.8*cm, 1.8*cm]))

    story.append(sp(0.2))
    story.append(h2("VAN对比"))
    story.append(TS2([
        ['车型', '货厢容积', '续航', '载质量', '快充', '电池质保', '座位'],
        ['V6E功能版', '6m³', '300-325km', '—', '35min', '8年/40万', '6座'],
        ['V6E明盲窗', '6m³', '350-355km', '—', '36min', '10年/80万', '6座'],
        ['V7E', '7.5m³', '365-375km', '1.5吨', '15min', '10年/80万', '2座'],
        ['V8E', '8.5m³', '460km', '1.61吨', '15min', '10年/80万', '2座'],
    ], [2.5*cm, 2*cm, 2*cm, 1.6*cm, 1.4*cm, 2*cm, 1.2*cm]))

    story.append(sp(0.2))
    story.append(h2("微卡/中卡对比"))
    story.append(TS2([
        ['车型', '货厢容积', '续航', '载质量', '快充', '电池质保'],
        ['F1E微卡', '7.7-9.7m³', '305km', '955-1600kg', '30min', '10年/80万'],
        ['F3E中卡', '—', '300-400km', '1.5t/3t', '支持', '10年/80万'],
    ], [2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm]))

    # ========== 八、话术 ==========
    story.append(h1("八、核心卖点话术"))
    story.append(TS2([
        ['系列', '话术'],
        ['轻卡-星智T', '硬核承载·极致续航\n峰值功率235kW，16000N·m轮端扭矩\n2C超充15分钟补能200km，三电10年/80万质保'],
        ['轻卡-星智H', '智芯三电·能耗最优\n电机效率97.86%，百公里32kWh\nEPB躺平休息，气刹下坡更安全'],
        ['VAN-V8E', '8方载重标杆\n8.5m³ + 1.61吨载重，同级最强\n2C超充15分钟，460km超长续航'],
        ['VAN-V7E', '7方全能选手\n7.5m³ + 1.5吨载重，15分钟补能200km\nOneBox制动28米刹停，乘用化座舱'],
        ['VAN-V6E', '6方性价比之选\n同级最大空间，270度尾门\n10年/80万质保，超长陪伴'],
        ['微卡-F1E', '真能载·真能跑·真能赚\n9.7m³大方量，1.84吨载质量\n30分钟快充，220V外放电'],
    ], [2.8*cm, 13.2*cm]))

    # ========== 九、需求推荐 ==========
    story.append(h1("九、客户需求推荐"))
    story.append(TS2([
        ['客户需求', '推荐车型', '理由'],
        ['城市快递/配送', 'F1E / V6E', '灵活通过，载货量足'],
        ['商超/仓储配送', 'V7E / 星智H', '7方空间+续航平衡'],
        ['长途货运', '星智T', '235kW+超充，无里程焦虑'],
        ['冷链运输', '星智T冷藏', '-29℃制冷，20分钟速冷'],
        ['重载建材', 'F3E / 星智T', '中卡承载，160mm大梁'],
        ['多人通勤+货运', 'V7E/V8E功能版', '座椅可翻折，拉人载货两用'],
    ], [3.5*cm, 4*cm, 8.5*cm]))

    # ========== 十、质保 ==========
    story.append(h1("十、质保与服务体系"))
    story.append(TS2([
        ['服务项目', '内容'],
        ['三电质保', '最高10年/80万公里（玄武电池）'],
        ['底盘免维护', '5年/30万km'],
        ['B端专属服务', '0息金融、长周期、管家服务、备用车、停运补偿'],
        ['金融方案', '可租可售可回购，多样化金融产品'],
    ], [3.5*cm, 12.5*cm]))

    story.append(sp(0.8))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GRAY_TEXT))
    story.append(Paragraph(
        '📌 声明：具体配置以实车为准。远程新能源商用车保留对所有参数和配置修改的权力，如有变更，恕不另行通知。',
        s['note']
    ))

    doc.build(story, onFirstPage=page_num, onLaterPages=page_num)
    print(f"PDF生成成功: {out}")
    return out

if __name__ == '__main__':
    build_pdf()
