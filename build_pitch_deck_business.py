#!/usr/bin/env python3
"""
Build ANDD Business Pitch Deck as .pptx for Google Slides upload.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Color Palette ──
DARK_BG = RGBColor(0x0A, 0x16, 0x28)
DARK_SURFACE = RGBColor(0x11, 0x1D, 0x33)
DARK_CARD = RGBColor(0x16, 0x24, 0x40)
BLUE_BRIGHT = RGBColor(0x3B, 0x82, 0xF6)
BLUE_LIGHT = RGBColor(0x60, 0xA5, 0xFA)
BLUE_DARK = RGBColor(0x1E, 0x40, 0xAF)
SILVER_LIGHT = RGBColor(0xD1, 0xD5, 0xDB)
SILVER_MID = RGBColor(0x9C, 0xA3, 0xAF)
SILVER_DARK = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xE2, 0xE8, 0xF0)
GREEN = RGBColor(0x22, 0xC5, 0x5E)
RED = RGBColor(0xEF, 0x44, 0x44)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
PURE_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def set_slide_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color=None, border_color=None, border_width=Pt(1)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    # Adjust corner rounding
    shape.adjustments[0] = 0.05
    return shape


def add_text_box(slide, left, top, width, height, text="", font_size=14, color=WHITE,
                 bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri", anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf.vertical_anchor = anchor
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_rich_text(slide, left, top, width, height):
    """Return a text frame for building rich paragraphs."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    return tf


def add_paragraph(tf, text="", font_size=14, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                  space_after=Pt(4), space_before=Pt(0), font_name="Calibri"):
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
    p.space_before = space_before
    return p


def add_bullet(tf, text, font_size=13, color=SILVER_LIGHT, bold=False, space_after=Pt(3)):
    p = tf.add_paragraph()
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = "Calibri"
    p.space_after = space_after
    p.space_before = Pt(0)
    # Use triangle bullet
    run = p.add_run()
    run.text = "  " + text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Calibri"
    # Add bullet character at start
    bullet_run = p.runs[0]
    bullet_run.text = "\u25b8  " + text
    return p


def add_stat_box(slide, left, top, width, height, value, label, value_color=BLUE_LIGHT,
                 fill=DARK_CARD, border=None):
    shape = add_shape(slide, left, top, width, height, fill_color=fill, border_color=border or RGBColor(0x1E, 0x3A, 0x5F))
    # Value
    add_text_box(slide, left, top + Inches(0.2), width, Inches(0.6), value,
                 font_size=28, color=value_color, bold=True, alignment=PP_ALIGN.CENTER)
    # Label
    add_text_box(slide, left + Inches(0.1), top + Inches(0.75), width - Inches(0.2), Inches(0.5), label,
                 font_size=9, color=SILVER_MID, bold=False, alignment=PP_ALIGN.CENTER)
    return shape


def section_label(slide, left, top, text):
    add_text_box(slide, left, top, Inches(3), Inches(0.3), text.upper(),
                 font_size=10, color=BLUE_BRIGHT, bold=True)


# ════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_slide_bg(slide)

# Logo
logo_path = os.path.join(os.path.dirname(__file__), "andd.png")
if os.path.exists(logo_path):
    slide.shapes.add_picture(logo_path, Inches(4.9), Inches(0.6), Inches(3.5))

# Title
add_text_box(slide, Inches(1), Inches(2.3), Inches(11.3), Inches(1.2),
             "AI Native Distributed\nDatacenter Network",
             font_size=42, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# Subtitle
add_text_box(slide, Inches(1.5), Inches(3.6), Inches(10.3), Inches(0.8),
             "A commercially scalable network of inference-specific micro datacenters\ndelivering AI models, agents, and on-demand token capacity at the edge",
             font_size=17, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# Stat boxes
add_stat_box(slide, Inches(3.1), Inches(4.7), Inches(2.2), Inches(1.15),
             "$162B", "DC Projects Blocked", value_color=BLUE_LIGHT)
add_stat_box(slide, Inches(5.55), Inches(4.7), Inches(2.2), Inches(1.15),
             "<2MW", "Per Site Footprint", value_color=BLUE_LIGHT)
add_stat_box(slide, Inches(8.0), Inches(4.7), Inches(2.2), Inches(1.15),
             "AI Native", "Autonomous Operations", value_color=GREEN)

# Date and confidential
add_text_box(slide, Inches(1), Inches(6.2), Inches(11.3), Inches(0.3),
             "Business Overview \u2014 April 2026",
             font_size=12, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(6.7), Inches(11.3), Inches(0.3),
             "CONFIDENTIAL \u2014 DO NOT DISTRIBUTE",
             font_size=9, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "The Problem")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.6),
             "The Datacenter Industry Has Hit a Wall",
             font_size=30, color=WHITE, bold=True)
add_text_box(slide, Inches(0.7), Inches(1.3), Inches(11.5), Inches(0.6),
             "Massive datacenter projects face unprecedented opposition while AI inference demand explodes. The industry needs a fundamentally different approach.",
             font_size=14, color=SILVER_MID)

# Three red stat boxes
add_stat_box(slide, Inches(0.7), Inches(2.1), Inches(3.8), Inches(1.2),
             "$162B", "of datacenter projects\nblocked by state & local pushback", value_color=RED)
add_stat_box(slide, Inches(4.75), Inches(2.1), Inches(3.8), Inches(1.2),
             "70%", "of East Coast internet traffic\nrouted through Northern Virginia alone", value_color=RED)
add_stat_box(slide, Inches(8.8), Inches(2.1), Inches(3.8), Inches(1.2),
             "300MW", "per hyperscale campus \u2014\nequivalent to a small power plant", value_color=RED)

# Left column - Why States Push Back
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

add_text_box(slide, LX, Inches(3.55), COL_W, Inches(0.35),
             "Why States Are Pushing Back", font_size=15, color=RED, bold=True)

tf = add_rich_text(slide, LX, Inches(3.95), COL_W, Inches(3.0))
for item in [
    "Hyperscale campuses overwhelm local power grids",
    "Massive water consumption for cooling (millions of gallons/day)",
    "Communities see burden without proportional economic benefit",
    "Environmental impact reviews blocking permits",
    "Political pressure from residents and local government",
]:
    add_bullet(tf, item, font_size=12, color=SILVER_LIGHT)

# Right column - What This Concentration Means
add_text_box(slide, RX, Inches(3.55), COL_W, Inches(0.35),
             "What This Concentration Means", font_size=15, color=RED, bold=True)

tf = add_rich_text(slide, RX, Inches(3.95), COL_W, Inches(3.0))
for item in [
    "Critical internet functions have no geographic redundancy",
    "No data sovereignty \u2014 governments have zero control over where data lives",
    "AI inference requires low latency that centralized facilities cannot serve at the edge",
    "A single regional disaster could degrade federal, financial, and defense systems simultaneously",
]:
    add_bullet(tf, item, font_size=12, color=SILVER_LIGHT)


# ════════════════════════════════════════════════════════════════
# SLIDE 3 — WHY THIS MAKES SENSE / MARKET OPPORTUNITY
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Market Opportunity")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.6),
             "$162B in Blocked Projects. The Market Needs an Alternative.",
             font_size=28, color=WHITE, bold=True)
add_text_box(slide, Inches(0.7), Inches(1.3), Inches(11.5), Inches(0.5),
             "The demand for compute capacity hasn't gone away \u2014 the deployment model is what's broken.",
             font_size=14, color=SILVER_MID)

# Left column - Blocked pipeline + Environmental
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

# Blocked Pipeline card
add_shape(slide, LX, Inches(2.0), COL_W, Inches(2.5), fill_color=DARK_CARD, border_color=RGBColor(0x4A, 0x1C, 0x1C))
add_text_box(slide, LX + Inches(0.2), Inches(2.1), COL_W - Inches(0.4), Inches(0.35),
             "The Blocked Pipeline", font_size=14, color=RED, bold=True)
tf = add_rich_text(slide, LX + Inches(0.2), Inches(2.45), COL_W - Inches(0.4), Inches(2.0))
for item in [
    "$162B of announced datacenter projects facing delays or cancellation",
    "States including VA, GA, IN, SC imposing moratoriums",
    "Environmental impact reviews adding 12-24+ months to timelines",
    "Grid interconnection queues extending 3-5+ years",
    "Community opposition escalating to state legislation",
]:
    add_bullet(tf, item, font_size=11, color=SILVER_LIGHT)

# Environmental card
add_shape(slide, LX, Inches(4.7), COL_W, Inches(1.8), fill_color=DARK_CARD, border_color=RGBColor(0x4A, 0x3A, 0x0A))
add_text_box(slide, LX + Inches(0.2), Inches(4.8), COL_W - Inches(0.4), Inches(0.35),
             "Environmental Concerns Are Real", font_size=14, color=AMBER, bold=True)
tf = add_rich_text(slide, LX + Inches(0.2), Inches(5.15), COL_W - Inches(0.4), Inches(1.2))
for item in [
    "Single hyperscale campus uses 1-5M gallons of water/day",
    "Concentrated power demand drives new fossil generation",
    "IEA projects DC electricity at 945-1,300 TWh by 2030",
]:
    add_bullet(tf, item, font_size=11, color=SILVER_LIGHT)

# Right column - Why Distributed Solves + Sovereignty
# Distributed card
add_shape(slide, RX, Inches(2.0), COL_W, Inches(2.5), fill_color=DARK_CARD, border_color=RGBColor(0x0E, 0x3A, 0x1E))
add_text_box(slide, RX + Inches(0.2), Inches(2.1), COL_W - Inches(0.4), Inches(0.35),
             "Why Distributed Solves This", font_size=14, color=GREEN, bold=True)
tf = add_rich_text(slide, RX + Inches(0.2), Inches(2.45), COL_W - Inches(0.4), Inches(2.0))
for item in [
    "Power: <2MW per site works within existing grid \u2014 no new generation needed",
    "Permitting: Small footprints within cell tower sites bypass permitting battles",
    "Water: Direct liquid cooling eliminates evaporative cooling towers",
    "Community: Creates local jobs and tax revenue without environmental burden",
]:
    add_bullet(tf, item, font_size=11, color=SILVER_LIGHT)

# Sovereignty card
add_shape(slide, RX, Inches(4.7), COL_W, Inches(1.8), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
add_text_box(slide, RX + Inches(0.2), Inches(4.8), COL_W - Inches(0.4), Inches(0.35),
             "Data Sovereignty Requires Local", font_size=14, color=BLUE_LIGHT, bold=True)
tf = add_rich_text(slide, RX + Inches(0.2), Inches(5.15), COL_W - Inches(0.4), Inches(1.2))
add_paragraph(tf, "States are increasingly mandating that government data remain within their borders. "
              "Municipalities need local compute for 911, traffic, and utility SCADA. "
              "Data sovereignty can only be addressed by local operation \u2014 no cloud policy can substitute for physical proximity.",
              font_size=11, color=SILVER_LIGHT)


# ════════════════════════════════════════════════════════════════
# SLIDE 4 — HOW WE'RE DOING THIS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Our Approach")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.6),
             "Micro Datacenters at Cellular Tower Sites",
             font_size=30, color=WHITE, bold=True)
add_text_box(slide, Inches(0.7), Inches(1.25), Inches(11.5), Inches(0.6),
             "Highly dispersed, inference-specific micro datacenters (<2MW each) deployed at existing cellular tower infrastructure \u2014 "
             "eliminating the permitting, power, and community opposition problems.",
             font_size=13, color=SILVER_MID)

# 4 stat boxes across the top
add_stat_box(slide, Inches(0.7), Inches(2.0), Inches(2.8), Inches(1.1),
             "<2MW", "Per site power draw", value_color=BLUE_LIGHT)
add_stat_box(slide, Inches(3.75), Inches(2.0), Inches(2.8), Inches(1.1),
             "60-90 days", "To deploy (prefab)", value_color=BLUE_LIGHT)
add_stat_box(slide, Inches(6.8), Inches(2.0), Inches(2.8), Inches(1.1),
             "Zero", "New permitting required", value_color=GREEN)
add_stat_box(slide, Inches(9.85), Inches(2.0), Inches(2.8), Inches(1.1),
             "40,000+", "Crown Castle tower sites", value_color=GREEN)

# Crown Castle callout
add_shape(slide, Inches(0.7), Inches(3.3), Inches(5.9), Inches(1.1),
          fill_color=RGBColor(0x12, 0x20, 0x3A), border_color=BLUE_BRIGHT)
add_text_box(slide, Inches(0.9), Inches(3.4), Inches(5.5), Inches(0.9),
             "Crown Castle Agreement: Active discussions to co-locate ANDD micro datacenters at their "
             "40,000+ tower sites across the US. Existing power, connectivity, and site access provide "
             "an immediate deployment pipeline.",
             font_size=12, color=SILVER_LIGHT)

# Right side cards
cards = [
    ("Existing Power & Connectivity", "Tower sites already have utility power feeds and fiber/microwave backhaul. We scale to the grid capacity that's already there."),
    ("Permitting Risk Eliminated", "By staying inside the existing site footprint, we operate under the tower's existing land use permits. No new environmental reviews."),
    ("Geographic Distribution Built-In", "Cell towers are sited for population coverage. We inherit a deployment map optimized for proximity to end users."),
    ("AI Native = Lower Operating Cost", "AI handles provisioning, monitoring, billing, and maintenance. 1 human operator per 20-50 sites, not 5-10 humans per site."),
]

y = Inches(3.3)
for title, desc in cards:
    add_shape(slide, Inches(6.9), y, Inches(5.9), Inches(0.9), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, Inches(7.1), y + Inches(0.05), Inches(5.5), Inches(0.25),
                 title, font_size=12, color=WHITE, bold=True)
    add_text_box(slide, Inches(7.1), y + Inches(0.3), Inches(5.5), Inches(0.55),
                 desc, font_size=10, color=SILVER_MID)
    y += Inches(1.0)


# ════════════════════════════════════════════════════════════════
# SLIDE 5 — WHAT'S NOVEL
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "What's Novel")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.6),
             "An Inference Network, Not Just Datacenters",
             font_size=30, color=WHITE, bold=True)
add_text_box(slide, Inches(0.7), Inches(1.25), Inches(11.5), Inches(0.5),
             "ANDD is building a commercially scalable network of inference-specific resources that makes AI capacity available like a utility.",
             font_size=14, color=SILVER_MID)

# Three feature cards
features = [
    ("AI Model Marketplace", "Customers access a wide catalog of AI models, LLMs, and agents hosted across the network. Consume inference as a service \u2014 no GPU provisioning needed.", RGBColor(0x28, 0x1A, 0x3A)),
    ("Elastic Token Capacity", "Customers purchase AI token capacity on-demand. The network routes to available GPUs across the mesh automatically \u2014 no capacity planning.", RGBColor(0x0E, 0x3A, 0x1E)),
    ("Edge-Native Inference", "Sub-10ms latency for real-time applications: autonomous vehicles, medical devices, industrial control, fraud detection.", RGBColor(0x12, 0x20, 0x3A)),
]

x = Inches(0.7)
for title, desc, bg in features:
    add_shape(slide, x, Inches(1.95), Inches(3.8), Inches(1.5), fill_color=bg, border_color=RGBColor(0x2A, 0x3A, 0x5F))
    add_text_box(slide, x + Inches(0.2), Inches(2.05), Inches(3.4), Inches(0.3),
                 title, font_size=14, color=WHITE, bold=True)
    add_text_box(slide, x + Inches(0.2), Inches(2.4), Inches(3.4), Inches(1.0),
                 desc, font_size=11, color=SILVER_LIGHT)
    x += Inches(4.05)

# Five differentiators
add_text_box(slide, Inches(0.7), Inches(3.7), Inches(6), Inches(0.35),
             "Five Things That Make ANDD Different", font_size=15, color=WHITE, bold=True)

diffs = [
    ("1.", "Cell tower co-location \u2014 40,000+ sites, existing permits, existing power"),
    ("2.", "<2MW per site \u2014 fits within current grid, no new generation needed"),
    ("3.", "AI-native operations \u2014 95%+ of ops automated, 60-75% lower staffing costs"),
    ("4.", "Inference-specific hardware \u2014 optimized for the 60-70% of AI compute that is inference"),
    ("5.", "Network mesh fabric \u2014 nodes cooperate, workloads route to optimal location automatically"),
]

tf = add_rich_text(slide, Inches(0.7), Inches(4.1), Inches(6.5), Inches(3.0))
for num, text in diffs:
    p = tf.add_paragraph()
    run_num = p.add_run()
    run_num.text = num + "  "
    run_num.font.size = Pt(13)
    run_num.font.color.rgb = BLUE_LIGHT
    run_num.font.bold = True
    run_num.font.name = "Calibri"
    run_text = p.add_run()
    run_text.text = text
    run_text.font.size = Pt(12)
    run_text.font.color.rgb = SILVER_LIGHT
    run_text.font.name = "Calibri"
    p.space_after = Pt(4)

# Moat card
add_shape(slide, Inches(7.5), Inches(3.7), Inches(5.2), Inches(2.8), fill_color=DARK_CARD, border_color=RGBColor(0x0E, 0x3A, 0x1E))
add_text_box(slide, Inches(7.7), Inches(3.8), Inches(4.8), Inches(0.3),
             "The Business Moat", font_size=14, color=GREEN, bold=True)
add_text_box(slide, Inches(7.7), Inches(4.15), Inches(4.8), Inches(2.2),
             "Every new site makes the network more valuable.\n\n"
             "\u25b8  More locations = lower latency for more customers\n"
             "\u25b8  More coverage = more addressable market\n"
             "\u25b8  More data = better AI capacity planning\n"
             "\u25b8  More nodes = higher network-wide utilization\n\n"
             "This is a network effect business, not a real estate business.",
             font_size=11, color=SILVER_LIGHT)


# ════════════════════════════════════════════════════════════════
# SLIDE 6 — CUSTOMERS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Customers")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "Who Buys Edge AI Inference Capacity",
             font_size=30, color=WHITE, bold=True)

customers = [
    ("AI / ML Companies", "Companies deploying AI models needing low-latency inference close to end users. LLM providers, computer vision, NLP, AI agents.", "Buy token capacity and GPU hours."),
    ("Government (Fed/State/Local)", "Data sovereignty, FedRAMP workloads, NG911, FirstNet, CJIS, defense-adjacent processing.", "Multi-year contracts, premium pricing."),
    ("Healthcare & Telemedicine", "HIPAA-compliant edge compute for medical imaging AI, remote diagnostics, patient data processing.", "Data must stay local, latency is life-critical."),
    ("Financial Services", "Fraud detection (sub-50ms), payment processing, data residency. Regional banks and fintech.", "High-value, SLA-sensitive."),
    ("Autonomous Systems", "V2X for autonomous vehicles, drone coordination, industrial robotics. Sub-10ms inference required.", "Growing rapidly, no alternative to edge."),
    ("Web3 / DePIN Projects", "Enterprise-grade infra for decentralized networks. Validator hosting, compute marketplace, settlement.", "Pay-per-use via crypto micro-transactions."),
]

positions = [
    (Inches(0.7), Inches(1.4)),
    (Inches(4.95), Inches(1.4)),
    (Inches(9.2), Inches(1.4)),
    (Inches(0.7), Inches(3.5)),
    (Inches(4.95), Inches(3.5)),
    (Inches(9.2), Inches(3.5)),
]

for i, (title, desc, highlight) in enumerate(customers):
    x, y = positions[i]
    w = Inches(3.95)
    h = Inches(1.85)
    add_shape(slide, x, y, w, h, fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, x + Inches(0.2), y + Inches(0.1), w - Inches(0.4), Inches(0.3),
                 title, font_size=13, color=WHITE, bold=True)
    add_text_box(slide, x + Inches(0.2), y + Inches(0.4), w - Inches(0.4), Inches(0.7),
                 desc, font_size=10, color=SILVER_MID)
    add_text_box(slide, x + Inches(0.2), y + Inches(1.2), w - Inches(0.4), Inches(0.5),
                 highlight, font_size=10, color=BLUE_LIGHT, bold=True)

# TAM stats
stats = [
    ("$500B+", "Edge computing TAM by 2030"),
    ("60-70%", "Of all AI compute is inference"),
    ("$25B+", "DePIN infrastructure market"),
]

x = Inches(0.7)
for value, label in stats:
    add_stat_box(slide, x, Inches(5.65), Inches(3.95), Inches(1.1),
                 value, label, value_color=BLUE_LIGHT)
    x += Inches(4.25)


# ════════════════════════════════════════════════════════════════
# SLIDE 7 — KEYS TO SUCCESS & RISKS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Execution")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "Keys to Success & Risk Mitigation",
             font_size=30, color=WHITE, bold=True)

# Left - Keys to Success
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

add_text_box(slide, LX, Inches(1.35), COL_W, Inches(0.35),
             "Keys to Success", font_size=16, color=GREEN, bold=True)

success_items = [
    ("Speed to Scale", "Prefab modular units deploy in 60-90 days vs. 18-24 months. Cell tower sites provide 40,000+ pre-validated locations. Target: 3-5 sites Year 1, 50 by Year 2, 300 by Year 4."),
    ("Cost Management", "AI-native operations cut staffing from $400K+/yr to $80-150K/yr per site. Power scales to existing grid \u2014 no infrastructure buildout premiums."),
    ("Compute Fill at Premium Rates", "Inference-specific positioning commands premium pricing. AI capacity planning ensures utilization by routing workloads across the mesh to fill available capacity."),
    ("Offtake Customers", "Government contracts (3-5 yr, premium rates) provide base revenue. AI companies and healthcare provide volume. Multi-rail revenue diversifies concentration risk."),
]

y = Inches(1.75)
for title, desc in success_items:
    add_shape(slide, LX, y, COL_W, Inches(1.15), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, LX + Inches(0.15), y + Inches(0.05), COL_W - Inches(0.3), Inches(0.25),
                 title, font_size=12, color=WHITE, bold=True)
    add_text_box(slide, LX + Inches(0.15), y + Inches(0.3), COL_W - Inches(0.3), Inches(0.8),
                 desc, font_size=10, color=SILVER_MID)
    y += Inches(1.25)

# Right - Risks
add_text_box(slide, RX, Inches(1.35), COL_W, Inches(0.35),
             "Key Risks & Mitigations", font_size=16, color=AMBER, bold=True)

risks = [
    ("Crown Castle Partnership", "MEDIUM", AMBER, "Agreement may not materialize. Mitigation: Cell towers are one channel \u2014 can co-locate at industrial parks, substations, ISP POPs. Multiple site strategies in parallel."),
    ("Utilization / Fill Rate", "MEDIUM", AMBER, "Sites may not reach target utilization fast enough. Mitigation: AI demand modeling drives site selection. Government anchor tenants provide base load."),
    ("Technology Execution", "LOW", GREEN, "AI management layer may not achieve target autonomy. Mitigation: Each component is proven tech. Innovation is integration. Graduated rollout with human fallback."),
    ("Competition", "LOW", GREEN, "Hyperscalers could replicate. Mitigation: Sub-2MW is structurally unattractive for them. Previous edge attempts failed on economics that AI ops now solve."),
]

y = Inches(1.75)
for title, level, level_color, desc in risks:
    add_shape(slide, RX, y, COL_W, Inches(1.15), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    # Title + risk badge
    add_text_box(slide, RX + Inches(0.15), y + Inches(0.05), Inches(3.5), Inches(0.25),
                 title, font_size=12, color=WHITE, bold=True)
    add_text_box(slide, RX + COL_W - Inches(1.1), y + Inches(0.08), Inches(0.9), Inches(0.22),
                 level, font_size=8, color=level_color, bold=True, alignment=PP_ALIGN.RIGHT)
    add_text_box(slide, RX + Inches(0.15), y + Inches(0.3), COL_W - Inches(0.3), Inches(0.8),
                 desc, font_size=10, color=SILVER_MID)
    y += Inches(1.25)


# ════════════════════════════════════════════════════════════════
# SLIDE 8 — WHAT IT COSTS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Unit Economics")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "What It Costs: Per-Site Economics",
             font_size=30, color=WHITE, bold=True)

# Left - CapEx
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

add_text_box(slide, LX, Inches(1.35), COL_W, Inches(0.3),
             "Capital Expenditure (Per 200kW Edge Node)", font_size=14, color=WHITE, bold=True)

add_shape(slide, LX, Inches(1.7), COL_W, Inches(3.2), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))

capex_items = [
    ("Modular enclosure + site prep", "$300K-$500K"),
    ("Compute & GPU hardware (4-8 racks)", "$600K-$1.0M"),
    ("Networking (switches, backhaul)", "$100K-$200K"),
    ("Power (UPS, PDU, switchgear)", "$150K-$250K"),
    ("Cooling (DLC + ambient)", "$100K-$150K"),
    ("Security, fire suppression, misc", "$50K-$100K"),
]

tf = add_rich_text(slide, LX + Inches(0.2), Inches(1.8), COL_W - Inches(0.4), Inches(2.2))
for component, cost in capex_items:
    p = tf.add_paragraph()
    run1 = p.add_run()
    run1.text = component
    run1.font.size = Pt(11)
    run1.font.color.rgb = SILVER_LIGHT
    run1.font.name = "Calibri"
    run2 = p.add_run()
    run2.text = "    " + cost
    run2.font.size = Pt(11)
    run2.font.color.rgb = WHITE
    run2.font.bold = True
    run2.font.name = "Calibri"
    p.space_after = Pt(3)

# Total
p = tf.add_paragraph()
p.space_before = Pt(8)
run1 = p.add_run()
run1.text = "Total CapEx per node    "
run1.font.size = Pt(13)
run1.font.color.rgb = WHITE
run1.font.bold = True
run1.font.name = "Calibri"
run2 = p.add_run()
run2.text = "$1.5M - $2.5M"
run2.font.size = Pt(14)
run2.font.color.rgb = BLUE_LIGHT
run2.font.bold = True
run2.font.name = "Calibri"

# CapEx offsets card
add_shape(slide, LX, Inches(5.1), COL_W, Inches(1.8), fill_color=DARK_CARD, border_color=RGBColor(0x0E, 0x3A, 0x1E))
add_text_box(slide, LX + Inches(0.2), Inches(5.2), COL_W - Inches(0.4), Inches(0.25),
             "CapEx Offsets", font_size=12, color=GREEN, bold=True)
tf = add_rich_text(slide, LX + Inches(0.2), Inches(5.5), COL_W - Inches(0.4), Inches(1.3))
for item in [
    "On-site solar (100kW): ~$150K installed",
    "Battery storage (500kWh): ~$200K installed",
    "IRA ITC credit (30-50%): -$105K to -$175K savings",
    "OZ tax benefits: Significant additional reduction",
]:
    add_bullet(tf, item, font_size=10, color=SILVER_LIGHT)

# Right - OpEx
add_text_box(slide, RX, Inches(1.35), COL_W, Inches(0.3),
             "Annual Operating Expenses (Per Node)", font_size=14, color=WHITE, bold=True)

add_shape(slide, RX, Inches(1.7), COL_W, Inches(3.2), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))

# Header row
add_text_box(slide, RX + Inches(0.2), Inches(1.75), Inches(2.0), Inches(0.25),
             "Category", font_size=9, color=BLUE_LIGHT, bold=True)
add_text_box(slide, RX + Inches(2.4), Inches(1.75), Inches(1.5), Inches(0.25),
             "Traditional", font_size=9, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, RX + Inches(4.0), Inches(1.75), Inches(1.7), Inches(0.25),
             "ANDD AI-Native", font_size=9, color=BLUE_LIGHT, bold=True, alignment=PP_ALIGN.CENTER)

opex_items = [
    ("Staffing / operations", "$400K+", "$80K-$150K", RED, GREEN),
    ("Power (@ $0.08/kWh)", "$140K", "$140K", SILVER_LIGHT, SILVER_LIGHT),
    ("Connectivity", "$100K", "$60K-$120K", SILVER_LIGHT, SILVER_LIGHT),
    ("Site lease / co-lo fee", "$50K-$100K", "$50K-$100K", SILVER_LIGHT, SILVER_LIGHT),
    ("Insurance, maintenance", "$50K", "$30K-$50K", SILVER_LIGHT, SILVER_LIGHT),
]

y_pos = Inches(2.05)
for cat, trad, andd, trad_c, andd_c in opex_items:
    add_text_box(slide, RX + Inches(0.2), y_pos, Inches(2.0), Inches(0.22),
                 cat, font_size=10, color=SILVER_LIGHT)
    add_text_box(slide, RX + Inches(2.4), y_pos, Inches(1.5), Inches(0.22),
                 trad, font_size=10, color=trad_c, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, RX + Inches(4.0), y_pos, Inches(1.7), Inches(0.22),
                 andd, font_size=10, color=andd_c, bold=True, alignment=PP_ALIGN.CENTER)
    y_pos += Inches(0.35)

# Total row
y_pos += Inches(0.15)
add_text_box(slide, RX + Inches(0.2), y_pos, Inches(2.0), Inches(0.25),
             "Total Annual OpEx", font_size=11, color=WHITE, bold=True)
add_text_box(slide, RX + Inches(2.4), y_pos, Inches(1.5), Inches(0.25),
             "$740K+", font_size=12, color=RED, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, RX + Inches(4.0), y_pos, Inches(1.7), Inches(0.25),
             "$360K-$560K", font_size=12, color=GREEN, bold=True, alignment=PP_ALIGN.CENTER)

# AI Ops advantage card
add_shape(slide, RX, Inches(5.1), COL_W, Inches(1.8), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
add_text_box(slide, RX + Inches(0.2), Inches(5.2), COL_W - Inches(0.4), Inches(0.25),
             "The AI Operations Advantage", font_size=12, color=BLUE_LIGHT, bold=True)
add_text_box(slide, RX + Inches(0.2), Inches(5.5), COL_W - Inches(0.4), Inches(1.2),
             "Traditional model: sub-2MW sites are margin-negative. Staffing costs alone consume most revenue.\n\n"
             "ANDD model: AI automation cuts operating costs by 40-55%, making 200kW sites margin-positive "
             "for the first time in the industry.",
             font_size=11, color=SILVER_LIGHT)


# ════════════════════════════════════════════════════════════════
# SLIDE 9 — RETURN ON INVESTMENT
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Financial Returns")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "Return on Investment",
             font_size=30, color=WHITE, bold=True)

# Left - Revenue Model
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

add_text_box(slide, LX, Inches(1.3), COL_W, Inches(0.3),
             "Per-Node Revenue Model (200kW, at target utilization)", font_size=13, color=WHITE, bold=True)

add_shape(slide, LX, Inches(1.65), COL_W, Inches(2.8), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))

rev_items = [
    ("AI inference (GPU hours, token capacity)", "$350K-$600K"),
    ("Compute & colocation (enterprise, gov)", "$100K-$250K"),
    ("Storage & CDN services", "$30K-$80K"),
    ("DePIN / Web3 hosting", "$20K-$70K"),
    ("Grid services (BESS demand response)", "$50K-$150K"),
]

tf = add_rich_text(slide, LX + Inches(0.2), Inches(1.75), COL_W - Inches(0.4), Inches(2.0))
for stream, amount in rev_items:
    p = tf.add_paragraph()
    run1 = p.add_run()
    run1.text = stream
    run1.font.size = Pt(11)
    run1.font.color.rgb = SILVER_LIGHT
    run1.font.name = "Calibri"
    run2 = p.add_run()
    run2.text = "    " + amount
    run2.font.size = Pt(11)
    run2.font.color.rgb = WHITE
    run2.font.bold = True
    run2.font.name = "Calibri"
    p.space_after = Pt(4)

# Total
p = tf.add_paragraph()
p.space_before = Pt(10)
run1 = p.add_run()
run1.text = "Total Annual Revenue    "
run1.font.size = Pt(13)
run1.font.color.rgb = WHITE
run1.font.bold = True
run1.font.name = "Calibri"
run2 = p.add_run()
run2.text = "$550K - $1.15M"
run2.font.size = Pt(14)
run2.font.color.rgb = GREEN
run2.font.bold = True
run2.font.name = "Calibri"

# Ramp card
add_shape(slide, LX, Inches(4.6), COL_W, Inches(1.6), fill_color=DARK_CARD, border_color=RGBColor(0x0E, 0x3A, 0x1E))
add_text_box(slide, LX + Inches(0.2), Inches(4.7), COL_W - Inches(0.4), Inches(0.25),
             "Ramp Assumptions", font_size=12, color=GREEN, bold=True)

ramp_data = [
    ("Year 1:", "30-40% utilization", "Covers OpEx + partial CapEx service"),
    ("Year 2:", "50-65% utilization", "Cash-flow positive"),
    ("Year 3+:", "70-85% utilization", "Full margin realization"),
]

tf = add_rich_text(slide, LX + Inches(0.2), Inches(5.0), COL_W - Inches(0.4), Inches(1.1))
for year, util, result in ramp_data:
    p = tf.add_paragraph()
    run1 = p.add_run()
    run1.text = year + "  "
    run1.font.size = Pt(11)
    run1.font.color.rgb = WHITE
    run1.font.bold = True
    run1.font.name = "Calibri"
    run2 = p.add_run()
    run2.text = util + "  \u2192  " + result
    run2.font.size = Pt(11)
    run2.font.color.rgb = SILVER_LIGHT
    run2.font.name = "Calibri"
    p.space_after = Pt(3)

# Right - Return stats
add_text_box(slide, RX, Inches(1.3), COL_W, Inches(0.3),
             "Investment Returns Summary", font_size=13, color=WHITE, bold=True)

return_stats = [
    ("30-45%", "Gross Margin\n(at target util.)", GREEN),
    ("2.5-4 yr", "CapEx Payback\n(per node)", GREEN),
    ("18-30%", "Unlevered IRR\n(10-yr hold)", GREEN),
    ("0%", "Federal Cap Gains\n(10-yr OZ hold)", GREEN),
]

positions_ret = [
    (RX, Inches(1.7)),
    (RX + Inches(3.05), Inches(1.7)),
    (RX, Inches(3.0)),
    (RX + Inches(3.05), Inches(3.0)),
]

for i, (value, label, color) in enumerate(return_stats):
    x, y = positions_ret[i]
    add_stat_box(slide, x, y, Inches(2.75), Inches(1.1),
                 value, label, value_color=color)

# OZ Tax Stack
add_shape(slide, RX, Inches(4.3), COL_W, Inches(2.0), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
add_text_box(slide, RX + Inches(0.2), Inches(4.4), COL_W - Inches(0.4), Inches(0.25),
             "Opportunity Zone Tax Stack", font_size=12, color=BLUE_LIGHT, bold=True)

tf = add_rich_text(slide, RX + Inches(0.2), Inches(4.7), COL_W - Inches(0.4), Inches(1.5))
for item in [
    "Deferral: Capital gains reinvested into QOF defer tax obligation",
    "Step-up: 10% basis step-up at 5 years (up to 30% for rural OZ)",
    "Exclusion: Zero capital gains tax on all appreciation after 10 years",
    "IRA credits: 30-50% ITC on solar/BESS further reduces effective cost",
]:
    add_bullet(tf, item, font_size=10, color=SILVER_LIGHT)

# Network scale note
add_shape(slide, RX, Inches(6.45), COL_W, Inches(0.7), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
add_text_box(slide, RX + Inches(0.2), Inches(6.5), COL_W - Inches(0.4), Inches(0.55),
             "Network Scale: Unit economics improve with scale \u2014 shared AI ops amortized across nodes, "
             "bandwidth purchasing power improves, mesh routing enables higher network-wide utilization.",
             font_size=10, color=SILVER_MID)


# ════════════════════════════════════════════════════════════════
# SLIDE 10 — SCALE PLAN
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Scale Plan")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "Path to Scale: Network Buildout",
             font_size=30, color=WHITE, bold=True)

phases = [
    ("Phase 1 \u2014 Prove", "Months 1-12", [
        "3-5 pilot sites at Crown Castle",
        "AI ops platform v1 operational",
        "Beta customers (gov, AI, health)",
        "SOC 2 Type I certification",
        "QOF structure established",
    ], "$8-15M", "Capital Required"),
    ("Phase 2 \u2014 Validate", "Months 12-24", [
        "20-50 nodes in regional clusters",
        "2-3 regional hubs deployed",
        "First government contracts",
        "AI handles >90% of ops",
        "FedRAMP Moderate authorization",
    ], "$40-100M", "Capital Required"),
    ("Phase 3 \u2014 Scale", "Months 24-48", [
        "100-300 nodes, 10+ hubs",
        "Full mesh fabric operational",
        "Federal government customers",
        "AI model marketplace live",
        "Cash-flow positive (network)",
    ], "$200-600M", "Capital Required"),
    ("Phase 4 \u2014 Dominate", "Months 48-72", [
        "500-1,000+ nodes nationwide",
        "Revenue funds growth",
        "International expansion",
        "Critical national infrastructure",
        "VPP grid services at scale",
    ], "Self-Funding", "Revenue-Funded"),
]

x = Inches(0.7)
for phase_title, timing, items, capital, cap_label in phases:
    add_shape(slide, x, Inches(1.35), Inches(2.95), Inches(4.8), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, x + Inches(0.15), Inches(1.4), Inches(2.65), Inches(0.25),
                 phase_title, font_size=11, color=BLUE_LIGHT, bold=True)
    add_text_box(slide, x + Inches(0.15), Inches(1.65), Inches(2.65), Inches(0.2),
                 timing, font_size=10, color=SILVER_LIGHT, bold=True)

    tf = add_rich_text(slide, x + Inches(0.15), Inches(1.9), Inches(2.65), Inches(2.5))
    for item in items:
        add_bullet(tf, item, font_size=9, color=SILVER_LIGHT, space_after=Pt(2))

    # Capital
    cap_color = GREEN if capital == "Self-Funding" else BLUE_LIGHT
    add_text_box(slide, x, Inches(4.7), Inches(2.95), Inches(0.45),
                 capital, font_size=18, color=cap_color, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x, Inches(5.1), Inches(2.95), Inches(0.2),
                 cap_label, font_size=8, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

    x += Inches(3.15)

# Bottom stats
stats_bottom = [
    ("$2.5M", "Avg CapEx per node"),
    ("60-90 days", "Deploy time (prefab)"),
    ("40,000+", "Available tower sites"),
]

x = Inches(0.7)
for value, label in stats_bottom:
    color = GREEN if "40,000" in value else BLUE_LIGHT
    add_stat_box(slide, x, Inches(6.3), Inches(3.95), Inches(0.95),
                 value, label, value_color=color)
    x += Inches(4.25)


# ════════════════════════════════════════════════════════════════
# SLIDE 11 — TEAM
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(0.7), Inches(0.4), "Team")
add_text_box(slide, Inches(0.7), Inches(0.7), Inches(11.5), Inches(0.5),
             "The Team Building This",
             font_size=30, color=WHITE, bold=True)

# Left - Founding team card
LX = Inches(0.7)
RX = Inches(6.9)
COL_W = Inches(5.9)

add_shape(slide, LX, Inches(1.4), COL_W, Inches(5.3), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
add_text_box(slide, LX + Inches(0.25), Inches(1.55), COL_W - Inches(0.5), Inches(0.3),
             "Founding Team", font_size=16, color=WHITE, bold=True)

add_text_box(slide, LX + Inches(0.25), Inches(1.95), COL_W - Inches(0.5), Inches(0.8),
             "Building ANDD requires expertise across datacenter infrastructure, AI/ML systems, "
             "telecommunications, real estate development, federal compliance, and financial structuring.",
             font_size=12, color=SILVER_LIGHT)

# Role table
roles = [
    ("CEO / Visionary", "Strategy, investor relations, partnerships"),
    ("CTO", "AI ops platform, infrastructure architecture"),
    ("VP Infrastructure", "Site buildout, hardware, power systems"),
    ("VP Sales / BD", "Government contracts, enterprise customers"),
    ("CFO", "QOF structure, capital markets, financial ops"),
]

y_pos = Inches(3.0)
for role, desc in roles:
    add_text_box(slide, LX + Inches(0.25), y_pos, Inches(2.2), Inches(0.25),
                 role, font_size=11, color=SILVER_LIGHT, bold=True)
    add_text_box(slide, LX + Inches(2.5), y_pos, Inches(3.2), Inches(0.25),
                 desc, font_size=11, color=SILVER_MID)
    y_pos += Inches(0.4)

# Right - Competencies
add_text_box(slide, RX, Inches(1.35), COL_W, Inches(0.3),
             "What the Team Must Excel At", font_size=14, color=WHITE, bold=True)

competencies = [
    ("Deals & Partnerships", "Crown Castle agreement. Utility interconnections. Government contract vehicles. OZ fund structure. Execution-dependent relationships requiring experienced operators."),
    ("AI Operations Engineering", "The AI management layer is the core differentiator. Deep ML/AI engineering to build the autonomous ops platform that makes the economics work."),
    ("Datacenter Operations", "Prefab deployment, power systems, cooling, physical security, compliance certifications. Proven operators who have built and run facilities."),
    ("Government & Compliance", "FedRAMP, SOC 2, HIPAA, CJIS, ITAR. Government procurement, security clearances, and patience for federal sales cycles."),
]

y = Inches(1.7)
for title, desc in competencies:
    add_shape(slide, RX, y, COL_W, Inches(1.2), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, RX + Inches(0.15), y + Inches(0.05), COL_W - Inches(0.3), Inches(0.25),
                 title, font_size=12, color=WHITE, bold=True)
    add_text_box(slide, RX + Inches(0.15), y + Inches(0.3), COL_W - Inches(0.3), Inches(0.85),
                 desc, font_size=10, color=SILVER_MID)
    y += Inches(1.3)


# ════════════════════════════════════════════════════════════════
# SLIDE 12 — THE ASK / CLOSING
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

section_label(slide, Inches(4.5), Inches(0.5), "The Opportunity")
add_text_box(slide, Inches(1), Inches(0.8), Inches(11.3), Inches(1.2),
             "The Compute Market Needs a New Model.\nThis Is It.",
             font_size=36, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1.5), Inches(2.1), Inches(10.3), Inches(0.7),
             "$162B in blocked datacenter projects. Exploding AI inference demand. States pushing back on hyperscale.\n"
             "ANDD delivers the compute capacity the market needs \u2014 without the problems.",
             font_size=14, color=SILVER_MID, alignment=PP_ALIGN.CENTER)

# 4 value prop boxes
props = [
    ("<2MW", "Fits existing grid\nNo pushback", BLUE_LIGHT),
    ("AI Native", "60-75% lower ops cost\nMargin-positive at 200kW", GREEN),
    ("40K+ Sites", "Crown Castle pipeline\nPre-permitted locations", BLUE_LIGHT),
    ("0% Tax", "On appreciation\n10-year OZ hold", GREEN),
]

x = Inches(1.2)
for value, label, color in props:
    add_stat_box(slide, x, Inches(3.0), Inches(2.6), Inches(1.2),
                 value, label, value_color=color)
    x += Inches(2.85)

# Three value cards
value_props = [
    ("Revenue from Year 1", "Infrastructure services generate income immediately upon deployment"),
    ("Network Appreciation", "Each new node increases the value of every existing node in the mesh"),
    ("National Impact", "Sovereign infrastructure, local jobs, and AI capacity for underserved communities"),
]

x = Inches(1.5)
for title, desc in value_props:
    add_shape(slide, x, Inches(4.5), Inches(3.2), Inches(1.0), fill_color=DARK_CARD, border_color=RGBColor(0x1E, 0x3A, 0x5F))
    add_text_box(slide, x + Inches(0.15), Inches(4.55), Inches(2.9), Inches(0.22),
                 title, font_size=10, color=BLUE_LIGHT, bold=True)
    add_text_box(slide, x + Inches(0.15), Inches(4.8), Inches(2.9), Inches(0.6),
                 desc, font_size=10, color=SILVER_LIGHT)
    x += Inches(3.45)

# Contact
add_text_box(slide, Inches(3.5), Inches(5.8), Inches(3), Inches(0.5),
             "Email\ncontact@andd.network",
             font_size=12, color=SILVER_LIGHT, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(7), Inches(5.8), Inches(3), Inches(0.5),
             "Web\nandd.network",
             font_size=12, color=SILVER_LIGHT, alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1), Inches(6.7), Inches(11.3), Inches(0.3),
             "CONFIDENTIAL \u2014 DO NOT DISTRIBUTE",
             font_size=9, color=SILVER_DARK, alignment=PP_ALIGN.CENTER)


# ── Save ──
output_path = os.path.join(os.path.dirname(__file__), "ANDD_Business_Pitch_Deck.pptx")
prs.save(output_path)
print(f"Saved: {output_path}")
