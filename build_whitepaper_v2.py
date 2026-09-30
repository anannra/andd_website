#!/usr/bin/env python3
"""
ANDD Whitepaper v2 — Monochromatic, two-column, mesh network imagery.
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

BASE_DIR = Path("/home/anoop/git/anannra/andd_website")
IMG_DIR = BASE_DIR / "images" / "v2"

# ── Monochromatic palette ──
# Near-black through silver-white, single accent
NEAR_BLACK   = RGBColor(0x0C, 0x0C, 0x14)
CHARCOAL     = RGBColor(0x1A, 0x1A, 0x2E)
DARK_GRAY    = RGBColor(0x2A, 0x2A, 0x3C)
MID_GRAY     = RGBColor(0x5A, 0x5A, 0x6E)
SILVER       = RGBColor(0x9A, 0x9A, 0xAA)
LIGHT_GRAY   = RGBColor(0xD0, 0xD0, 0xD8)
OFF_WHITE    = RGBColor(0xF2, 0xF2, 0xF5)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)

# Single accent — muted steel blue
ACCENT       = RGBColor(0x6B, 0x8A, 0xA6)
ACCENT_LIGHT = RGBColor(0x8A, 0xA8, 0xC4)

# Hex versions for XML
H_CHARCOAL   = "1A1A2E"
H_DARK_GRAY  = "2A2A3C"
H_ACCENT     = "6B8AA6"
H_LIGHT_BG   = "F2F2F5"
H_MID_BG     = "E8E8EE"
H_WHITE      = "FFFFFF"

# Image assignments (map roles to downloaded files)
IMG = {
    "cover":       IMG_DIR / "mesh1.jpg",    # earth network
    "servers":     IMG_DIR / "mesh2.jpg",    # server room
    "abstract":    IMG_DIR / "mesh3.jpg",    # abstract mesh
    "blockchain":  IMG_DIR / "mesh4.jpg",    # blockchain viz
    "circuit":     IMG_DIR / "mesh5.jpg",    # circuit board
    "cyber":       IMG_DIR / "mesh6.jpg",    # cyber security
    "code":        IMG_DIR / "mesh7.jpg",    # matrix
    "ai_brain":    IMG_DIR / "mesh9.jpg",    # AI brain
    "cables":      IMG_DIR / "mesh10.jpg",   # network cables
    "telecom":     IMG_DIR / "mesh11.jpg",   # 5G tower
    "city":        IMG_DIR / "mesh12.jpg",   # night city
    "dark_server": IMG_DIR / "mesh14.jpg",   # dark server
    "network":     IMG_DIR / "mesh16.jpg",   # network abstract
    "dark_abs":    IMG_DIR / "mesh17.jpg",   # dark abstract
}


# Column width constant (8.5" page - 0.7" L margin - 0.7" R margin = 7.1" text area)
# Two columns with 0.25" gutter: (7.1 - 0.25) / 2 = 3.425"
# Use 3.3" to leave breathing room
COL_MAX_WIDTH = Inches(3.3)
COL_MAX_TWIPS = 4752  # 3.3" in twips


def constrain_table_width(tbl, max_width_twips=COL_MAX_TWIPS):
    """Force a table to fit within the column width."""
    tblPr = tbl._tbl.tblPr
    if tblPr is None:
        tblPr = tbl._tbl.get_or_add_tblPr()
    # Set preferred width to 100% (of column)
    tblW = parse_xml(
        f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>'
    )
    # Remove existing tblW
    for existing in tblPr.findall(qn('w:tblW')):
        tblPr.remove(existing)
    tblPr.append(tblW)

    # Set layout to fixed (prevents auto-expand)
    tblLayout = parse_xml(
        f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'
    )
    for existing in tblPr.findall(qn('w:tblLayout')):
        tblPr.remove(existing)
    tblPr.append(tblLayout)

    # Distribute column widths evenly
    n_cols = len(tbl.columns)
    col_w = max_width_twips // n_cols
    tblGrid = tbl._tbl.tblGrid
    for gridCol in tblGrid.findall(qn('w:gridCol')):
        gridCol.set(qn('w:w'), str(col_w))

    # Also set each cell width explicitly
    for row in tbl.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = parse_xml(
                f'<w:tcW {nsdecls("w")} w:w="{col_w}" w:type="dxa"/>'
            )
            for existing in tcPr.findall(qn('w:tcW')):
                tcPr.remove(existing)
            tcPr.append(tcW)


# ── Utility functions ──

def shd(cell, color_hex):
    """Set cell background."""
    cell._tc.get_or_add_tcPr().append(
        parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    )

def cell_margins(cell, top=20, left=50, bottom=20, right=50):
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    ))

def no_borders(cell):
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))

def thin_bottom_border(cell, color=H_ACCENT):
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))

def set_row_height(row, height_twips):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trPr.append(parse_xml(
        f'<w:trHeight {nsdecls("w")} w:val="{height_twips}" w:hRule="atLeast"/>'
    ))


def run_styled(paragraph, text, size=10, color=None, bold=False, italic=False, font="Calibri Light"):
    r = paragraph.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.color.rgb = color or CHARCOAL
    r.bold = bold
    r.italic = italic
    return r


def add_img(paragraph, path, width=Inches(2.9)):
    r = paragraph.add_run()
    try:
        r.add_picture(str(path), width=width)
    except:
        r.add_text(f"[{path.stem}]")


# ── Two-column section helper ──

def start_two_col_section(doc):
    """Add a continuous section break and set 2 columns."""
    new_section = doc.add_section()
    new_section.start_type = 1  # continuous
    new_section.left_margin = Inches(0.7)
    new_section.right_margin = Inches(0.7)
    new_section.top_margin = Inches(0.6)
    new_section.bottom_margin = Inches(0.6)
    # Set 2 columns with spacing
    sectPr = new_section._sectPr
    cols = parse_xml(
        f'<w:cols {nsdecls("w")} w:num="2" w:space="360" w:equalWidth="1"/>'
    )
    # Remove existing cols if any
    for existing in sectPr.findall(qn('w:cols')):
        sectPr.remove(existing)
    sectPr.append(cols)
    return new_section


def start_one_col_section(doc):
    """Return to single column with continuous break."""
    new_section = doc.add_section()
    new_section.start_type = 1
    new_section.left_margin = Inches(0.7)
    new_section.right_margin = Inches(0.7)
    new_section.top_margin = Inches(0.6)
    new_section.bottom_margin = Inches(0.6)
    sectPr = new_section._sectPr
    cols = parse_xml(
        f'<w:cols {nsdecls("w")} w:num="1" w:space="720"/>'
    )
    for existing in sectPr.findall(qn('w:cols')):
        sectPr.remove(existing)
    sectPr.append(cols)
    return new_section


# ── Styled elements ──

def heading1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run_styled(p, text, size=14, color=CHARCOAL, bold=True, font="Calibri")
    # Thin accent underline
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False
    constrain_table_width(tbl)
    c = tbl.cell(0, 0)
    c.text = ""
    shd(c, H_ACCENT)
    no_borders(c)
    row = tbl.rows[0]
    row._tr.get_or_add_trPr().append(
        parse_xml(f'<w:trHeight {nsdecls("w")} w:val="20" w:hRule="exact"/>')
    )
    return p


def heading2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run_styled(p, text, size=10, color=DARK_GRAY, bold=True, font="Calibri")
    return p


def heading3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run_styled(p, text, size=8.5, color=ACCENT, bold=True, font="Calibri")
    return p


def body(doc, text, size=8, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.15
    run_styled(p, text, size=size, color=color or MID_GRAY, font="Calibri Light")
    return p


def body_bold(doc, text, size=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.15
    run_styled(p, text, size=size, color=CHARCOAL, bold=True, font="Calibri")
    return p


def bullet(doc, prefix, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.1)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.1
    run_styled(p, "\u2022 ", size=7, color=ACCENT, font="Calibri")
    if prefix:
        run_styled(p, prefix + " ", size=7, color=CHARCOAL, bold=True, font="Calibri")
    run_styled(p, text, size=7, color=MID_GRAY, font="Calibri Light")
    return p


def callout(doc, title, text):
    """Monochrome callout box with left accent bar — compact, column-constrained."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False
    constrain_table_width(tbl)
    c = tbl.cell(0, 0)
    shd(c, H_LIGHT_BG)
    cell_margins(c, 50, 100, 50, 100)
    c._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="{H_ACCENT}"/>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))
    pt = c.paragraphs[0]
    pt.paragraph_format.space_after = Pt(2)
    run_styled(pt, title, size=8, color=CHARCOAL, bold=True, font="Calibri")
    pb = c.add_paragraph()
    pb.paragraph_format.space_before = Pt(0)
    pb.paragraph_format.line_spacing = 1.1
    run_styled(pb, text, size=7.5, color=MID_GRAY, font="Calibri Light")


def stat_bar(doc, stats):
    """Dark stat bar — monochrome, compact, column-constrained."""
    n = len(stats)
    tbl = doc.add_table(rows=2, cols=n)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    constrain_table_width(tbl)
    for i, (num, label) in enumerate(stats):
        c1 = tbl.cell(0, i)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        shd(c1, H_CHARCOAL)
        cell_margins(c1, 40, 20, 8, 20)
        no_borders(c1)
        run_styled(p1, num, size=14, color=WHITE, bold=True, font="Calibri")

        c2 = tbl.cell(1, i)
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        shd(c2, H_CHARCOAL)
        cell_margins(c2, 8, 20, 40, 20)
        no_borders(c2)
        run_styled(p2, label, size=6.5, color=SILVER, font="Calibri Light")


def data_table(doc, headers, rows):
    """Monochrome styled data table — compact, column-constrained."""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.autofit = False
    constrain_table_width(tbl)

    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = ""
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        shd(c, H_CHARCOAL)
        cell_margins(c, 25, 40, 25, 40)
        run_styled(p, h, size=6.5, color=WHITE, bold=True, font="Calibri")
        c._tc.get_or_add_tcPr().append(parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'<w:bottom w:val="single" w:sz="2" w:space="0" w:color="{H_ACCENT}"/>'
            f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'</w:tcBorders>'
        ))

    for i, row_data in enumerate(rows):
        for j, val in enumerate(row_data):
            c = tbl.cell(i + 1, j)
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            bg = H_LIGHT_BG if i % 2 == 0 else H_WHITE
            shd(c, bg)
            cell_margins(c, 18, 40, 18, 40)
            run_styled(p, str(val), size=6.5, color=MID_GRAY, font="Calibri Light")
            c._tc.get_or_add_tcPr().append(parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:bottom w:val="single" w:sz="1" w:space="0" w:color="E8E8EE"/>'
                f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'</w:tcBorders>'
            ))

    return tbl


def photo(doc, img_path, caption="", width=Inches(2.9)):
    """Insert photo with optional caption — compact."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run()
    try:
        r.add_picture(str(img_path), width=width)
    except:
        r.add_text(f"[{img_path.stem}]")
    if caption:
        pc = doc.add_paragraph()
        pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pc.paragraph_format.space_after = Pt(5)
        run_styled(pc, caption, size=6.5, color=SILVER, italic=True, font="Calibri Light")


def col_break(doc):
    """Insert a column break."""
    p = doc.add_paragraph()
    r = p.add_run()
    br = parse_xml(f'<w:br {nsdecls("w")} w:type="column"/>')
    r._r.append(br)


# ================================================================
# BUILD DOCUMENT
# ================================================================

def build():
    doc = Document()

    # ── Default styles ──
    style = doc.styles["Normal"]
    style.font.name = "Calibri Light"
    style.font.size = Pt(9.5)
    style.font.color.rgb = MID_GRAY
    style.paragraph_format.space_after = Pt(4)

    # ── Page setup (first section — cover) ──
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.left_margin = Inches(0.7)
    sec.right_margin = Inches(0.7)
    sec.top_margin = Inches(0.5)
    sec.bottom_margin = Inches(0.5)

    # ==============================================================
    # COVER PAGE — full bleed dark, mesh imagery
    # ==============================================================
    # Dark full-width cover table
    cover = doc.add_table(rows=1, cols=1)
    cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    cc = cover.cell(0, 0)
    shd(cc, "0C0C14")
    cell_margins(cc, 200, 200, 200, 200)
    no_borders(cc)

    # Cover image
    pi = cc.paragraphs[0]
    pi.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ri = pi.add_run()
    try:
        ri.add_picture(str(IMG["cover"]), width=Inches(6.5))
    except:
        pass

    # Spacer
    cc.add_paragraph()

    # Title
    pt = cc.add_paragraph()
    pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pt, "ANDD", size=48, color=WHITE, bold=True, font="Calibri")

    ps = cc.add_paragraph()
    ps.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(ps, "AI NATIVE DISTRIBUTED DATACENTERS", size=16, color=ACCENT_LIGHT, font="Calibri")

    pst = cc.add_paragraph()
    pst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pst, "A Technical Architecture for Sovereign, Resilient,\nAI-Managed Edge Infrastructure", size=11, color=SILVER, font="Calibri Light")

    # Spacer
    cc.add_paragraph()

    pv = cc.add_paragraph()
    pv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pv, "Whitepaper v2.0  \u2022  March 2026", size=9, color=MID_GRAY, font="Calibri Light")

    pc = cc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pc, "contact@andd.network  \u2022  andd.network", size=9, color=ACCENT, font="Calibri Light")

    doc.add_page_break()

    # ==============================================================
    # TABLE OF CONTENTS — single column
    # ==============================================================
    heading1(doc, "Table of Contents")

    toc_items = [
        ("01", "Executive Summary"),
        ("02", "The Case for Decentralization"),
        ("03", "ANDD Architecture Overview"),
        ("04", "Technical Architecture"),
        ("05", "Bandwidth & Connectivity"),
        ("06", "Energy & Mitigation Strategies"),
        ("07", "AI-Native Operations"),
        ("08", "Resilience Through Decentralization"),
        ("09", "Payment Architecture"),
        ("10", "DePIN Integration & Pressure Test"),
        ("11", "Opportunity Zone Alignment"),
        ("12", "Implementation Roadmap"),
        ("13", "Conclusion"),
    ]
    for num, title in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(0.35))
        run_styled(p, num, size=9, color=ACCENT, bold=True, font="Calibri")
        run_styled(p, f"\t{title}", size=9, color=CHARCOAL, font="Calibri Light")

    doc.add_page_break()

    # ==============================================================
    # BODY — TWO COLUMNS
    # ==============================================================
    start_two_col_section(doc)

    # ── 1. EXECUTIVE SUMMARY ──
    heading1(doc, "01  Executive Summary")

    body(doc, "The global compute infrastructure serving AI, critical services, and digital economies is dangerously concentrated. Fewer than 30 hyperscale campuses process the vast majority of U.S. AI inference, financial transactions, government data, and emergency communications.")

    body(doc, "This concentration creates single points of failure for national security, economic continuity, and community resilience \u2014 and leaves underserved regions permanently behind.")

    callout(doc,
        "The ANDD Model",
        "A network of hundreds to thousands of sub-2MW edge datacenters, deployed across Opportunity Zones, forming an interconnected mesh fabric entirely managed by AI. Autonomous onboarding, billing, provisioning, and maintenance \u2014 no human operators required for standard operations."
    )

    doc.add_paragraph()
    stat_bar(doc, [("<2MW", "Per Site"), ("100s+", "Locations"), ("4", "HW Domains"), ("99.99%", "SLA Target")])
    doc.add_paragraph()

    photo(doc, IMG["servers"], "Enterprise-grade edge infrastructure", width=Inches(2.9))

    body(doc, "This whitepaper details the four hardware domains, bandwidth and energy profiles, AI-native operations model, payment architecture spanning fiat to crypto micro-transactions, and a rigorous pressure test against existing DePIN projects.")

    # ── 2. THE CASE FOR DECENTRALIZATION ──
    heading1(doc, "02  The Case for Decentralization")

    heading2(doc, "The Concentration Problem")

    body(doc, "Northern Virginia hosts over 70% of East Coast internet traffic. The top five metro markets account for the majority of U.S. datacenter capacity. This creates compounding vulnerabilities:")

    bullet(doc, "National Security.", "A coordinated attack on fewer than a dozen campuses could degrade federal agencies, financial markets, and defense communications simultaneously.")
    bullet(doc, "Latency Inequality.", "Communities >50ms from hyperscale regions cannot access real-time AI, telemedicine, or autonomous vehicle coordination.")
    bullet(doc, "Sovereignty Erosion.", "Government data depends on three to four hyperscale vendors' operational decisions and pricing.")
    bullet(doc, "Grid Strain.", "A single 300MW campus demands the output of a small power plant, straining regional grids.")

    photo(doc, IMG["city"], "Concentrated infrastructure leaves most communities behind", width=Inches(2.9))

    heading2(doc, "Why Now")

    bullet(doc, "AI Inference at the Edge.", "60\u201370% of all AI compute is inference \u2014 latency-sensitive, geographically distributed, ideal for edge.")
    bullet(doc, "DePIN Needs Upgrading.", "Consumer hardware hits reliability ceilings. Enterprise customers need 99.99% uptime and compliance.")
    bullet(doc, "Federal Policy Tailwind.", "Opportunity Zones (8,764 tracts), bipartisan AI infrastructure support, rural broadband funding.")

    heading2(doc, "The AI-Native Unlock")

    body(doc, "Previous distributed datacenter attempts failed on economics \u2014 sub-2MW sites can\u2019t justify full operations teams. ANDD inverts this: AI handles onboarding, provisioning, billing, monitoring, and maintenance. The marginal cost of a new site approaches hardware cost alone.")

    # ── 3. ARCHITECTURE OVERVIEW ──
    heading1(doc, "03  Architecture Overview")

    photo(doc, IMG["network"], "Interconnected mesh fabric \u2014 no single point of failure", width=Inches(2.9))

    heading2(doc, "Three-Tier Mesh Fabric")

    data_table(doc,
        ["Tier", "Component", "Power", "Role"],
        [
            ["3", "AI Control Plane", "Distributed", "Global routing, billing, capacity planning"],
            ["2", "Regional Hubs", "1\u20132MW", "Aggregation, peering, training GPUs"],
            ["1", "Edge Nodes", "200kW\u2013500kW", "Local compute, inference, storage"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Connectivity Per Node")

    data_table(doc,
        ["Link Type", "Medium", "Bandwidth"],
        [
            ["Primary uplink", "Fiber / microwave", "10+ Gbps"],
            ["Redundant uplink", "Diverse fiber / 5G / LEO sat", "1\u201310 Gbps"],
            ["Mesh peering", "Direct node-to-node", "10 Gbps"],
            ["2nd hub path", "Via mesh or direct", "Variable"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Site Layout")

    data_table(doc,
        ["System", "Components", "Spec"],
        [
            ["IT", "Compute (x4\u20138) + AI (x2\u20134) + Storage (x2\u20134)", "Configurable mix"],
            ["Network", "Leaf-spine + edge router", "100/400GbE + BGP"],
            ["Power", "Utility + ATS + UPS + solar/BESS", "Microgrid capable"],
            ["Cooling", "DLC + immersion + air economizer", "PUE 1.15\u20131.25"],
        ]
    )

    # ── 4. TECHNICAL ARCHITECTURE ──
    heading1(doc, "04  Technical Architecture")

    heading2(doc, "AI Accelerators")

    photo(doc, IMG["circuit"], "Purpose-built silicon for edge inference", width=Inches(2.9))

    data_table(doc,
        ["Accelerator", "TDP", "Memory", "Tier"],
        [
            ["NVIDIA L4", "72W", "24GB", "Edge (efficient)"],
            ["NVIDIA L40S", "300W", "48GB", "Edge (inference)"],
            ["AMD MI300X", "750W", "192GB HBM3", "Edge / Hub"],
            ["AMD MI325X", "750W", "256GB HBM3e", "Edge / Hub"],
            ["Intel Gaudi 3", "~600W", "128GB HBM2e", "Edge (cost)"],
            ["NVIDIA H100", "700W", "80GB HBM3", "Hub (train)"],
            ["NVIDIA H200", "700W", "141GB HBM3e", "Hub (large)"],
            ["NVIDIA B200", "1,000W", "192GB HBM3e", "Hub (train)"],
            ["GB200 NVL2", "2,700W", "384GB HBM3e", "Hub (liquid)"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Edge AI Feasibility")

    data_table(doc,
        ["Workload", "Hardware", "Power", "Latency"],
        [
            ["LLM 7\u201313B", "1x L40S", "300W", "20\u2013100ms/tok"],
            ["LLM 70B", "2\u20134x H100", "700W\u20131.4kW", "50\u2013200ms/tok"],
            ["Image/video", "1x L4", "72W", "5\u201320ms"],
            ["Speech", "1x L4", "72W", "<100ms"],
            ["RAG pipeline", "1\u20132x H100", "1\u20132kW", "100\u2013500ms"],
            ["Fraud detection", "1x L40S", "300W", "<50ms"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Software Stack")

    data_table(doc,
        ["Layer", "Components"],
        [
            ["AI Management", "Onboarding, Provisioning, Billing, SLA agents"],
            ["Orchestration", "K3s/RKE2, Istio mesh, AI scheduler"],
            ["Infrastructure", "SDN (OVS/VPP), Ceph/MinIO, AI-controlled DCIM"],
            ["Hardware", "BMC/Redfish, GPU drivers, SONiC/Cumulus"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Security")
    bullet(doc, "Zero-trust:", "mTLS on all workload-to-workload communication")
    bullet(doc, "Hardware root of trust:", "TPM 2.0, measured boot, remote attestation")
    bullet(doc, "Tenant isolation:", "SR-IOV, SEV-SNP/TDX confidential compute")
    bullet(doc, "Physical:", "Biometric access, AI surveillance, SCIF options")
    bullet(doc, "Compliance:", "FedRAMP, SOC 2, HIPAA, CJIS, ITAR")

    # ── 5. BANDWIDTH ──
    heading1(doc, "05  Bandwidth & Connectivity")

    data_table(doc,
        ["Tier", "Primary", "Redundant", "Mesh", "Total"],
        [
            ["Edge 200kW", "10G", "1\u201310G", "10G", "20\u201330G"],
            ["Edge 500kW", "40G", "10G", "25G", "50\u201375G"],
            ["Hub 1\u20132MW", "100G", "40G", "100G", "200\u2013300G"],
        ]
    )

    doc.add_paragraph()
    photo(doc, IMG["cables"], "Redundant, multi-path connectivity", width=Inches(2.9))

    heading3(doc, "Backhaul by Geography")
    data_table(doc,
        ["Type", "Primary", "Backup"],
        [
            ["Urban", "Multi-carrier fiber 10\u201340G", "5G/LTE 1\u20135G"],
            ["Suburban", "Fiber 10\u201340G", "Diverse fiber 10G"],
            ["Rural", "Licensed wireless / LEO sat 1\u201310G", "5G/LTE"],
        ]
    )

    doc.add_paragraph()
    heading3(doc, "Protocol Stack")
    bullet(doc, "Underlay:", "eBPF + SRv6 segment routing")
    bullet(doc, "Overlay:", "WireGuard/MACsec + VXLAN/GENEVE")
    bullet(doc, "Peering:", "Automated BGP with RPKI")
    bullet(doc, "DNS:", "Anycast across all nodes")
    bullet(doc, "GSLB:", "AI-driven, latency/cost/carbon aware")

    # ── 6. ENERGY ──
    heading1(doc, "06  Energy & Mitigation")

    data_table(doc,
        ["Tier", "IT", "Cooling", "Infra", "Total", "PUE"],
        [
            ["Edge 200kW", "150kW", "25kW", "25kW", "200kW", "1.15\u20131.25"],
            ["Edge 500kW", "380kW", "65kW", "55kW", "500kW", "1.15\u20131.25"],
            ["Hub 2MW", "1,500kW", "280kW", "220kW", "2MW", "1.15\u20131.25"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Cooling Comparison")

    data_table(doc,
        ["Technology", "Cooling kW", "IT Capacity", "PUE"],
        [
            ["Air (DX)", "150\u2013200kW", "300\u2013350kW", "1.40\u20131.80"],
            ["Rear-door HX", "75\u2013125kW", "375\u2013425kW", "1.20\u20131.40"],
            ["Direct liquid", "40\u201375kW", "425\u2013460kW", "1.10\u20131.20"],
            ["Immersion (1\u03c6)", "15\u201330kW", "470\u2013485kW", "1.02\u20131.06"],
            ["Immersion (2\u03c6)", "10\u201320kW", "480\u2013490kW", "1.01\u20131.04"],
        ]
    )

    doc.add_paragraph()
    callout(doc, "30% More Compute, Same Power",
        "Moving from air cooling to immersion saves ~300kW per MW \u2014 increasing usable compute by 30% within the same power envelope.")

    heading2(doc, "Renewable Economics")

    data_table(doc,
        ["Component", "Spec", "Cost", "Value"],
        [
            ["Solar", "100kW carport", "~$150K", "175 MWh/yr"],
            ["BESS (LFP)", "500kWh/250kW", "~$200K", "2hr backup + cycling"],
            ["IRA ITC", "30\u201350%", "\u2013$105K\u2013$175K", "Capital reduction"],
            ["Grid services", "Freq. reg + DR", "\u2014", "$50\u2013200K/yr/MW"],
        ]
    )

    doc.add_paragraph()
    body_bold(doc, "Effective payback: 2\u20134 years after incentives.")

    heading2(doc, "Federal Funding")
    data_table(doc,
        ["Program", "Amount", "Use"],
        [
            ["DOE GRIP", "$10.5B", "Microgrids, DER"],
            ["DOE LPO", "$400B+", "Clean energy lending"],
            ["ARPA-E COOLERCHIPS", "$42M", "DC cooling R&D"],
            ["IRA ITC", "30\u201350%", "Solar, BESS, fuel cells"],
            ["NTIA BEAD", "$42.45B", "Broadband + edge"],
        ]
    )

    # ── 7. AI-NATIVE OPERATIONS ──
    heading1(doc, "07  AI-Native Operations")

    photo(doc, IMG["ai_brain"], "AI agents manage the entire datacenter lifecycle", width=Inches(2.9))

    body(doc, "Traditional operations require full-time staff per site, establishing a ~5MW minimum viable size. ANDD eliminates this with autonomous AI agents:")

    data_table(doc,
        ["Agent", "Function"],
        [
            ["Orchestration", "Coordinates sub-agents, escalates exceptions"],
            ["Onboarding", "Lead qualification, proposals, KYC, provisioning"],
            ["Provisioning", "Workload mapping, node placement, auto-scaling"],
            ["Billing", "Sub-second metering, invoicing, fiat+crypto reconciliation"],
            ["Maintenance", "Sensor telemetry, digital twins, preventive scheduling"],
            ["SLA Guardian", "Threshold monitoring, auto-remediation, credit issuance"],
        ]
    )

    doc.add_paragraph()
    callout(doc, "1 Human per 20\u201350 Nodes",
        "A 10\u201325x improvement over traditional staffing. Humans handle exceptions, strategy, physical maintenance, and compliance oversight.")

    heading3(doc, "Self-Hosting Architecture")
    bullet(doc, "", "Foundation LLM runs on ANDD\u2019s own GPUs \u2014 no external API dependency")
    bullet(doc, "", "Specialized models for maintenance, networking, billing")
    bullet(doc, "", "Staged rollout: shadow \u2192 canary \u2192 full, with auto-rollback")
    bullet(doc, "", "Full reasoning chain logging for auditability")

    # ── 8. RESILIENCE ──
    heading1(doc, "08  Resilience Through Decentralization")

    photo(doc, IMG["cyber"], "Distributed architecture eliminates single points of failure", width=Inches(2.9))

    heading3(doc, "Payments")
    body(doc, "Distributed card authorization, ACH, FedNow gateways across hundreds of nodes. Local store-and-forward during backbone disruptions. Crypto rails as backup settlement layer.")

    heading3(doc, "Energy Grid")
    body(doc, "Distributed SCADA/EMS hosting. Edge compute for DER control loops (<10ms). Virtual power plant from distributed BESS. Microgrid islanding during emergencies.")

    heading3(doc, "Emergency Services")
    body(doc, "Local NG911 hosting. FirstNet edge compute. Emergency operations center computing. LEO satellite backhaul when terrestrial networks fail.")

    heading3(doc, "Utilities & Water")
    body(doc, "Local SCADA for water/wastewater/gas. Semi-air-gapped operation. AI anomaly detection for contamination and cyber intrusion.")

    heading2(doc, "Quantified Advantage")
    data_table(doc,
        ["Architecture", "Per-Unit Uptime", "System Availability"],
        [
            ["Single hyperscale", "99.99%", "99.99% (67 min/yr down)"],
            ["ANDD mesh (100 nodes)", "99.95% per node", "99.9999%+ (graceful degradation)"],
        ]
    )

    # ── 9. PAYMENTS ──
    heading1(doc, "09  Payment Architecture")

    heading2(doc, "Fiat Tiers")
    data_table(doc,
        ["Tier", "Model", "Methods", "Use Case"],
        [
            ["Starter", "Monthly", "Card, ACH", "Startups"],
            ["Professional", "Monthly/Annual", "ACH, wire", "Mid-market"],
            ["Enterprise", "Annual", "Wire, PO", "Large enterprise"],
            ["Government", "Multi-year", "Treasury/PO", "Federal/state/local"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Crypto & Micro-Transactions")

    data_table(doc,
        ["Rail", "Use Case", "Finality", "Cost/Tx"],
        [
            ["Ethereum L1", "Enterprise contracts", "~12 min", "$1\u2013$20"],
            ["Solana", "High-frequency", "Sub-second", "~$0.001"],
            ["L2 (Arbitrum/Base)", "Medium-frequency", "Minutes", "$0.01\u20130.10"],
            ["Payment channels", "Micro-transactions", "Instant", "Near-zero"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Smart Contract SLAs")
    body(doc, "Programmable SLAs encode uptime targets, latency floors, and measurement periods. Oracle-fed performance data triggers automatic stablecoin credit issuance on breach \u2014 no human claims process.")

    heading2(doc, "Hybrid Orchestration")
    data_table(doc,
        ["Customer", "Primary", "Secondary", "Micro-Tx"],
        [
            ["Enterprise", "Wire/ACH", "Card", "N/A"],
            ["Government", "PO/Treasury", "ACH", "N/A"],
            ["Startup", "Card", "USDC", "Per-API"],
            ["DePIN", "Stablecoin", "Payment channel", "Per-request"],
            ["Web3", "USDC/token", "Payment channel", "Per-request"],
        ]
    )

    # ── 10. DePIN PRESSURE TEST ──
    heading1(doc, "10  DePIN Pressure Test")

    photo(doc, IMG["blockchain"], "Enterprise-grade backbone for decentralized protocols", width=Inches(2.9))

    heading2(doc, "Lessons from DePIN Projects")

    data_table(doc,
        ["Project", "Success", "Failure", "ANDD Fix"],
        [
            ["Helium", "900K+ hotspots", "No SLA, wrong locations", "AI-driven demand placement"],
            ["Filecoin", "22+ EiB capacity", "Empty capacity, slow retrieval", "Utilization-based incentives"],
            ["Render", "Real 3D rendering demand", "Consumer GPUs can\u2019t do AI", "Datacenter-grade GPUs"],
            ["Akash", "70\u201385% cheaper", "No SLA enforcement", "Smart contract SLAs"],
            ["io.net", "GPU clustering for ML", "Heterogeneous, high latency", "Homogeneous co-located HW"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "The Enterprise-Grade Gap")

    data_table(doc,
        ["Dimension", "Consumer DePIN", "ANDD"],
        [
            ["Uptime", "90\u201398%", "99.99% SLA-backed"],
            ["Redundancy", "None", "N+1 power/cooling/network"],
            ["Security", "None", "Biometric, surveillance"],
            ["Compliance", "None", "FedRAMP, SOC 2, HIPAA"],
            ["Power", "Residential", "UPS + BESS + fuel cell"],
            ["Cooling", "Consumer fans", "DLC + immersion"],
            ["Connectivity", "Broadband", "Multi-provider, SLA"],
            ["Sovereignty", "Unknown", "Per-tenant geo-restrictions"],
        ]
    )

    doc.add_paragraph()
    callout(doc, "ANDD Completes DePIN",
        "The tokenomics and demand aggregation work. The physical infrastructure needs upgrading to enterprise grade. ANDD provides that backbone.")

    heading2(doc, "What Can Be Built on ANDD")

    data_table(doc,
        ["Category", "Examples", "Why Edge Required"],
        [
            ["Smart City / IoT", "Traffic, sensors, digital twins", "<10ms control loops"],
            ["Autonomous Vehicles", "V2X, HD maps, inference", "Safety-critical latency"],
            ["Health AI", "Diagnostics, monitoring", "HIPAA + low latency"],
            ["Edge AI / MLOps", "Model serving, RAG, agents", "GPU at the edge"],
            ["DePIN Protocols", "Compute, storage, wireless", "Enterprise backbone"],
            ["Fintech", "Payments, fraud detection", "Compliance + <50ms"],
            ["Content Delivery", "Video, gaming, AR/VR", "Bandwidth offload"],
            ["Defense", "Classified, SIGINT, C2", "Sovereign infrastructure"],
            ["Emergency Services", "NG911, FirstNet, alerts", "Functions during disasters"],
            ["AgTech", "Precision ag, drones", "Rural edge compute"],
        ]
    )

    # ── 11. OPPORTUNITY ZONES ──
    heading1(doc, "11  Opportunity Zone Alignment")

    data_table(doc,
        ["Tier", "Incentive", "Requirement", "Benefit"],
        [
            ["1", "Capital gains deferral", "Invest in QOF", "Defer tax; rolling 5-yr window"],
            ["2", "Basis step-up", "Hold 5+ years", "10% (30% rural)"],
            ["3", "10-year exclusion", "Hold 10+ years", "Zero tax on appreciation"],
        ]
    )

    doc.add_paragraph()
    heading2(doc, "Community Impact (200kW Node)")
    data_table(doc,
        ["Impact", "Estimate"],
        [
            ["Construction jobs", "15\u201330 (6\u201312 month build)"],
            ["Permanent jobs", "1\u20133 technicians"],
            ["Property tax", "$50K\u2013$150K/yr"],
            ["Utility revenue", "$150K\u2013$300K/yr"],
            ["Multiplier", "1.5\u20132.0x direct spending"],
            ["Digital benefit", "Gigabit + AI + edge compute"],
        ]
    )

    # ── 12. ROADMAP ──
    heading1(doc, "12  Implementation Roadmap")

    data_table(doc,
        ["Phase", "Timeline", "Milestones"],
        [
            ["Foundation", "Mo 1\u201312", "AI layer, 200kW design, 3\u20135 pilots, SOC 2, QOF"],
            ["Formation", "Mo 12\u201324", "20\u201350 nodes, hubs, >90% autonomous, FedRAMP"],
            ["Scale", "Mo 24\u201348", "100\u2013300 nodes, smart SLAs, federal customers"],
            ["Continental", "Mo 48\u201372", "500\u20131000+ nodes, full autonomy, VPP"],
        ]
    )

    # ── 13. CONCLUSION ──
    heading1(doc, "13  Conclusion")

    body(doc, "The concentration of compute into hyperscale campuses was an artifact of an era when operational economics demanded scale and AI didn\u2019t exist as an operational tool. That era is ending.")

    body(doc, "ANDD demonstrates that AI-native operations eliminate the economic barrier to distributed deployment. The marginal cost of a new edge node approaches hardware cost alone.")

    callout(doc, "ANDD delivers:",
        "\u2022 Sovereignty \u2014 compute stays where it\u2019s governed\n"
        "\u2022 Security \u2014 no single target degrades the network\n"
        "\u2022 Resilience \u2014 survives what cripples centralized\n"
        "\u2022 Equity \u2014 capabilities reach underserved communities\n"
        "\u2022 DePIN \u2014 enterprise backbone for decentralized protocols\n"
        "\u2022 Viability \u2014 fiat to crypto, subscriptions to micro-tx"
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(p, "The question is how quickly it can be deployed.\nANDD is the answer.", size=11, color=CHARCOAL, bold=True, font="Calibri")

    # ── Back to single column for footer ──
    start_one_col_section(doc)

    # Accent line
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    c.text = ""
    shd(c, H_ACCENT)
    no_borders(c)
    tbl.rows[0]._tr.get_or_add_trPr().append(
        parse_xml(f'<w:trHeight {nsdecls("w")} w:val="20" w:hRule="exact"/>')
    )

    doc.add_paragraph()
    pf = doc.add_paragraph()
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pf, "contact@andd.network  \u2022  andd.network", size=10, color=ACCENT, font="Calibri Light")

    pd = doc.add_paragraph()
    pd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_styled(pd, "This document contains forward-looking statements. Technical specifications represent design targets. Tax information is for informational purposes only.", size=7, color=SILVER, italic=True, font="Calibri Light")

    # ── Save ──
    out = BASE_DIR / "ANDD_Whitepaper_v2.docx"
    doc.save(str(out))
    print(f"Saved: {out}")
    print(f"Size: {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build()
