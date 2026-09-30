#!/usr/bin/env python3
"""Build ANDD Investor Pitch Deck as a .pptx file (Google Slides compatible)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Colors ──
DARK_BG = RGBColor(0x0A, 0x16, 0x28)
DARK_SURFACE = RGBColor(0x11, 0x1D, 0x33)
DARK_CARD = RGBColor(0x16, 0x24, 0x40)
BLUE_BRIGHT = RGBColor(0x3B, 0x82, 0xF6)
BLUE_LIGHT = RGBColor(0x60, 0xA5, 0xFA)
BLUE_MID = RGBColor(0x2B, 0x6C, 0xB0)
SILVER_LIGHT = RGBColor(0xD1, 0xD5, 0xDB)
SILVER_MID = RGBColor(0x9C, 0xA3, 0xAF)
SILVER_DARK = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xE2, 0xE8, 0xF0)
GREEN = RGBColor(0x22, 0xC5, 0x5E)
RED = RGBColor(0xEF, 0x44, 0x44)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
CARD_BORDER = RGBColor(0x1E, 0x3A, 0x5C)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_WIDTH
prs.slide_height = SLIDE_HEIGHT

LOGO_PATH = os.path.join(os.path.dirname(__file__), "andd.png")


def set_slide_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=14,
                color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_rich_textbox(slide, left, top, width, height):
    """Return a text_frame for adding multiple runs."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    return tf


def add_paragraph(tf, text, font_size=14, color=WHITE, bold=False,
                  alignment=PP_ALIGN.LEFT, space_after=Pt(4), font_name="Calibri"):
    if len(tf.paragraphs) == 1 and tf.paragraphs[0].text == "":
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_after = space_after
    return p


def add_card(slide, left, top, width, height, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_CARD
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    shape.shadow.inherit = False
    return shape


def add_section_label(slide, left, top, text):
    add_textbox(slide, left, top, Inches(4), Inches(0.35), text,
                font_size=11, color=BLUE_BRIGHT, bold=True)


def add_title(slide, left, top, width, text, font_size=32):
    add_textbox(slide, left, top, width, Inches(0.9), text,
                font_size=font_size, color=WHITE, bold=True)


def add_subtitle_text(slide, left, top, width, text, font_size=16):
    add_textbox(slide, left, top, width, Inches(1.2), text,
                font_size=font_size, color=SILVER_MID)


def add_stat(slide, left, top, value, label, value_color=BLUE_LIGHT):
    add_textbox(slide, left, top, Inches(2.5), Inches(0.6), value,
                font_size=36, color=value_color, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, left, top + Inches(0.6), Inches(2.5), Inches(0.5),
                label, font_size=9, color=SILVER_MID,
                alignment=PP_ALIGN.CENTER)


def add_bullet_list(slide, left, top, width, items, font_size=12,
                    color=SILVER_LIGHT, bullet_color=BLUE_BRIGHT):
    tf = add_rich_textbox(slide, left, top, width, Inches(len(items) * 0.35))
    for i, item in enumerate(items):
        p = add_paragraph(tf, f"\u25b8  {item}", font_size=font_size,
                          color=color, space_after=Pt(4))
    return tf


def build_table(slide, left, top, width, rows, col_widths, headers=None,
                header_color=BLUE_LIGHT, cell_color=SILVER_LIGHT):
    """Build a styled table on the slide."""
    n_rows = len(rows) + (1 if headers else 0)
    n_cols = len(col_widths)
    table_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width,
                                          Inches(n_rows * 0.38))
    table = table_shape.table

    # Set column widths
    total_parts = sum(col_widths)
    for i, w in enumerate(col_widths):
        table.columns[i].width = int(width * w / total_parts)

    row_idx = 0
    if headers:
        for j, h in enumerate(headers):
            cell = table.cell(0, j)
            cell.text = h
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.color.rgb = header_color
                p.font.bold = True
                p.font.name = "Calibri"
            cell.fill.solid()
            cell.fill.fore_color.rgb = DARK_CARD
        row_idx = 1

    for r, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(row_idx + r, j)
            text = val if isinstance(val, str) else val[0]
            color = cell_color if isinstance(val, str) else val[1]
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.color.rgb = color
                p.font.name = "Calibri"
            cell.fill.solid()
            cell.fill.fore_color.rgb = DARK_BG

    # Style borders by making them subtle
    return table_shape


# ═══════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_slide_bg(slide)

# Logo
if os.path.exists(LOGO_PATH):
    logo_width = Inches(3.5)
    logo_left = (SLIDE_WIDTH - logo_width) // 2
    slide.shapes.add_picture(LOGO_PATH, logo_left, Inches(1.0),
                             width=logo_width)

add_textbox(slide, Inches(1), Inches(3.8), Inches(11.333), Inches(0.8),
            "AI Native Distributed Datacenters",
            font_size=44, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(4.7), Inches(9.333), Inches(0.7),
            "Sovereign, resilient, AI-managed edge infrastructure for the next era of compute",
            font_size=18, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(5.6), Inches(9.333), Inches(0.4),
            "Investor Presentation \u2014 March 2026",
            font_size=13, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(6.3), Inches(9.333), Inches(0.3),
            "CONFIDENTIAL \u2014 DO NOT DISTRIBUTE",
            font_size=10, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

L = Inches(0.8)
add_section_label(slide, L, Inches(0.4), "THE PROBLEM")
add_title(slide, L, Inches(0.7), Inches(11), "America's Compute Infrastructure Is Dangerously Concentrated")
add_subtitle_text(slide, L, Inches(1.5), Inches(10),
    "Fewer than 30 hyperscale campuses process the vast majority of AI inference, "
    "financial transactions, government data, and emergency communications in the United States.")

# Stats row
stats = [("70%", "East Coast internet\ntraffic through NoVA alone"),
         ("5", "Metro markets with majority\nof U.S. DC capacity"),
         ("$10T+", "Daily payments flowing\nthrough concentrated infra"),
         ("945 TWh", "Projected DC electricity\nby 2030 (IEA)")]
for i, (val, label) in enumerate(stats):
    add_stat(slide, L + Inches(i * 3), Inches(2.7), val, label)

# 4 cards
cards = [
    ("National Security", "A coordinated attack on fewer than a dozen campuses could degrade federal agencies, financial markets, and defense communications simultaneously.", RED),
    ("Latency Inequality", "Communities 50ms+ from the nearest hyperscale region are locked out of real-time AI, telemedicine, autonomous vehicles, and fintech.", RED),
    ("Grid Strain", "A single 300MW campus demands the output of a small power plant. Concentrated demand strains grids and creates political backlash.", RED),
    ("Sovereignty Erosion", "Government data and critical infrastructure depend on the operational decisions and pricing of 3-4 hyperscale vendors.", RED),
]
card_w = Inches(2.85)
card_h = Inches(2.2)
for i, (title, desc, title_color) in enumerate(cards):
    cl = L + Inches(i * 3)
    ct = Inches(4.2)
    add_card(slide, cl, ct, card_w, card_h)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.15), card_w - Inches(0.4),
                Inches(0.35), title, font_size=14, color=title_color, bold=True)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.55), card_w - Inches(0.4),
                card_h - Inches(0.7), desc, font_size=11, color=SILVER_MID)


# ═══════════════════════════════════════════════════
# SLIDE 3 — WHY NOW
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "TIMING")
add_title(slide, L, Inches(0.7), Inches(11), "Five Converging Trends Make This Urgent")

trends = [
    ("1", "AI Inference Moves to the Edge",
     "Inference is 60-70% of all AI compute \u2014 bursty, latency-sensitive, geographically distributed. Training stays centralized; inference demands the edge."),
    ("2", "DePIN Needs Enterprise-Grade Infra",
     "The DePIN movement validated demand for decentralized compute, but consumer hardware can't meet 99.99% uptime and compliance requirements."),
    ("3", "Federal Policy Tailwinds",
     "OZ program made permanent. $10.5B GRIP, $42.45B BEAD, 30-50% IRA tax credits, and $400B+ DOE lending authority \u2014 all aligned with distributed deployment."),
    ("4", "Real-Time Apps Proliferating",
     "NG911, FirstNet, autonomous vehicles, industrial IoT, and AR/VR all demand sub-10ms latency that only distributed infrastructure can deliver."),
    ("5", "Hardware Has Caught Up",
     "Inference GPUs at 72-300W, direct liquid cooling enabling 50-120kW/rack in small facilities, and prefab enclosures compressing deployment to 60-90 days."),
    ("\u2192", "The Window Is Open",
     "The convergence of AI capability, hardware miniaturization, federal incentives, and market demand creates a once-in-a-generation infrastructure opportunity."),
]
card_w = Inches(3.8)
card_h = Inches(2.2)
for i, (num, title, desc) in enumerate(trends):
    col = i % 3
    row = i // 3
    cl = L + Inches(col * 4)
    ct = Inches(1.6) + Inches(row * 2.5)
    border = BLUE_BRIGHT if i == 5 else CARD_BORDER
    add_card(slide, cl, ct, card_w, card_h, border_color=border)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.15), Inches(0.5), Inches(0.35),
                num, font_size=16, color=BLUE_LIGHT, bold=True)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.5), card_w - Inches(0.4),
                Inches(0.35), title, font_size=13, color=WHITE, bold=True)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.9), card_w - Inches(0.4),
                card_h - Inches(1), desc, font_size=11, color=SILVER_MID)


# ═══════════════════════════════════════════════════
# SLIDE 4 — THE SOLUTION
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "THE SOLUTION")
add_title(slide, L, Inches(0.7), Inches(11), "ANDD: A Network of AI-Managed Edge Datacenters")
add_subtitle_text(slide, L, Inches(1.4), Inches(10),
    "Hundreds to thousands of sub-2MW edge datacenters deployed in Opportunity Zones, "
    "forming an interconnected mesh fabric entirely managed by AI.")

# Left: 4 cards in 2x2 grid
sol_cards = [
    ("Edge Nodes", "200kW-500kW modular facilities, 4-20 racks. Deployed in 60-90 days."),
    ("Regional Hubs", "1-2MW aggregation points. Training-class GPUs, dense peering, compliance perimeter."),
    ("AI Control Plane", "Distributed consensus across all hubs. Manages workload routing, capacity planning, billing."),
    ("Mesh Fabric", "Every node peers with adjacent nodes + connects to 2+ hubs. Self-healing in <30 seconds."),
]
cw = Inches(3)
ch = Inches(1.5)
for i, (title, desc) in enumerate(sol_cards):
    col = i % 2
    row = i // 2
    cl = L + Inches(col * 3.2)
    ct = Inches(2.6) + Inches(row * 1.7)
    add_card(slide, cl, ct, cw, ch)
    add_textbox(slide, cl + Inches(0.15), ct + Inches(0.1), cw - Inches(0.3),
                Inches(0.3), title, font_size=13, color=WHITE, bold=True)
    add_textbox(slide, cl + Inches(0.15), ct + Inches(0.45), cw - Inches(0.3),
                ch - Inches(0.5), desc, font_size=10, color=SILVER_MID)

# Right: 3-tier architecture diagram
rx = Inches(7.2)
tier_w = Inches(5.3)

add_textbox(slide, rx, Inches(2.5), tier_w, Inches(0.3),
            "THREE-TIER ARCHITECTURE", font_size=10, color=BLUE_LIGHT,
            bold=True, alignment=PP_ALIGN.CENTER)

tiers = [
    ("Tier 3: AI Control Plane", "Distributed consensus", Inches(3.6), BLUE_BRIGHT),
    ("Tier 2: Regional Hubs (1-2MW)", "3+ hubs \u2022 Training GPUs \u2022 Dense peering", Inches(4.2), BLUE_MID),
    ("Tier 1: Edge Nodes (200kW-500kW)", "100s-1000s nodes \u2022 OZ-deployed \u2022 Mesh-peered", Inches(4.8), CARD_BORDER),
]
for label, sub, y, border in tiers:
    tw = Inches(4.5) if "Tier 3" in label else Inches(5) if "Tier 2" in label else tier_w
    tx = rx + (tier_w - tw) // 2
    add_card(slide, tx, y, tw, Inches(0.5), border_color=border)
    add_textbox(slide, tx + Inches(0.1), y + Inches(0.02), tw - Inches(0.2),
                Inches(0.25), label, font_size=11, color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, tx + Inches(0.1), y + Inches(0.25), tw - Inches(0.2),
                Inches(0.2), sub, font_size=9, color=SILVER_MID,
                alignment=PP_ALIGN.CENTER)

# Stats row at bottom right
rstats = [("99.9999%+", "Network Uptime"), ("<5ms", "Edge Latency"), ("60 days", "Deploy Time")]
for i, (v, l) in enumerate(rstats):
    sx = rx + Inches(i * 1.8)
    add_textbox(slide, sx, Inches(5.7), Inches(1.7), Inches(0.4), v,
                font_size=20, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, sx, Inches(6.1), Inches(1.7), Inches(0.3), l,
                font_size=8, color=SILVER_MID, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 5 — AI-NATIVE OPERATIONS
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "KEY DIFFERENTIATOR")
add_title(slide, L, Inches(0.7), Inches(11), "AI-Native Operations: The Economic Unlock")
add_subtitle_text(slide, L, Inches(1.4), Inches(10),
    "Previous distributed datacenter models failed because sub-2MW sites can't support "
    "traditional staffing costs. AI changes the math entirely.")

# Table on left
build_table(slide, L, Inches(2.6), Inches(6.2),
    [
        ["Facilities staff (24/7 techs)", "15-20%", ("Yes \u2014 predictive maintenance + dispatch", GREEN)],
        ["Network operations (NOC)", "10-15%", ("Yes \u2014 AI monitoring + auto-remediation", GREEN)],
        ["Sales & customer mgmt", "10-15%", ("Yes \u2014 AI onboarding + self-service", GREEN)],
        ["Billing & finance", "5-8%", ("Yes \u2014 automated metering + invoicing", GREEN)],
        ["Compliance & reporting", "5-10%", ("Partial \u2014 AI generates, human signs off", AMBER)],
        ["Power & cooling", "30-40%", ("Optimizable \u2014 AI thermal + demand response", GREEN)],
    ],
    col_widths=[3, 1.5, 4],
    headers=["Cost Category", "Traditional %", "AI Automated?"]
)

# Right side cards
rx = Inches(7.4)
rw = Inches(5.1)

# Result card
add_card(slide, rx, Inches(2.6), rw, Inches(2.1), border_color=GREEN)
add_textbox(slide, rx + Inches(0.2), Inches(2.7), rw - Inches(0.4), Inches(0.3),
            "The Result", font_size=14, color=GREEN, bold=True)
tf = add_rich_textbox(slide, rx + Inches(0.2), Inches(3.05), rw - Inches(0.4), Inches(1.5))
add_paragraph(tf, "1 human operator per 20-50 edge nodes", font_size=12, color=SILVER_LIGHT, bold=True)
add_paragraph(tf, "200 nodes need 4-10 people, not the 600-1,000 a traditional operator would require.", font_size=11, color=SILVER_MID)
add_paragraph(tf, "", font_size=6)
add_paragraph(tf, "AI handles >95% of operational tasks \u2014 onboarding, provisioning, billing, monitoring, maintenance, and incident response.", font_size=11, color=SILVER_MID)

# Agents card
add_card(slide, rx, Inches(4.9), rw, Inches(2.3))
add_textbox(slide, rx + Inches(0.2), Inches(5.0), rw - Inches(0.4), Inches(0.3),
            "Five Specialized AI Agents", font_size=13, color=WHITE, bold=True)
agents = ["Customer Onboarding Agent", "Provisioning Agent", "Billing & Revenue Agent",
          "Predictive Maintenance Agent", "SLA Guardian Agent"]
add_bullet_list(slide, rx + Inches(0.2), Inches(5.4), rw - Inches(0.4), agents, font_size=11)


# ═══════════════════════════════════════════════════
# SLIDE 6 — TARGET MARKETS
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "MARKET")
add_title(slide, L, Inches(0.7), Inches(11), "Six Target Constituencies, One Network")

markets = [
    ("Communities & Local Gov", "Public safety (NG911, FirstNet), smart-city sensors, utility SCADA, municipal applications."),
    ("Startups & Developers", "Edge compute without building your own. AI inference, low-latency APIs, and pay-per-use pricing."),
    ("Blockchain & Web3", "Enterprise-grade DePIN backbone. Validator hosting, DePIN compute, and token settlement."),
    ("Regional Fintech", "Data residency compliance, sub-50ms fraud detection, local payment processing."),
    ("Government & Defense", "Sovereign infrastructure. FedRAMP, CJIS, ITAR compliance paths. SCIF-compatible buildout."),
    ("Telcos & ISPs", "Extend edge footprint without CapEx. Carrier-neutral peering, 5G edge compute, CDN offload."),
]
cw = Inches(3.8)
ch = Inches(1.7)
for i, (title, desc) in enumerate(markets):
    col = i % 3
    row = i // 3
    cl = L + Inches(col * 4)
    ct = Inches(1.6) + Inches(row * 1.9)
    add_card(slide, cl, ct, cw, ch)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.15), cw - Inches(0.4),
                Inches(0.3), title, font_size=13, color=WHITE, bold=True)
    add_textbox(slide, cl + Inches(0.2), ct + Inches(0.5), cw - Inches(0.4),
                ch - Inches(0.6), desc, font_size=11, color=SILVER_MID)

# Bottom stats
bstats = [("$500B+", "Global Edge Computing\nTAM by 2030"),
          ("$25B+", "DePIN Infrastructure\nMarket"),
          ("8,764", "Opportunity Zones\nfor Deployment")]
for i, (v, l) in enumerate(bstats):
    sx = L + Inches(i * 4)
    add_card(slide, sx, Inches(5.6), Inches(3.8), Inches(1.2))
    add_textbox(slide, sx, Inches(5.7), Inches(3.8), Inches(0.5), v,
                font_size=28, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, sx, Inches(6.2), Inches(3.8), Inches(0.5), l,
                font_size=9, color=SILVER_MID, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 7 — TECHNOLOGY
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "TECHNOLOGY")
add_title(slide, L, Inches(0.7), Inches(11), "Four Hardware Domains, One Software Fabric")

tech_cards = [
    ("C", "Compute", "AMD EPYC / Intel Xeon / Ampere Altra Max. 256GB-1TB DDR5. 20-40kW/rack.", BLUE_LIGHT),
    ("S", "Storage", "NVMe SSD (hot) + HDD (warm). 100TB-2PB per site. Erasure coding across 3+ nodes.", GREEN),
    ("N", "Connectivity", "100-400GbE internal. 10-100Gbps backhaul. Direct peering with ISPs, CDNs, cloud on-ramps.", AMBER),
    ("AI", "AI Accelerators", "Edge: L4 (72W), L40S (300W), MI300X. Hubs: H100/H200/B200/GB200. Direct liquid cooling.", RGBColor(0xA8, 0x55, 0xF7)),
]
cw = Inches(2.85)
for i, (icon, title, desc, icon_color) in enumerate(tech_cards):
    cl = L + Inches(i * 3)
    add_card(slide, cl, Inches(1.5), cw, Inches(1.8))
    add_textbox(slide, cl + Inches(0.2), Inches(1.6), Inches(0.5), Inches(0.35),
                icon, font_size=14, color=icon_color, bold=True)
    add_textbox(slide, cl + Inches(0.2), Inches(1.95), cw - Inches(0.4), Inches(0.3),
                title, font_size=13, color=WHITE, bold=True)
    add_textbox(slide, cl + Inches(0.2), Inches(2.3), cw - Inches(0.4), Inches(0.8),
                desc, font_size=10, color=SILVER_MID)

# Software Stack table (left)
build_table(slide, L, Inches(3.6), Inches(5.8),
    [
        [("Layer 4", BLUE_LIGHT), "AI Management \u2014 Onboarding, Provisioning, Billing, SLA agents"],
        [("Layer 3", BLUE_LIGHT), "Orchestration \u2014 Kubernetes (K3s/RKE2), Istio, AI workload scheduler"],
        [("Layer 2", BLUE_LIGHT), "Infrastructure \u2014 SDN (OVS/VPP), Storage (Ceph/MinIO), AI-controlled DCIM"],
        [("Layer 1", BLUE_LIGHT), "Hardware \u2014 BMC/Redfish, GPU drivers, SONiC/Cumulus switches"],
    ],
    col_widths=[1.2, 5],
    headers=["Software Stack", ""]
)

# Security (right)
add_textbox(slide, Inches(7.4), Inches(3.6), Inches(5), Inches(0.3),
            "Security (Defense-in-Depth)", font_size=14, color=WHITE, bold=True)
sec_items = [
    "Zero-trust networking (mTLS everywhere)",
    "Hardware root of trust (TPM 2.0, measured boot)",
    "Confidential computing (SEV-SNP / TDX)",
    "Physical security (biometric, surveillance, tamper-evident)",
    "FedRAMP, SOC 2, HIPAA, CJIS, ITAR paths from Day 1",
]
add_bullet_list(slide, Inches(7.4), Inches(4.05), Inches(5), sec_items, font_size=11)


# ═══════════════════════════════════════════════════
# SLIDE 8 — DEPIN BACKBONE
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "DEPIN STRATEGY")
add_title(slide, L, Inches(0.7), Inches(11), "The Enterprise-Grade Backbone DePIN Needs")
add_subtitle_text(slide, L, Inches(1.35), Inches(10),
    "ANDD doesn't compete with DePIN projects \u2014 it completes them.")

# Left: comparison table
build_table(slide, L, Inches(2.3), Inches(5.8),
    [
        ["Uptime", ("90-98%", RED), ("99.99% SLA-backed", GREEN)],
        ["Redundancy", ("None", RED), ("N+1 power, cooling, network", GREEN)],
        ["Physical Security", ("None", RED), ("Biometric + surveillance", GREEN)],
        ["Compliance", ("None", RED), ("FedRAMP, SOC 2, HIPAA", GREEN)],
        ["Connectivity", ("Residential", RED), ("Multi-provider, SLA-backed", GREEN)],
        ["Data Sovereignty", ("Unknown", RED), ("Per-tenant geographic controls", GREEN)],
    ],
    col_widths=[2, 2, 2.5],
    headers=["Dimension", "Consumer DePIN", "ANDD"]
)

# Right: layered architecture
rx = Inches(7.2)
add_textbox(slide, rx, Inches(2.2), Inches(5), Inches(0.3),
            "Layered Architecture", font_size=14, color=WHITE, bold=True)

layers = [
    ("Layer 4 \u2014 DePIN Application", "Helium 5G, Render, Akash, io.net, custom projects", RGBColor(0xA8, 0x55, 0xF7)),
    ("Layer 3 \u2014 DePIN Protocol", "Token incentives, proofs, marketplace, governance", RGBColor(0xA8, 0x55, 0xF7)),
    ("Layer 2 \u2014 ANDD Physical Infrastructure", "Enterprise-grade compute, storage, GPU, connectivity", BLUE_LIGHT),
    ("Layer 1 \u2014 ANDD AI Operations", "Autonomous provisioning, SLA enforcement, billing", BLUE_LIGHT),
]
for i, (label, desc, color) in enumerate(layers):
    y = Inches(2.6) + Inches(i * 0.75)
    add_card(slide, rx, y, Inches(5.3), Inches(0.65), border_color=color)
    add_textbox(slide, rx + Inches(0.15), y + Inches(0.02), Inches(5), Inches(0.25),
                label, font_size=9, color=color, bold=True)
    add_textbox(slide, rx + Inches(0.15), y + Inches(0.3), Inches(5), Inches(0.25),
                desc, font_size=10, color=SILVER_LIGHT)

add_textbox(slide, rx, Inches(5.7), Inches(5.3), Inches(0.3),
            "DePIN projects own protocol + application layers. ANDD owns infrastructure + operations.",
            font_size=10, color=SILVER_MID, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 9 — OPPORTUNITY ZONES & INVESTOR INCENTIVES
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.3), "INVESTOR INCENTIVES")
add_title(slide, L, Inches(0.6), Inches(11), "Opportunity Zone Alignment: Powerful Tax Benefits", font_size=28)
add_subtitle_text(slide, L, Inches(1.2), Inches(11),
    "OZ program made permanent by the One Big Beautiful Bill Act of 2025. "
    "ANDD deployment in 8,764 designated tracts unlocks triple-layer tax incentives.", font_size=14)

# 3 tier cards
oz_tiers = [
    ("Tier 1", "Capital Gains Deferral", "Defer tax on eligible capital gains by reinvesting into a Qualified Opportunity Fund. Rolling 5-year window.", CARD_BORDER),
    ("Tier 2", "Basis Step-Up", "10% step-up at 5 years. Up to 30% for rural OZ investments via Qualified Rural Opportunity Funds.", CARD_BORDER),
    ("Tier 3", "10-Year Exclusion", "ZERO federal capital gains tax on ALL appreciation of the new investment when held 10+ years.", GREEN),
]
for i, (tier, title, desc, border) in enumerate(oz_tiers):
    cl = L + Inches(i * 4)
    add_card(slide, cl, Inches(2.1), Inches(3.8), Inches(1.7), border_color=border)
    add_textbox(slide, cl, Inches(2.15), Inches(3.8), Inches(0.25), tier,
                font_size=9, color=BLUE_LIGHT if i < 2 else GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, cl + Inches(0.2), Inches(2.4), Inches(3.4), Inches(0.3), title,
                font_size=14, color=WHITE if i < 2 else GREEN, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, cl + Inches(0.2), Inches(2.75), Inches(3.4), Inches(0.9), desc,
                font_size=11, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# Community Impact table (left)
add_textbox(slide, L, Inches(3.95), Inches(5.5), Inches(0.3),
            "Per-Site Community Impact (200kW Node)", font_size=13, color=WHITE, bold=True)
build_table(slide, L, Inches(4.3), Inches(5.5),
    [
        ["Construction jobs", "15-30 (6-12 mo build)"],
        ["Permanent operations jobs", "1-3 technicians"],
        ["Annual property tax revenue", "$50K-$150K"],
        ["Annual utility revenue (local)", "$150K-$300K"],
        ["Indirect multiplier", "1.5-2.0x direct spend"],
    ],
    col_widths=[3, 2]
)

# Funding streams (right)
add_textbox(slide, Inches(7.2), Inches(3.95), Inches(5.3), Inches(0.3),
            "Additional Federal Funding Streams", font_size=13, color=WHITE, bold=True)
funding = [
    "DOE GRIP Program: $10.5B for microgrids & distributed energy",
    "DOE Loan Programs Office: $400B+ lending authority",
    "NTIA BEAD: $42.45B for broadband co-location",
    "IRA Tax Credits: 30-50% ITC for solar, BESS, fuel cells",
    "USDA REAP: Grants/loans for rural renewable energy",
]
add_bullet_list(slide, Inches(7.2), Inches(4.35), Inches(5.3), funding, font_size=11)


# ═══════════════════════════════════════════════════
# SLIDE 10 — BUSINESS MODEL
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.3), "BUSINESS MODEL")
add_title(slide, L, Inches(0.6), Inches(11), "Multi-Rail Revenue Architecture")

# Revenue Streams table (left)
add_textbox(slide, L, Inches(1.3), Inches(5.5), Inches(0.3),
            "Revenue Streams", font_size=13, color=WHITE, bold=True)
build_table(slide, L, Inches(1.65), Inches(5.5),
    [
        ["Starter", "Monthly post-paid", "Startups, developers"],
        ["Professional", "Monthly/Annual", "Mid-market, fintech"],
        ["Enterprise", "Annual contracts (15-20% discount)", "Large enterprise, telcos"],
        ["Government", "Multi-year (3-5 yr)", "Federal, state, local"],
        ["DePIN", "Real-time micro-txns", "Web3, blockchain projects"],
    ],
    col_widths=[1.5, 3, 2.5],
    headers=["Tier", "Model", "Customer"]
)

# Payment Rails (left, below table)
add_textbox(slide, L, Inches(4.2), Inches(5.5), Inches(0.3),
            "Payment Rails", font_size=13, color=WHITE, bold=True)
rails = [
    "Fiat: Credit card, ACH, wire, PO-backed (via Stripe/Adyen)",
    "Stablecoin: USDC/USDT on Ethereum, Solana, L2s",
    "Micro-transactions: Payment channels for sub-cent settlement",
    "Smart Contract SLAs: Automatic credit enforcement on-chain",
]
add_bullet_list(slide, L, Inches(4.55), Inches(5.5), rails, font_size=11)

# Unit Economics (right)
rx = Inches(7.2)
add_textbox(slide, rx, Inches(1.3), Inches(5.3), Inches(0.3),
            "Unit Economics (200kW Edge Node)", font_size=13, color=WHITE, bold=True)
build_table(slide, rx, Inches(1.65), Inches(5.3),
    [
        ["CapEx per node", "$1.5M-$2.5M"],
        ["Annual revenue (at utilization)", "$500K-$1M+"],
        ["Traditional OpEx (staffing)", ("$400K+ (margin killer)", RED)],
        ["ANDD AI-native OpEx", ("$80K-$150K", GREEN)],
        ["Power cost (@ $0.08/kWh)", "$140K/yr"],
        ["Connectivity", "$60K-$120K/yr"],
    ],
    col_widths=[3, 2]
)

# Margin card
add_card(slide, rx, Inches(4.2), Inches(5.3), Inches(1.2), border_color=GREEN)
add_textbox(slide, rx + Inches(0.2), Inches(4.3), Inches(4.9), Inches(0.3),
            "Margin Unlock", font_size=13, color=GREEN, bold=True)
add_textbox(slide, rx + Inches(0.2), Inches(4.6), Inches(4.9), Inches(0.7),
            "AI-native operations reduce staffing costs by 60-75%, making sub-2MW facilities "
            "margin-positive for the first time. Traditional model: margin-negative below 5MW. "
            "ANDD: profitable at 200kW.",
            font_size=11, color=SILVER_LIGHT)

# Energy card
add_card(slide, rx, Inches(5.6), Inches(5.3), Inches(1.2))
add_textbox(slide, rx + Inches(0.2), Inches(5.7), Inches(4.9), Inches(0.3),
            "Energy Revenue Upside", font_size=13, color=WHITE, bold=True)
add_textbox(slide, rx + Inches(0.2), Inches(6.0), Inches(4.9), Inches(0.7),
            "On-site solar + BESS generates $50K-$200K/yr in grid services revenue "
            "(demand response, frequency regulation). 2-4 year payback after IRA credits.",
            font_size=11, color=SILVER_MID)


# ═══════════════════════════════════════════════════
# SLIDE 11 — WHY WE WIN
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "COMPETITIVE ADVANTAGE")
add_title(slide, L, Inches(0.7), Inches(11), "Why Previous Models Failed. Why ANDD Wins.")

# Failure mode table (left)
build_table(slide, L, Inches(1.5), Inches(6.2),
    [
        ["Operational cost", ("Too high <2MW", RED), ("AI ops: 1 human per 20-50 nodes", GREEN)],
        ["Location selection", ("Deployer-driven", RED), ("AI demand modeling", GREEN)],
        ["Hardware reliability", ("Consumer-grade", RED), ("Enterprise-grade, AI-monitored", GREEN)],
        ["Utilization", ("Supply/demand mismatch", RED), ("AI capacity planning", GREEN)],
        ["SLA enforcement", ("Reputation-only", RED), ("Smart contract SLAs", GREEN)],
        ["Compliance", ("Ignored", RED), ("FedRAMP, SOC 2, HIPAA built-in", GREEN)],
        ["Network effects", ("Isolated nodes", RED), ("Mesh fabric", GREEN)],
        ["Token value", ("Speculation-driven", RED), ("Utility-driven, real revenue", GREEN)],
    ],
    col_widths=[2, 2, 3],
    headers=["Challenge", "How Others Failed", "ANDD"]
)

# Right: competitor cards
rx = Inches(7.4)
rw = Inches(5.1)
comps = [
    ("EdgeConneX / Vapor IO / EdgeMicro",
     "Deployed small edge sites but relied on traditional human operations. Could not achieve economics below 1-2MW."),
    ("Helium",
     "900K+ hotspots deployed. Couldn't guarantee coverage or uptime where it mattered. Consumer hardware = no enterprise adoption."),
    ("Filecoin",
     "22+ EiB capacity. Mostly empty \"committed capacity.\" Industrial miners dominate, undermining decentralization."),
    ("Telco Edge (MEC)",
     "AT&T, Verizon announced edge strategies. Underdelivered due to carrier lock-in and org misalignment. ANDD is carrier-neutral."),
]
for i, (title, desc) in enumerate(comps):
    cy = Inches(1.5) + Inches(i * 1.45)
    add_card(slide, rx, cy, rw, Inches(1.3))
    add_textbox(slide, rx + Inches(0.15), cy + Inches(0.1), rw - Inches(0.3),
                Inches(0.3), title, font_size=12, color=WHITE, bold=True)
    add_textbox(slide, rx + Inches(0.15), cy + Inches(0.4), rw - Inches(0.3),
                Inches(0.8), desc, font_size=10, color=SILVER_MID)


# ═══════════════════════════════════════════════════
# SLIDE 12 — RESILIENCE & NATIONAL SECURITY
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "NATIONAL SECURITY VALUE")
add_title(slide, L, Inches(0.7), Inches(11), "Resilience the Nation Needs")
add_subtitle_text(slide, L, Inches(1.35), Inches(10),
    "ANDD's distributed architecture provides resilience that no single-campus model can match \u2014 "
    "for payments, energy, emergency services, and defense.")

res_cards = [
    ("Payments", "Distributed processing for card authorization, ACH, FedNow. Local store-and-forward during backbone disruptions."),
    ("Energy Grid", "Distributed SCADA/EMS hosting. Virtual power plant from aggregated BESS. Microgrid islanding for grid emergencies."),
    ("Emergency Services", "Local NG911 hosting. FirstNet edge compute for first responders. Emergency ops center computing."),
    ("Defense", "Sovereign infrastructure not dependent on hyperscale vendors. SCIF-capable sites. SIPRNet/NIPRNet gateway."),
]
cw = Inches(2.85)
for i, (title, desc) in enumerate(res_cards):
    cl = L + Inches(i * 3)
    add_card(slide, cl, Inches(2.4), cw, Inches(1.8))
    add_textbox(slide, cl + Inches(0.15), Inches(2.5), cw - Inches(0.3), Inches(0.3),
                title, font_size=13, color=WHITE, bold=True)
    add_textbox(slide, cl + Inches(0.15), Inches(2.85), cw - Inches(0.3), Inches(1.2),
                desc, font_size=10, color=SILVER_MID)

# Comparison boxes at bottom
add_card(slide, L, Inches(4.6), Inches(5.5), Inches(2.2), border_color=RED)
add_textbox(slide, L, Inches(4.7), Inches(5.5), Inches(0.25),
            "SINGLE HYPERSCALE CAMPUS", font_size=9, color=RED, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, L, Inches(5.0), Inches(5.5), Inches(0.6), "67 min",
            font_size=40, color=RED, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, L, Inches(5.6), Inches(5.5), Inches(0.3),
            "Expected annual downtime", font_size=12, color=SILVER_MID,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, L, Inches(5.95), Inches(5.5), Inches(0.3),
            "99.99% uptime + 1% catastrophic failure risk/yr",
            font_size=10, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)

add_card(slide, Inches(7), Inches(4.6), Inches(5.5), Inches(2.2), border_color=GREEN)
add_textbox(slide, Inches(7), Inches(4.7), Inches(5.5), Inches(0.25),
            "ANDD MESH (100 NODES)", font_size=9, color=GREEN, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(7), Inches(5.0), Inches(5.5), Inches(0.6), "99.9999%+",
            font_size=40, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(7), Inches(5.6), Inches(5.5), Inches(0.3),
            "Network-level availability", font_size=12, color=SILVER_MID,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(7), Inches(5.95), Inches(5.5), Inches(0.3),
            "Graceful degradation, not catastrophic failure",
            font_size=10, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 13 — COORDINATION & SETTLEMENT
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.3), "COORDINATION & SETTLEMENT")
add_title(slide, L, Inches(0.6), Inches(11), "Network-Native Consensus for Sovereign Operations", font_size=28)
add_subtitle_text(slide, L, Inches(1.2), Inches(10),
    "A distributed network of AI-managed datacenters requires a coordination and settlement layer "
    "that is as resilient as the infrastructure it serves.", font_size=14)

# Left side
add_textbox(slide, L, Inches(2.0), Inches(5.5), Inches(0.3),
            "The Problem with External Chains", font_size=13, color=WHITE, bold=True)
ext_problems = [
    "Solana outage = DePIN settlement halted",
    "Ethereum gas spike = micro-transactions uneconomical",
    "L2 sequencer dependency = sovereignty gap",
    "Application-layer consensus can't leverage ANDD's mesh fabric",
    "Traditional chains break under asymmetric network partitions",
]
add_bullet_list(slide, L, Inches(2.35), Inches(5.5), ext_problems, font_size=11)

add_textbox(slide, L, Inches(4.3), Inches(5.5), Inches(0.3),
            "What ANDD Needs", font_size=13, color=WHITE, bold=True)
build_table(slide, L, Inches(4.6), Inches(5.8),
    [
        [("Consensus", BLUE_LIGHT), "BFT integrated into the network fabric \u2014 not a Layer 7 overlay"],
        [("Propagation", BLUE_LIGHT), "Lightweight messages that work on LEO satellite and constrained backhaul"],
        [("Partitions", BLUE_LIGHT), "Both sides of a fiber cut keep transacting; resync when reconnected"],
        [("Privacy", BLUE_LIGHT), "Commercially sensitive billing and tenant data stays private"],
        [("AI Integration", BLUE_LIGHT), "Machine-readable state so AI agents can reason about on-chain data"],
    ],
    col_widths=[1.5, 5]
)

# Right: sovereign stack
rx = Inches(7.2)
add_textbox(slide, rx, Inches(2.0), Inches(5.3), Inches(0.3),
            "The Full Sovereign Stack", font_size=13, color=WHITE, bold=True)

stack_layers = [
    ("Application", "Customer workloads, DePIN protocols, gov services", SILVER_MID),
    ("Smart Contract Execution", "Privacy-preserving runtime for SLAs, billing, DePIN settlement", RGBColor(0xA8, 0x55, 0xF7)),
    ("Consensus & Settlement", "Network-native BFT consensus on ANDD hub infrastructure", RGBColor(0xA8, 0x55, 0xF7)),
    ("Network Fabric", "BIER multicast, SRv6, mesh interconnection", BLUE_LIGHT),
    ("AI Operations", "Autonomous management reading/writing on-chain state", BLUE_LIGHT),
    ("Physical Infrastructure", "Compute, GPU, storage, power, security", SILVER_MID),
    ("Energy & Resilience", "Microgrids, BESS, solar, fuel cells", SILVER_MID),
]
for i, (label, desc, color) in enumerate(stack_layers):
    y = Inches(2.4) + Inches(i * 0.62)
    add_card(slide, rx, y, Inches(5.3), Inches(0.55), border_color=color)
    add_textbox(slide, rx + Inches(0.12), y + Inches(0.02), Inches(5), Inches(0.22),
                label.upper(), font_size=8, color=color, bold=True)
    add_textbox(slide, rx + Inches(0.12), y + Inches(0.25), Inches(5), Inches(0.22),
                desc, font_size=10, color=SILVER_LIGHT)

add_textbox(slide, rx, Inches(6.8), Inches(5.3), Inches(0.25),
            "No external dependency at any layer. Fully sovereign.",
            font_size=10, color=SILVER_MID, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 14 — ROADMAP
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.4), "ROADMAP")
add_title(slide, L, Inches(0.7), Inches(11), "Path to Continental Coverage")

phases = [
    ("Phase 1 \u2014 Foundation", "Months 1-12", [
        "AI management layer architecture",
        "200kW reference design certified",
        "3-5 pilot sites in diverse geographies",
        "SOC 2 Type I certification",
        "Beta customers across 3+ segments",
        "QOF structure established",
    ]),
    ("Phase 2 \u2014 Network Formation", "Months 12-24", [
        "20-50 edge nodes in regional clusters",
        "2-3 regional hubs deployed",
        "AI handles >90% of ops autonomously",
        "First government customers",
        "2-3 DePIN projects onboarded",
        "FedRAMP Moderate authorization",
    ]),
    ("Phase 3 \u2014 Scale", "Months 24-48", [
        "100-300 nodes, 10+ regional hubs",
        "Full mesh fabric operational",
        "Smart contract SLAs live",
        "Federal government customers",
        "Defense network integration",
        "10+ active DePIN projects",
    ]),
    ("Phase 4 \u2014 Continental Coverage", "Months 48-72", [
        "500-1,000+ edge nodes nationwide",
        "Full AI autonomy for standard ops",
        "International expansion (allied nations)",
        "Self-sustaining: revenue funds growth",
        "VPP grid services at scale",
        "Critical national infrastructure status",
    ]),
]

cw = Inches(2.85)
for i, (title, timeline, items) in enumerate(phases):
    cl = L + Inches(i * 3)
    border = BLUE_BRIGHT if i == 0 else CARD_BORDER
    add_card(slide, cl, Inches(1.5), cw, Inches(3.8), border_color=border)
    add_textbox(slide, cl + Inches(0.15), Inches(1.55), cw - Inches(0.3), Inches(0.25),
                title.upper(), font_size=9, color=BLUE_LIGHT, bold=True)
    add_textbox(slide, cl + Inches(0.15), Inches(1.85), cw - Inches(0.3), Inches(0.25),
                timeline, font_size=11, color=SILVER_LIGHT, bold=True)
    add_bullet_list(slide, cl + Inches(0.15), Inches(2.2), cw - Inches(0.3),
                    items, font_size=10, color=SILVER_LIGHT)

# Bottom stats
rm_stats = [("3-5", "Pilot Sites Year 1"), ("50", "Nodes by Year 2"),
            ("300", "Nodes by Year 4"), ("1,000+", "Nodes by Year 6")]
for i, (v, l) in enumerate(rm_stats):
    sx = L + Inches(i * 3)
    add_textbox(slide, sx, Inches(5.7), Inches(2.85), Inches(0.5), v,
                font_size=24, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, sx, Inches(6.15), Inches(2.85), Inches(0.3), l,
                font_size=9, color=SILVER_MID, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SLIDE 15 — ENERGY & SUSTAINABILITY
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_section_label(slide, L, Inches(0.3), "ENERGY STRATEGY")
add_title(slide, L, Inches(0.6), Inches(11), "Clean, Resilient, Revenue-Generating Power")

# Left: microgrid table
add_textbox(slide, L, Inches(1.2), Inches(5.5), Inches(0.3),
            "Microgrid Architecture (Per Site)", font_size=13, color=WHITE, bold=True)
build_table(slide, L, Inches(1.55), Inches(5.8),
    [
        ["Utility Grid", "Primary power source, metered for demand response"],
        ["On-Site Solar", "30-50% energy offset, IRA 30-50% ITC"],
        ["BESS (LFP Battery)", "2-4hr backup + peak shaving + grid services"],
        ["Fuel Cell (PEM/SOFC)", "Clean backup, 50-65% efficiency, zero local emissions"],
        ["AI Microgrid Controller", "Islanding-capable, optimizes cost + resilience"],
    ],
    col_widths=[2, 4],
    headers=["Component", "Role"]
)

# Left: cooling table
add_textbox(slide, L, Inches(4.1), Inches(5.5), Inches(0.3),
            "Cooling Efficiency", font_size=13, color=WHITE, bold=True)
build_table(slide, L, Inches(4.4), Inches(5.8),
    [
        ["Air cooling (DX)", ("1.40-1.80", RED), "Industry legacy"],
        ["Direct liquid (DLC)", ("1.10-1.20", GREEN), "ANDD baseline for GPU racks"],
        ["Immersion", ("1.02-1.06", GREEN), "Max density option"],
    ],
    col_widths=[2, 1.5, 3],
    headers=["Technology", "PUE", "Impact"]
)
add_textbox(slide, L, Inches(5.75), Inches(5.5), Inches(0.5),
            "Moving from air to immersion saves ~300kW per MW \u2014 effectively +30% usable compute capacity.",
            font_size=10, color=SILVER_MID)

# Right: energy economics
rx = Inches(7.2)
add_textbox(slide, rx, Inches(1.2), Inches(5.3), Inches(0.3),
            "Energy Economics (200kW Node)", font_size=13, color=WHITE, bold=True)
build_table(slide, rx, Inches(1.55), Inches(5.3),
    [
        ["100kW solar array", "~$150K installed"],
        ["500kWh BESS", "~$200K installed"],
        ["IRA ITC (30-50%)", ("-$105K to -$175K", GREEN)],
        ["Annual utility savings", ("$40K-$80K", GREEN)],
        ["Peak shaving value", ("$24K-$150K/yr", GREEN)],
        ["Grid services revenue", ("$50K-$200K/yr per MW", GREEN)],
        ["Effective payback", ("2-4 years", GREEN)],
    ],
    col_widths=[3, 2]
)

# VPP card
add_card(slide, rx, Inches(4.7), Inches(5.3), Inches(1.8), border_color=GREEN)
add_textbox(slide, rx + Inches(0.2), Inches(4.8), Inches(4.9), Inches(0.3),
            "Virtual Power Plant at Scale", font_size=13, color=GREEN, bold=True)
add_textbox(slide, rx + Inches(0.2), Inches(5.15), Inches(4.9), Inches(1.2),
            "Distributed BESS across hundreds of sites aggregates into a VPP providing grid services \u2014 "
            "frequency regulation, demand response, capacity reserves \u2014 with geographic diversity that "
            "reduces correlated failure risk. Additional revenue stream on top of compute services.",
            font_size=11, color=SILVER_LIGHT)


# ═══════════════════════════════════════════════════
# SLIDE 16 — THE ASK
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_textbox(slide, Inches(1.5), Inches(0.5), Inches(10), Inches(0.25),
            "THE OPPORTUNITY", font_size=11, color=BLUE_BRIGHT, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(1), Inches(0.9), Inches(11.333), Inches(1.0),
            "Invest in America's Distributed Compute Future",
            font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(2), Inches(2.0), Inches(9.333), Inches(0.8),
            "ANDD is building the infrastructure layer the nation needs \u2014 sovereign, resilient, "
            "AI-managed, and aligned with the most powerful tax incentives in a generation.",
            font_size=16, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# 3 stat cards
ask_stats = [
    ("0%", "Federal capital gains tax on\nappreciation after 10-year OZ hold", GREEN),
    ("15-20yr", "Datacenter asset useful life \u2014\nnatural alignment with OZ hold period", BLUE_LIGHT),
    ("$50B+", "Federal funding aligned with\nANDD's deployment model", BLUE_LIGHT),
]
for i, (v, l, vc) in enumerate(ask_stats):
    cl = Inches(1.2) + Inches(i * 3.8)
    add_card(slide, cl, Inches(3.1), Inches(3.5), Inches(1.5))
    add_textbox(slide, cl, Inches(3.2), Inches(3.5), Inches(0.6), v,
                font_size=28, color=vc, bold=True, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, cl + Inches(0.2), Inches(3.8), Inches(3.1), Inches(0.6), l,
                font_size=11, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# 3 value props
props = [
    ("CURRENT INCOME", "Revenue from infrastructure services from Year 1"),
    ("APPRECIATION", "Asset value grows as network scales and utilization increases"),
    ("NATIONAL IMPACT", "Jobs, connectivity, and AI capabilities for underserved communities"),
]
for i, (title, desc) in enumerate(props):
    cl = Inches(1.2) + Inches(i * 3.8)
    add_card(slide, cl, Inches(5.0), Inches(3.5), Inches(1.3))
    add_textbox(slide, cl + Inches(0.15), Inches(5.1), Inches(3.2), Inches(0.25),
                title, font_size=9, color=BLUE_LIGHT, bold=True)
    add_textbox(slide, cl + Inches(0.15), Inches(5.4), Inches(3.2), Inches(0.7),
                desc, font_size=12, color=SILVER_LIGHT)


# ═══════════════════════════════════════════════════
# SLIDE 17 — CONTACT / CLOSING
# ═══════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

if os.path.exists(LOGO_PATH):
    logo_width = Inches(2.8)
    logo_left = (SLIDE_WIDTH - logo_width) // 2
    slide.shapes.add_picture(LOGO_PATH, logo_left, Inches(1.2), width=logo_width)

add_textbox(slide, Inches(1), Inches(3.5), Inches(11.333), Inches(0.8),
            "Let's Build Together",
            font_size=40, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(4.4), Inches(9.333), Inches(0.8),
            "The question is no longer whether distributed, AI-managed datacenter infrastructure "
            "is technically feasible. The question is how quickly it can be deployed.",
            font_size=16, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# Contact info
add_textbox(slide, Inches(3.5), Inches(5.5), Inches(3), Inches(0.25),
            "EMAIL", font_size=9, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(3.5), Inches(5.75), Inches(3), Inches(0.3),
            "contact@andd.network", font_size=14, color=SILVER_LIGHT, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(6.833), Inches(5.5), Inches(3), Inches(0.25),
            "WEB", font_size=9, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(6.833), Inches(5.75), Inches(3), Inches(0.3),
            "andd.network", font_size=14, color=SILVER_LIGHT, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(2), Inches(6.5), Inches(9.333), Inches(0.3),
            "CONFIDENTIAL \u2014 DO NOT DISTRIBUTE",
            font_size=10, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════
output_path = os.path.join(os.path.dirname(__file__), "ANDD_Pitch_Deck.pptx")
prs.save(output_path)
print(f"Saved: {output_path}")
