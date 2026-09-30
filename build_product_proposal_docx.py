#!/usr/bin/env python3
"""Build ANDD_Product_Offering_Proposal.docx from the markdown source,
styled to match ANDD_Whitepaper_v4.docx with visual enhancements.

Design system (extracted from the v4 whitepaper):
  ink      #16202B  headings, table header fill, dark callouts
  body     #44505E  running text
  cyan     #0F7A9A  accent: eyebrows, wordmark turned-A, H3
  warmgray #8A8373  labels, small print
  hairline #CFC9B8  table rules
  zebra    #FBFAF6  alternating table rows
  cream    #F0E3D2  light callout fill
  rust     #B5651C  confidential mark
  softink  #D8DEE4  body text inside dark callouts

Enhancements over v4: horizontal-only table rules, cyan accent bar on
callouts, two-column contents, stat-tile strip reused from the cover.

Design pass (Aug 2026): cyan H3 (restores v4 fidelity), long leads
regular-weight, TOC hanging indent + hairlines, hairline-framed stat
strip, repeating table headers across page breaks, keep-with-next on
headings, hanging indent in the ten-rules box, bottom-anchored
confidential block on the cover.
"""

import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

INK = RGBColor(0x16, 0x20, 0x2B)
BODY = RGBColor(0x44, 0x50, 0x5E)
CYAN = RGBColor(0x0F, 0x7A, 0x9A)
WARMGRAY = RGBColor(0x8A, 0x83, 0x73)
RUST = RGBColor(0xB5, 0x65, 0x1C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFTINK = RGBColor(0xD8, 0xDE, 0xE4)
HAIRLINE = "CFC9B8"
ZEBRA = "FBFAF6"
CREAM = "F0E3D2"
INKHEX = "16202B"
CYANHEX = "0F7A9A"

SRC = "ANDD_Product_Offering_Proposal.md"
OUT = "ANDD_Product_Offering_Proposal.docx"
CONTENT_W = 9360  # twips, 6.5in


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
    """Add runs to par, honoring **bold** and *italic* markers."""
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
    set_font(p.add_run("// " + text.upper()), 8, CYAN, True, spacing=24)
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


def table_borders(tbl, horizontal_only=True, color=HAIRLINE, size=2):
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    spec = {"top": "single", "bottom": "single", "insideH": "single",
            "left": "none", "right": "none", "insideV": "none"}
    if not horizontal_only:
        spec = {k: "single" for k in spec}
    for side, val in spec.items():
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), val)
        if val == "single":
            b.set(qn("w:sz"), str(size))
            b.set(qn("w:color"), color)
        borders.append(b)
    tblpr.append(borders)


def no_borders(tbl):
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "bottom", "left", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        borders.append(b)
    tblpr.append(borders)


def cell_par(cell, text, size=8.5, color=BODY, bold=False, before=0, after=0, line=1.15):
    p = cell.paragraphs[0] if not cell.paragraphs[0].runs else cell.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = line
    add_runs(p, text, size, color, bold)
    return p


def col_widths(rows):
    """Distribute CONTENT_W by content weight (sqrt of longest cell)."""
    ncols = len(rows[0])
    weights = []
    for c in range(ncols):
        longest = max(len(r[c]) for r in rows if c < len(r))
        weights.append(max(6.0, min(60.0, longest)) ** 0.5)
    total = sum(weights)
    return [int(CONTENT_W * w / total) for w in weights]


def data_table(doc, rows, before=2, after=10):
    widths = col_widths(rows)
    tbl = doc.add_table(rows=0, cols=len(rows[0]))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    table_borders(tbl, horizontal_only=True)
    for i, row in enumerate(rows):
        tr = tbl.add_row()
        if i == 0:
            # repeat the header row when the table breaks across pages
            trpr = tr._tr.get_or_add_trPr()
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
                cell_par(cell, cell_text, 8.5, WHITE, True)
            else:
                if i % 2 == 0:
                    shade(tcpr, ZEBRA)
                cell_par(cell, cell_text, 8.5, BODY)
    # spacing around the table (tiny run so the spacer stays short)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(after - 8 if after > 8 else 0)
    set_font(sp.add_run(" "), 4, BODY)
    return tbl


def callout(doc, title, body_lines, dark=True, hang=None):
    """Single-cell callout box with a cyan accent bar (left border).
    hang: inches of hanging indent for numbered lines."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.rows[0].cells[0]
    cell.width = Twips(CONTENT_W)
    cell_margins(cell, top=140, bottom=140, left=180, right=180)
    tcpr = cell._tc.get_or_add_tcPr()
    shade(tcpr, INKHEX if dark else CREAM)
    # borders: none except a 6pt cyan left bar
    tblpr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "none")
        borders.append(b)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "18")
    left.set(qn("w:color"), CYANHEX)
    borders.append(left)
    tblpr.append(borders)
    if title:
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        set_font(p.add_run(title), 11, WHITE if dark else INK, True)
    first = not title
    for line in body_lines:
        if first:
            p = cell.paragraphs[0]
            first = False
        else:
            p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.22
        if hang:
            p.paragraph_format.left_indent = Inches(hang)
            p.paragraph_format.first_line_indent = Inches(-hang)
        add_runs(p, line, size=10, color=SOFTINK if dark else BODY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl


def stat_tiles(doc, tiles):
    """4-col strip framed by hairlines: big ink number over spaced label."""
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
        set_font(p.add_run(num), 20, INK, True)
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        set_font(p2.add_run(label.upper()), 7, WARMGRAY, spacing=16)
    return tbl


def hrule(doc, color=CYANHEX, size=12, before=2, after=10):
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
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "15")
        col = OxmlElement("w:color")
        col.set(qn("w:val"), "8A8373")
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


# ----------------------------------------------------------------------------
# Parse the markdown
# ----------------------------------------------------------------------------

md = open(SRC).read()
lines = md.split("\n")

sections = []  # list of (num, title, blocks); block = ("p"|"h3"|"table"|"olist"|"note", payload)
i = 0
# skip front matter until the first "## "
while i < len(lines) and not lines[i].startswith("## "):
    i += 1

cur = None
while i < len(lines):
    ln = lines[i]
    if ln.startswith("## "):
        m = re.match(r"## (\d+)\. (.+)", ln)
        cur = {"num": m.group(1), "title": m.group(2), "blocks": []}
        sections.append(cur)
        i += 1
    elif ln.startswith("### "):
        m = re.match(r"### (?:\d+\.\d+ )?(.+)", ln)
        cur["blocks"].append(("h3", m.group(1)))
        i += 1
    elif ln.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                rows.append(cells)
            i += 1
        cur["blocks"].append(("table", rows))
    elif re.match(r"\d+\. ", ln):
        items = []
        while i < len(lines) and re.match(r"\d+\. ", lines[i]):
            items.append(re.match(r"\d+\. (.+)", lines[i]).group(1))
            i += 1
        cur["blocks"].append(("olist", items))
    elif ln.strip() == "---" or not ln.strip():
        i += 1
    elif ln.startswith("*") and ln.endswith("*") and not ln.startswith("**"):
        cur["blocks"].append(("note", ln.strip("*")))
        i += 1
    else:
        cur["blocks"].append(("p", ln.strip()))
        i += 1

# ----------------------------------------------------------------------------
# Build the document
# ----------------------------------------------------------------------------

doc = Document()
sec = doc.sections[0]
sec.page_width = Twips(12240)
sec.page_height = Twips(15840)
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sec, m, Inches(1))

# Normal style defaults
normal = doc.styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(10.5)
normal.font.color.rgb = BODY

# --- header / footer ---
hdr = sec.header
hp = hdr.paragraphs[0]
hp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), 2)  # right
set_font(hp.add_run("∀"), 10, CYAN, True)
set_font(hp.add_run("NDD"), 10, INK, True)
set_font(hp.add_run("\tProduct Offering Proposal"), 7.5, WARMGRAY, spacing=20)

ftr = sec.footer
fp = ftr.paragraphs[0]
fp.paragraph_format.tab_stops.add_tab_stop(Inches(3.25), 1)  # center
fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), 2)   # right
set_font(fp.add_run("ANDD.AI  ·  CONFIDENTIAL"), 7.5, WARMGRAY, spacing=16)
set_font(fp.add_run("\tPRODUCT PROPOSAL v1.0  ·  AUGUST 2026"), 7.5, WARMGRAY, spacing=16)
set_font(fp.add_run("\t// "), 7.5, CYAN, True)
set_font(fp.add_run("PAGE "), 7.5, WARMGRAY, spacing=16)
field(fp, "PAGE")

# --- cover ---
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(30)
p.paragraph_format.space_after = Pt(0)
set_font(p.add_run("∀"), 24, CYAN, True)
set_font(p.add_run("NDD"), 24, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(60)
set_font(p.add_run("AI-NATIVE DISTRIBUTED DATACENTERS"), 8, WARMGRAY, True, spacing=30)

eyebrow(doc, "PRODUCT PROPOSAL v1.0  ·  AUGUST 2026", after=10)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("The Product Offering"), 29, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("& 36-Month Roadmap"), 29, CYAN, True)

para(doc,
     "How customers discover, sign up for, and consume the ANDD network: "
     "offers, billing, SLAs, go-to-market, and the 12/24/36-month roadmap. "
     "ANDD sells the three things that do not deflate as token prices fall: "
     "milliseconds, jurisdiction, and reliability.",
     size=12, after=40, line=1.35)

stat_tiles(doc, [
    ("23-25%", "node breakeven utilization"),
    ("40-60%", "pre-sold at ground-break"),
    ("$350-550M", "run rate at month 36"),
    ("60%", "new ARR zero-touch"),
])

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(170)
p.paragraph_format.space_after = Pt(4)
set_font(p.add_run("CONFIDENTIAL  ·  DO NOT DISTRIBUTE"), 8.5, RUST, True, spacing=20)
para(doc, "Prepared for customer, partner, and investor discussion  ·  ANDD  ·  andd.ai",
     size=9, color=WARMGRAY, after=0)

doc.add_page_break()

# --- contents (two columns) ---
eyebrow(doc, "CONTENTS", after=2)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
set_font(p.add_run("Contents"), 14, INK, True)

half = (len(sections) + 1) // 2
toc = doc.add_table(rows=half, cols=2)
toc.autofit = False
tblpr = toc._tbl.tblPr
borders = OxmlElement("w:tblBorders")
for side in ("top", "bottom", "left", "right", "insideV"):
    b = OxmlElement(f"w:{side}")
    b.set(qn("w:val"), "none")
    borders.append(b)
ih = OxmlElement("w:insideH")
ih.set(qn("w:val"), "single")
ih.set(qn("w:sz"), "2")
ih.set(qn("w:color"), HAIRLINE)
borders.append(ih)
tblpr.append(borders)
for idx, s in enumerate(sections):
    r, c = idx % half, idx // half
    cell = toc.rows[r].cells[c]
    cell.width = Twips(CONTENT_W // 2)
    cell_margins(cell, top=90, bottom=90, left=40, right=160)
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.left_indent = Inches(0.32)
    cp.paragraph_format.first_line_indent = Inches(-0.32)
    set_font(cp.add_run(f"{int(s['num']):02d}"), 10, CYAN, True)
    set_font(cp.add_run("   " + s["title"]), 10, INK, False)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(30)
add_runs(p, "Prepared through a four-desk process: market research (live comparables, "
            "August 2026), product management, commercialization, and engineering. "
            "Where the desks disagreed, engineering's physical gates won. Nothing in "
            "this proposal promises what the network's density cannot yet deliver.",
         9, WARMGRAY, italic=True)

# --- sections ---
CALLOUT_DARK_PREFIXES = ("Directional targets:", "As a sales weapon:")

for s in sections:
    # page break + eyebrow + H1
    brk = doc.add_paragraph()
    brk.paragraph_format.space_after = Pt(0)
    run = brk.add_run()
    run._element.append(OxmlElement("w:br"))
    run._element[-1].set(qn("w:type"), "page")
    eyebrow(doc, f"{int(s['num']):02d} · {s['title']}")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(f"{s['num']}. {s['title']}"), 15, INK, True)
    hrule(doc).paragraph_format.keep_with_next = True

    lead_done = False
    ten_rules = s["title"].lower().startswith("the ten")
    for kind, payload in s["blocks"]:
        if kind == "h3":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            set_font(p.add_run(payload), 11.5, CYAN, True)
        elif kind == "table":
            data_table(doc, payload)
        elif kind == "olist":
            if ten_rules:
                body = [f"**{n:02d}**   {t}" for n, t in enumerate(payload, 1)]
                callout(doc, None, body, dark=False, hang=0.3)
            else:
                for n, item in enumerate(payload, 1):
                    p = doc.add_paragraph()
                    p.paragraph_format.space_after = Pt(4)
                    p.paragraph_format.line_spacing = 1.18
                    p.paragraph_format.left_indent = Inches(0.28)
                    p.paragraph_format.first_line_indent = Inches(-0.28)
                    set_font(p.add_run(f"{n:02d}"), 9, CYAN, True)
                    add_runs(p, "   " + item, 10.5, BODY)
        elif kind == "note":
            para(doc, payload, size=9, color=WARMGRAY, italic=True, before=8)
        else:  # paragraph
            if payload.startswith(CALLOUT_DARK_PREFIXES):
                title, rest = payload.split(":", 1)
                callout(doc, title, [rest.strip()], dark=True)
            elif not lead_done:
                # short thesis leads stay bold; long leads read better regular
                bold_lead = len(payload) <= 260
                para(doc, payload, size=11.5, color=INK, bold=bold_lead,
                     line=1.32, after=10)
                lead_done = True
            else:
                para(doc, payload)

doc.save(OUT)
print(f"Wrote {OUT}")
