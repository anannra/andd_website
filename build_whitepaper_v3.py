#!/usr/bin/env python3
"""
ANDD Whitepaper v3 — Professional Edition with Generated Infographics.

Generates a polished single-column whitepaper with matplotlib-rendered
data visualizations, clean typography, and consistent branding.
"""

import os, tempfile, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from PIL import Image, ImageDraw, ImageFilter

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path("/home/anoop/git/anannra/andd_website")
OUT_FILE = BASE_DIR / "ANDD_Whitepaper_v3.docx"
TMP_DIR  = tempfile.mkdtemp(prefix="andd_v3_")

# Brand palette
C_NAVY      = "#0B1D32"
C_DARK_BLUE = "#122B46"
C_BLUE      = "#1B5E9E"
C_ACCENT    = "#2E9CDB"
C_CYAN      = "#00C6D7"
C_TEAL      = "#0FA38C"
C_LIGHT_BG  = "#F0F4F8"
C_WARM_GRAY = "#E4E7EC"
C_MID_GRAY  = "#8892A0"
C_DARK_TEXT  = "#15202B"
C_WHITE     = "#FFFFFF"
C_ORANGE    = "#E86830"
C_RED       = "#D73B3B"
C_GREEN     = "#2AA66A"
C_GOLD      = "#D4A843"

# docx RGBColors
RGB_NAVY      = RGBColor(0x0B, 0x1D, 0x32)
RGB_DARK_BLUE = RGBColor(0x12, 0x2B, 0x46)
RGB_BLUE      = RGBColor(0x1B, 0x5E, 0x9E)
RGB_ACCENT    = RGBColor(0x2E, 0x9C, 0xDB)
RGB_CYAN      = RGBColor(0x00, 0xC6, 0xD7)
RGB_LIGHT_BG  = RGBColor(0xF0, 0xF4, 0xF8)
RGB_WARM_GRAY = RGBColor(0xE4, 0xE7, 0xEC)
RGB_MID_GRAY  = RGBColor(0x88, 0x92, 0xA0)
RGB_DARK_TEXT = RGBColor(0x15, 0x20, 0x2B)
RGB_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

H_NAVY      = "0B1D32"
H_DARK_BLUE = "122B46"
H_BLUE      = "1B5E9E"
H_ACCENT    = "2E9CDB"
H_LIGHT_BG  = "F0F4F8"
H_WARM_GRAY = "E4E7EC"
H_WHITE     = "FFFFFF"

FONT_HEADING = "Calibri"
FONT_BODY    = "Calibri"

# Matplotlib global style
plt.rcParams.update({
    "figure.facecolor": C_WHITE,
    "axes.facecolor":   C_WHITE,
    "font.family":      "sans-serif",
    "font.sans-serif":  ["Calibri", "Helvetica", "Arial", "DejaVu Sans"],
    "text.color":       C_DARK_TEXT,
    "axes.labelcolor":  C_DARK_TEXT,
    "xtick.color":      C_MID_GRAY,
    "ytick.color":      C_MID_GRAY,
    "axes.edgecolor":   C_WARM_GRAY,
    "axes.grid":        False,
})

# =============================================================================
# GRAPHIC GENERATION FUNCTIONS
# =============================================================================

def _save(fig, name, dpi=200):
    path = os.path.join(TMP_DIR, f"{name}.png")
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return path


def gfx_cover():
    """Abstract network mesh on dark gradient — cover page hero image."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(C_NAVY)

    rng = np.random.RandomState(42)
    n = 65
    x = rng.uniform(0.3, 9.7, n)
    y = rng.uniform(0.3, 5.2, n)

    # Draw connections
    for i in range(n):
        dists = np.sqrt((x - x[i])**2 + (y - y[i])**2)
        neighbors = np.argsort(dists)[1:5]
        for j in neighbors:
            alpha = max(0.04, 0.25 - dists[j] * 0.06)
            ax.plot([x[i], x[j]], [y[i], y[j]], color=C_ACCENT, alpha=alpha, lw=0.7)

    # Draw nodes with glow
    sizes = rng.uniform(15, 70, n)
    ax.scatter(x, y, s=sizes * 3, c=C_ACCENT, alpha=0.15, edgecolors="none", zorder=2)
    ax.scatter(x, y, s=sizes, c=C_CYAN, alpha=0.7, edgecolors="none", zorder=3)

    # Highlight hub nodes
    hubs = rng.choice(n, 5, replace=False)
    ax.scatter(x[hubs], y[hubs], s=200, c=C_CYAN, alpha=0.3, edgecolors="none", zorder=2)
    ax.scatter(x[hubs], y[hubs], s=90, c=C_WHITE, alpha=0.9, edgecolors="none", zorder=4)

    return _save(fig, "cover", dpi=250)


def gfx_concentration():
    """Horizontal bar chart — datacenter concentration by metro area."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    metros = ["Northern Virginia", "Dallas-Fort Worth", "Phoenix", "Chicago", "Silicon Valley", "All Other Metros"]
    shares = [35, 14, 10, 8, 7, 26]
    colors = [C_RED, C_ORANGE, C_ORANGE, C_GOLD, C_GOLD, C_MID_GRAY]

    bars = ax.barh(range(len(metros)), shares, color=colors, height=0.6, edgecolor="none")
    ax.set_yticks(range(len(metros)))
    ax.set_yticklabels(metros, fontsize=10, color=C_DARK_TEXT)
    ax.set_xlabel("% of U.S. Datacenter Capacity", fontsize=10, color=C_MID_GRAY)
    ax.set_title("Datacenter Capacity Concentration", fontsize=13, fontweight="bold",
                 color=C_NAVY, pad=12)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    for bar, val in zip(bars, shares):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val}%", va="center", fontsize=10, fontweight="bold", color=C_DARK_TEXT)

    fig.tight_layout()
    return _save(fig, "concentration")


def gfx_three_tier():
    """3-tier architecture diagram — edge → hub → control plane."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7)
    ax.axis("off")

    def rounded_box(x, y, w, h, color, label, sublabel="", lcolor=C_WHITE):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                             facecolor=color, edgecolor="none", zorder=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + (0.12 if sublabel else 0),
                label, ha="center", va="center", fontsize=10,
                fontweight="bold", color=lcolor, zorder=3)
        if sublabel:
            ax.text(x + w/2, y + h/2 - 0.22, sublabel, ha="center", va="center",
                    fontsize=7.5, color=lcolor, alpha=0.8, zorder=3)

    # Tier 3 — Control plane
    rounded_box(3.5, 5.7, 5, 0.9, C_NAVY, "AI Control Plane", "Distributed BFT Consensus")

    # Tier 2 — Hubs
    hx = [1.5, 4.75, 8.0]
    for i, x in enumerate(hx):
        rounded_box(x, 3.6, 2.5, 0.9, C_BLUE,
                    f"Regional Hub {chr(65+i)}", "1–2 MW")
        ax.annotate("", xy=(x + 1.25, 4.5), xytext=(6, 5.7),
                    arrowprops=dict(arrowstyle="-", color=C_ACCENT, lw=1.3, alpha=0.6))

    # Hub-to-hub backbone
    for i in range(len(hx) - 1):
        ax.annotate("", xy=(hx[i] + 2.5, 4.05), xytext=(hx[i+1], 4.05),
                    arrowprops=dict(arrowstyle="<->", color=C_CYAN, lw=1.5, alpha=0.7))

    # Tier 1 — Edge nodes
    edge_positions = [
        (0.3, 1.0), (2.1, 1.5), (3.3, 0.5),
        (4.2, 1.6), (5.5, 0.8), (6.5, 1.5),
        (7.6, 0.6), (8.8, 1.4), (10.2, 1.0), (11.0, 1.8)
    ]
    for ex, ey in edge_positions:
        circle = plt.Circle((ex, ey), 0.32, color=C_ACCENT, alpha=0.8, zorder=2)
        ax.add_patch(circle)
        ax.text(ex, ey, "E", ha="center", va="center", fontsize=7,
                fontweight="bold", color=C_WHITE, zorder=3)

    # Connect edges to nearest hub
    for ex, ey in edge_positions:
        nearest = min(hx, key=lambda hx_: abs(ex - (hx_ + 1.25)))
        ax.plot([ex, nearest + 1.25], [ey + 0.32, 3.6], color=C_ACCENT,
                alpha=0.3, lw=0.8, zorder=1)

    # Mesh connections between nearby edges
    for i, (x1, y1) in enumerate(edge_positions):
        for j, (x2, y2) in enumerate(edge_positions):
            if i < j and np.sqrt((x1-x2)**2 + (y1-y2)**2) < 2.5:
                ax.plot([x1, x2], [y1, y2], color=C_CYAN, alpha=0.15, lw=0.6, ls="--", zorder=1)

    # Tier labels
    ax.text(11.8, 6.15, "TIER 3", fontsize=8, color=C_MID_GRAY, ha="right", fontweight="bold")
    ax.text(11.8, 4.05, "TIER 2", fontsize=8, color=C_MID_GRAY, ha="right", fontweight="bold")
    ax.text(11.8, 1.2, "TIER 1", fontsize=8, color=C_MID_GRAY, ha="right", fontweight="bold")

    ax.set_title("ANDD Three-Tier Network Topology", fontsize=14, fontweight="bold",
                 color=C_NAVY, pad=15)
    return _save(fig, "three_tier")


def gfx_hardware_domains():
    """4-panel hardware domain breakdown."""
    fig, axes = plt.subplots(2, 2, figsize=(8.5, 5))
    domains = [
        ("Compute", ["AMD EPYC 9004", "Intel Xeon 6", "Ampere Altra Max"],
         ["256GB–1TB DDR5", "20–40kW / rack", "Containers, VMs, CI/CD"], C_BLUE),
        ("Storage", ["NVMe SSD (Hot Tier)", "QLC SSD / HDD (Warm)", "S3 + NFS + Dist. FS"],
         ["100TB–2PB per site", "Erasure coded 3+ nodes", "11 nines durability"], C_TEAL),
        ("Connectivity", ["100GbE Leaf-Spine", "10–100Gbps Backhaul", "5G/CBRS + SIPRNet"],
         ["Multi-carrier peering", "BGP + SD-WAN", "Carrier-neutral IXP"], C_ACCENT),
        ("AI Accelerators", ["NVIDIA L4 / L40S", "AMD MI300X / MI325X", "H100/H200/B200/GB200"],
         ["72W–2,700W range", "24–384 GB HBM", "Inference + Training"], C_ORANGE),
    ]

    for ax, (title, items, specs, color) in zip(axes.flat, domains):
        ax.set_xlim(0, 10); ax.set_ylim(0, 6)
        ax.axis("off")
        # Header bar
        header = FancyBboxPatch((0.2, 4.6), 9.6, 1.2, boxstyle="round,pad=0.1",
                                facecolor=color, edgecolor="none")
        ax.add_patch(header)
        ax.text(5, 5.2, title, ha="center", va="center", fontsize=12,
                fontweight="bold", color=C_WHITE)
        # Items
        for i, (item, spec) in enumerate(zip(items, specs)):
            yy = 3.6 - i * 1.4
            ax.text(0.5, yy, "●", fontsize=8, color=color, va="center")
            ax.text(1.2, yy, item, fontsize=9, fontweight="bold", color=C_DARK_TEXT, va="center")
            ax.text(1.2, yy - 0.45, spec, fontsize=7.5, color=C_MID_GRAY, va="center")

    fig.suptitle("Four Hardware Domains", fontsize=14, fontweight="bold", color=C_NAVY, y=1.02)
    fig.tight_layout()
    return _save(fig, "hardware_domains")


def gfx_software_stack():
    """Layered horizontal bar diagram of the software platform stack."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8)
    ax.axis("off")

    layers = [
        ("Layer 4: AI Management", "Onboarding · Provisioning · Billing · SLA Guardian", C_NAVY),
        ("Layer 3: Orchestration", "Kubernetes (K3s/RKE2) · Service Mesh (Istio) · AI Scheduler", C_BLUE),
        ("Layer 2: Infrastructure", "SD-WAN/SDN · Storage Fabric (Ceph) · DCIM/BMS", C_ACCENT),
        ("Layer 1: Hardware Abstraction", "BMC/Redfish · GPU Drivers · SONiC/Cumulus", C_TEAL),
    ]

    for i, (title, desc, color) in enumerate(layers):
        y = 6.2 - i * 1.5
        w = 10.5 - i * 0.3
        x = (12 - w) / 2
        box = FancyBboxPatch((x, y), w, 1.1, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor="none", alpha=0.92)
        ax.add_patch(box)
        ax.text(6, y + 0.7, title, ha="center", va="center", fontsize=11,
                fontweight="bold", color=C_WHITE)
        ax.text(6, y + 0.28, desc, ha="center", va="center", fontsize=8, color=C_WHITE, alpha=0.85)

    # Arrow on right
    ax.annotate("", xy=(11.5, 1.8), xytext=(11.5, 7.3),
                arrowprops=dict(arrowstyle="->", color=C_MID_GRAY, lw=1.5))
    ax.text(11.7, 4.5, "AI\nOrchestrates\nAll Layers", fontsize=7, color=C_MID_GRAY,
            ha="left", va="center", fontstyle="italic")

    ax.set_title("ANDD Software Platform Architecture", fontsize=14, fontweight="bold",
                 color=C_NAVY, pad=15)
    return _save(fig, "software_stack")


def gfx_opex_comparison():
    """Grouped bar chart — traditional vs AI-native operational costs."""
    fig, ax = plt.subplots(figsize=(8.5, 4))
    categories = ["Facilities\nStaff", "Network\nOps (NOC)", "Sales &\nCustomer Mgmt",
                  "Billing &\nFinance", "Compliance", "Power &\nCooling"]
    traditional = [17.5, 12.5, 12.5, 6.5, 7.5, 35]
    ai_native   = [3.0,  2.0,  1.5,  1.0, 4.0, 30]

    x = np.arange(len(categories))
    w = 0.35
    b1 = ax.bar(x - w/2, traditional, w, label="Traditional Ops", color=C_RED, alpha=0.8, edgecolor="none")
    b2 = ax.bar(x + w/2, ai_native, w, label="AI-Native Ops", color=C_ACCENT, alpha=0.9, edgecolor="none")

    ax.set_ylabel("% of Total OpEx", fontsize=10, color=C_MID_GRAY)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8.5)
    ax.set_title("Operational Cost Comparison: Traditional vs AI-Native", fontsize=13,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.legend(fontsize=9, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 42)

    fig.tight_layout()
    return _save(fig, "opex_comparison")


def gfx_pue_comparison():
    """Bar chart — PUE across facility types."""
    fig, ax = plt.subplots(figsize=(8.5, 3.5))
    types  = ["Hyperscale\n(Google/Meta)", "Large\nColocation", "Traditional\nEdge (<1MW)",
              "Modern Edge\n(Purpose-built)", "ANDD\nTarget", "Immersion\nCooling"]
    typical = [1.15, 1.40, 1.60, 1.30, 1.20, 1.06]
    best    = [1.07, 1.20, 1.25, 1.12, 1.15, 1.03]

    x = np.arange(len(types))
    w = 0.32
    ax.bar(x - w/2, typical, w, label="Typical PUE", color=C_ORANGE, alpha=0.75, edgecolor="none")
    ax.bar(x + w/2, best, w, label="Best-in-Class PUE", color=C_GREEN, alpha=0.85, edgecolor="none")

    ax.axhline(y=1.0, color=C_MID_GRAY, ls=":", lw=0.8, alpha=0.5)
    ax.text(5.7, 1.005, "Ideal (1.0)", fontsize=7, color=C_MID_GRAY, ha="right")

    ax.set_ylabel("PUE", fontsize=10, color=C_MID_GRAY)
    ax.set_xticks(x)
    ax.set_xticklabels(types, fontsize=8)
    ax.set_title("Power Usage Effectiveness (PUE) by Facility Type", fontsize=13,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.legend(fontsize=9, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0.95, 1.85)

    fig.tight_layout()
    return _save(fig, "pue_comparison")


def gfx_resilience():
    """Visual comparison of centralized vs distributed resilience."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

    # Centralized
    ax1.set_xlim(0, 6); ax1.set_ylim(0, 6)
    ax1.axis("off")
    ax1.set_title("Centralized Model", fontsize=12, fontweight="bold", color=C_RED, pad=8)
    big = plt.Circle((3, 3), 1.5, color=C_RED, alpha=0.2, zorder=1)
    ax1.add_patch(big)
    big2 = plt.Circle((3, 3), 0.8, color=C_RED, alpha=0.6, zorder=2)
    ax1.add_patch(big2)
    ax1.text(3, 3, "Single\nCampus", ha="center", va="center", fontsize=9,
             fontweight="bold", color=C_WHITE, zorder=3)
    ax1.text(3, 0.8, "99.99% uptime\n~67 min downtime/yr\n1% catastrophic risk",
             ha="center", va="center", fontsize=8.5, color=C_DARK_TEXT)

    # Distributed
    ax2.set_xlim(0, 6); ax2.set_ylim(0, 6)
    ax2.axis("off")
    ax2.set_title("ANDD Distributed Mesh", fontsize=12, fontweight="bold", color=C_GREEN, pad=8)
    rng = np.random.RandomState(7)
    nx, ny = rng.uniform(0.8, 5.2, 20), rng.uniform(1.5, 5.2, 20)
    for i in range(20):
        for j in range(i+1, 20):
            if np.sqrt((nx[i]-nx[j])**2 + (ny[i]-ny[j])**2) < 1.8:
                ax2.plot([nx[i], nx[j]], [ny[i], ny[j]], color=C_GREEN, alpha=0.15, lw=0.6)
    ax2.scatter(nx, ny, s=60, c=C_GREEN, alpha=0.8, edgecolors="none", zorder=3)
    ax2.text(3, 0.8, "100 nodes × 99.95% each\n>99.9999% network availability\nFailure prob: 10⁻⁴⁷",
             ha="center", va="center", fontsize=8.5, color=C_DARK_TEXT)

    fig.suptitle("Resilience: Centralized vs. Distributed", fontsize=14, fontweight="bold",
                 color=C_NAVY, y=1.04)
    fig.tight_layout()
    return _save(fig, "resilience")


def gfx_depin_radar():
    """Radar chart comparing Consumer DePIN vs ANDD on multiple dimensions."""
    categories = ["Uptime", "Redundancy", "Physical\nSecurity", "Compliance",
                  "Power Quality", "Cooling", "Connectivity", "Support", "Data\nSovereignty"]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    consumer = [3, 1, 1, 1, 2, 1, 3, 2, 1]
    andd     = [9, 9, 9, 8, 9, 9, 9, 8, 9]
    consumer += consumer[:1]
    andd += andd[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=7, color=C_MID_GRAY)
    ax.spines["polar"].set_color(C_WARM_GRAY)
    ax.grid(color=C_WARM_GRAY, alpha=0.5)

    ax.fill(angles, consumer, alpha=0.15, color=C_RED)
    ax.plot(angles, consumer, color=C_RED, lw=2, label="Consumer DePIN")
    ax.fill(angles, andd, alpha=0.15, color=C_ACCENT)
    ax.plot(angles, andd, color=C_ACCENT, lw=2, label="ANDD")

    ax.legend(loc="lower right", bbox_to_anchor=(1.25, -0.05), fontsize=10, frameon=False)
    ax.set_title("Enterprise-Grade Gap: Consumer DePIN vs ANDD", fontsize=13,
                 fontweight="bold", color=C_NAVY, pad=25)
    return _save(fig, "depin_radar")


def gfx_payment_architecture():
    """Payment rails flow diagram."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.axis("off")

    def rbox(x, y, w, h, color, text, sub=""):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(box)
        ax.text(x+w/2, y+h/2+(0.1 if sub else 0), text, ha="center", va="center",
                fontsize=9, fontweight="bold", color=C_WHITE)
        if sub:
            ax.text(x+w/2, y+h/2-0.18, sub, ha="center", va="center",
                    fontsize=7, color=C_WHITE, alpha=0.8)

    def arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=C_MID_GRAY, lw=1.3))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.2, label, ha="center", fontsize=7, color=C_MID_GRAY)

    # Customer types
    rbox(0.2, 4.5, 2.2, 0.9, C_BLUE, "Enterprise", "Wire / ACH")
    rbox(0.2, 3.1, 2.2, 0.9, C_ACCENT, "Startup", "Card / USDC")
    rbox(0.2, 1.7, 2.2, 0.9, C_TEAL, "DePIN Project", "Stablecoin")
    rbox(0.2, 0.3, 2.2, 0.9, C_NAVY, "Government", "PO / Treasury")

    # Billing Agent
    rbox(4.0, 2.4, 2.5, 1.5, C_NAVY, "AI Billing\nAgent", "Unified Ledger")
    for y in [4.95, 3.55, 2.15, 0.75]:
        arrow(2.4, y, 4.0, 3.15)

    # Payment rails
    rbox(8.0, 4.2, 3.5, 0.9, C_BLUE, "Fiat Rails", "Stripe / Adyen")
    rbox(8.0, 2.8, 3.5, 0.9, C_TEAL, "Crypto Rails", "Solana / L2 / Okopipi")
    rbox(8.0, 1.4, 3.5, 0.9, C_ORANGE, "Smart Contract SLAs", "Auto-enforced")
    rbox(8.0, 0.0, 3.5, 0.9, C_ACCENT, "Micro-Transactions", "Payment Channels")

    arrow(6.5, 3.5, 8.0, 4.65, "Fiat")
    arrow(6.5, 3.15, 8.0, 3.25, "Crypto")
    arrow(6.5, 2.8, 8.0, 1.85, "SLA")
    arrow(6.5, 2.5, 8.0, 0.45, "Micro")

    ax.set_title("Hybrid Payment Architecture", fontsize=14, fontweight="bold",
                 color=C_NAVY, pad=15)
    return _save(fig, "payment_architecture")


def gfx_oz_impact():
    """Opportunity Zone economic impact infographic."""
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5)
    ax.axis("off")

    stats = [
        ("15–30", "Construction\nJobs", C_BLUE),
        ("$150K+", "Annual Property\nTax Revenue", C_TEAL),
        ("$300K+", "Annual Utility\nRevenue", C_ACCENT),
        ("1.5–2×", "Economic\nMultiplier", C_GREEN),
        ("0%", "Capital Gains\nTax (10yr hold)", C_NAVY),
    ]

    for i, (value, label, color) in enumerate(stats):
        x = 1.2 + i * 2.1
        circle = plt.Circle((x, 3.0), 0.85, color=color, alpha=0.12, zorder=1)
        ax.add_patch(circle)
        ax.text(x, 3.2, value, ha="center", va="center", fontsize=18,
                fontweight="bold", color=color, zorder=2)
        ax.text(x, 1.6, label, ha="center", va="center", fontsize=8.5,
                color=C_DARK_TEXT, linespacing=1.4)

    ax.set_title("Per-Site Community Impact (200kW Edge Node in Opportunity Zone)",
                 fontsize=13, fontweight="bold", color=C_NAVY, pad=15)
    return _save(fig, "oz_impact")


def gfx_okopipi_stack():
    """Full sovereign stack diagram — Okopipi integration."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 9)
    ax.axis("off")

    layers = [
        ("Application Layer", "Customer workloads · DePIN protocols · Gov services · AI inference",
         "Customers / DePIN Projects", C_MID_GRAY),
        ("Smart Contract Execution", "Privacy-preserving quorum runtime · Deterministic ordering",
         "Okopipi", C_NAVY),
        ("Consensus & Settlement", "BLA on f-masking grid · MTU-sized proofs · PQ checkpoints",
         "Okopipi (on ANDD hubs)", C_DARK_BLUE),
        ("Network Fabric", "BIER multicast · View-aware routing · SRv6 · Mesh interconnection",
         "ANDD Mesh + Okopipi", C_BLUE),
        ("AI Operations", "Autonomous onboarding · Provisioning · Billing · SLA enforcement",
         "ANDD AI Management", C_ACCENT),
        ("Physical Infrastructure", "Compute · Storage · GPU · Cooling · Power · Security",
         "ANDD Edge Nodes + Hubs", C_TEAL),
        ("Energy & Resilience", "Microgrids · BESS · Solar · Fuel cells · Grid services",
         "ANDD On-site Generation", C_GREEN),
    ]

    for i, (title, desc, owner, color) in enumerate(layers):
        y = 7.8 - i * 1.1
        box = FancyBboxPatch((0.5, y), 8.5, 0.85, boxstyle="round,pad=0.08",
                             facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(box)
        ax.text(4.75, y + 0.52, title, ha="center", va="center", fontsize=10,
                fontweight="bold", color=C_WHITE)
        ax.text(4.75, y + 0.2, desc, ha="center", va="center", fontsize=7,
                color=C_WHITE, alpha=0.8)
        # Owner label on right
        ax.text(10.2, y + 0.42, owner, ha="left", va="center", fontsize=7.5,
                color=color, fontweight="bold")

    ax.text(10.2, 8.8, "Owner", ha="left", va="center", fontsize=8,
            color=C_MID_GRAY, fontweight="bold")

    ax.set_title("ANDD + Okopipi: The Sovereign Full Stack", fontsize=14,
                 fontweight="bold", color=C_NAVY, pad=15)
    return _save(fig, "okopipi_stack")


def gfx_roadmap():
    """Horizontal timeline roadmap."""
    fig, ax = plt.subplots(figsize=(9.5, 3.5))
    ax.set_xlim(-0.5, 13); ax.set_ylim(0, 5)
    ax.axis("off")

    phases = [
        (0, 2.5, "Phase 1", "Foundation", "Mo 1–12", "3–5 pilot sites\nSOC 2 cert\nQOF formation", C_BLUE),
        (3, 2.5, "Phase 2", "Network Formation", "Mo 12–24", "20–50 nodes\nFedRAMP auth\n90%+ AI ops", C_ACCENT),
        (6, 2.5, "Phase 3", "Scale", "Mo 24–48", "100–300 nodes\n10+ hubs\nSmart contract SLAs", C_TEAL),
        (9, 2.5, "Phase 4", "Continental", "Mo 48–72", "500–1,000+ nodes\nFull AI autonomy\nIntl. expansion", C_NAVY),
    ]

    # Timeline bar
    ax.plot([0.3, 12.2], [2.6, 2.6], color=C_WARM_GRAY, lw=3, solid_capstyle="round", zorder=1)

    for x, w, phase, title, period, desc, color in phases:
        # Dot on timeline
        ax.scatter(x + 1.25, 2.6, s=120, color=color, zorder=3, edgecolors=C_WHITE, linewidth=2)
        # Phase card above
        box = FancyBboxPatch((x + 0.1, 3.2), 2.3, 1.4, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(box)
        ax.text(x + 1.25, 4.2, f"{phase}: {title}", ha="center", va="center", fontsize=8,
                fontweight="bold", color=C_WHITE)
        ax.text(x + 1.25, 3.65, period, ha="center", va="center", fontsize=7,
                color=C_WHITE, alpha=0.8)
        # Description below
        ax.text(x + 1.25, 1.5, desc, ha="center", va="center", fontsize=7,
                color=C_DARK_TEXT, linespacing=1.4)

    ax.set_title("Implementation Roadmap", fontsize=14, fontweight="bold", color=C_NAVY, pad=12)
    return _save(fig, "roadmap")


def gfx_agent_architecture():
    """AI Agent architecture diagram."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.5)
    ax.axis("off")

    def rbox(x, y, w, h, color, text, sub=""):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor="none", alpha=0.9)
        ax.add_patch(box)
        ax.text(x+w/2, y+h/2+(0.12 if sub else 0), text, ha="center", va="center",
                fontsize=9, fontweight="bold", color=C_WHITE)
        if sub:
            ax.text(x+w/2, y+h/2-0.2, sub, ha="center", va="center",
                    fontsize=7, color=C_WHITE, alpha=0.8)

    # Orchestration agent (top)
    rbox(3.5, 5.2, 5, 0.9, C_NAVY, "Orchestration Agent",
         "Coordinates all sub-agents · Resolves conflicts · Escalates to humans")

    # Sub-agents
    agents = [
        (0.2, 3.2, "Customer\nOnboarding", C_BLUE),
        (2.6, 3.2, "Provisioning", C_ACCENT),
        (5.0, 3.2, "Billing &\nRevenue", C_TEAL),
        (7.4, 3.2, "Predictive\nMaintenance", C_GREEN),
        (9.8, 3.2, "SLA\nGuardian", C_ORANGE),
    ]

    for x, y, label, color in agents:
        rbox(x, y, 2.0, 1.2, color, label)
        # Connection to orchestrator
        ax.plot([x + 1.0, 6.0], [y + 1.2, 5.2], color=C_MID_GRAY, lw=0.8, alpha=0.5, ls="--")

    # Shared state store (bottom)
    rbox(2.0, 0.6, 8, 0.9, C_WARM_GRAY, "Shared Context & State Store",
         "Customer profiles · Capacity maps · Billing ledger · SLA contracts")
    # Override text color for light background
    for txt in ax.texts:
        pass  # keep as is

    # Connections down to state store
    for x, y, _, _ in agents:
        ax.plot([x + 1.0, x + 1.0], [y, 1.5], color=C_MID_GRAY, lw=0.6, alpha=0.3, ls=":")

    # Fix the state store text to dark
    # Re-draw state store text in dark
    rbox2 = FancyBboxPatch((2.0, 0.6), 8, 0.9, boxstyle="round,pad=0.1",
                           facecolor=C_LIGHT_BG, edgecolor=C_WARM_GRAY, linewidth=1)
    ax.add_patch(rbox2)
    ax.text(6.0, 1.17, "Shared Context & State Store", ha="center", va="center",
            fontsize=9, fontweight="bold", color=C_DARK_TEXT)
    ax.text(6.0, 0.85, "Customer profiles · Capacity maps · Billing ledger · SLA contracts",
            ha="center", va="center", fontsize=7, color=C_MID_GRAY)

    ax.set_title("AI Agent Architecture", fontsize=14, fontweight="bold", color=C_NAVY, pad=15)
    return _save(fig, "agent_architecture")


def gfx_bandwidth():
    """Bandwidth profile comparison by site tier."""
    fig, ax = plt.subplots(figsize=(8.5, 3.5))

    tiers = ["Edge Node\n(200kW)", "Edge Node\n(500kW)", "Regional Hub\n(1–2MW)"]
    primary   = [10, 40, 100]
    redundant = [5,  10, 40]
    mesh      = [10, 25, 100]

    x = np.arange(len(tiers))
    w = 0.22
    ax.bar(x - w, primary, w, label="Primary Uplink", color=C_BLUE, edgecolor="none")
    ax.bar(x, redundant, w, label="Redundant Uplink", color=C_ACCENT, edgecolor="none")
    ax.bar(x + w, mesh, w, label="Inter-Node Mesh", color=C_TEAL, edgecolor="none")

    ax.set_ylabel("Bandwidth (Gbps)", fontsize=10, color=C_MID_GRAY)
    ax.set_xticks(x)
    ax.set_xticklabels(tiers, fontsize=9)
    ax.set_title("Bandwidth Profile by Site Tier", fontsize=13, fontweight="bold",
                 color=C_NAVY, pad=12)
    ax.legend(fontsize=8.5, frameon=False, ncol=3, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return _save(fig, "bandwidth")


def gfx_cooling():
    """Cooling technology comparison — effective IT capacity from 500kW facility."""
    fig, ax = plt.subplots(figsize=(8.5, 3.5))

    techs = ["Air Cooling\n(DX)", "Rear-Door\nHeat Exch.", "Direct-to-Chip\nLiquid", "Single-Phase\nImmersion", "Two-Phase\nImmersion"]
    it_capacity = [325, 400, 442, 477, 485]
    pue = [1.60, 1.30, 1.15, 1.04, 1.025]

    colors = [C_RED, C_ORANGE, C_GOLD, C_TEAL, C_GREEN]
    bars = ax.bar(range(len(techs)), it_capacity, color=colors, width=0.55, edgecolor="none")

    ax2 = ax.twinx()
    ax2.plot(range(len(techs)), pue, "o-", color=C_NAVY, lw=2, markersize=8, zorder=5)
    ax2.set_ylabel("PUE", fontsize=10, color=C_NAVY)
    ax2.set_ylim(0.9, 1.8)
    ax2.spines["top"].set_visible(False)

    ax.set_xticks(range(len(techs)))
    ax.set_xticklabels(techs, fontsize=8)
    ax.set_ylabel("Effective IT Capacity (kW)", fontsize=10, color=C_MID_GRAY)
    ax.set_title("Cooling Technology Impact on 500kW Facility", fontsize=13,
                 fontweight="bold", color=C_NAVY, pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, 550)

    for bar, val in zip(bars, it_capacity):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
                f"{val}kW", ha="center", fontsize=8, fontweight="bold", color=C_DARK_TEXT)

    fig.tight_layout()
    return _save(fig, "cooling")


# =============================================================================
# DOCUMENT HELPERS
# =============================================================================

doc = None  # global document reference


def init_doc():
    global doc
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = FONT_BODY
    style.font.size = Pt(10.5)
    style.font.color.rgb = RGB_DARK_TEXT
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.line_spacing = 1.2

    # Page setup
    section = doc.sections[0]
    section.page_width  = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin    = Inches(0.8)
    section.bottom_margin = Inches(0.7)
    section.left_margin   = Inches(0.9)
    section.right_margin  = Inches(0.9)

    # Header
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "ANDD Network  |  Whitepaper v3.0  |  March 2026"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = hp.runs[0]
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGB_MID_GRAY
    run.font.name = FONT_BODY

    # Footer with page number
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run()
    run.font.size = Pt(8)
    run.font.color.rgb = RGB_MID_GRAY
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run._r.append(fldChar1)
    run2 = fp.add_run()
    fldCode = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run2._r.append(fldCode)
    run3 = fp.add_run()
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run3._r.append(fldChar2)


def add_image(path, width=Inches(6.5)):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run()
    try:
        run.add_picture(path, width=width)
    except Exception:
        run.text = "[Image could not be loaded]"
        run.font.color.rgb = RGB_MID_GRAY


def heading1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(28)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = FONT_HEADING
    run.font.size = Pt(22)
    run.font.color.rgb = RGB_NAVY
    run.bold = True
    # Add accent line below
    line = doc.add_paragraph()
    line.paragraph_format.space_before = Pt(0)
    line.paragraph_format.space_after = Pt(10)
    r = line.add_run()
    # Use a thin table as a colored line
    return p


def accent_line():
    """Add a thin colored accent line."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = tbl.cell(0, 0)
    cell.text = ""
    cell.width = Inches(2)
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{H_ACCENT}"/>'))
    # Set row height very small
    tr = tbl.rows[0]._tr
    trPr = tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:trHeight {nsdecls("w")} w:val="40" w:hRule="exact"/>'))
    # Remove cell borders
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))
    # Table width
    tblPr = tbl._tbl.tblPr
    if tblPr is None:
        tblPr = tbl._tbl.get_or_add_tblPr()
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))


def section_heading(number, title):
    heading1(f"{number}. {title}")
    accent_line()


def heading2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = FONT_HEADING
    run.font.size = Pt(15)
    run.font.color.rgb = RGB_BLUE
    run.bold = True


def heading3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = FONT_HEADING
    run.font.size = Pt(12)
    run.font.color.rgb = RGB_ACCENT
    run.bold = True


def body(text, space_after=Pt(6)):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 1.25
    run = p.add_run(text)
    run.font.name = FONT_BODY
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGB_DARK_TEXT
    return p


def body_bold(text):
    p = body("")
    p.runs[0].text = ""
    run = p.add_run(text)
    run.font.name = FONT_BODY
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGB_DARK_TEXT
    run.bold = True
    return p


def bullet(text, level=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    indent = Inches(0.25 + level * 0.25)
    p.paragraph_format.left_indent = indent
    p.paragraph_format.first_line_indent = Inches(-0.2)
    marker = "●" if level == 0 else "○"
    run = p.add_run(f"{marker}  {text}")
    run.font.name = FONT_BODY
    run.font.size = Pt(10)
    run.font.color.rgb = RGB_DARK_TEXT
    return p


def callout(text, title=""):
    """Accent-bordered callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    # Clear default paragraph
    cell.paragraphs[0].clear()

    if title:
        tp = cell.paragraphs[0]
        tr = tp.add_run(title)
        tr.font.name = FONT_HEADING
        tr.font.size = Pt(11)
        tr.font.color.rgb = RGB_NAVY
        tr.bold = True
        tp.paragraph_format.space_after = Pt(4)
        bp = cell.add_paragraph()
    else:
        bp = cell.paragraphs[0]

    br = bp.add_run(text)
    br.font.name = FONT_BODY
    br.font.size = Pt(10)
    br.font.color.rgb = RGB_DARK_TEXT
    bp.paragraph_format.space_after = Pt(2)

    # Style cell
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{H_LIGHT_BG}"/>'))
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{H_ACCENT}"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="100" w:type="dxa"/>'
        f'<w:left w:w="180" w:type="dxa"/>'
        f'<w:bottom w:w="100" w:type="dxa"/>'
        f'<w:right w:w="120" w:type="dxa"/>'
        f'</w:tcMar>'
    ))

    # Remove table outer borders
    tblPr = tbl._tbl.tblPr
    if tblPr is None:
        tblPr = tbl._tbl.get_or_add_tblPr()
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))


def data_table(headers, rows, col_widths=None):
    """Professional styled data table."""
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True

    # Header row
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        run.font.name = FONT_HEADING
        run.font.size = Pt(9)
        run.font.color.rgb = RGB_WHITE
        run.bold = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{H_NAVY}"/>'))
        tcPr.append(parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="50" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
            f'<w:bottom w:w="50" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
            f'</w:tcMar>'
        ))

    # Data rows
    for r_idx, row in enumerate(rows):
        bg = H_WHITE if r_idx % 2 == 0 else H_LIGHT_BG
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = FONT_BODY
            run.font.size = Pt(9)
            run.font.color.rgb = RGB_DARK_TEXT
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg}"/>'))
            tcPr.append(parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'<w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
                f'<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
                f'</w:tcMar>'
            ))

    # Remove default borders, add subtle grid
    tblPr = tbl._tbl.tblPr
    if tblPr is None:
        tblPr = tbl._tbl.get_or_add_tblPr()
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{H_WARM_GRAY}"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{H_WARM_GRAY}"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="single" w:sz="2" w:space="0" w:color="{H_WARM_GRAY}"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tblBorders>'
    ))

    # Set column widths if provided
    if col_widths:
        tblGrid = tbl._tbl.tblGrid
        for gridCol, w in zip(tblGrid.findall(qn('w:gridCol')), col_widths):
            gridCol.set(qn('w:w'), str(int(w * 1440)))  # inches to twips


def page_break():
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(docx_break_type=7)  # page break


# python-docx break type constant
import docx.oxml
docx_break_type = 7  # not used directly; we use the XML approach

def page_break():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    br = parse_xml(f'<w:br {nsdecls("w")} w:type="page"/>')
    run._r.append(br)


# =============================================================================
# CONTENT — COVER PAGE
# =============================================================================

def build_cover(img_cover):
    # Spacer
    for _ in range(2):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("AI Native Distributed Datacenters")
    run.font.name = FONT_HEADING
    run.font.size = Pt(32)
    run.font.color.rgb = RGB_NAVY
    run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(20)
    run = p.add_run("A Technical Architecture for Sovereign, Resilient,\nAI-Managed Edge Infrastructure")
    run.font.name = FONT_HEADING
    run.font.size = Pt(15)
    run.font.color.rgb = RGB_BLUE

    # Cover image
    add_image(img_cover, width=Inches(6.2))

    # Subtitle
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("ANDD Network — Whitepaper v3.0")
    run.font.name = FONT_HEADING
    run.font.size = Pt(14)
    run.font.color.rgb = RGB_ACCENT
    run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("March 2026")
    run.font.name = FONT_BODY
    run.font.size = Pt(12)
    run.font.color.rgb = RGB_MID_GRAY

    # Contact
    for _ in range(3):
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("contact@andd.network  |  andd.network")
    run.font.name = FONT_BODY
    run.font.size = Pt(10)
    run.font.color.rgb = RGB_MID_GRAY

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run("CONFIDENTIAL")
    run.font.name = FONT_HEADING
    run.font.size = Pt(9)
    run.font.color.rgb = RGB_MID_GRAY
    run.bold = True


# =============================================================================
# CONTENT — TABLE OF CONTENTS
# =============================================================================

def build_toc():
    page_break()
    heading1("Table of Contents")
    accent_line()

    sections = [
        ("1", "Executive Summary"),
        ("2", "The Case for Decentralization"),
        ("3", "ANDD Architecture Overview"),
        ("4", "Technical Architecture"),
        ("5", "Software Platform Architecture"),
        ("6", "Bandwidth & Connectivity Requirements"),
        ("7", "Energy Requirements & Mitigation Strategies"),
        ("8", "AI-Native Operations"),
        ("9", "Resilience Through Decentralization"),
        ("10", "Payment Architecture"),
        ("11", "DePIN Integration & Pressure Test"),
        ("12", "Opportunity Zone Alignment"),
        ("13", "Okopipi Integration: Network-Native Consensus"),
        ("14", "Implementation Roadmap"),
        ("15", "Conclusion"),
    ]
    for num, title in sections:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(0.5))
        run = p.add_run(f"{num}.")
        run.font.name = FONT_HEADING
        run.font.size = Pt(11)
        run.font.color.rgb = RGB_ACCENT
        run.bold = True
        run2 = p.add_run(f"\t{title}")
        run2.font.name = FONT_BODY
        run2.font.size = Pt(11)
        run2.font.color.rgb = RGB_DARK_TEXT


# =============================================================================
# CONTENT — ALL SECTIONS
# =============================================================================

def build_section_1():
    page_break()
    section_heading("1", "Executive Summary")

    body("The global compute infrastructure serving AI, critical services, and digital economies is dangerously concentrated. Fewer than 30 hyperscale campuses in the United States process the vast majority of AI inference, financial transactions, government data, and emergency communications. This concentration creates single points of failure for national security, economic continuity, and community resilience — and it leaves underserved regions permanently behind.")

    body_bold("ANDD (AI Native Distributed Datacenters) proposes a fundamentally different model:")

    body("A network of hundreds to thousands of sub-2MW edge datacenters, deployed across federally designated Opportunity Zones, forming an interconnected mesh fabric that is entirely managed and operated by artificial intelligence. No human operators provision servers. No human billing clerks process invoices. No human technicians schedule maintenance windows. The AI management layer handles customer onboarding, capacity planning, workload routing, billing, compliance reporting, and predictive maintenance autonomously — achieving operational economics that make sub-2MW facilities viable at scale.")

    callout(
        "This whitepaper presents the technical architecture, infrastructure requirements, and economic model for the ANDD network. It details the four hardware domains (Compute, Storage, Connectivity, AI Accelerators), the bandwidth and energy profiles for each site, mitigation strategies for power resilience through renewables and microgrids, and the payment architecture spanning fiat subscriptions to real-time crypto micro-transactions.",
        title="Scope"
    )

    body("The ANDD network serves six constituencies:")
    bullet("Communities and local governments needing public safety and smart-city infrastructure")
    bullet("Startups requiring edge compute without building their own")
    bullet("Blockchain and Web3 projects needing reliable DePIN backbone")
    bullet("Regional fintech with data residency mandates")
    bullet("State and federal agencies requiring sovereign, defense-compatible infrastructure")
    bullet("Telcos extending their edge footprint")

    body("By aligning deployment with Opportunity Zones, ANDD simultaneously unlocks investor tax incentives (capital gains deferral, basis step-up, and the 10-year appreciation exclusion) while delivering jobs, connectivity, and AI capabilities to the communities that need them most.")


def build_section_2(img_concentration):
    page_break()
    section_heading("2", "The Case for Decentralization")

    heading2("2.1 The Concentration Problem")

    body("The current datacenter landscape in the United States is defined by extreme geographic concentration. Northern Virginia alone hosts over 70% of internet traffic on the East Coast. The top five metro markets account for a disproportionate share of total U.S. datacenter capacity.")

    add_image(img_concentration, width=Inches(6.0))

    body("This concentration creates compounding vulnerabilities:")

    body_bold("National Security Exposure.")
    body("A coordinated attack — physical, cyber, or electromagnetic — on fewer than a dozen campuses could degrade the operational capacity of federal agencies, financial markets, and defense communications simultaneously. The Department of Defense increasingly relies on commercial cloud infrastructure through programs like JWCC (Joint Warfighting Cloud Capability). When that commercial infrastructure is concentrated in the same geographic corridors, military continuity of operations becomes coupled to civilian infrastructure vulnerabilities.")

    body_bold("Latency Inequality.")
    body("Communities more than 50 milliseconds from the nearest hyperscale region cannot participate in latency-sensitive applications: real-time AI inference, telemedicine, autonomous vehicle coordination, AR/VR, or high-frequency financial services. Light in fiber travels at roughly 200km per millisecond — for applications requiring sub-10ms response, the service boundary of a centralized datacenter extends no more than 50–100km in practice.")

    body_bold("Sovereignty Erosion.")
    body("When all compute runs through a handful of corporate campuses, government data, municipal systems, and critical infrastructure become dependent on the operational decisions and pricing power of three to four hyperscale vendors. Municipalities have already experienced service disruptions during hyperscale provider outages affecting 911 dispatch, traffic management, and water system monitoring.")

    body_bold("Grid Strain.")
    body("Hyperscale campuses are now the largest single consumers of electricity in their host regions. The IEA projects global datacenter electricity consumption could reach 945–1,300 TWh by 2030, with AI workloads as the primary growth driver. Distributing the same total compute across hundreds of sub-2MW facilities spreads the load across dozens of utility territories and avoids transmission bottlenecks.")

    body_bold("Supply Chain Concentration.")
    body("When a small number of hyperscale operators dominate procurement of GPUs, networking equipment, and power infrastructure, smaller players face multi-year lead times and unfavorable pricing. ANDD's modular, standardized design uses commonly available equipment at scales that avoid competing directly with hyperscale procurement volumes.")

    heading2("2.2 Why Distributed Edge, Why Now")

    body("Five converging trends make the distributed edge datacenter model not only viable but urgent:")

    bullet("AI Inference is Moving to the Edge — inference accounts for 60–70% of all AI compute cycles and is the fastest-growing segment. A single inference server with 4–8× NVIDIA L40S cards can serve meaningful regional AI workloads.")
    bullet("DePIN Requires Enterprise-Grade Physical Infrastructure — enterprise customers require 99.99% uptime, N+1 redundancy, physical security, and compliance certifications that consumer-grade nodes cannot provide.")
    bullet("Federal Policy Now Incentivizes Distributed Deployment — the Opportunity Zone program (made permanent by the One Big Beautiful Bill Act of 2025), combined with DOE GRIP ($10.5B), BEAD ($42.45B), and IRA tax credits, creates unprecedented funding alignment.")
    bullet("Real-Time Applications Are Proliferating — NG911, FirstNet, autonomous V2X, industrial IoT, and AR/VR all require sub-20ms local infrastructure.")
    bullet("The Hardware Has Caught Up — inference-optimized GPUs (L4 at 72W, L40S at 300W), direct liquid cooling, and prefabricated modular enclosures compress deployment from 18–24 months to 60–90 days.")

    heading2("2.3 The AI-Native Differentiator")

    body("Previous attempts at distributed datacenter networks failed primarily on operational economics. A sub-2MW facility cannot justify the cost of a full-time site manager, network engineer, and facilities technician.")

    data_table(
        ["Cost Category", "% of OpEx", "Scalable by AI?"],
        [
            ["Facilities staff (24/7)", "15–20%", "Yes — predictive maintenance + dispatched field service"],
            ["Network operations (NOC)", "10–15%", "Yes — AI-driven monitoring, automated remediation"],
            ["Sales & customer mgmt", "10–15%", "Yes — AI onboarding, self-service provisioning"],
            ["Billing & finance", "5–8%", "Yes — automated metering, invoicing, reconciliation"],
            ["Compliance & reporting", "5–10%", "Partially — AI generates reports, human signs off"],
            ["Power & cooling", "30–40%", "Optimizable — AI thermal management, demand response"],
        ]
    )

    callout(
        "ANDD inverts this equation by making AI the operator. The target operating model is one human operator per 20–50 edge nodes, with AI handling >95% of operational tasks autonomously. A network of 200 edge nodes requires a team of 4–10 people rather than the 600–1,000 a traditional operator would need.",
        title="The Economic Unlock"
    )

    heading2("2.4 Failure Mode Analysis")

    body("Understanding why earlier distributed models failed is essential:")
    bullet("EdgeConneX / Vapor IO / EdgeMicro (2015–2022) — relied on traditional human operations, couldn't achieve economics below 1–2MW. Lesson: AI-native operations are a prerequisite, not an optimization.")
    bullet("Decentralized compute (BOINC, Folding@home) — lacked economic incentives and availability guarantees. Lesson: Token incentives solve motivation; enterprise hardware solves reliability.")
    bullet("Micro-datacenter attempts (containers, towers) — non-standard form factors, no network effects. Lesson: Standardized modular design with mesh networking creates compounding value.")
    bullet("Telco edge (MEC) — underdelivered due to carrier lock-in and operational misalignment. Lesson: Edge must be carrier-neutral and open to all customers.")


def build_section_3(img_three_tier):
    page_break()
    section_heading("3", "ANDD Architecture Overview")

    heading2("3.1 Design Principles")

    body("The ANDD architecture is governed by five principles:")
    bullet("No single point of failure at any layer — every component is designed with redundancy; the mesh topology ensures loss of any node, link, or hub does not partition the network.")
    bullet("Horizontal scalability from day one — scales by adding nodes, not enlarging them. Designed for 5 to 5,000 nodes without architectural changes.")
    bullet("Location-aware intelligence — the AI control plane continuously reasons about geography, jurisdiction, environmental conditions, and demand patterns for real-time optimization.")
    bullet("Defense-in-depth security — zero-trust networking (mTLS), hardware root of trust (TPM 2.0), confidential computing (SEV-SNP/TDX), and physical security provide overlapping layers.")
    bullet("AI-first operations — every operational process is designed for AI agents as the primary operator, with human escalation as the exception path.")

    heading2("3.2 Network Topology")

    add_image(img_three_tier, width=Inches(6.2))

    heading3("Tier 1 — Edge Nodes (200kW–500kW)")
    body("The atomic unit of the ANDD network. Each edge node is a modular, prefabricated facility deployable in 60–90 days, containing a configurable mix of compute, storage, connectivity, and AI accelerator hardware.")

    data_table(
        ["Parameter", "200kW Node", "500kW Node"],
        [
            ["Footprint", "400–600 sq ft", "800–1,200 sq ft"],
            ["Rack count", "4–8 racks", "10–20 racks"],
            ["IT load capacity", "150kW", "380kW"],
            ["Deployment time", "60–90 days (prefab)", "90–120 days (prefab)"],
            ["Power redundancy", "N+1 UPS, dual utility feed", "N+1 UPS, dual feed, gen/fuel cell"],
            ["Cooling", "N+1 DLC pumps, ambient air backup", "N+1 DLC + immersion, ambient backup"],
            ["Network uplinks", "2 (primary + redundant)", "3+ (primary + redundant + mesh)"],
        ]
    )

    body("Edge nodes are deployed in Opportunity Zones, with site selection driven by the AI control plane scoring: population density, fiber proximity, power availability, mesh distance, OZ designation, and pre-committed demand.")

    heading3("Tier 2 — Regional Hubs (1–2MW)")
    body("Aggregation points providing higher-density compute, regional storage caching, peering interconnection, and backhaul concentration. Each regional hub serves 5–15 edge nodes.")
    bullet("Training-class GPU infrastructure (H100/H200/B200/GB200 with NVLink)")
    bullet("Dense peering with Tier 1 transit, cloud on-ramps, and CDN providers")
    bullet("Regional storage cache for low-latency retrieval")
    bullet("Full AI reasoning stack for the management layer")
    bullet("Compliance boundary for government and regulated-industry customers")

    heading3("Tier 3 — AI Control Plane (Distributed)")
    body("Not a centralized cloud but a distributed consensus system running across all regional hubs. Uses BFT consensus (HotStuff/DiemBFT lineage) ensuring the network functions correctly even if up to one-third of hubs are compromised. Latency-sensitive functions use eventually consistent federated protocols for immediate local action.")

    heading2("3.3 Mesh Interconnection")
    body("Mesh peering is the architectural innovation that distinguishes ANDD from a traditional hub-and-spoke topology. Edge nodes within ~100km establish direct peering links enabling:")
    bullet("Local traffic exchange at <2ms latency (vs 10–20ms through hub)")
    bullet("Failover capacity — reroute through mesh peers when hub uplink fails")
    bullet("Distributed workload migration — stream directly to adjacent peers")

    callout(
        "With 100 nodes each at 99.95% uptime and only 70% required for full service, the probability of network-level failure is effectively zero (10⁻⁴⁷).",
        title="Mathematical Resilience"
    )


def build_section_4(img_hardware):
    page_break()
    section_heading("4", "Technical Architecture")

    heading2("4.1 Four Hardware Domains")
    body("Each ANDD site deploys a configurable mix across four hardware domains, with ratios determined by the AI control plane based on local demand.")

    add_image(img_hardware, width=Inches(6.2))

    heading3("4.1.1 Compute")
    body("High-density 1U/2U servers (AMD EPYC 9004 / Intel Xeon 6 / Ampere Altra Max) with 256GB–1TB DDR5, operating at 20–40kW per rack. ARM-based servers handle power-efficient always-on workloads; x86 handles legacy and HPC tasks.")

    heading3("4.1.2 Storage")
    body("NVMe SSD hot tier (100TB–500TB) and QLC SSD / HDD warm tier (500TB–2PB) per site, with S3-compatible object, NFS/SMB block, and distributed file system protocols. Erasure coded across 3+ geographically distinct nodes, providing 99.999999999% (11 nines) durability.")

    heading3("4.1.3 Connectivity")
    body("100GbE leaf-spine internal fabric (upgradable to 400GbE), 10–100 Gbps fiber backhaul, direct peering with regional ISPs and CDNs, 5G/CBRS wireless, and SIPRNet/NIPRNet gateway capability for defense customers.")

    heading3("4.1.4 AI Accelerators")

    data_table(
        ["Accelerator", "TDP", "Memory", "Memory BW", "Deployment"],
        [
            ["NVIDIA L4", "72W", "24GB GDDR6", "300 GB/s", "Edge (efficient inference)"],
            ["NVIDIA L40S", "300W", "48GB GDDR6X", "864 GB/s", "Edge (inference)"],
            ["AMD MI300X", "750W", "192GB HBM3", "5.3 TB/s", "Edge/Hub (inference)"],
            ["AMD MI325X", "750W", "256GB HBM3e", "6.0 TB/s", "Edge/Hub (large model)"],
            ["NVIDIA H100 SXM", "700W", "80GB HBM3", "3.35 TB/s", "Hub (training+inference)"],
            ["NVIDIA H200 SXM", "700W", "141GB HBM3e", "4.8 TB/s", "Hub (large model serving)"],
            ["NVIDIA B200", "1,000W", "192GB HBM3e", "8.0 TB/s", "Hub (training)"],
            ["NVIDIA GB200 NVL2", "2,700W", "384GB HBM3e", "16 TB/s", "Hub (liquid-cooled)"],
        ]
    )

    heading3("Edge AI Workload Feasibility")
    data_table(
        ["Workload", "Hardware Required", "Power", "Latency"],
        [
            ["LLM inference (7–13B)", "1× L40S or 1× MI300X", "300–750W", "20–100ms/token"],
            ["LLM inference (70B)", "2–4× H100 or 1× MI300X", "700W–1.4kW", "50–200ms/token"],
            ["Real-time image/video", "1× L4", "72W", "5–20ms"],
            ["Speech recognition", "1× L4", "72W", "<100ms"],
            ["RAG pipeline", "1–2× H100 + vector DB", "1–2kW", "100–500ms"],
            ["Real-time fraud detection", "1× L40S", "300W", "<50ms"],
        ]
    )

    heading2("4.2 Software Stack")
    body("Orchestration via lightweight Kubernetes (K3s/RKE2) federated across the mesh. Software-defined networking (OVS/VPP) provides tenant isolation. Ceph/MinIO provides unified storage with AI-enforced placement policies. Every sensor feeds into an AI-controlled building management system.")

    heading2("4.3 Security Architecture")
    bullet("Zero-trust networking — every workload-to-workload communication is mTLS encrypted")
    bullet("Hardware root of trust — TPM 2.0, measured boot, remote attestation")
    bullet("Tenant isolation — SR-IOV for network, SEV-SNP/TDX for confidential computing, separate encryption keys per tenant")
    bullet("Physical security — biometric access, 24/7 AI-monitored surveillance, tamper-evident racks; SCIF options for government")
    bullet("Compliance paths — FedRAMP, SOC 2, HIPAA, CJIS, ITAR built in from day one")


def build_section_5(img_stack):
    page_break()
    section_heading("5", "Software Platform Architecture")

    body("The ANDD software platform is a set of loosely coupled, event-driven microservices running on the same Kubernetes infrastructure it manages — a self-hosting architecture that aligns incentives.")

    add_image(img_stack, width=Inches(6.2))

    heading2("5.1 Platform Architecture Layers")

    data_table(
        ["Layer", "Purpose", "Key Technologies"],
        [
            ["Agent Runtime", "Hosts AI agent processes, enforces guardrails", "Custom framework, LLM inference, sandboxing"],
            ["Event Fabric", "Collects, routes, stores events/telemetry", "Kafka/Redpanda, Flink stream processing"],
            ["State Store", "Persistent operational data", "CockroachDB, etcd, Redis"],
            ["Actuation Layer", "Translates agent decisions to changes", "Kubernetes API, Redfish, gNMI, Modbus"],
            ["Observability", "Metrics, logs, traces, AI audit trails", "Prometheus+Thanos, Loki, Jaeger"],
            ["API Gateway", "Customer and DePIN integration APIs", "Kong/Envoy, GraphQL + REST + gRPC"],
            ["Identity & Access", "Auth, tenant isolation", "OIDC/OAuth2, SPIFFE/SPIRE, OPA"],
        ]
    )

    heading2("5.2 Event-Driven Data Architecture")
    body("Every state change — temperature reading, workload deployment, payment received, disk error, BGP route change — is captured as an immutable event. AI agents consume event streams rather than polling, enabling real-time response and full auditability. Total telemetry per edge node: ~1.2 GB/day (~15 KB/second sustained).")

    body("Events flow through a three-stage pipeline:")
    bullet("Stage 1: Local Processing (Edge Node) — real-time anomaly detection, billing aggregation, local alerts, event filtering")
    bullet("Stage 2: Regional Aggregation (Hub) — cross-node correlation, SLA monitoring, AI agent input preparation, persistent storage")
    bullet("Stage 3: Global Reconciliation (Control Plane) — network-wide capacity planning, billing reconciliation, model performance monitoring")

    heading2("5.3 Agent-to-Infrastructure Actuation")
    body("AI agents issue structured, validated, reversible actions through a controlled actuation layer. Every action has pre-conditions, dry-run mode, blast radius annotation, rollback procedure, and configurable approval gates.")

    body("Action execution pipeline: Agent emits intent → Validation engine checks pre-conditions → OPA policy evaluation → Approval gate (based on blast radius) → Execution → Post-action verification → Immutable audit log.")

    heading2("5.4 Agent Coordination")
    body("Multiple concurrent agents use distributed resource locking (scoped, time-bounded, queued, preemptible) and DAG-based multi-step operation orchestration. Conflict resolution follows a priority hierarchy: Safety > SLA Guardian > Predictive Maintenance > Provisioning > Billing > Optimization.")

    heading2("5.5 AI/ML Pipeline")
    data_table(
        ["Model Type", "Architecture", "Deployment", "Update Frequency"],
        [
            ["Foundation reasoning", "Fine-tuned LLM (70B+)", "Regional Hubs", "Quarterly major, monthly fine-tune"],
            ["Predictive maintenance", "Time-series transformer", "Edge + Hubs", "Monthly retraining"],
            ["Workload scheduler", "Reinforcement learning", "Regional Hubs", "Continuous online learning"],
            ["Anomaly detection", "Autoencoder + statistical", "Edge Nodes", "On new hardware intro"],
            ["Network optimizer", "Graph neural network", "Regional Hubs", "Weekly retraining"],
            ["Demand forecaster", "Temporal fusion transformer", "Control Plane", "Daily retraining"],
        ]
    )

    body("Model updates deploy through four stages: Shadow Mode (log-only on single hub) → Canary (5–10% of network) → Graduated Rollout (25% → 50% → 75% → 100%) → Full Production (previous model retained as hot standby for 30 days).")

    heading2("5.6 Observability and Auditability")
    body("Every AI agent decision is logged with: trigger, context, reasoning chain, alternatives considered, outcome, and compliance tags. The audit trail is immutable (append-only with cryptographic chaining) and retained for 7 years. Government customers access tenant-specific trails through a dedicated compliance portal.")

    heading2("5.7 Multi-Tenancy Enforcement")
    body("Isolation is enforced at every layer: Kubernetes namespaces + SEV-SNP/TDX for compute, per-tenant VXLAN overlays + SR-IOV for network, separate Ceph pools with per-tenant encryption for storage, MIG/passthrough for GPU, per-tenant RBAC and OPA policies for management, SPIFFE certificates and Vault-managed keys for cryptographic isolation.")


def build_section_6(img_bw):
    page_break()
    section_heading("6", "Bandwidth & Connectivity Requirements")

    add_image(img_bw, width=Inches(6.0))

    heading2("6.1 Backhaul Architecture")
    data_table(
        ["Site Type", "Primary Uplink", "Backup", "Peering"],
        [
            ["Urban Edge Node", "Dark/Lit Fiber 10–40G", "5G/LTE-A 1–5G", "ISPs, Cloud On-Ramps, CDN"],
            ["Suburban Edge Node", "Fiber 10–40G", "2nd carrier fiber 10G", "ISPs, Cloud On-Ramps, CDN"],
            ["Rural Edge Node", "E-band wireless + LEO sat", "5G/LTE-A 0.5–1G", "Regional ISPs"],
            ["Regional Hub", "Tier 1 transit 100G", "2nd provider 40G", "All above + direct transit peering"],
        ]
    )

    heading2("6.2 Network Protocol Stack")
    bullet("Underlay: eBPF-accelerated IP routing with SRv6 segment routing")
    bullet("Overlay: WireGuard/MACsec encrypted tunnels, VXLAN/GENEVE for tenant isolation")
    bullet("Peering: Automated BGP with RPKI validation and route leak detection")
    bullet("DNS: Anycast across all nodes for automatic geo-routing")
    bullet("Load Balancing: AI-driven GSLB factoring latency, capacity, energy cost, and carbon intensity")

    heading2("6.3 Bandwidth Cost Optimization")
    bullet("Local traffic exchange — ANDD sites function as micro-exchange points, keeping local traffic local")
    bullet("CDN offload — caching at every edge node eliminates redundant backhaul")
    bullet("AI-driven traffic engineering — optimizes routing to minimize paid transit")
    bullet("Graduated deployment — rural sites start low-bandwidth and upgrade with demand")


def build_section_7(img_pue, img_cooling):
    page_break()
    section_heading("7", "Energy Requirements & Mitigation Strategies")

    heading2("7.1 Per-Site Power Profile")
    data_table(
        ["Site Tier", "IT Load", "Total Power", "Target PUE"],
        [
            ["Edge Node (200kW)", "150kW", "200kW", "1.30–1.35"],
            ["Edge Node (500kW)", "380kW", "500kW", "1.30–1.35"],
            ["Regional Hub (2MW)", "1,500kW", "2,000kW", "1.30–1.35"],
        ]
    )

    add_image(img_pue, width=Inches(6.0))

    heading2("7.2 Renewable Integration")
    body("On-site solar offsets 30–50% of annual energy. LFP battery systems provide peak shaving, solar time-shifting, grid services revenue ($50–150/kW-year), and 2–4 hour backup. IRA incentives (30–50% ITC) drive effective payback to 2–4 years.")

    heading2("7.3 Fuel Cells")
    bullet("Solid Oxide (SOFC) — 65% efficiency on natural gas/biogas, 300kW per Bloom Energy Server, validated by Equinix deployments")
    bullet("PEM (hydrogen) — instant-on backup, zero emissions, 72+ hour runtime from standard tube trailer, piloted by Microsoft, Google, and Equinix")

    heading2("7.4 Microgrid Architecture")
    body("For maximum resilience, ANDD sites operate as self-contained microgrids with four modes: Grid-Connected (normal), Peak Shaving (demand charge mitigation), Islanded (full self-sufficiency during grid outage), and Emergency (priority power to critical workloads, shed non-essential load).")

    heading2("7.5 Cooling Efficiency")

    add_image(img_cooling, width=Inches(6.0))

    callout(
        "Moving from air cooling (PUE 1.5) to immersion (PUE 1.05) saves ~300kW of cooling power in a 1MW facility — effectively increasing usable compute capacity by 30% within the same power envelope.",
        title="Key Insight"
    )

    body("Direct Liquid Cooling (DLC) is the ANDD baseline for all GPU and high-density racks. Cold plates capture 70–80% of heat at the source, achieving zero water consumption — a significant advantage over hyperscale evaporative cooling. Waste heat at 35–45°C is suitable for building heating, agricultural greenhouses, or district heating.")


def build_section_8(img_opex, img_agents):
    page_break()
    section_heading("8", "AI-Native Operations")

    heading2("8.1 The Autonomous Datacenter Thesis")
    body("Traditional datacenter operations depend on human operators at every layer. These costs establish a minimum viable facility size — typically 5MW+ — below which operations are not sustainable. ANDD eliminates this constraint by replacing human operational roles with specialized AI agents.")

    add_image(img_opex, width=Inches(6.0))

    heading2("8.2 AI Agent Architecture")

    add_image(img_agents, width=Inches(6.2))

    body_bold("Customer Onboarding Agent")
    body("Handles the entire customer lifecycle: qualifies leads through conversational AI, generates custom proposals, executes KYC/KYB verification, provisions tenant environments. No human sales team required for standard deployments.")

    body_bold("Provisioning Agent")
    body("Transforms requirements into running infrastructure: selects optimal node placement, deploys virtual networks/storage/compute/GPU, configures monitoring and auto-scaling. Completes in minutes what traditionally takes days.")

    body_bold("Billing & Revenue Agent")
    body("Meters at sub-second granularity, generates invoices, settles micro-transactions in real-time, detects anomalies, reconciles fiat and crypto streams into unified financial reporting.")

    body_bold("Predictive Maintenance Agent")
    body("Ingests all hardware telemetry, maintains digital twins with failure probability models, schedules preventive replacements during low-utilization windows, coordinates workload migration before maintenance, dispatches field technicians with precise automated work orders.")

    body_bold("SLA Guardian Agent")
    body("Continuously monitors performance against SLA thresholds, triggers automated remediation before breach, generates compliance reports, calculates and issues credits automatically.")

    heading2("8.3 Human-in-the-Loop Design")
    body("Humans remain for: exception handling (low-confidence situations), strategic decisions (pricing, expansion, partnerships), physical maintenance (hardware swaps), and compliance oversight (regulatory sign-off).")

    callout(
        "Target ratio: one human operator per 20–50 edge nodes — a 10–25× improvement over traditional staffing models. This is the economic unlock that makes the distributed model viable.",
        title="Staffing Model"
    )


def build_section_9(img_resilience):
    page_break()
    section_heading("9", "Resilience Through Decentralization")

    add_image(img_resilience, width=Inches(6.0))

    heading2("9.1 Payments Infrastructure")
    body("The U.S. payment system processes over $10 trillion daily through networks that depend on datacenter infrastructure in a handful of locations. ANDD provides distributed payment processing nodes, local settlement capability during backbone disruptions, and crypto/stablecoin rails as backup.")

    heading2("9.2 Energy Grid")
    body("ANDD hosts distributed SCADA/EMS systems resilient to localized attacks, provides edge computing for DER control loops (<10ms), aggregates distributed BESS into a virtual power plant for grid services, and supports microgrid islanding during grid emergencies.")

    heading2("9.3 Emergency Services & Public Safety")
    bullet("Local NG911 hosting — continues even when backhaul is disrupted")
    bullet("FirstNet/public safety broadband edge — body cameras, mapping, resource tracking in degraded conditions")
    bullet("Emergency operations center computing — local incident management during disasters")
    bullet("Satellite backhaul resilience — LEO connectivity when terrestrial networks are damaged")

    heading2("9.4 Utilities & Water Systems")
    body("Local SCADA hosting, air-gapped operation capability for critical utilities, and AI-powered anomaly detection with sub-second response for contamination, leaks, or cyber intrusion.")


def build_section_10(img_payment):
    page_break()
    section_heading("10", "Payment Architecture")

    add_image(img_payment, width=Inches(6.2))

    heading2("10.1 Fiat Payment Rails")
    data_table(
        ["Tier", "Model", "Payment Methods", "Use Case"],
        [
            ["Starter", "Monthly post-paid", "Credit card, ACH", "Startups, developers"],
            ["Professional", "Monthly/Annual", "ACH, wire", "Mid-market, fintech"],
            ["Enterprise", "Annual custom", "Wire, ACH, PO-backed", "Large enterprise, telcos"],
            ["Government", "Annual/Multi-year", "Treasury/PO systems", "Federal, state, local gov"],
        ]
    )

    heading2("10.2 Digital & Crypto Payment Rails")
    body("ANDD accepts stablecoins (USDC, USDT) on Ethereum L1 (large payments), Solana (high-frequency, ~$0.001/tx), and Ethereum L2s (balance of cost and security). For DePIN projects, payment channels enable micro-transactions down to fractions of a cent with periodic on-chain settlement.")

    heading2("10.3 Smart Contract SLAs")
    body("Programmable SLAs encoded as smart contracts that automatically enforce service commitments. When the oracle reports uptime below target (e.g., <99.99%), credits are calculated proportionally and transferred to the tenant's wallet automatically — no human claims process, no disputes.")

    heading2("10.4 ANDD Network Token (Future)")
    body("A native utility token is contemplated (subject to regulatory analysis) for: capacity reservation staking, DePIN incentive alignment for third-party infrastructure operators, governance voting on network parameters, and a burn mechanism creating deflationary pressure proportional to usage.")


def build_section_11(img_depin):
    page_break()
    section_heading("11", "DePIN Integration & Pressure Test")

    heading2("11.1 Case Studies")

    body_bold("Helium (Wireless/IoT)")
    body("Deployed 900,000+ hotspots, proving token-incentivized infrastructure works — but consumer hardware suffered unreliable uptime and coverage was deployer-driven, not demand-driven. ANDD lesson: AI-driven location selection and enterprise-grade hardware are non-negotiable.")

    body_bold("Filecoin (Storage)")
    body("Accumulated 22+ EiB capacity but most is empty \"committed capacity\" sealed for block rewards. ANDD lesson: incentives must be tied to actual utilization, not committed capacity.")

    body_bold("Render Network (GPU)")
    body("Successfully aggregated GPUs for 3D rendering, but consumer GPUs cannot meet the reliability, thermal, and ECC requirements of production AI inference. ANDD lesson: datacenter GPUs in purpose-built facilities, not desktop cards in apartments.")

    body_bold("Akash Network (Compute)")
    body("Created a functioning marketplace undercutting cloud by 70–85%, but provider reliability is inconsistent with no enforceable SLA mechanism. ANDD lesson: smart contract SLAs backed by infrastructure, not reputation scores.")

    heading2("11.2 The Enterprise-Grade Gap")

    add_image(img_depin, width=Inches(5.0))

    data_table(
        ["Dimension", "Consumer DePIN", "ANDD"],
        [
            ["Uptime", "90–98% (best effort)", "99.99% (SLA-backed)"],
            ["Redundancy", "None", "N+1 power, cooling, network"],
            ["Physical Security", "None", "Biometric, surveillance, tamper-evident"],
            ["Compliance", "None", "FedRAMP, SOC 2, HIPAA, CJIS"],
            ["Power Quality", "Residential (variable)", "UPS-backed, conditioned, BESS backup"],
            ["Connectivity", "Residential broadband", "Multi-provider, redundant, SLA-backed"],
            ["Data Sovereignty", "Unknown/uncontrolled", "Configurable per-tenant restrictions"],
        ]
    )

    callout(
        "ANDD does not compete with DePIN projects — it completes them. DePIN projects own the protocol and application layers; ANDD owns the physical infrastructure and AI operations layers. The tokenomics and demand aggregation work; the physical infrastructure needs upgrading.",
        title="ANDD as DePIN Backbone"
    )


def build_section_12(img_oz):
    page_break()
    section_heading("12", "Opportunity Zone Alignment")

    heading2("12.1 Strategic Rationale")
    body("ANDD's deployment is deliberately aligned with 8,764 federally designated Opportunity Zones — economically distressed census tracts where compute infrastructure creates maximum community impact.")

    heading2("12.2 Tax Incentive Structure")
    body("The Opportunity Zone program, made permanent by the One Big Beautiful Bill Act of 2025, provides three tiers of benefit for Qualified Opportunity Fund investments:")
    bullet("Tier 1 — Capital Gains Deferral: reinvest eligible gains into a QOF within a rolling 5-year window")
    bullet("Tier 2 — Basis Step-Up: 10% step-up at 5+ years (up to 30% for rural OZs via Qualified Rural Opportunity Funds)")
    bullet("Tier 3 — 10-Year Exclusion: zero federal capital gains tax on all appreciation after 10+ years")

    heading2("12.3 Per-Site Community Impact")

    add_image(img_oz, width=Inches(6.2))

    heading2("12.4 Investor Return Model")
    body("A QOF investing in ANDD edge nodes acquires assets that: generate revenue from Year 1, appreciate as the network grows, qualify for the 10-year exclusion on all appreciation, align naturally with the 10-year hold requirement (15–20 year infrastructure useful life), and provide current income through revenue sharing during the hold period.")

    heading2("12.5 Bridging the Digital Divide")
    bullet("Carrier-grade connectivity infrastructure for local ISP interconnection")
    bullet("Community-facing services: municipal apps, telemedicine, educational platforms at minimal latency")
    bullet("Workforce development: local technicians gain transferable datacenter and AI infrastructure skills")
    bullet("Anchor tenant for further commercial development in the OZ")


def build_section_13(img_okopipi):
    page_break()
    section_heading("13", "Okopipi Integration: Network-Native Consensus")

    heading2("13.1 Why ANDD Needs a Network-Native Blockchain")
    body("ANDD's payment and coordination systems currently depend on external blockchains (Solana, Ethereum L2) and traditional databases, creating three architectural tensions:")
    bullet("External blockchain dependency undermines sovereignty — Solana outages disrupt DePIN settlement, Ethereum gas spikes make micro-transactions uneconomical")
    bullet("Traditional blockchains assume stable networks — ANDD operates in degraded backhaul, asymmetric partitions, and contested network environments")
    bullet("Application-layer consensus cannot leverage ANDD's network fabric — duplicating routing intelligence atop infrastructure ANDD already provides")

    body("Okopipi (Venable, 2026) resolves all three by integrating consensus directly into the network fabric at Layers 2 and 3.")

    heading2("13.2 Architecture Mapping")

    add_image(img_okopipi, width=Inches(6.2))

    data_table(
        ["ANDD Tier", "Okopipi Role", "Capabilities"],
        [
            ["Regional Hub", "C-node (consensus)", "Full BLA, block production, archive node"],
            ["Edge Node (500kW)", "R-node + partial validator", "Routing, light validation, local contract execution"],
            ["Edge Node (200kW)", "R-node + light client", "Routing, header verification, selective materialization"],
            ["IoT / constrained", "Light client", "Header-only verification, selective receipt fetching"],
        ]
    )

    heading2("13.3 Integration Benefits")
    bullet("Native settlement replaces all external blockchain dependencies — zero Solana/Ethereum risk")
    bullet("MTU-sized consensus messages work within bandwidth constraints of rural LEO satellite and LTE links")
    bullet("Privacy-preserving execution keeps tenant billing and usage data confidential")
    bullet("AI agents read/write chain state directly via typed reflection layer schemas — no ABI parsing")
    bullet("Post-quantum epoch checkpoints enable trustworthy resynchronization after extended partitions")
    bullet("Selective disclosure policies satisfy FedRAMP/CJIS/HIPAA audit requirements without exposing unrelated tenant data")

    callout(
        "No external dependency at any layer. The entire stack — from the photovoltaic panel on the roof to the smart contract executing a DePIN reward distribution — runs on ANDD infrastructure, coordinated by ANDD's AI agents, settled on Okopipi's network-native consensus.",
        title="Sovereign Infrastructure"
    )


def build_section_14(img_roadmap):
    page_break()
    section_heading("14", "Implementation Roadmap")

    add_image(img_roadmap, width=Inches(6.5))

    heading2("Phase 1: Foundation (Months 1–12)")
    bullet("Finalize AI management layer architecture and begin training specialized agents")
    bullet("Design and certify modular edge node enclosure (200kW reference design)")
    bullet("Deploy 3–5 pilot sites in diverse geographies (urban, suburban, rural OZ locations)")
    bullet("Establish carrier interconnection agreements with 3+ Tier 1 transit providers")
    bullet("Complete SOC 2 Type I certification")
    bullet("Form Qualified Opportunity Fund structure")

    heading2("Phase 2: Network Formation (Months 12–24)")
    bullet("Scale to 20–50 edge nodes forming regional mesh clusters")
    bullet("Deploy 2–3 regional hubs serving pilot clusters")
    bullet("AI management layer handles >90% of operational tasks autonomously")
    bullet("Onboard first government customers (state/local level)")
    bullet("Activate DePIN integration APIs — onboard 2–3 DePIN projects")
    bullet("Complete FedRAMP authorization (Moderate baseline)")

    heading2("Phase 3: Scale (Months 24–48)")
    bullet("Scale to 100–300 edge nodes with 10+ regional hubs")
    bullet("Full mesh fabric operational with automated workload routing")
    bullet("Launch smart contract SLA system and micro-transaction payment channels")
    bullet("Onboard federal government customers; integrate defense networks at select sites")
    bullet("Expand DePIN ecosystem to 10+ active projects")

    heading2("Phase 4: Continental Coverage (Months 48–72)")
    bullet("Scale to 500–1,000+ edge nodes across all major U.S. regions")
    bullet("Full AI autonomy for standard operations")
    bullet("International expansion planning (allied nations with sovereignty interests)")
    bullet("Network becomes self-sustaining: revenue funds continued expansion")
    bullet("Virtual power plant from distributed BESS provides meaningful grid services revenue")


def build_section_15():
    page_break()
    section_heading("15", "Conclusion")

    body("The concentration of compute infrastructure into a handful of hyperscale campuses was an artifact of an era when operational economics demanded scale and AI did not yet exist as an operational tool. That era is ending.")

    body("ANDD demonstrates that AI-native operations eliminate the economic barrier to distributed deployment. When AI handles onboarding, provisioning, billing, monitoring, and maintenance, the marginal cost of adding a new edge node approaches the cost of the hardware itself. This economic unlock enables a network architecture that is superior on every dimension that matters:")

    bullet("Sovereignty — compute and data stay where they are generated and governed, under the jurisdiction of the communities and governments they serve")
    bullet("Security — no single target can degrade the network; mesh architecture ensures graceful degradation, not catastrophic failure")
    bullet("Resilience — distributed power, connectivity, and compute survive events that would cripple centralized alternatives")
    bullet("Equity — Opportunity Zone deployment delivers advanced capabilities to underserved communities, not just affluent coastal metros")
    bullet("DePIN Readiness — enterprise-grade physical infrastructure provides the reliable foundation decentralized protocols need for mainstream adoption")
    bullet("Economic Viability — multiple payment rails serve every customer type from federal agencies to autonomous DePIN protocols")

    callout(
        "The question is no longer whether distributed, AI-managed datacenter infrastructure is technically feasible. The question is how quickly it can be deployed. ANDD is the answer.",
        title=""
    )

    # Contact
    body("")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(30)
    run = p.add_run("Contact: contact@andd.network  |  Web: andd.network")
    run.font.name = FONT_BODY
    run.font.size = Pt(11)
    run.font.color.rgb = RGB_ACCENT
    run.bold = True

    body("")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    run = p.add_run("This document contains forward-looking statements about technology capabilities, market conditions, and business plans. Actual results may differ. Technical specifications represent design targets based on currently available and near-term technology. Regulatory and tax information is provided for informational purposes and should not be construed as legal or tax advice.")
    run.font.name = FONT_BODY
    run.font.size = Pt(8)
    run.font.color.rgb = RGB_MID_GRAY
    run.italic = True


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("ANDD Whitepaper v3 — Professional Edition")
    print("=" * 50)

    # Generate all graphics
    print("Generating infographics...")
    img_cover         = gfx_cover()
    img_concentration = gfx_concentration()
    img_three_tier    = gfx_three_tier()
    img_hardware      = gfx_hardware_domains()
    img_stack         = gfx_software_stack()
    img_opex          = gfx_opex_comparison()
    img_pue           = gfx_pue_comparison()
    img_cooling       = gfx_cooling()
    img_resilience    = gfx_resilience()
    img_depin         = gfx_depin_radar()
    img_payment       = gfx_payment_architecture()
    img_oz            = gfx_oz_impact()
    img_okopipi       = gfx_okopipi_stack()
    img_roadmap       = gfx_roadmap()
    img_agents        = gfx_agent_architecture()
    img_bw            = gfx_bandwidth()
    print(f"  Generated 16 infographics in {TMP_DIR}")

    # Build document
    print("Building document...")
    init_doc()

    build_cover(img_cover)
    build_toc()
    build_section_1()
    build_section_2(img_concentration)
    build_section_3(img_three_tier)
    build_section_4(img_hardware)
    build_section_5(img_stack)
    build_section_6(img_bw)
    build_section_7(img_pue, img_cooling)
    build_section_8(img_opex, img_agents)
    build_section_9(img_resilience)
    build_section_10(img_payment)
    build_section_11(img_depin)
    build_section_12(img_oz)
    build_section_13(img_okopipi)
    build_section_14(img_roadmap)
    build_section_15()

    # Save
    doc.save(str(OUT_FILE))
    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"\nSaved: {OUT_FILE}")
    print(f"Size:  {size_kb:.0f} KB")

    # Cleanup temp
    import shutil
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    print("Temp files cleaned up.")
    print("Done.")


if __name__ == "__main__":
    main()
