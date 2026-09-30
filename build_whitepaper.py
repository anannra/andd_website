#!/usr/bin/env python3
"""
Build a modern, styled ANDD Whitepaper .docx with photos and professional formatting.
"""

import os
import io
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import re

BASE_DIR = Path("/home/anoop/git/anannra/andd_website")
IMG_DIR = BASE_DIR / "images"
IMG_DIR.mkdir(exist_ok=True)

# ANDD brand colors
NAVY = RGBColor(0x0A, 0x16, 0x28)
DARK_BLUE = RGBColor(0x11, 0x1D, 0x33)
MED_BLUE = RGBColor(0x1A, 0x3A, 0x5C)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)
LIGHT_BLUE = RGBColor(0x60, 0xA5, 0xFA)
SILVER = RGBColor(0xC0, 0xC0, 0xC0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x2E)
BODY_TEXT = RGBColor(0x33, 0x33, 0x44)
LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8)
TABLE_HEADER_BG = "1A3A5C"
TABLE_ALT_BG = "F0F4F8"
TABLE_BORDER = "3B82F6"

# Unsplash photo URLs (free, no auth needed for direct CDN)
PHOTO_URLS = {
    "cover": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&q=85",  # server room
    "edge_dc": "https://images.unsplash.com/photo-1600267185393-e158a98703de?w=800&q=80",  # data center
    "smart_city": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=800&q=80",  # smart city night
    "emergency": "https://images.unsplash.com/photo-1587738972117-c4e12e857fea?w=800&q=80",  # emergency vehicle
    "solar_energy": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800&q=80",  # solar panels
    "ai_chip": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",  # AI abstract
    "telecom": "https://images.unsplash.com/photo-1562408590-e32931084e23?w=800&q=80",  # 5G tower
    "fintech": "https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?w=800&q=80",  # finance tech
    "healthcare": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80",  # telemedicine
    "blockchain": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&q=80",  # blockchain
    "government": "https://images.unsplash.com/photo-1501466044931-62695aada8e9?w=800&q=80",  # capitol/gov
    "network": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",  # global network
    "cooling": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80",  # server cooling
    "community": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=800&q=80",  # community
    "autonomous": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&q=80",  # robot/AI
    "payments": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80",  # digital payment
}


def download_image(name, url, width=800):
    """Download image from URL, save to IMG_DIR. Return path or None."""
    path = IMG_DIR / f"{name}.jpg"
    if path.exists():
        return path
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "ANDD-Whitepaper-Builder/1.0"})
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content))
        img = img.convert("RGB")
        # Resize to consistent width
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
        img.save(path, "JPEG", quality=85)
        print(f"  Downloaded: {name}")
        return path
    except Exception as e:
        print(f"  Failed to download {name}: {e}")
        return None


def create_gradient_placeholder(name, label, width=800, height=400):
    """Create a gradient placeholder image with label text."""
    path = IMG_DIR / f"{name}.jpg"
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Dark blue gradient
    for y in range(height):
        r = int(0x0A + (0x1A - 0x0A) * y / height)
        g = int(0x16 + (0x3A - 0x16) * y / height)
        b = int(0x28 + (0x5C - 0x28) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add label text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) / 2, (height - th) / 2), label, fill=(0x60, 0xA5, 0xFA), font=font)

    img.save(path, "JPEG", quality=85)
    return path


def get_image(name, fallback_label=""):
    """Get image path — download or create placeholder."""
    if name in PHOTO_URLS:
        path = download_image(name, PHOTO_URLS[name])
        if path:
            return path
    return create_gradient_placeholder(name, fallback_label or name.replace("_", " ").title())


def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_border(cell, **kwargs):
    """Set cell borders."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}></w:tcBorders>')
    for edge, val in kwargs.items():
        element = parse_xml(
            f'<w:{edge} {nsdecls("w")} w:val="{val.get("val", "single")}" '
            f'w:sz="{val.get("sz", "4")}" w:space="0" '
            f'w:color="{val.get("color", TABLE_BORDER)}"/>'
        )
        tcBorders.append(element)
    tcPr.append(tcBorders)


def style_table(table, has_header=True):
    """Apply modern styling to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Style all cells
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            # Padding
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'<w:top w:w="60" w:type="dxa"/>'
                f'<w:left w:w="100" w:type="dxa"/>'
                f'<w:bottom w:w="60" w:type="dxa"/>'
                f'<w:right w:w="100" w:type="dxa"/>'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)

            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(2)
                paragraph.paragraph_format.space_after = Pt(2)
                for run in paragraph.runs:
                    run.font.size = Pt(9)
                    run.font.name = "Calibri"

            if i == 0 and has_header:
                set_cell_shading(cell, TABLE_HEADER_BG)
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = WHITE
                        run.font.bold = True
                        run.font.size = Pt(9)
            elif i % 2 == 0:
                set_cell_shading(cell, TABLE_ALT_BG)


def add_styled_heading(doc, text, level=1):
    """Add a heading with ANDD brand styling."""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Calibri"
        if level == 1:
            run.font.size = Pt(26)
            run.font.color.rgb = MED_BLUE
        elif level == 2:
            run.font.size = Pt(20)
            run.font.color.rgb = MED_BLUE
        elif level == 3:
            run.font.size = Pt(14)
            run.font.color.rgb = ACCENT_BLUE
    return h


def add_body(doc, text, bold=False, italic=False, color=None):
    """Add a body paragraph."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = color or BODY_TEXT
    run.bold = bold
    run.italic = italic
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = Pt(16)
    return p


def add_bullet(doc, text, bold_prefix=""):
    """Add a bullet point with optional bold prefix."""
    p = doc.add_paragraph(style="List Bullet")
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = BODY_TEXT
        run.bold = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = BODY_TEXT
    else:
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(10.5)
            run.font.color.rgb = BODY_TEXT
    p.paragraph_format.space_after = Pt(4)
    return p


def add_photo_row(doc, images_with_captions, img_width=Inches(2.8)):
    """Add a row of photos with captions using a table layout."""
    n = len(images_with_captions)
    table = doc.add_table(rows=2, cols=n)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    for i, (img_path, caption) in enumerate(images_with_captions):
        # Image cell
        cell = table.cell(0, i)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        try:
            run.add_picture(str(img_path), width=img_width)
        except Exception as e:
            run.add_text(f"[Image: {caption}]")

        # Caption cell
        cell2 = table.cell(1, i)
        p2 = cell2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(caption)
        run2.font.name = "Calibri"
        run2.font.size = Pt(9)
        run2.font.color.rgb = MED_BLUE
        run2.italic = True

    # Remove borders
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

    return table


def add_single_photo(doc, img_path, caption="", width=Inches(6.0)):
    """Add a single centered photo with caption."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    try:
        run.add_picture(str(img_path), width=width)
    except:
        run.add_text(f"[Image: {caption}]")
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

    if caption:
        pc = doc.add_paragraph()
        pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_c = pc.add_run(caption)
        run_c.font.name = "Calibri"
        run_c.font.size = Pt(9)
        run_c.font.color.rgb = MED_BLUE
        run_c.italic = True
        pc.paragraph_format.space_after = Pt(12)


def add_accent_line(doc):
    """Add a colored horizontal line as a visual separator."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Use a thin table as a line
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, TABLE_BORDER.replace("#", ""))
    cell.width = Inches(6)
    # Make row very thin
    tr = tbl.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    trHeight = parse_xml(f'<w:trHeight {nsdecls("w")} w:val="40" w:hRule="exact"/>')
    trPr.append(trHeight)
    # Remove text
    cell.text = ""


def add_callout_box(doc, title, text):
    """Add a styled callout/highlight box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, "EFF6FF")

    # Add border
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{TABLE_BORDER}"/>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

    # Padding
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="120" w:type="dxa"/>'
        f'<w:left w:w="200" w:type="dxa"/>'
        f'<w:bottom w:w="120" w:type="dxa"/>'
        f'<w:right w:w="200" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

    p_title = cell.paragraphs[0]
    run_t = p_title.add_run(title)
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(12)
    run_t.font.color.rgb = MED_BLUE
    run_t.bold = True

    p_body = cell.add_paragraph()
    run_b = p_body.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10.5)
    run_b.font.color.rgb = BODY_TEXT


def add_stat_row(doc, stats):
    """Add a row of key statistics in styled boxes."""
    n = len(stats)
    table = doc.add_table(rows=2, cols=n)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, (number, label) in enumerate(stats):
        # Number cell
        cell = table.cell(0, i)
        set_cell_shading(cell, TABLE_HEADER_BG)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(number)
        run.font.name = "Calibri"
        run.font.size = Pt(22)
        run.font.color.rgb = LIGHT_BLUE
        run.bold = True

        # Label cell
        cell2 = table.cell(1, i)
        set_cell_shading(cell2, TABLE_HEADER_BG)
        p2 = cell2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run(label)
        run2.font.name = "Calibri"
        run2.font.size = Pt(9)
        run2.font.color.rgb = SILVER

    # Remove internal borders, keep outer subtle
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="0A1628"/>'
                f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="0A1628"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)
            # Padding
            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'<w:top w:w="100" w:type="dxa"/>'
                f'<w:left w:w="80" w:type="dxa"/>'
                f'<w:bottom w:w="100" w:type="dxa"/>'
                f'<w:right w:w="80" w:type="dxa"/>'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)


def add_table_from_data(doc, headers, rows, col_widths=None):
    """Add a styled table from header list and row data."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.name = "Calibri"
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = WHITE
        set_cell_shading(cell, TABLE_HEADER_BG)

    # Data rows
    for i, row_data in enumerate(rows):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            run.font.color.rgb = BODY_TEXT
            if (i + 1) % 2 == 0:
                set_cell_shading(cell, TABLE_ALT_BG)

    # Apply column widths if specified
    if col_widths:
        for j, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[j].width = w

    style_table(table)
    return table


# ============================================================
# MAIN DOCUMENT BUILDER
# ============================================================

def build_document():
    print("Downloading images...")
    images = {}
    for name, url in PHOTO_URLS.items():
        images[name] = get_image(name, name.replace("_", " ").title())

    print("\nBuilding document...")
    doc = Document()

    # ---- Page setup ----
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)

    # ---- Default font ----
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(11)
    font.color.rgb = BODY_TEXT

    # Heading styles
    for level, size, color in [(1, 26, MED_BLUE), (2, 20, MED_BLUE), (3, 14, ACCENT_BLUE)]:
        hs = doc.styles[f"Heading {level}"]
        hs.font.name = "Calibri"
        hs.font.size = Pt(size)
        hs.font.color.rgb = color
        hs.font.bold = True

    # ======================================
    # COVER PAGE
    # ======================================
    # Add some space before cover
    for _ in range(3):
        doc.add_paragraph()

    # Cover image
    add_single_photo(doc, images["cover"], width=Inches(6.5))

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("AI NATIVE DISTRIBUTED DATACENTERS")
    run.font.name = "Calibri"
    run.font.size = Pt(32)
    run.font.color.rgb = MED_BLUE
    run.bold = True
    p.paragraph_format.space_before = Pt(24)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run("A Technical Architecture for Sovereign, Resilient,\nAI-Managed Edge Infrastructure")
    run2.font.name = "Calibri"
    run2.font.size = Pt(16)
    run2.font.color.rgb = ACCENT_BLUE

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run3 = p3.add_run("ANDD Network  |  Whitepaper v1.0  |  March 2026")
    run3.font.name = "Calibri"
    run3.font.size = Pt(11)
    run3.font.color.rgb = SILVER
    p3.paragraph_format.space_before = Pt(20)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run4 = p4.add_run("contact@andd.network  |  andd.network")
    run4.font.name = "Calibri"
    run4.font.size = Pt(10)
    run4.font.color.rgb = MED_BLUE

    # Page break
    doc.add_page_break()

    # ======================================
    # TABLE OF CONTENTS (styled list)
    # ======================================
    add_styled_heading(doc, "Table of Contents", level=1)

    toc_items = [
        "1. Executive Summary",
        "2. The Case for Decentralization",
        "3. ANDD Architecture Overview",
        "4. Technical Architecture",
        "5. Bandwidth & Connectivity Requirements",
        "6. Energy Requirements & Mitigation Strategies",
        "7. AI-Native Operations",
        "8. Resilience Through Decentralization",
        "9. Payment Architecture",
        "10. DePIN Integration & Pressure Test",
        "11. Opportunity Zone Alignment",
        "12. Implementation Roadmap",
        "13. Conclusion",
    ]
    for item in toc_items:
        p = doc.add_paragraph()
        run = p.add_run(item)
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.color.rgb = MED_BLUE
        p.paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # ======================================
    # 1. EXECUTIVE SUMMARY
    # ======================================
    add_styled_heading(doc, "1. Executive Summary", level=1)

    add_body(doc, "The global compute infrastructure serving AI, critical services, and digital economies is dangerously concentrated. Fewer than 30 hyperscale campuses in the United States process the vast majority of AI inference, financial transactions, government data, and emergency communications. This concentration creates single points of failure for national security, economic continuity, and community resilience \u2014 and it leaves underserved regions permanently behind.")

    add_callout_box(doc,
        "The ANDD Vision",
        "A network of hundreds to thousands of sub-2MW edge datacenters, deployed across federally designated Opportunity Zones, forming an interconnected mesh fabric that is entirely managed and operated by artificial intelligence. No human operators provision servers. No human billing clerks process invoices. The AI management layer handles customer onboarding, capacity planning, workload routing, billing, compliance reporting, and predictive maintenance autonomously."
    )

    doc.add_paragraph()  # spacing

    # Stats bar
    add_stat_row(doc, [
        ("<2MW", "Per Datacenter"),
        ("100s+", "Edge Locations"),
        ("4", "Hardware Domains"),
        ("99.99%", "SLA Target"),
    ])

    doc.add_paragraph()

    add_body(doc, "This whitepaper presents the technical architecture, infrastructure requirements, and economic model for the ANDD network. It details the four hardware domains (Compute, Storage, Connectivity, AI Accelerators), the bandwidth and energy profiles for each site, mitigation strategies for power resilience through renewables and microgrids, and the payment architecture spanning fiat subscriptions to real-time crypto micro-transactions.")

    add_body(doc, "Critically, it pressure-tests the ANDD model against the track record of existing Decentralized Physical Infrastructure Network (DePIN) projects \u2014 analyzing why consumer-grade approaches have struggled and how enterprise-grade, AI-native infrastructure resolves those failure modes.")

    # Photo row: commercial applications preview
    add_photo_row(doc, [
        (images["smart_city"], "Smart City Infrastructure"),
        (images["ai_chip"], "AI at the Edge"),
    ], img_width=Inches(3.0))

    doc.add_page_break()

    # ======================================
    # 2. THE CASE FOR DECENTRALIZATION
    # ======================================
    add_styled_heading(doc, "2. The Case for Decentralization", level=1)

    add_styled_heading(doc, "2.1 The Concentration Problem", level=2)

    add_body(doc, "The current datacenter landscape in the United States is defined by extreme geographic concentration. Northern Virginia alone hosts over 70% of internet traffic on the East Coast. The top five metro markets (Northern Virginia, Dallas-Fort Worth, Phoenix, Chicago, Silicon Valley) account for a disproportionate share of total U.S. datacenter capacity.")

    add_single_photo(doc, images["network"], "Global network infrastructure \u2014 concentrated and vulnerable", width=Inches(5.5))

    add_body(doc, "This concentration creates compounding vulnerabilities:", bold=True)

    add_bullet(doc, " A coordinated attack on fewer than a dozen campuses could degrade federal agencies, financial markets, and defense communications simultaneously. Geographic clustering means a single regional disaster threatens a nationally significant share of compute capacity.", bold_prefix="National Security Exposure.")
    add_bullet(doc, " Communities more than 50ms from the nearest hyperscale region cannot participate in latency-sensitive applications: real-time AI inference, telemedicine, autonomous vehicle coordination, AR/VR. The digital divide is not merely a bandwidth problem; it is a proximity problem.", bold_prefix="Latency Inequality.")
    add_bullet(doc, " Government data, municipal systems, and critical infrastructure become dependent on the operational decisions and pricing power of three to four hyperscale vendors.", bold_prefix="Sovereignty Erosion.")
    add_bullet(doc, " A single 300MW campus demands the equivalent output of a small natural gas plant. Dominion Energy in Virginia has cited datacenter load growth as the primary driver of new generation capacity.", bold_prefix="Grid Strain.")

    add_styled_heading(doc, "2.2 Why Distributed Edge, Why Now", level=2)

    add_body(doc, "Three converging trends make the distributed edge datacenter model not only viable but urgent:", bold=True)

    add_callout_box(doc, "AI Inference is Moving to the Edge",
        "While training remains centralized, inference \u2014 60-70% of all AI compute \u2014 is increasingly latency-sensitive and geographically distributed. Autonomous vehicles need sub-10ms inference. Smart-city sensors generate data that loses value traversing 2,000 miles to a hyperscale region.")

    doc.add_paragraph()
    add_callout_box(doc, "DePIN Requires Enterprise-Grade Infrastructure",
        "Projects built on consumer hardware have hit reliability ceilings. Enterprise customers require 99.99% uptime, N+1 redundancy, physical security, and compliance certifications that consumer-grade nodes cannot provide.")

    doc.add_paragraph()
    add_callout_box(doc, "Federal Policy Now Incentivizes Distribution",
        "The Opportunity Zone program (8,764 designated census tracts), bipartisan AI infrastructure interest, and rural broadband initiatives create an unprecedented policy tailwind.")

    add_styled_heading(doc, "2.3 The AI-Native Differentiator", level=2)

    add_body(doc, "Previous attempts at distributed datacenter networks failed primarily on operational economics. A sub-2MW facility cannot justify full-time site managers, network engineers, and facilities technicians. ANDD inverts this equation by making AI the operator. When all operations are handled by autonomous AI systems, the marginal cost of adding a new site approaches the cost of the hardware and connectivity alone. This is the economic unlock that makes distributed viable for the first time.")

    doc.add_page_break()

    # ======================================
    # 3. ANDD ARCHITECTURE OVERVIEW
    # ======================================
    add_styled_heading(doc, "3. ANDD Architecture Overview", level=1)

    add_styled_heading(doc, "3.1 Network Topology", level=2)

    add_body(doc, "The ANDD network is organized as a three-tier mesh fabric:")

    add_table_from_data(doc,
        ["Tier", "Component", "Power Class", "Quantity", "Connects To"],
        [
            ["Tier 3", "AI Control Plane", "Distributed", "1 (logical)", "All Regional Hubs (consensus)"],
            ["Tier 2", "Regional Hubs", "1\u20132MW", "3+ initially", "Control Plane + 5\u201315 Edge Nodes + Peering Exchanges"],
            ["Tier 1", "Edge Nodes", "200kW\u2013500kW", "100s\u20131000s", "Regional Hub + Adjacent Edge Nodes (mesh) + 2nd Hub (redundant)"],
        ]
    )

    doc.add_paragraph()
    add_single_photo(doc, images["edge_dc"], "ANDD edge node \u2014 enterprise-grade, modular, deployable in 60\u201390 days", width=Inches(5.5))

    add_body(doc, "Tier 1 \u2014 Edge Nodes (200kW\u2013500kW). The atomic unit of the network. Modular, prefabricated facilities deployable in 60-90 days. Each contains a configurable mix of compute, storage, connectivity, and AI accelerator hardware.", bold=True)

    add_body(doc, "Tier 2 \u2014 Regional Hubs (1\u20132MW). Aggregation points providing higher-density compute, regional storage caching, peering interconnection, and backhaul concentration. Each serves 5\u201315 edge nodes.", bold=True)

    add_body(doc, "Tier 3 \u2014 AI Control Plane (Distributed). A distributed consensus system running across all regional hubs. Handles global workload routing, billing reconciliation, capacity planning, and AI model updates. Byzantine fault-tolerant.", bold=True)

    add_styled_heading(doc, "3.2 Mesh Interconnection", level=2)

    add_body(doc, "Every edge node maintains four types of connectivity:")

    add_table_from_data(doc,
        ["Connection Type", "Medium", "Bandwidth", "Purpose"],
        [
            ["Primary Uplink", "Fiber / Licensed Microwave", "10+ Gbps", "Primary backhaul to regional hub"],
            ["Redundant Uplink", "Diverse Fiber / 5G / LEO Satellite", "1\u201310 Gbps", "Backup path via different route"],
            ["Mesh Peering", "Direct node-to-node", "10 Gbps", "Local traffic exchange and failover"],
            ["2nd Hub Path", "Via mesh or direct", "Variable", "Ensures no single hub failure isolates node"],
        ]
    )

    add_styled_heading(doc, "3.3 Single-Site Physical Layout", level=2)

    add_table_from_data(doc,
        ["System Layer", "Components", "Specification"],
        [
            ["IT Equipment", "Compute Racks (x4\u20138), AI Accelerator Racks (x2\u20134), Storage Racks (x2\u20134)", "Configurable mix based on local demand"],
            ["Network Fabric", "Top-of-Rack / Leaf-Spine Switches", "100GbE / 400GbE internal"],
            ["Network Edge", "Edge Router / Firewall", "BGP peering, SD-WAN, encryption"],
            ["External Links", "Primary + Redundant Uplinks", "Fiber 10G+ primary; 5G/Satellite backup"],
            ["Power", "Utility + ATS + Li-Ion UPS + Optional Solar/Fuel Cell", "15\u201330 min UPS runtime; microgrid capable"],
            ["Cooling", "Direct Liquid Cooling + Ambient Air Economization", "Target PUE 1.15\u20131.25"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 4. TECHNICAL ARCHITECTURE
    # ======================================
    add_styled_heading(doc, "4. Technical Architecture", level=1)

    add_styled_heading(doc, "4.1 Four Hardware Domains", level=2)

    # 4.1.1 Compute
    add_styled_heading(doc, "4.1.1 Compute", level=3)
    add_table_from_data(doc,
        ["Component", "Specification"],
        [
            ["Platform", "High-density 1U/2U servers, ARM and x86"],
            ["Processors", "AMD EPYC 9004 / Intel Xeon 6 / Ampere Altra Max"],
            ["Memory", "256GB\u20131TB DDR5 per node"],
            ["Density", "20\u201340kW per rack"],
            ["Use Cases", "Containerized workloads, VM hosting, CI/CD, general-purpose"],
        ]
    )

    # 4.1.2 Storage
    doc.add_paragraph()
    add_styled_heading(doc, "4.1.2 Storage", level=3)
    add_table_from_data(doc,
        ["Component", "Specification"],
        [
            ["Hot Tier", "NVMe SSD arrays, 100TB\u2013500TB per site"],
            ["Warm Tier", "QLC SSD / high-density HDD, 500TB\u20132PB per site"],
            ["Protocol", "S3-compatible object, NFS/SMB block, distributed file system"],
            ["Replication", "Erasure coding across 3+ nodes; 11 nines durability"],
            ["Use Cases", "CDN caching, data lakes, AI training data, backup"],
        ]
    )

    # 4.1.3 Connectivity
    doc.add_paragraph()
    add_styled_heading(doc, "4.1.3 Connectivity", level=3)
    add_table_from_data(doc,
        ["Component", "Specification"],
        [
            ["Internal Fabric", "100GbE leaf-spine, upgradable to 400GbE"],
            ["Backhaul", "10\u2013100 Gbps fiber (primary), diverse redundant path"],
            ["Peering", "Direct peering with regional ISPs, CDNs, cloud on-ramps"],
            ["Wireless", "5G/LTE-A small cells, CBRS spectrum"],
            ["Specialized", "Defense network interconnection (SIPRNet/NIPRNet capable)"],
        ]
    )

    # 4.1.4 AI Hardware
    doc.add_paragraph()
    add_styled_heading(doc, "4.1.4 AI Hardware", level=3)

    add_single_photo(doc, images["ai_chip"], "Purpose-built AI accelerators power inference at the edge", width=Inches(5.5))

    add_table_from_data(doc,
        ["Accelerator", "TDP", "Memory", "Memory BW", "Deployment"],
        [
            ["NVIDIA L4", "72W", "24GB GDDR6", "300 GB/s", "Edge Node (efficient inference)"],
            ["NVIDIA L40S", "300W", "48GB GDDR6X", "864 GB/s", "Edge Node (inference)"],
            ["AMD MI300X", "750W", "192GB HBM3", "5.3 TB/s", "Edge Node / Hub (inference)"],
            ["AMD MI325X", "750W", "256GB HBM3e", "6.0 TB/s", "Edge / Hub (large models)"],
            ["Intel Gaudi 3", "~600W", "128GB HBM2e", "3.7 TB/s", "Edge (cost-efficient)"],
            ["NVIDIA H100 SXM", "700W", "80GB HBM3", "3.35 TB/s", "Regional Hub (training)"],
            ["NVIDIA H200 SXM", "700W", "141GB HBM3e", "4.8 TB/s", "Regional Hub (large models)"],
            ["NVIDIA B200", "1,000W", "192GB HBM3e", "8.0 TB/s", "Regional Hub (training)"],
            ["NVIDIA GB200 NVL2", "2,700W", "384GB HBM3e", "16 TB/s", "Hub (liquid-cooled)"],
        ]
    )

    doc.add_paragraph()
    add_body(doc, "Edge AI Workload Feasibility:", bold=True)
    add_table_from_data(doc,
        ["Workload", "Hardware", "Power", "Latency"],
        [
            ["LLM inference (7\u201313B)", "1x L40S or MI300X", "300\u2013750W", "20\u2013100ms/token"],
            ["LLM inference (70B)", "2\u20134x H100 PCIe", "700W\u20131.4kW", "50\u2013200ms/token"],
            ["Real-time image/video", "1x L4", "72W", "5\u201320ms"],
            ["Speech recognition", "1x L4", "72W", "<100ms"],
            ["Recommender systems", "2\u20134x GPU + CPU", "1\u20133kW", "10\u201350ms"],
            ["RAG", "1\u20132x H100 + vector DB", "1\u20132kW", "100\u2013500ms"],
            ["Fraud detection", "1x L40S", "300W", "<50ms"],
            ["Medical imaging", "1x L40S", "300W", "<1s"],
        ]
    )

    # 4.2 Software Stack
    doc.add_paragraph()
    add_styled_heading(doc, "4.2 Software Stack", level=2)

    add_table_from_data(doc,
        ["Layer", "Component 1", "Component 2", "Component 3"],
        [
            ["AI Management", "Onboarding Agent", "Provisioning Agent", "Billing + SLA Monitor"],
            ["Orchestration", "Kubernetes (K3s/RKE2)", "Service Mesh (Istio)", "AI-Optimized Scheduler"],
            ["Infrastructure", "SDN (OVS/VPP)", "Storage (Ceph/MinIO)", "DCIM/BMS (AI-Controlled)"],
            ["Hardware Abstraction", "BMC/IPMI/Redfish", "GPU Driver Layer", "Switch OS (SONiC/Cumulus)"],
        ]
    )

    # 4.3 Security
    doc.add_paragraph()
    add_styled_heading(doc, "4.3 Security Architecture", level=2)

    add_bullet(doc, " Every workload-to-workload communication is mTLS encrypted. No implicit trust based on network location.", bold_prefix="Zero-trust networking.")
    add_bullet(doc, " TPM 2.0 on all servers. Measured boot. Remote attestation verifies node integrity cryptographically.", bold_prefix="Hardware root of trust.")
    add_bullet(doc, " SR-IOV for network, SEV-SNP/TDX for confidential computing, separate encryption keys per tenant.", bold_prefix="Tenant isolation.")
    add_bullet(doc, " Biometric access, 24/7 AI-monitored surveillance, tamper-evident racks. SCIF-compatible options.", bold_prefix="Physical security.")
    add_bullet(doc, " FedRAMP, SOC 2, HIPAA, CJIS, ITAR compliance paths built in from day one.", bold_prefix="Compliance.")

    doc.add_page_break()

    # ======================================
    # 5. BANDWIDTH
    # ======================================
    add_styled_heading(doc, "5. Bandwidth & Connectivity Requirements", level=1)

    add_table_from_data(doc,
        ["Site Tier", "Primary Uplink", "Redundant", "Mesh", "Total Backhaul"],
        [
            ["Edge Node (200kW)", "10 Gbps", "1\u201310 Gbps", "10 Gbps", "20\u201330 Gbps"],
            ["Edge Node (500kW)", "40 Gbps", "10 Gbps", "25 Gbps", "50\u201375 Gbps"],
            ["Regional Hub (1\u20132MW)", "100 Gbps", "40 Gbps", "100 Gbps", "200\u2013300 Gbps"],
        ]
    )

    doc.add_paragraph()
    add_single_photo(doc, images["telecom"], "Multi-carrier connectivity ensures resilient backhaul", width=Inches(5.5))

    add_styled_heading(doc, "Backhaul by Site Type", level=3)
    add_table_from_data(doc,
        ["Site Type", "Primary", "Bandwidth", "Backup", "Backup BW"],
        [
            ["Urban", "Dark/Lit Fiber (multi-carrier)", "10\u201340 Gbps", "5G/LTE-A", "1\u20135 Gbps"],
            ["Suburban", "Fiber (1\u20132 carriers)", "10\u201340 Gbps", "Diverse Fiber", "10 Gbps"],
            ["Rural", "Licensed Wireless / LEO Sat", "1\u201310 Gbps", "5G/LTE-A", "500M\u20131 Gbps"],
        ]
    )

    doc.add_paragraph()
    add_styled_heading(doc, "Protocol Stack", level=3)
    add_bullet(doc, " eBPF-accelerated IP routing with segment routing (SRv6)", bold_prefix="Underlay:")
    add_bullet(doc, " WireGuard/MACsec encrypted tunnels; VXLAN/GENEVE tenant isolation", bold_prefix="Overlay:")
    add_bullet(doc, " Automated BGP with RPKI validation and route leak detection", bold_prefix="Peering:")
    add_bullet(doc, " Anycast DNS across all nodes for automatic geo-routing", bold_prefix="DNS:")
    add_bullet(doc, " AI-driven GSLB factoring latency, capacity, energy cost, carbon intensity", bold_prefix="Load Balancing:")

    doc.add_page_break()

    # ======================================
    # 6. ENERGY
    # ======================================
    add_styled_heading(doc, "6. Energy Requirements & Mitigation Strategies", level=1)

    add_single_photo(doc, images["solar_energy"], "On-site solar generation offsets 30\u201350% of facility energy consumption", width=Inches(5.5))

    add_styled_heading(doc, "6.1 Per-Site Power Profile", level=2)

    add_table_from_data(doc,
        ["Site Tier", "IT Load", "Cooling", "Infra", "Total", "Target PUE"],
        [
            ["Edge Node (200kW)", "150kW", "25kW", "25kW", "200kW", "1.15\u20131.25"],
            ["Edge Node (500kW)", "380kW", "65kW", "55kW", "500kW", "1.15\u20131.25"],
            ["Regional Hub (2MW)", "1,500kW", "280kW", "220kW", "2,000kW", "1.15\u20131.25"],
        ]
    )

    doc.add_paragraph()
    add_body(doc, "PUE Benchmarks \u2014 ANDD vs. Industry:", bold=True)
    add_table_from_data(doc,
        ["Facility Type", "Typical PUE", "Best-in-Class", "Primary Cooling"],
        [
            ["Hyperscale (Google, Meta)", "1.10\u20131.20", "1.06\u20131.08", "Evaporative + liquid"],
            ["Large colocation", "1.30\u20131.50", "1.15\u20131.25", "Chilled water + air"],
            ["Traditional edge (<1MW)", "1.40\u20131.80", "1.20\u20131.30", "DX air conditioning"],
            ["ANDD Edge (purpose-built)", "1.15\u20131.25", "1.02\u20131.10", "DLC + immersion"],
        ]
    )

    add_styled_heading(doc, "6.2 Cooling Technology Comparison", level=2)

    add_single_photo(doc, images["cooling"], "Direct liquid cooling eliminates the traditional edge efficiency penalty", width=Inches(5.5))

    add_table_from_data(doc,
        ["Technology", "Cooling Power (500kW site)", "Effective IT", "PUE", "Capital Premium"],
        [
            ["Air cooling (DX)", "150\u2013200kW", "300\u2013350kW", "1.40\u20131.80", "Baseline"],
            ["Rear-door heat exchangers", "75\u2013125kW", "375\u2013425kW", "1.20\u20131.40", "+15\u201325%"],
            ["Direct-to-chip liquid", "40\u201375kW", "425\u2013460kW", "1.10\u20131.20", "+25\u201340%"],
            ["Single-phase immersion", "15\u201330kW", "470\u2013485kW", "1.02\u20131.06", "+30\u201350%"],
            ["Two-phase immersion", "10\u201320kW", "480\u2013490kW", "1.01\u20131.04", "+40\u201360%"],
        ]
    )

    add_callout_box(doc, "Key Insight",
        "Moving from air cooling (PUE 1.5) to immersion (PUE 1.05) saves ~300kW of cooling power in a 1MW facility \u2014 effectively increasing usable compute capacity by 30% within the same power envelope.")

    add_styled_heading(doc, "6.3 Renewable Integration Economics", level=2)

    add_body(doc, "Sizing Example \u2014 200kW Edge Node:", bold=True)
    add_table_from_data(doc,
        ["Component", "Specification", "Cost", "Annual Value"],
        [
            ["Solar Array", "100kW, carport-mounted", "~$150,000", "175 MWh/yr generation"],
            ["BESS (LFP)", "500kWh / 250kW", "~$200,000", "2hr backup + daily cycling"],
            ["IRA Tax Credit", "30\u201350% ITC", "\u2013$105K to \u2013$175K", "Reduces effective capital"],
            ["Utility Savings", "Offset + peak shaving", "\u2014", "$40K\u2013$80K/yr"],
            ["Grid Services", "Freq. regulation, DR", "\u2014", "$50K\u2013$200K/yr per MW"],
        ]
    )

    add_body(doc, "Effective payback: 2\u20134 years after IRA credits and grid services revenue.", bold=True, color=ACCENT_BLUE)

    add_styled_heading(doc, "6.4 Federal Funding Landscape", level=2)

    add_table_from_data(doc,
        ["Program", "Funding", "Relevance to ANDD"],
        [
            ["DOE GRIP", "$10.5 billion", "Microgrids, DER, grid modernization"],
            ["DOE Loan Programs Office", "$400B+ lending", "Clean energy, fuel cells, distributed generation"],
            ["ARPA-E COOLERCHIPS", "$42 million", "Datacenter cooling efficiency R&D"],
            ["IRA Investment Tax Credit", "30\u201350%", "Solar, battery, fuel cells at ANDD sites"],
            ["USDA REAP", "Grants + loans", "Rural renewable energy"],
            ["NTIA BEAD", "$42.45 billion", "Broadband + co-located edge infrastructure"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 7. AI-NATIVE OPERATIONS
    # ======================================
    add_styled_heading(doc, "7. AI-Native Operations", level=1)

    add_single_photo(doc, images["autonomous"], "AI agents manage the entire datacenter lifecycle autonomously", width=Inches(5.5))

    add_styled_heading(doc, "7.1 The Autonomous Datacenter Thesis", level=2)

    add_body(doc, "Traditional datacenter operations depend on human operators at every layer. These human costs establish a minimum viable facility size \u2014 typically 5MW+ \u2014 below which operations are not economically sustainable. ANDD eliminates this constraint by replacing human operational roles with specialized AI agents.")

    add_styled_heading(doc, "7.2 AI Agent Architecture", level=2)

    add_table_from_data(doc,
        ["Agent", "Function", "Key Capabilities"],
        [
            ["Orchestration Agent", "Coordinates all sub-agents", "Conflict resolution, human escalation when confidence < threshold"],
            ["Customer Onboarding", "Full customer lifecycle", "Lead qualification, proposals, KYC/KYB, tenant provisioning"],
            ["Provisioning Agent", "Infrastructure deployment", "Workload-to-resource mapping, optimal node placement, auto-scaling"],
            ["Billing & Revenue", "Financial operations", "Sub-second metering, invoicing, micro-transactions, fiat+crypto reconciliation"],
            ["Predictive Maintenance", "Prevent failures", "Sensor telemetry, digital twins, preventive scheduling, work order dispatch"],
            ["SLA Guardian", "Ensure commitments", "Threshold monitoring, auto-remediation, compliance reports, credit issuance"],
        ]
    )

    doc.add_paragraph()
    add_callout_box(doc, "Target: 1 Human Operator per 20\u201350 Edge Nodes",
        "A 10\u201325x improvement over traditional staffing models. Humans handle exception escalation, strategic decisions, physical maintenance, and compliance oversight. The AI handles everything else.")

    doc.add_page_break()

    # ======================================
    # 8. RESILIENCE
    # ======================================
    add_styled_heading(doc, "8. Resilience Through Decentralization", level=1)

    add_body(doc, "The United States\u2019 critical infrastructure \u2014 payments, energy, communications, emergency services \u2014 has migrated to cloud systems hosted in concentrated datacenter corridors. This creates systemic risk that individual redundancy measures cannot address.")

    # Commercial applications photo grid
    add_styled_heading(doc, "Commercial Applications: What ANDD Protects", level=2)

    add_photo_row(doc, [
        (images["fintech"], "Payments & Fintech"),
        (images["emergency"], "Emergency Services"),
    ], img_width=Inches(3.0))

    doc.add_paragraph()

    add_photo_row(doc, [
        (images["healthcare"], "Healthcare & Telemedicine"),
        (images["government"], "Government & Defense"),
    ], img_width=Inches(3.0))

    doc.add_paragraph()

    add_styled_heading(doc, "8.1 Payments Infrastructure", level=3)
    add_body(doc, "The U.S. payment system processes over $10 trillion daily through networks that depend on a handful of datacenter locations. ANDD distributes payment processing \u2014 card authorization, ACH, FedNow gateways \u2014 across hundreds of edge nodes with local store-and-forward capability during backbone disruptions.")

    add_styled_heading(doc, "8.2 Energy Grid", level=3)
    add_body(doc, "ANDD nodes host distributed SCADA/EMS systems, provide sub-10ms control loops for DERs, aggregate into a virtual power plant for grid services, and island during grid emergencies to maintain critical local services.")

    add_styled_heading(doc, "8.3 Emergency Services & Public Safety", level=3)
    add_body(doc, "Local NG911 hosting, FirstNet edge compute, emergency operations center computing, satellite backhaul resilience, and community notification systems \u2014 all functioning even when terrestrial backhaul is disrupted.")

    add_styled_heading(doc, "8.4 Utilities & Water Systems", level=3)
    add_body(doc, "Local SCADA hosting for water treatment, wastewater, and gas distribution. Semi-air-gapped operation capability. AI-powered anomaly detection for contamination, leaks, and cyber intrusion at sub-second response times.")

    add_styled_heading(doc, "8.5 Resilience Quantification", level=2)
    add_table_from_data(doc,
        ["Architecture", "Uptime per Unit", "System Availability", "Failure Mode"],
        [
            ["Single hyperscale campus", "99.99%", "99.99% (67 min downtime/yr)", "Catastrophic \u2014 total loss on failure"],
            ["ANDD mesh (100 nodes, 70% needed)", "99.95% per node", "99.9999%+ network-level", "Graceful degradation \u2014 linear performance decrease"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 9. PAYMENT ARCHITECTURE
    # ======================================
    add_styled_heading(doc, "9. Payment Architecture", level=1)

    add_single_photo(doc, images["payments"], "From enterprise wire transfers to real-time crypto micro-transactions", width=Inches(5.5))

    add_styled_heading(doc, "9.1 Fiat Subscription Tiers", level=2)

    add_table_from_data(doc,
        ["Tier", "Model", "Billing", "Payment Methods", "Use Case"],
        [
            ["Starter", "Monthly", "Post-paid, NET 30", "Credit card, ACH", "Startups, developers"],
            ["Professional", "Monthly/Annual", "Post-paid, NET 30", "ACH, wire", "Mid-market, fintech"],
            ["Enterprise", "Annual", "Custom, NET 45\u201360", "Wire, ACH, PO-backed", "Large enterprise, telcos"],
            ["Government", "Annual/Multi-year", "Per procurement regs", "Treasury/PO systems", "Federal, state, local gov"],
        ]
    )

    add_styled_heading(doc, "9.2 Digital & Crypto Payment Rails", level=2)
    add_table_from_data(doc,
        ["Chain", "Use Case", "Finality", "Cost per Tx"],
        [
            ["Ethereum L1", "Large enterprise contracts", "~12 min", "$1\u2013$20"],
            ["Solana", "High-frequency, lower-value", "Sub-second", "~$0.001"],
            ["Ethereum L2 (Arbitrum, Base)", "Medium-frequency", "Minutes", "$0.01\u2013$0.10"],
            ["Payment Channels (off-chain)", "Micro-transactions", "Instant (off-chain)", "Near-zero"],
        ]
    )

    add_styled_heading(doc, "9.3 Smart Contract SLAs", level=2)
    add_body(doc, "ANDD introduces programmable SLAs \u2014 smart contracts that encode service level commitments and automatically enforce them:")

    add_table_from_data(doc,
        ["Contract Element", "Logic", "Purpose"],
        [
            ["Uptime Target", "9999 basis points (99.99%)", "SLA threshold"],
            ["Latency Target", "<5ms edge latency", "Performance floor"],
            ["Measurement Period", "30-day rolling window", "Evaluation cadence"],
            ["Oracle Integration", "getUptime(tenantId, period)", "Verified performance data"],
            ["Automated Payout", "paymentToken.transfer(tenant, credit)", "Instant SLA credit to tenant wallet"],
            ["Event Logging", "emit SLACreditIssued()", "Immutable on-chain audit trail"],
        ]
    )

    add_styled_heading(doc, "9.4 Hybrid Payment Orchestration", level=2)
    add_table_from_data(doc,
        ["Customer Type", "Primary Payment", "Secondary", "Micro-Tx"],
        [
            ["Enterprise", "Wire / ACH (annual)", "Credit card (overage)", "N/A"],
            ["Government", "PO / Treasury", "ACH", "N/A"],
            ["Startup", "Credit card (monthly)", "USDC", "Per-API-call"],
            ["DePIN Project", "Stablecoin", "Payment channel", "Per-request"],
            ["Web3 Native", "USDC / token", "Payment channel", "Per-request"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 10. DePIN PRESSURE TEST
    # ======================================
    add_styled_heading(doc, "10. DePIN Integration & Pressure Test", level=1)

    add_single_photo(doc, images["blockchain"], "DePIN \u2014 the promise of decentralized physical infrastructure meets enterprise reality", width=Inches(5.5))

    add_styled_heading(doc, "10.1 Case Studies: Lessons from DePIN Projects", level=2)

    add_table_from_data(doc,
        ["Project", "What Worked", "What Failed", "ANDD Lesson"],
        [
            ["Helium", "900K+ hotspots globally; proved token incentives bootstrap networks", "Over-provisioned where enthusiasts live, not where demand is; consumer hardware = no SLA", "Location must be demand-driven; enterprise hardware required"],
            ["Filecoin", "22+ EiB storage; cryptographic proof-of-storage", "Mostly empty \"committed capacity\"; favors industrial miners; slow retrieval", "Incentives tied to utilization, not capacity"],
            ["Render", "Real 3D rendering demand; millions of jobs processed", "Consumer GPUs can't guarantee uptime, thermal mgmt, or ECC for AI inference", "AI compute must be datacenter-grade"],
            ["Akash", "70\u201385% cheaper than hyperscale; functioning marketplace", "Inconsistent uptime; no SLA enforcement; enterprise won't trust anonymous providers", "Smart contract SLAs + enterprise facilities = trust layer"],
            ["io.net", "Distributed GPU clustering for AI/ML", "Heterogeneous consumer GPUs; inter-node latency kills training; benchmark ≠ production", "Homogeneous, co-located hardware within each site"],
        ]
    )

    doc.add_paragraph()
    add_styled_heading(doc, "10.2 The Enterprise-Grade Gap", level=2)

    add_table_from_data(doc,
        ["Dimension", "Consumer DePIN", "ANDD"],
        [
            ["Uptime", "90\u201398% (best effort)", "99.99% (SLA-backed)"],
            ["Redundancy", "None", "N+1 power, cooling, network"],
            ["Physical Security", "None", "Biometric, surveillance, tamper-evident"],
            ["Compliance", "None", "FedRAMP, SOC 2, HIPAA, CJIS"],
            ["Power Quality", "Residential (variable)", "UPS + BESS + generator/fuel cell"],
            ["Cooling", "Consumer fans", "DLC, immersion, AI-optimized"],
            ["Connectivity", "Residential broadband", "Multi-provider, redundant, SLA-backed"],
            ["Data Sovereignty", "Unknown", "Configurable per-tenant geo-restrictions"],
        ]
    )

    doc.add_paragraph()
    add_callout_box(doc, "ANDD Completes DePIN",
        "ANDD does not compete with DePIN projects \u2014 it completes them. The tokenomics and demand aggregation work; the physical infrastructure layer needs upgrading to enterprise grade. ANDD provides that backbone.")

    add_styled_heading(doc, "10.3 What Can Be Built on ANDD", level=2)

    add_body(doc, "ANDD as infrastructure enables an ecosystem of applications and services that require reliable, distributed, low-latency compute:")

    # Applications photo grid
    add_photo_row(doc, [
        (images["smart_city"], "Smart City & IoT"),
        (images["healthcare"], "Telemedicine & Health AI"),
    ], img_width=Inches(3.0))

    doc.add_paragraph()

    add_photo_row(doc, [
        (images["community"], "Community Connectivity"),
        (images["blockchain"], "DePIN & Web3 Protocols"),
    ], img_width=Inches(3.0))

    doc.add_paragraph()

    add_table_from_data(doc,
        ["Application Category", "Examples", "Why ANDD is Required"],
        [
            ["Smart City & IoT", "Traffic management, environmental sensors, connected streetlights, digital twins", "Sub-10ms latency for real-time control; local data processing"],
            ["Autonomous Vehicles", "V2X communication, HD map updates, real-time inference", "Safety-critical latency requirements; geographic coverage"],
            ["Telemedicine & Health AI", "Remote diagnostics, medical image analysis, patient monitoring", "Data residency (HIPAA), low latency, high availability"],
            ["Edge AI / MLOps", "Model serving, fine-tuning, RAG pipelines, AI agents", "GPU at the edge; avoid round-trip to hyperscale"],
            ["DePIN Protocols", "Decentralized compute, storage, wireless, sensing networks", "Enterprise-grade backbone for consumer-proven protocols"],
            ["Fintech & Payments", "Real-time payment processing, fraud detection, crypto settlement", "Data residency, sub-50ms latency, regulatory compliance"],
            ["Content Delivery", "Video streaming, gaming, AR/VR content, CDN edge caching", "Bandwidth offload, latency reduction"],
            ["Defense & Intelligence", "Classified workloads, SIGINT processing, C2 systems", "Sovereign infrastructure, defense network compatible"],
            ["Emergency Services", "NG911, FirstNet, incident management, community alerts", "Must function during disasters when backhaul fails"],
            ["Agricultural Tech", "Precision agriculture, drone coordination, sensor networks", "Rural coverage, local processing, low-bandwidth backhaul"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 11. OPPORTUNITY ZONES
    # ======================================
    add_styled_heading(doc, "11. Opportunity Zone Alignment", level=1)

    add_single_photo(doc, images["community"], "Building digital infrastructure in the communities that need it most", width=Inches(5.5))

    add_styled_heading(doc, "11.1 Tax Incentive Structure", level=2)

    add_table_from_data(doc,
        ["Tier", "Incentive", "Requirement", "Benefit"],
        [
            ["Tier 1", "Capital Gains Deferral", "Reinvest into QOF", "Defer tax on eligible gains; rolling 5-year window"],
            ["Tier 2", "Basis Step-Up", "Hold 5+ years", "10% step-up (30% for rural OZ via Qualified Rural OFs)"],
            ["Tier 3", "10-Year Exclusion", "Hold 10+ years", "Zero federal capital gains tax on all new appreciation"],
        ]
    )

    add_styled_heading(doc, "11.2 Per-Site Community Impact", level=2)

    add_table_from_data(doc,
        ["Impact Category", "Estimate (200kW Edge Node)"],
        [
            ["Construction jobs", "15\u201330 (6\u201312 month build)"],
            ["Permanent operations jobs", "1\u20133 (technicians, supplemented by AI)"],
            ["Annual property tax revenue", "$50,000\u2013$150,000"],
            ["Annual utility revenue", "$150,000\u2013$300,000"],
            ["Indirect economic multiplier", "1.5\u20132.0x direct spending"],
            ["Digital infrastructure", "Gigabit connectivity, AI capabilities, edge compute"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 12. IMPLEMENTATION ROADMAP
    # ======================================
    add_styled_heading(doc, "12. Implementation Roadmap", level=1)

    add_table_from_data(doc,
        ["Phase", "Timeline", "Key Milestones"],
        [
            ["Phase 1: Foundation", "Months 1\u201312", "AI management layer; 200kW reference design; 3\u20135 pilot sites; SOC 2 Type I; QOF formation"],
            ["Phase 2: Network Formation", "Months 12\u201324", "20\u201350 nodes; regional hubs; >90% autonomous ops; first gov customers; DePIN APIs; FedRAMP"],
            ["Phase 3: Scale", "Months 24\u201348", "100\u2013300 nodes; smart contract SLAs; micro-transactions; federal customers; defense integration"],
            ["Phase 4: Continental Coverage", "Months 48\u201372", "500\u20131,000+ nodes; full AI autonomy; international expansion; VPP grid services; self-sustaining"],
        ]
    )

    doc.add_page_break()

    # ======================================
    # 13. CONCLUSION
    # ======================================
    add_styled_heading(doc, "13. Conclusion", level=1)

    add_body(doc, "The concentration of compute infrastructure into a handful of hyperscale campuses was an artifact of an era when operational economics demanded scale and AI did not yet exist as an operational tool. That era is ending.")

    add_body(doc, "ANDD demonstrates that AI-native operations eliminate the economic barrier to distributed deployment. When AI handles onboarding, provisioning, billing, monitoring, and maintenance, the marginal cost of adding a new edge node approaches the cost of the hardware itself.")

    add_callout_box(doc, "ANDD delivers on every dimension that matters:",
        "\u2022 Sovereignty \u2014 Compute stays where it is generated and governed\n"
        "\u2022 Security \u2014 No single target can degrade the network\n"
        "\u2022 Resilience \u2014 Distributed power, connectivity, and compute survive events that cripple centralized alternatives\n"
        "\u2022 Equity \u2014 Advanced capabilities reach underserved communities\n"
        "\u2022 DePIN Readiness \u2014 Enterprise-grade backbone for decentralized protocols\n"
        "\u2022 Economic Viability \u2014 Multiple payment rails serve every customer type"
    )

    doc.add_paragraph()
    add_body(doc, "The question is no longer whether distributed, AI-managed datacenter infrastructure is technically feasible. The question is how quickly it can be deployed.", bold=True, color=MED_BLUE)

    doc.add_paragraph()
    add_body(doc, "ANDD is the answer.", bold=True, color=ACCENT_BLUE)

    # Footer
    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("contact@andd.network  |  andd.network")
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = MED_BLUE

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run("This document contains forward-looking statements about technology capabilities, market conditions, and business plans. Actual results may differ. Technical specifications represent design targets. Regulatory and tax information is for informational purposes and should not be construed as legal or tax advice.")
    run2.font.name = "Calibri"
    run2.font.size = Pt(8)
    run2.font.color.rgb = SILVER
    run2.italic = True

    # ---- Save ----
    output_path = BASE_DIR / "ANDD_Whitepaper.docx"
    doc.save(str(output_path))
    print(f"\nSaved: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build_document()
