#!/usr/bin/env python3
"""Build Native_Networks_Product_Guide.docx: the external, customer- and
partner-facing product document derived from ANDD_Product_Offering_Proposal.md
(Aug 2026) and the Native Networks deck (Sept 2026).

Design: the v4 whitepaper document conventions (Arial, ink header rows,
horizontal-only hairline tables, accent-bar callouts, hairline stat tiles)
re-tokened to the Native Networks palette.
"""

import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ---- tokens (Native Networks, print) ------------------------------------
INK = RGBColor(0x11, 0x1A, 0x30)
BODY = RGBColor(0x3A, 0x44, 0x58)
ACCENT = RGBColor(0x4C, 0x6F, 0xFF)     # indigo
SKY = RGBColor(0x0E, 0x8E, 0xC7)        # sky, darkened for print
GRAY = RGBColor(0x6B, 0x74, 0x88)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xD8, 0xDE, 0xF2)
HAIRLINE = "D5DAE8"
ZEBRA = "F4F6FB"
LIGHT = "EEF1FA"
INKHEX = "111A30"
ACCENTHEX = "4C6FFF"

OUT = "/home/anoop/git/anannra/andd_website/Native_Networks_Product_Guide.docx"
MARK = "/home/anoop/git/anannra/andd_website/proposals/assets/mark-print.png"
CONTENT_W = 9360  # twips, 6.5in


# ---- helpers ---------------------------------------------------------------
def set_font(run, size=10.5, color=BODY, bold=False, italic=False, spacing=None):
    f = run.font
    f.name = "Arial"
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Arial")
    f.size = Pt(size)
    f.color.rgb = color
    f.bold = bold
    f.italic = italic
    if spacing:
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:val"), str(spacing))
        rpr.append(sp)


def add_runs(par, text, size=10.5, color=BODY, bold=False, italic=False):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            set_font(par.add_run(part[2:-2]), size, INK if color == BODY else color, True, italic)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            set_font(par.add_run(part[1:-1]), size, color, bold, True)
        else:
            set_font(par.add_run(part), size, color, bold, italic)


def para(doc, text, size=10.5, color=BODY, bold=False, italic=False,
         before=0, after=8, line=1.18, align=None, keep_next=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if keep_next:
        pf.keep_with_next = True
    if align:
        p.alignment = align
    add_runs(p, text, size, color, bold, italic)
    return p


def eyebrow(doc, text, before=0, after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(text.upper()), 8, ACCENT, True, spacing=24)
    return p


def shade(el, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    el.append(shd)


def cell_margins(cell, top=70, bottom=70, left=110, right=110):
    tcpr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for side, w in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), str(w))
        m.set(qn("w:type"), "dxa")
        mar.append(m)
    tcpr.append(mar)


def table_borders(tbl, color=HAIRLINE, size=2):
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    spec = {"top": "single", "bottom": "single", "insideH": "single",
            "left": "none", "right": "none", "insideV": "none"}
    for side, val in spec.items():
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), val)
        if val == "single":
            b.set(qn("w:sz"), str(size))
            b.set(qn("w:color"), color)
        borders.append(b)
    tblpr.append(borders)


def cell_par(cell, text, size=8.5, color=BODY, bold=False, before=0, after=0, line=1.15):
    p = cell.paragraphs[0] if not cell.paragraphs[0].runs else cell.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = line
    add_runs(p, text, size, color, bold)
    return p


def col_widths(rows, weights=None):
    ncols = len(rows[0])
    if weights is None:
        weights = []
        for c in range(ncols):
            longest = max(len(r[c]) for r in rows if c < len(r))
            weights.append(max(6.0, min(60.0, longest)) ** 0.5)
    total = sum(weights)
    return [int(CONTENT_W * w / total) for w in weights]


def table(doc, rows, weights=None, after=10, size=8.5):
    widths = col_widths(rows, weights)
    tbl = doc.add_table(rows=0, cols=len(rows[0]))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    # keep the grid in step with the cell widths so LibreOffice and Word agree
    for g, w in zip(tbl._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        g.set(qn("w:w"), str(w))
    table_borders(tbl)
    for i, row in enumerate(rows):
        tr = tbl.add_row()
        trpr = tr._tr.get_or_add_trPr()
        if i == 0:
            th = OxmlElement("w:tblHeader")
            th.set(qn("w:val"), "true")
            trpr.append(th)
        for j, cell_text in enumerate(row):
            cell = tr.cells[j]
            cell.width = Twips(widths[j])
            cell_margins(cell)
            tcpr = cell._tc.get_or_add_tcPr()
            if i == 0:
                shade(tcpr, INKHEX)
                cell_par(cell, cell_text, size, WHITE, True)
            else:
                if i % 2 == 0:
                    shade(tcpr, ZEBRA)
                cell_par(cell, cell_text, size, BODY)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(max(after - 8, 0))
    set_font(sp.add_run(" "), 4, BODY)
    return tbl


def callout(doc, title, body_lines, dark=True, hang=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Twips(CONTENT_W)
    cell_margins(cell, top=140, bottom=140, left=180, right=180)
    tcpr = cell._tc.get_or_add_tcPr()
    shade(tcpr, INKHEX if dark else LIGHT)
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        borders.append(b)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "18")
    left.set(qn("w:color"), ACCENTHEX)
    borders.append(left)
    tblpr.append(borders)
    if title:
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        set_font(p.add_run(title), 11, WHITE if dark else INK, True)
    first = not title
    for line in body_lines:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.22
        if hang:
            p.paragraph_format.left_indent = Inches(hang)
            p.paragraph_format.first_line_indent = Inches(-hang)
        add_runs(p, line, size=10, color=SOFT if dark else BODY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl


def stat_tiles(doc, tiles):
    tbl = doc.add_table(rows=1, cols=len(tiles))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("left", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        borders.append(b)
    for side in ("top", "bottom"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), HAIRLINE)
        borders.append(b)
    tblpr.append(borders)
    w = CONTENT_W // len(tiles)
    for j, (num, label) in enumerate(tiles):
        cell = tbl.rows[0].cells[j]
        cell.width = Twips(w)
        cell_margins(cell, top=130, bottom=130, left=40, right=40)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        set_font(p.add_run(num), 15, INK, True)
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        set_font(p2.add_run(label.upper()), 7, GRAY, spacing=16)
    return tbl


def hrule(doc, color=ACCENTHEX, size=12, before=2, after=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    ppr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    ppr.append(pbdr)
    return p


def field(par, instr):
    for tag, attr in (("w:fldChar", {"w:fldCharType": "begin"}),
                      ("w:instrText", None),
                      ("w:fldChar", {"w:fldCharType": "end"})):
        r = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        fonts = OxmlElement("w:rFonts")
        for a in ("w:ascii", "w:hAnsi"):
            fonts.set(qn(a), "Arial")
        sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "15")
        col = OxmlElement("w:color"); col.set(qn("w:val"), "6B7488")
        rpr.append(fonts); rpr.append(sz); rpr.append(col)
        r.append(rpr)
        el = OxmlElement(tag)
        if attr:
            for k, v in attr.items():
                el.set(qn(k), v)
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = instr
        r.append(el)
        par._p.append(r)


def page_break(doc):
    brk = doc.add_paragraph()
    brk.paragraph_format.space_after = Pt(0)
    run = brk.add_run()
    run._element.append(OxmlElement("w:br"))
    run._element[-1].set(qn("w:type"), "page")


def h1(doc, num, title, new_page=False):
    if new_page:
        page_break(doc)
    eyebrow(doc, f"{num:02d} · {title}", before=0 if new_page else 26)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(f"{num}. {title}"), 15, INK, True)
    hrule(doc).paragraph_format.keep_with_next = True


def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(text), 11.5, ACCENT, True)


def lead(doc, text):
    para(doc, text, size=11.5, color=INK, bold=len(text) <= 220, line=1.32, after=10, keep_next=True)


def bullets(doc, items, size=10.5):
    for item in items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.18
        p.paragraph_format.left_indent = Inches(0.24)
        p.paragraph_format.first_line_indent = Inches(-0.24)
        set_font(p.add_run("•"), size, ACCENT, True)
        add_runs(p, "\t" + item, size, BODY)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(0.24))


def numbered(doc, items):
    for n, item in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.18
        p.paragraph_format.left_indent = Inches(0.28)
        p.paragraph_format.first_line_indent = Inches(-0.28)
        set_font(p.add_run(f"{n:02d}"), 9, ACCENT, True)
        add_runs(p, "   " + item, 10.5, BODY)


def note(doc, text):
    para(doc, text, size=8.5, color=GRAY, italic=True, before=2, after=10)


# ---- document --------------------------------------------------------------
doc = Document()
sec = doc.sections[0]
sec.page_width = Twips(12240)
sec.page_height = Twips(15840)
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sec, m, Inches(1))
normal = doc.styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(10.5)
normal.font.color.rgb = BODY

hp = sec.header.paragraphs[0]
hp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), 2)
set_font(hp.add_run("Native Networks"), 10, INK, True)
set_font(hp.add_run("\tProduct Guide"), 7.5, GRAY, spacing=20)

fp = sec.footer.paragraphs[0]
fp.paragraph_format.tab_stops.add_tab_stop(Inches(3.25), 1)
fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), 2)
set_font(fp.add_run("NATIVE NETWORKS  ·  ANDD.AI"), 7.5, GRAY, spacing=16)
set_font(fp.add_run("\tPRODUCT GUIDE v1.0  ·  SEPTEMBER 2026"), 7.5, GRAY, spacing=16)
set_font(fp.add_run("\tPAGE "), 7.5, GRAY, spacing=16)
field(fp, "PAGE")

# --- cover ---
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(24)
p.paragraph_format.space_after = Pt(6)
p.add_run().add_picture(MARK, width=Inches(1.15))
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
set_font(p.add_run("Native Networks"), 22, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(54)
set_font(p.add_run("SMALL MODULAR AI DATACENTERS  ·  ANDD.AI"), 8, GRAY, True, spacing=30)

eyebrow(doc, "PRODUCT GUIDE v1.0  ·  SEPTEMBER 2026", after=10)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("Products, Locations,"), 29, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("Service Levels & Pricing"), 29, ACCENT, True)

para(doc,
     "What we sell, where it runs, when it is available, what it costs, and what "
     "we commit to. Native Networks builds and operates 500 kW to 20 MW AI "
     "datacenters sited where power and fiber already exist, so inference runs "
     "locally instead of round-tripping to a distant cloud.",
     size=12, after=36, line=1.35)

stat_tiles(doc, [
    ("500 kW–20 MW", "per site, grown as contracted"),
    ("90–180 days", "from site selection to live"),
    ("< 30 ms", "round trip in the service area"),
    ("99.99%", "highest contracted availability"),
])

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(96)
p.paragraph_format.space_after = Pt(4)
set_font(p.add_run("FOR CUSTOMERS AND PARTNERS"), 8.5, ACCENT, True, spacing=20)
para(doc, "Indicative pricing and service levels are current as of September 2026 and are "
          "confirmed in a written quote. Native Networks  ·  andd.ai  ·  contact@andd.ai",
     size=9, color=GRAY, after=0)

page_break(doc)

# --- contents ---
SECTIONS = [
    "What we sell", "Products", "Technical capabilities", "Deployment and tenancy",
    "Locations and availability", "Distributed capabilities", "Service levels and support",
    "Security and sovereignty", "Customer proposition", "Integration and onboarding",
    "Pricing and commercial terms", "Partner program",
]
eyebrow(doc, "CONTENTS", after=2)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
set_font(p.add_run("Contents"), 14, INK, True)
half = (len(SECTIONS) + 1) // 2
toc = doc.add_table(rows=half, cols=2)
toc.autofit = False
tblpr = toc._tbl.tblPr
borders = OxmlElement("w:tblBorders")
for side in ("top", "bottom", "left", "right", "insideV"):
    b = OxmlElement(f"w:{side}"); b.set(qn("w:val"), "none"); borders.append(b)
ih = OxmlElement("w:insideH"); ih.set(qn("w:val"), "single"); ih.set(qn("w:sz"), "2"); ih.set(qn("w:color"), HAIRLINE)
borders.append(ih); tblpr.append(borders)
for idx, title in enumerate(SECTIONS):
    r, c = idx % half, idx // half
    cell = toc.rows[r].cells[c]
    cell.width = Twips(CONTENT_W // 2)
    cell_margins(cell, top=90, bottom=90, left=40, right=160)
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.left_indent = Inches(0.32)
    cp.paragraph_format.first_line_indent = Inches(-0.32)
    set_font(cp.add_run(f"{idx + 1:02d}"), 10, ACCENT, True)
    set_font(cp.add_run("   " + title), 10, INK, False)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(30)
add_runs(p, "How to read this guide. Sections 1 to 11 are for customers. Section 12 is for "
            "referral, reseller, managed-service, and real-estate partners. Anything marked "
            "*planned* is on the roadmap and not yet orderable; anything marked *indicative* "
            "is confirmed in a written quote.", 9, GRAY, italic=True)

# =========================================================================
h1(doc, 1, "What we sell", new_page=True)
lead(doc, "Native Networks sells three things that do not get cheaper as token prices fall: "
          "proximity, sovereignty, and automated operations.")
para(doc, "We build and operate small modular AI datacenters, 500 kW to 20 MW, from two "
          "pre-engineered modules: the EC500 (500 kW) and the EC1000 (1 MW). Sites are placed "
          "where utility capacity and fiber already exist, next to the carrier, so a workload's "
          "round trip stays inside its own region. A site starts with one module and grows to "
          "20 MW as customers contract capacity.")
para(doc, "Customers buy the network four ways: managed inference by the token or the "
          "endpoint, dedicated or shared compute by the GPU-hour, private capacity by the "
          "kilowatt or the whole module, and optional services (storage, network, sovereign "
          "controls) attached to any of them.")

table(doc, [
    ["Family", "Products", "Buy it as", "Typical buyer"],
    ["Managed inference", "Serverless Inference, Dedicated Endpoint, Tune", "Per token · per GPU-replica-hour", "Developers, AI product teams, ISVs"],
    ["Compute", "GPU On-demand, Reserved, Spot · Bare Metal · Kubernetes · VM", "Per GPU-hour or per node-hour", "Platform and infrastructure teams"],
    ["Private capacity", "Capacity Block · Private Site (EC500 / EC1000) · Site-as-a-Service", "Per kW-month · per module-month", "Enterprises, carriers, utilities, public sector"],
    ["Optional services", "Storage · Network · Sovereign bundles · Web3 services", "Attached to any product above", "Any"],
], weights=[1.1, 2.4, 1.6, 1.7])

callout(doc, "Why local", [
    "Inference is now the majority of AI compute, and real-time voice, agentic sessions, "
    "inline security, and physical AI cannot tolerate a distant round trip. Hyperscale "
    "capacity was built for centralized training and cannot arrive in time to serve the "
    "edge. Native Networks fills that layer: capacity under 30 ms from the user, with "
    "placement, residency, and service levels you can audit.",
])

# =========================================================================
h1(doc, 2, "Products")
lead(doc, "Every product has a named SKU, a metering unit, an SLA class, and a residency capability. Quotes are generated from the same catalog you see here.")

h2(doc, "2.1 Managed inference")
table(doc, [
    ["SKU", "What you get", "Included", "Not included", "Options"],
    ["AI-Serverless", "OpenAI-compatible API over a curated open-weight catalog (7B to 70B+ chat, embeddings, speech, image), routed to the nearest site with the model warm",
     "Model hosting, autoscaling, metering, playground, usage API", "Custom models, guaranteed throughput, private networking",
     "Std (best effort) · Metro (latency-pinned, p99 SLA) · Resident (jurisdiction-pinned, attested) · Batch (24 h window, half price)"],
    ["AI-Dedicated", "Single-tenant endpoint on named GPUs: catalog model or your own weights and LoRA adapters; guaranteed tokens/sec and p99 latency; autoscaling floor and ceiling; placement control",
     "GPUs, serving stack, monitoring, SLA operations, private endpoint", "Model licences you do not hold, application code",
     "Edge or Hub placement · Confidential (attested confidential computing, +15–25%) · private interconnect"],
    ["AI-Tune (planned)", "Managed fine-tuning (SFT, DPO, LoRA) and mid-scale training with one-click deploy to a Dedicated Endpoint",
     "Job orchestration, cost estimate before launch, output weights", "Data preparation, evaluation design", "Hub sites only; availability follows the first hub"],
], weights=[1.0, 2.6, 1.6, 1.4, 2.0], size=8)

h2(doc, "2.2 Dedicated and shared compute")
table(doc, [
    ["SKU", "What you get", "Tenancy", "Billing", "Notes"],
    ["CMP-GPU On-demand", "Whole GPUs on Blackwell-class racks, per-minute billing", "Dedicated GPU, shared site", "Per GPU-hour", "No commitment"],
    ["CMP-GPU Reserved", "The same GPUs at a 1- or 3-year commitment", "Dedicated GPU, shared site", "Per GPU-hour, discounted 25–50%", "Resource or spend commit"],
    ["CMP-GPU Spot", "Preemptible GPUs at 60–75% off with a 2-minute reclaim notice", "Dedicated GPU while held", "Per GPU-minute", "Best for batch and CI"],
    ["CMP-Metal", "Dedicated bare-metal servers, customer-managed OS", "Single tenant", "Per node-hour or node-month", "Successor product for displaced Equinix Metal customers"],
    ["CMP-K8s / CMP-VM", "Managed Kubernetes namespaces, scale-to-zero containers, x86 and Arm VMs with confidential variants", "Shared with VM-grade isolation", "Per vCPU-hour, per 100 ms container", "Untrusted tenants never share a GPU"],
], weights=[1.3, 2.6, 1.4, 1.5, 1.7], size=8)

h2(doc, "2.3 Private capacity")
table(doc, [
    ["SKU", "What you get", "Term", "Billing"],
    ["NOD-Capacity Block", "Reserved kilowatts and GPU mix at a named site or region; quarterly flex of 15% either way without an amendment", "12–60 months", "Fixed $/kW-month plus usage at deep discount"],
    ["NOD-Private Site", "A whole EC500 or EC1000 module operated for one customer, on our site or on your campus (hospital, utility, carrier)", "36–60 months, take-or-pay", "One-time site charge plus module-month"],
    ["NOD-Site-as-a-Service", "White-label capacity for carriers and municipalities: your brand, our fabric, portal, and API", "5–10 years", "Revenue share or wholesale"],
    ["NOD-Fractional", "A guaranteed slice of a site, 25% and up", "12–36 months", "Per kW-month"],
], weights=[1.4, 3.2, 1.2, 1.8], size=8)

h2(doc, "2.4 Optional services")
table(doc, [
    ["Line", "SKUs", "What it adds"],
    ["Storage (STO)", "Object (S3-compatible, erasure-coded across 3+ sites, 11-nines durability) · Block (NVMe) · File (NFS/SMB) · Archive · Backup · Resident variants", "Data next to the GPUs; residency pinned per bucket; egress at $0.01/GB or less, free inside the fabric"],
    ["Network (NET)", "Private interconnect (10/100 GbE ports) · Carrier-neutral peering · Metro wavelengths · CDN with AI response cache · Zero-trust mesh VPN", "Direct paths into your premises and into cloud on-ramps (AWS, Azure, GCP) at hub sites"],
    ["Sovereign (SOV)", "Compliance bundles (FedRAMP Moderate, CJIS, HIPAA, ITAR; sold only once the authorization exists) · Secure cage · Air-gap site · NG911 continuity · Model enclave", "Control sets wrapped around any base SKU, with boundary documentation and continuous-monitoring feeds your auditors can subscribe to"],
    ["Web3 (DPN)", "Validator hosting with anti-correlation placement · Managed RPC · Verifiable compute · Programmable SLA API", "Machine-readable pricing, telemetry, and settlement for protocols that need datacenter-grade reliability"],
], weights=[1.0, 3.2, 2.6], size=8)

# =========================================================================
h1(doc, 3, "Technical capabilities")
lead(doc, "Launch sites run NVIDIA GB200 NVL72-class racks. The platform is silicon-agnostic by design, so the fleet can add AMD Instinct and inference-specific accelerators as they qualify.")
table(doc, [
    ["Capability", "Specification"],
    ["Accelerators", "GB200 NVL72-class racks: 72 Blackwell GPUs and 36 Grace CPUs per rack, about 13 TB of HBM per rack, NVLink-connected as one domain. Three racks per EC500, six per EC1000. Whole-GPU tenancy is the minimum unit for any customer; fractional sharing only inside one customer's own workloads"],
    ["CPU and memory", "Grace Arm cores paired to each GPU; x86 and Arm general-purpose nodes for VMs, containers, and bare metal, 256 GB to 1 TB DDR5 per node"],
    ["Storage", "NVMe hot tier and QLC warm tier per site; object storage erasure-coded across three or more sites once a region has three sites; archive on HDD with 12-hour retrieval"],
    ["Networking", "400 GbE inside the site; carrier-adjacent siting removes the backhaul hop; bonded fiber backhaul of 10 to 100 Gbps with Starlink as a diverse backup; carrier-neutral peering at hub sites"],
    ["Supported models", "Curated open-weight catalog per site (5 to 8 models kept warm): Llama, Qwen, DeepSeek, Mistral, and Gemma-class chat models from 7B to 70B+, embeddings, speech-to-text, and image models. Bring your own weights and LoRA adapters on Dedicated Endpoints"],
    ["Software and frameworks", "OpenAI-compatible inference API; vLLM and SGLang-class serving; Kubernetes with GPU operator; S3-compatible storage API; REST and gRPC capacity API; Terraform and Pulumi providers; Kubernetes CRDs for GPU pools, endpoints, and residency policy"],
    ["Confidential computing", "AMD SEV-SNP and Intel TDX attested VMs; GPU confidential-computing mode for attested inference (planned for hub sites)"],
    ["Workload limits", "Serverless rate limits by tier (20, 600, 6,000 requests per minute; custom above); context length per model card; Spot reclaim notice of 2 minutes; cold starts apply to scale-to-zero tiers, and the warm tier is priced separately"],
], weights=[1.2, 5.3], size=8.5)

# =========================================================================
h1(doc, 4, "Deployment and tenancy")
lead(doc, "Choose the scope (one site or many), the hardware boundary (dedicated or shared), and who operates what.")
table(doc, [
    ["Option", "Choices", "What it means"],
    ["Scope", "Single-site · Multi-site (metro pair) · Multi-region", "Single-site carries a 99.9% SLA. A diversity-audited metro pair with automated failover carries 99.99%. Multi-region adds cross-site routing and residency per region"],
    ["Hardware", "Dedicated GPU · Dedicated server · Dedicated module · Shared with VM-grade isolation", "GPUs are never shared across customers. Shared applies only to CPU containers and VMs, isolated at the VM level"],
    ["Operations", "Fully managed · Customer-managed", "Fully managed covers hardware lifecycle, firmware and drivers, the serving stack, monitoring, patching, capacity management, and SLA operations. Customer-managed (Bare Metal, bring-your-own Kubernetes) covers the hardware, power, network, and site; you run the OS and above"],
    ["Placement", "Any site · Named metro · Named jurisdiction · Named site", "Placement is enforced by the scheduler and, for Resident SKUs, attested per request or per object"],
], weights=[1.0, 2.2, 3.6], size=8.5)

callout(doc, "What fully managed includes", [
    "Hardware procurement, spares, and refresh · Firmware, drivers, and serving-stack updates · 24/7 monitoring and the SLA guardian that reroutes and fails over before a breach · Security patching and vulnerability management · Capacity planning and expansion in 500 kW or 1 MW steps · Usage metering, invoicing, and automatic SLA credits.",
    "Not included: your application code, model licences you do not already hold, and the classification and legal basis of your data.",
], dark=False)

# =========================================================================
h1(doc, 5, "Locations and availability")
lead(doc, "Four launch sites in the United States and the United Kingdom, each 500 kW and expandable to 20 MW. The land-to-power pipeline exceeds 1 GW.")
table(doc, [
    ["Site", "Region", "Status", "Initial capacity", "Expansion", "Provisioning"],
    ["Phoenix", "Arizona, US", "Launch site (pilot)", "EC500, 500 kW", "To 20 MW as contracted", "Existing capacity under 30 days; new module 90–180 days"],
    ["Dallas", "Texas, US", "Launch site (pilot)", "EC500, 500 kW", "To 20 MW as contracted", "Same"],
    ["Newcastle", "North East England, UK", "Launch site (pilot)", "EC500, 500 kW", "To 20 MW as contracted", "Same"],
    ["Leeds", "Yorkshire, UK", "Launch site (pilot)", "EC500, 500 kW", "To 20 MW as contracted", "Same"],
    ["Next 30 US states", "20 MW per state", "Planned", "EC500 or EC1000 first module", "To 20 MW per state", "Anchor commitment opens the site; live 90–180 days from site selection"],
    ["Further UK regions", "By demand", "Planned", "EC500", "To 20 MW", "Same"],
], weights=[1.1, 1.3, 1.1, 1.2, 1.2, 1.9], size=8)
para(doc, "**Status definitions.** *Pilot*: the site is contracted and in build or acceptance; pilot customers run on beta terms with credits capped at one month of fees. *Live*: general availability with the full SLA schedule. *Planned*: on the pipeline; capacity can be reserved with a creditable deposit and a delivery-date SLA, but is not yet orderable on demand.")
para(doc, "**Provisioning times.** Serverless: minutes. Dedicated Endpoint or GPU on an existing site: same day to 1 business day. Capacity Block on an existing site: under 30 days. New module or new site: 90 to 180 days from site selection, with the date committed in the contract. Live capacity and the maintenance calendar are published on the status page.")

# =========================================================================
h1(doc, 6, "Distributed capabilities")
lead(doc, "The network is one fabric. You choose where a workload may run; the scheduler chooses the best site inside that boundary and moves work when a site degrades.")
table(doc, [
    ["Capability", "How it works", "Available from"],
    ["Location selection", "Pick any site, a named metro, a named jurisdiction (state, county, or country), or a specific site. Latency service areas are published from measured data, not drawn as circles", "Launch"],
    ["Workload routing", "Serverless requests go to the nearest site with the model warm. Dedicated Endpoints stay where you pinned them. Anycast front doors in metros with three or more sites", "Launch; anycast with metro density"],
    ["Regional capacity allocation", "Capacity Blocks reserve kilowatts per site or per region; quarterly flex of 15% either way through the portal without an amendment", "Launch"],
    ["Failover", "Metro pairs fail over automatically in under 30 seconds after a diversity audit and drills; cross-region failover for Platinum class", "Metro pairs as they qualify"],
    ["Runs locally", "Real-time inference, dedicated endpoints, hot storage, private interconnect, public-safety and sovereign workloads pinned in-jurisdiction", "Launch"],
    ["Runs across sites", "Batch inference, spot capacity, geo-erasure-coded object storage, backup, fine-tuning and large-model serving at hub sites, cross-site failover", "As each region reaches three sites"],
], weights=[1.3, 3.8, 1.4], size=8.5)
para(doc, "The value compounds with density. One site gives you proximity. A metro pair gives you 99.99%. Three sites in a region give you anycast, geo-durable storage, and no-exclusion maintenance. Hundreds of sites per region give you the same placement, latency, and residency guarantees everywhere your users are.")

# =========================================================================
h1(doc, 7, "Service levels and support")
lead(doc, "Service levels are gated on physical topology, not on marketing. Credits are automatic: they appear on the invoice with no claim to file.")
h2(doc, "7.1 Availability classes")
table(doc, [
    ["Class", "Monthly availability", "Topology required", "Default for"],
    ["Best-effort", "Monitored, not credited", "Any", "Free, Spot, Batch"],
    ["Bronze", "99.9%", "Single site with N+1 power, dual backhaul, on-site spares", "Starter"],
    ["Silver", "99.95%", "Site plus automatic metro failover", "Pro"],
    ["Gold", "99.99%", "Diversity-audited metro pair, drilled failover under 30 s", "Enterprise, Dedicated Endpoints, object storage"],
    ["Platinum (planned)", "99.99% contracted, 99.999% measured and published", "Three or more sites across metros", "Sovereign bundles, NG911, Web3 backbone"],
], weights=[1.1, 1.6, 2.4, 1.9], size=8.5)

h2(doc, "7.2 Credit schedule")
table(doc, [
    ["Breach", "Bronze", "Silver", "Gold", "Platinum"],
    ["Below target, above 99.0%", "10%", "15%", "25%", "50%"],
    ["Below 99.0%, above 95.0%", "25%", "35%", "50%", "100%"],
    ["Below 95.0%", "50%", "75%", "100%", "100%"],
    ["Latency (p99 over target by 20%+ in an hour)", "n/a", "5% per breach-hour, cap 20%", "5% per breach-hour, cap 30%", "5% per breach-hour, cap 50%"],
    ["Confirmed data loss (object storage)", "12 months of storage fees for the affected data", "", "", ""],
    ["Residency boundary violation", "100% of the monthly charge for the resource, and notification within 24 hours", "", "", ""],
], weights=[2.2, 1.0, 1.3, 1.3, 1.3], size=8)
note(doc, "Credits are a percentage of the affected resource's monthly charge. Pilot sites run on beta terms: 99.9% target, credits capped at one month of fees. Availability and latency are measured by Native Networks probes and gateway telemetry, co-signed by an independent probe vendor; the methodology and raw data are published on the status page and never restated.")

h2(doc, "7.3 Other commitments")
table(doc, [
    ["Dimension", "Commitment"],
    ["Latency", "p99 network round trip of 30 ms or less inside a site's published service area; 10 ms or less inside the metro polygon; time-to-first-token targets per model class on Dedicated Endpoints"],
    ["Throughput", "Contracted tokens per second floor on Dedicated Endpoints"],
    ["Durability", "11 nines for object storage once erasure-coded across three sites"],
    ["Recovery", "RPO 15 minutes and RTO 4 hours for managed storage and platform services"],
    ["Delivery dates", "Contracted go-live date on Capacity Blocks and Private Sites, with liquidated damages for delay"],
    ["Maintenance", "Pilot and single sites: one weekly window (Tuesday 02:00–06:00 local), excluded from the SLA. Metro pairs: rolling zero-downtime updates, no exclusion"],
], weights=[1.1, 5.4], size=8.5)

h2(doc, "7.4 Support")
table(doc, [
    ["Plan", "Hours", "Severity 1 response", "Severity 2 / 3", "Escalation"],
    ["Free", "Community and AI assistant", "Best effort", "Best effort", "None"],
    ["Starter", "AI assistant 24/7, email in business hours", "24 hours", "2 business days / 5 business days", "Support lead"],
    ["Pro", "24/7", "1–4 hours, human", "8 hours / next business day", "Support lead, then service delivery manager"],
    ["Enterprise", "24/7 with a named technical account contact", "1 hour", "4 hours / next business day", "Named contact, service delivery manager, VP Operations"],
    ["Government", "24/7, cleared personnel where required", "15 minutes", "1 hour / 4 hours", "Contractual escalation matrix"],
], weights=[0.9, 1.9, 1.3, 1.6, 1.8], size=8)
para(doc, "Severity 1 is a production outage or SLA breach in progress; Severity 2 is degraded production; Severity 3 is a non-production issue or question. Status, incidents, and credits paid to date are public on the status page.")

# =========================================================================
h1(doc, 8, "Security and sovereignty")
lead(doc, "Residency is a scheduler rule, not a consulting engagement. You choose the boundary and receive an attestation that the workload stayed inside it.")
table(doc, [
    ["Control", "What you get"],
    ["Access control", "SSO (SAML, OIDC), role-based access, per-project API keys with scopes and expiry, hardware-key MFA for administrators, full audit log exportable to your SIEM"],
    ["Encryption", "TLS 1.3 in transit; AES-256 at rest with per-tenant keys; customer-managed keys on Enterprise and Government plans; attested confidential VMs and, at hub sites, confidential GPU mode for the Confidential variants"],
    ["Data ownership", "Your data, prompts, outputs, and weights are yours. Native Networks does not train on customer data and does not access it except to operate the service under your instruction"],
    ["Retention and deletion", "You set retention per bucket and per endpoint; logs default to 30 days. On termination, an export window is guaranteed before cryptographic erasure, and erasure is certified in writing"],
    ["Geo-pinning", "Placement by metro, state, county, or country; attested per request (inference) or per object (storage); any confirmed boundary violation pays a full-month credit and is disclosed within 24 hours"],
    ["Tenancy isolation", "Whole-GPU tenancy for every customer; VM-grade isolation for shared CPU tiers; dedicated cages and air-gapped sites for sovereign workloads"],
    ["Personnel", "Background-checked operations staff; citizenship and clearance guarantees inside sovereign bundles; every automated action runs through a policy engine with typed, audited, reversible steps"],
    ["Compliance roadmap", "SOC 2 Type I in the first year of operation, then Type II; FedRAMP Moderate, CJIS, HIPAA, and ITAR bundles are sold only after the authorization exists. Until then, the compliance evidence pack is available on request"],
], weights=[1.2, 5.3], size=8.5)

# =========================================================================
h1(doc, 9, "Customer proposition")
lead(doc, "Use Native Networks where the round trip is the problem: real-time AI, regulated data, and services that have to keep running when the wide-area network does not.")
table(doc, [
    ["Use case", "Why local", "Product fit"],
    ["Real-time and agentic AI", "Voice, copilots, and multi-step agents feel broken above a few tens of milliseconds", "Serverless Metro, Dedicated Endpoint"],
    ["Fraud and risk scoring", "Sub-50 ms decision budgets and state-level residency for financial data", "Dedicated Confidential, Resident storage, private interconnect"],
    ["Healthcare imaging and clinical AI", "PHI stays in-jurisdiction; imaging inference near the scanner", "Dedicated Endpoint, HIPAA bundle (as authorized), Private Site on campus"],
    ["Public safety and NG911", "Call routing, transcription, and video analytics must survive a backhaul partition", "NG911 continuity, Private Site, air-gap option"],
    ["Physical AI and mobility", "Vehicle and robot loops need single-digit milliseconds at the roadside", "Metro-pinned endpoints at carrier-adjacent sites"],
    ["Carrier and MEC services", "Sell edge AI to your enterprise base on your own brand", "Site-as-a-Service, wholesale"],
    ["Utilities and grid", "Substation-adjacent compute for SCADA, forecasting, and demand response", "Private Site, Capacity Block"],
    ["Web3 infrastructure", "Validators that are provably not co-located; settlement and SLAs a protocol can compose", "Validator hosting, programmable SLA API"],
], weights=[1.5, 2.9, 2.1], size=8.5)

callout(doc, "What scale buys you", [
    "**Proximity.** Hundreds of sites per region put the same catalog within 30 ms of every user, not only those near a hyperscale campus.",
    "**Latency you can contract.** Metro-pinned classes carry a credited p99 latency SLA; no hyperscale region offers one.",
    "**Sovereignty by default.** Residency is a placement rule on every SKU, so a new jurisdiction is a checkbox, not a project.",
    "**Resilience.** Sites peer with neighbors; a metro pair reaches 99.99%, and a region with three sites keeps serving through maintenance and a site loss.",
    "**Cost.** Modules cost about half the capital per megawatt of a hyperscale build and are live in 90 to 180 days, and egress stays at $0.01/GB or less.",
], dark=True)

# =========================================================================
h1(doc, 10, "Integration and onboarding")
lead(doc, "Most customers change one base URL. The rest follow a five-step path with a fixed acceptance test at the end.")
h2(doc, "10.1 Interfaces")
table(doc, [
    ["Interface", "Detail"],
    ["Inference API", "OpenAI-compatible endpoints (chat, embeddings, audio, images); drop-in for LiteLLM, LangChain, and vLLM clients; per-request placement headers"],
    ["Capacity API", "REST and gRPC (v1, additive-only): sites, offers, reservations, dedicated endpoints; Kubernetes CRDs for GPU pools, endpoints, and residency policy"],
    ["Storage API", "S3-compatible with a published compatibility matrix; block via CSI; residency policy set at bucket or volume creation"],
    ["Billing and usage API", "Line-item usage events, hourly rollups, invoices, budgets and alerts, and a machine-readable price sheet; signed usage exports for audit"],
    ["Portal and concierge", "Web portal for projects, keys, placement, spend caps, and SLA telemetry; a conversational concierge that quotes live prices and can provision below $250k of contract value"],
    ["Infrastructure as code", "Terraform and Pulumi providers; Kubernetes-native lifecycle for bring-your-own clusters"],
], weights=[1.3, 5.2], size=8.5)

h2(doc, "10.2 Onboarding path")
numbered(doc, [
    "**Sign up and place.** Self-serve account with an instant API key, or an enterprise agreement e-signed with the security questionnaire pre-answered. Choose placement and spend caps.",
    "**Trial or pilot.** 14-day trial with $500 in credits for self-serve customers. Paid pilots of $10k to $50k, fixed scope, for enterprise and public-sector customers; pilot fees credit against the first-year commitment.",
    "**Migrate.** Migration assistance is included on Pro and above: endpoint mapping, model parity testing, data transfer with free ingress, and parallel-run support. Interconnect ordered in step 1 lands before cut-over.",
    "**Accept.** The acceptance test below is run jointly and signed off.",
    "**Operate.** Production service levels start at acceptance; the named contact and escalation path are active from day one.",
])

h2(doc, "10.3 Acceptance criteria (pilot and production)")
table(doc, [
    ["Criterion", "Measured as", "Pass"],
    ["Latency", "p99 network round trip from the customer's named endpoints inside the service area over 7 days", "At or below the contracted figure"],
    ["Availability", "Measured availability over the pilot period", "At or above the class target"],
    ["Throughput", "Sustained tokens per second on the Dedicated Endpoint at the contracted concurrency", "At or above the contracted floor"],
    ["Placement", "Residency attestations for a sample of requests and objects", "100% inside the boundary"],
    ["Failover (metro pair)", "Drilled loss of one site", "Recovery under 30 seconds, no data loss"],
    ["Billing", "Usage report reconciles to the customer's own counts", "Within 0.1%"],
], weights=[1.3, 3.2, 2.0], size=8.5)

# =========================================================================
h1(doc, 11, "Pricing and commercial terms")
lead(doc, "List prices are public and machine-readable. Discounts buy commitment or term. The figures below are indicative for September 2026 and are confirmed in a written quote.")
h2(doc, "11.1 Charging units and indicative list rates (USD)")
table(doc, [
    ["Product", "Unit", "Indicative list", "Modifiers"],
    ["Serverless, small models (up to 8B)", "Per 1M tokens, blended", "$0.10–0.15", "Metro +15–40% · Resident +20–30% · Batch −50% · cached input discounted"],
    ["Serverless, mid models (9B–34B)", "Per 1M tokens, blended", "$0.30–0.50", "Same"],
    ["Serverless, large models (35B–72B)", "Per 1M tokens, blended", "$0.85–1.00", "Same"],
    ["GPU On-demand, GB200-class", "Per GPU-hour", "$4.50", "Confidential +15–25%"],
    ["GPU Reserved, 1 year", "Per GPU-hour", "$3.15 (about 30% off)", "Resource or spend commit"],
    ["GPU Reserved, 3 years", "Per GPU-hour", "$2.50 (about 45% off)", ""],
    ["GPU Spot", "Per GPU-minute", "60–75% off on-demand", "2-minute reclaim"],
    ["Full NVL72 rack, reserved", "Per rack-month", "About $165k (1 year) · $130k (3 years)", "72 GPUs; on-demand equivalent about $235k"],
    ["Capacity Block", "Per kW-month", "Quoted per site", "5-year anchor terms typically 40–55% below list"],
    ["Private Site, EC500", "Per module-month", "Quoted; anchor pricing", "36–60 months, take-or-pay floor of 70–85%"],
    ["Object storage", "Per GB-month", "Parity with hyperscale standard tiers", "Resident +25–40% · Archive about one fifth"],
    ["Egress", "Per GB", "$0.01 or less; free inside the fabric", "Ingress free"],
    ["Interconnect port", "Per port-month", "Quoted (10 GbE, 100 GbE)", "One-time cross-connect charge"],
], weights=[2.0, 1.4, 1.7, 2.4], size=8)

h2(doc, "11.2 Plans")
table(doc, [
    ["", "Free", "Starter", "Pro", "Enterprise", "Government"],
    ["Platform fee", "$0", "$49 / month", "$499 / month", "Custom annual, about $60k minimum", "Per contract vehicle"],
    ["Included credits", "$5, expiring", "$60", "$650", "Negotiated pool", "Negotiated"],
    ["Serverless rate limit", "20 RPM", "600 RPM", "6,000 RPM", "Custom", "Custom"],
    ["Products", "Serverless, pay as you go", "Adds Kubernetes, VM, storage, Spot, CDN", "Adds Dedicated, Tune, Reserved, interconnect, Web3", "Adds private capacity, wavelengths, white-label", "Adds all sovereign SKUs"],
    ["Default SLA class", "Best-effort", "Bronze", "Silver", "Gold", "Gold or Platinum track"],
    ["Residency pinning", "None", "Metro", "State", "State or county, attested", "Full sovereign controls"],
    ["Billing", "Prepaid only", "Monthly card or ACH, net 30", "Monthly or annual, ACH or wire", "Annual, net 45–60", "Per procurement, multi-year"],
], weights=[1.3, 1.0, 1.2, 1.3, 1.5, 1.2], size=8)

h2(doc, "11.3 Commitments, minimums, and overages")
table(doc, [
    ["Term", "Detail"],
    ["Minimum commitment", "None on pay-as-you-go. Enterprise plans start at about $60k per year. Capacity Blocks run 12 to 60 months; Private Sites 36 to 60 months with a 70–85% take-or-pay floor and a remarketing clause that credits back half the proceeds of resold capacity"],
    ["Contract lengths", "Monthly (Starter, Pro), annual (Enterprise), 1- and 3-year reserved, 5-year and longer anchor agreements"],
    ["Reservation options", "Prepaid credit packs (5–15% off by size, 12-month expiry) · Reserved 1 or 3 years (25–35% and 40–50% off) · Capacity Block with 15% quarterly flex · Forward capacity options (3–8% of strike, callable and tradeable back)"],
    ["Setup fees", "None for self-serve and Dedicated Endpoints. One-time charges apply to interconnect cross-connects and to Private Sites"],
    ["Overages", "Metered at list after included credits. Alerts at 50, 75, 90, and 100% of budget with one-click actions: raise the cap, buy a credit pack, or convert to a commitment. Hard caps are on by default for Free and Starter; Pro and above get anomaly detection that pauses runaway spend pending confirmation"],
    ["Annual prepay", "15–20% off the platform fee and committed usage"],
    ["Marketplaces (planned)", "Private offers on AWS, Azure, and GCP marketplaces so committed cloud spend can be applied to Native Networks capacity"],
], weights=[1.3, 5.2], size=8.5)

h2(doc, "11.4 Worked examples")
table(doc, [
    ["Customer", "Configuration", "Indicative monthly", "Notes"],
    ["Developer", "Serverless, 50M tokens per month on an 8B model, Metro placement", "$8", "$0.12 per 1M tokens plus a 30% Metro uplift; no platform fee on Free"],
    ["AI startup", "Pro plan; Dedicated Endpoint on 2 GB200-class GPUs, 1-year reserved; 2 TB object storage", "About $5,500", "2 × $3.15 × 730 h = $4,600; Pro $499; storage about $40; Silver SLA with automatic credits"],
    ["Regional bank", "Enterprise plan; one NVL72 rack, 1-year reserved, state-pinned Resident placement; 100 GbE interconnect; 50 TB Resident object storage", "About $175,000", "Rack about $165k; platform about $5k; storage about $1.5k; interconnect quoted; Gold SLA where a metro pair exists"],
    ["Anchor tenant", "Private Site EC500 (3 racks, 216 GPUs) on a 5-year take-or-pay at anchor pricing of $2.50 per GPU-hour", "About $395,000", "About $4.7M per year; 80% floor gives a $3.8M minimum; delivery-date SLA with liquidated damages; expansion rights to further modules"],
], weights=[1.0, 2.6, 1.2, 2.5], size=8)
note(doc, "All figures exclude taxes and are illustrative. Serverless token prices track the open-model market and are updated on the public price sheet; GPU and capacity prices are held for the contract term.")

# =========================================================================
h1(doc, 12, "Partner program", new_page=True)
lead(doc, "For CBRE and other real-estate, channel, and technology partners. Every partner deal keeps the zero-touch model: partners sell with our concierge and portal under their own brand, and inherit the same automatic SLA credits.")
h2(doc, "12.1 Commercial framework")
table(doc, [
    ["Model", "Who it suits", "Economics", "Ownership and billing"],
    ["Referral", "Advisors, brokers, and consultancies that introduce qualified opportunities", "Referral fee of 5–10% of first-year contract value (proposed), paid on the customer's first invoice", "Native Networks contracts and bills the customer; the partner keeps referral rights on renewals for 24 months"],
    ["Reseller", "Carriers, MSPs, SIs, and VARs that own the customer relationship", "20–35% off list, tiered by committed annual volume", "Partner paper with flow-down terms; partner is customer of record, bills the end customer, and provides first-line support"],
    ["Managed service (white-label)", "Carriers and MSPs selling edge AI under their own brand", "Reseller pricing plus a licence for the white-label portal and onboarding concierge", "Partner owns the account, renewals, and billing; Native Networks operates the fabric and honours the SLA to the partner"],
    ["Site and real-estate partner", "Owners and operators contributing land, power, fiber, or anchor demand", "Revenue share of 10–25% of site net revenue for 5–10 years, scaled to the contribution; or a fixed ground lease", "Native Networks contracts with tenants; the partner receives a quarterly statement and share"],
], weights=[1.2, 1.9, 2.0, 2.3], size=8)
table(doc, [
    ["Rule", "Detail"],
    ["Eligibility", "Signed partner agreement, one accredited seller, and one technical contact; annual recertification"],
    ["Deal registration", "Register the named account in the partner portal; registration protects the opportunity for six months and is renewable while active"],
    ["Account ownership", "The registering partner owns the opportunity. Referral accounts belong to Native Networks; reseller and managed-service accounts belong to the partner"],
    ["Renewals", "Reseller and managed-service partners retain renewals while in good standing; referral fees continue for the first two renewal cycles"],
    ["Contracting", "Referral: Native Networks paper. Reseller and managed service: partner paper with the Native Networks flow-down schedule (SLA, acceptable use, residency, data terms)"],
    ["Rules of engagement", "No resale into US federal agencies without Native Networks compliance sign-off. Standard-class capacity may not be resold as guaranteed-latency service. List prices are public; reservation floors are not to be disclosed"],
], weights=[1.3, 5.2], size=8.5)

h2(doc, "12.2 Sales enablement")
table(doc, [
    ["Topic", "Detail"],
    ["Ideal customer profiles", "AI product companies with real-time users in a metro we serve; regulated enterprises (financial services, healthcare) with residency obligations; carriers and utilities with sites and power; state and local government with public-safety workloads; Web3 protocols that need reliable, provably distributed infrastructure"],
    ["Qualification questions", "Where are your users, and what latency budget do they have? What data must stay in which jurisdiction? What is your current GPU spend and utilization? Do you need dedicated hardware or a shared endpoint? When do you need capacity, and for how long? Who signs, and on what paper?"],
    ["Approved claims", "500 kW to 20 MW sites from EC500 and EC1000 modules · Live in 90 to 180 days · Under 30 ms round trip in the service area · No community water draw and minimal noise · About half the capital per megawatt of hyperscale, five to ten times faster · Automatic SLA credits, no claims process · More than 1 GW of land-to-power pipeline"],
    ["Claims not approved", "Five-nines contracts · FedRAMP, CJIS, HIPAA, or ITAR authorization before it is granted · Capacity dates at planned sites without a signed reservation · Any statement that Standard-class capacity carries a latency SLA"],
    ["Solution examples", "Dedicated Endpoint for a voice agent in Dallas · Resident inference and storage for a bank in Arizona · Private Site on a hospital campus · Site-as-a-Service for a regional carrier · Capacity Block anchoring a new state site"],
    ["Quotation process", "Partner portal generates list and partner-net quotes from the live catalog in minutes; opportunities above $250k of contract value get a Native Networks solutions lead; anchor and site deals go through the capacity desk"],
    ["Training and presales", "Half-day seller accreditation and one-day technical accreditation, both online; shared demo environment; presales engineers on request through the portal with a one-business-day response"],
], weights=[1.3, 5.2], size=8.5)

h2(doc, "12.3 Delivery responsibilities")
table(doc, [
    ["Scope", "Native Networks", "Technology partners", "Customer or partner of record"],
    ["Site, power, interconnect", "Selects, contracts, and operates; utility and fiber agreements", "Site owners contribute land, power, or fiber under a site agreement", "None (Private Site on customer campus: provides the site and utility feed)"],
    ["Modules, foundations, cooling", "Designs, procures, installs, and maintains", "Module and precast manufacturers build to specification", "None"],
    ["GPUs, servers, network hardware", "Procures, operates, refreshes, holds spares", "NVIDIA, AMD, and OEM supply and warranty", "None"],
    ["Platform software and serving stack", "Operates the fabric, scheduler, serving, metering, and SLA guardian", "Open-source and vendor components under Native Networks support contracts", "Customer-managed tiers: OS and above on Bare Metal and bring-your-own Kubernetes"],
    ["Models and weights", "Curated open-weight catalog with licences that permit commercial serving", "Model publishers and marketplaces", "Own weights, adapters, and any licence they require"],
    ["Licences", "OS, virtualization, and serving-stack licences included in managed tiers", "Vendors", "Application, database, and third-party model licences"],
    ["Application management", "None", "SIs and MSPs under their own contracts", "Owns application code, deployment, and change management"],
    ["Monitoring and SLA operations", "24/7 monitoring, failover, credits", "Independent probe vendor co-signs measurements", "Monitors its own application; consumes telemetry APIs"],
    ["Security", "Physical, platform, and tenancy isolation; compliance evidence", "Attestation and key-management vendors", "Identity, data classification, workload security, and legal basis for data"],
    ["Support and billing", "Direct customers: support and invoicing. Partners: second-line support and partner billing", "Vendor escalation", "Reseller and managed-service partners: first-line support and end-customer billing"],
], weights=[1.4, 2.0, 1.6, 2.0], size=8)

para(doc, "**Next step.** Register an opportunity or request a quote at andd.ai, or write to contact@andd.ai.", before=12)

doc.save(OUT)
print("Wrote", OUT)
