#!/usr/bin/env python3
"""Build Native_Networks_Edge_Module_RFP_v3.docx.

Version 3.0 of the Edge Module Requirements RFP (EC500 / EC1000), restyled to
the Native Networks document system (nn_docx) and updated to the September
2026 positioning: Native Networks brand, US and UK siting, the anchor /
reserve / spot commercial ladder, and the Bronze-to-Platinum SLA classes.
"""

from docx.shared import Pt, Inches, RGBColor, Twips
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from nn_docx import (Document, INK, BODY, ACCENT, GRAY, WHITE, HAIRLINE, CONTENT_W,
                     set_font, add_runs, para, eyebrow, cell_margins, table, callout,
                     stat_tiles, field, page_break, h1, h2, lead, bullets, numbered, note)

OUT = "/home/anoop/git/anannra/andd_website/Native_Networks_Edge_Module_RFP_v3.docx"
MARK = "/home/anoop/git/anannra/andd_website/proposals/assets/mark-print.png"
TOPOLOGY = "/home/anoop/git/anannra/andd_website/proposals/assets/mesh-topology.png"
AMBER = RGBColor(0xB7, 0x79, 0x1F)

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
set_font(hp.add_run("\tEdge Module RFP  ·  v3.0"), 7.5, GRAY, spacing=20)

fp = sec.footer.paragraphs[0]
fp.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), 2)
set_font(fp.add_run("NATIVE NETWORKS  ·  CONFIDENTIAL  ·  EDGE MODULE RFP v3.0  ·  SEPTEMBER 2026"), 7.5, GRAY, spacing=16)
set_font(fp.add_run("\tPAGE "), 7.5, GRAY, spacing=16)
field(fp, "PAGE")

# --- cover -----------------------------------------------------------------
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(24)
p.paragraph_format.space_after = Pt(6)
p.add_run().add_picture(MARK, width=Inches(1.15))
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
set_font(p.add_run("Native Networks"), 22, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(50)
set_font(p.add_run("SMALL MODULAR AI DATACENTERS  ·  ANDD.AI"), 8, GRAY, True, spacing=30)

eyebrow(doc, "REQUEST FOR PROPOSAL  ·  VERSION 3.0  ·  SEPTEMBER 2026", after=10)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("Edge Module"), 29, INK, True)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
p.paragraph_format.line_spacing = 1.02
set_font(p.add_run("Requirements"), 29, ACCENT, True)

para(doc,
     "EC500 (500 kW) and EC1000 (1 MW): technical, compute, power, cooling, "
     "storage, connectivity, security, operations, and deployment requirements "
     "for the standardized module that Native Networks multiplies into a network "
     "of 500 kW to 20 MW AI datacenters sited where power and fiber already exist.",
     size=12, after=34, line=1.35)

stat_tiles(doc, [
    ("216 / 432", "GPUs per EC500 / EC1000"),
    ("≈ 1.15", "target PUE, direct liquid"),
    ("3 PB", "tiered storage per module"),
    ("90–180 days", "site selection to live"),
])

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(120)
p.paragraph_format.space_after = Pt(4)
set_font(p.add_run("CONFIDENTIAL  ·  ISSUED TO PROSPECTIVE VENDORS  ·  NOT FOR REDISTRIBUTION"), 8.5, AMBER, True, spacing=20)
para(doc, "This document specifies Native Networks' requirements for its standardized edge "
          "datacenter modules and invites qualified vendors to submit competing proposals. "
          "It does not constitute an offer or a commitment to contract.",
     size=9, color=GRAY, after=10)
page_break(doc)

# --- contents ----------------------------------------------------------------
SECTIONS = [
    "Purpose and scope", "AI grid architecture", "Module definitions", "Compute requirements",
    "Power requirements", "Cooling requirements", "Storage requirements",
    "Connectivity and networking requirements", "Multi-tenancy and orchestration requirements",
    "Deployment and siting requirements", "Use cases", "Commercial and offtake requirements",
    "Physical security requirements", "Electronic (cyber) security requirements",
    "OAM requirements", "Service level requirements", "Vendor response requirements",
]
eyebrow(doc, "CONTENTS", after=2)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(14)
set_font(p.add_run("Contents"), 14, INK, True)
half = (len(SECTIONS) + 2) // 2
toc = doc.add_table(rows=half, cols=2)
toc.autofit = False
tblpr = toc._tbl.tblPr
borders = OxmlElement("w:tblBorders")
for side in ("top", "bottom", "left", "right", "insideV"):
    b = OxmlElement(f"w:{side}"); b.set(qn("w:val"), "none"); borders.append(b)
ih = OxmlElement("w:insideH"); ih.set(qn("w:val"), "single"); ih.set(qn("w:sz"), "2"); ih.set(qn("w:color"), HAIRLINE)
borders.append(ih); tblpr.append(borders)
entries = [(f"{i + 1:02d}", t) for i, t in enumerate(SECTIONS)] + [("A", "Appendix A. Reference mesh topology")]
for idx, (num, title) in enumerate(entries):
    r, c = idx % half, idx // half
    cell = toc.rows[r].cells[c]
    cell.width = Twips(CONTENT_W // 2)
    cell_margins(cell, top=80, bottom=80, left=40, right=160)
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.left_indent = Inches(0.32)
    cp.paragraph_format.first_line_indent = Inches(-0.32)
    set_font(cp.add_run(num), 10, ACCENT, True)
    set_font(cp.add_run("   " + title), 10, INK, False)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(26)
add_runs(p, "How to read this document. Sections 2 to 16 are requirements; Section 17 states what "
            "a proposal must contain and how it is evaluated. Where a range is given, it defines "
            "the acceptable envelope for a vendor solution. Values in square brackets are "
            "completed at issue.", 9, GRAY, italic=True)

eyebrow(doc, "REVISION HISTORY", before=26, after=4)
table(doc, [
    ["Version", "Date", "Change"],
    ["1.0", "August 2026", "Initial draft issued as ANDD Edge Module RFP"],
    ["2.0", "September 2026", "Physical security, cyber security, OAM, SLA, and vendor-response sections added; reference topology appendix"],
    ["3.0", "September 2026", "Reissued under the Native Networks brand; siting extended to the United Kingdom; commercial and SLA sections aligned to the September 2026 product guide; launch sites named; document restyled"],
], weights=[0.8, 1.2, 4.5], size=8)


# =========================================================================
h1(doc, 1, "Purpose and scope", new_page=True)
lead(doc, "This Request for Proposal defines Native Networks' technical, compute, power, and "
          "deployment requirements for its standardized edge datacenter modules, the EC500 "
          "(500 kW) and EC1000 (1 MW), and invites qualified vendors to propose solutions that meet them.")
para(doc, "Native Networks builds and operates small modular AI datacenters, 500 kW to 20 MW, "
          "sited where power and fiber already exist, so that inference runs locally rather than "
          "round-tripping to a distant hyperscale core. The module is the repeatable unit that the "
          "network multiplies; these requirements govern that unit. The first four sites are in "
          "Phoenix, Dallas, Newcastle, and Leeds, and the program extends to 20 MW per state across "
          "30 U.S. states and further UK regions.")
para(doc, "The requirements are organized by subsystem (grid architecture, compute, power, cooling, "
          "storage, connectivity, orchestration) and by deployment, followed by the use cases the "
          "modules must serve, the security, operations, and service-level requirements, and the "
          "vendor response requirements.")

# =========================================================================
h1(doc, 2, "AI grid architecture")
lead(doc, "Native Networks is not a single datacenter. It is a mesh of sub-20 MW sites, each peering "
          "with its neighbors and at least two hubs, so that every workload finds the closest GPU.")
para(doc, "Today a few dozen hyperscale campuses run most AI inference, and everything outside their "
          "low-latency radius pays the round trip. The grid distributes that compute to where the "
          "users are; the modules specified in this document are the cells that make up the grid.")

h2(doc, "2.1 The programmable mesh: four hardware domains")
para(doc, "Each site is a configurable mix of four hardware domains. The control plane sets the ratio "
          "per site and rebalances it quarterly as demand shifts. This specification configures the "
          "fourth domain (AI hardware) in detail; the other three are summarized because every module "
          "must carry all four.")
table(doc, [
    ["Domain", "Role in the grid", "Key specifications"],
    ["01 Compute", "Dense general base: containerized workloads, APIs, databases, and pipelines at every site", "Arm and x86 (EPYC, Xeon, Altra); 256 GB to 1 TB DDR5; 20 to 40 kW per rack"],
    ["02 Storage", "Erasure-coded and chunked across three or more sites; no single node holds a complete copy of a tenant's data", "NVMe hot 100 to 500 TB; QLC warm 0.5 to 2 PB; 11-nines durability"],
    ["03 Connectivity", "Carrier-neutral micro-IXP; direct peering with regional ISPs, CDNs, and cloud on-ramps; government-capable", "Internal 100 / 400 GbE; backhaul 10 to 100 Gbps; redundant fiber, 5G, and LEO"],
    ["04 AI hardware", "Silicon-agnostic accelerators: the GPU tier this specification configures", "NVIDIA Grace Blackwell today; roadmap AMD, ASIC, custom; direct liquid cooling, immersion on the roadmap"],
], weights=[1.1, 2.8, 2.6], size=8.5)

h2(doc, "2.2 Mesh routing and resilience")
para(doc, "The network is a graph, not a spoke. Every edge node peers with its neighbors and at least "
          "two hubs, and the control plane routes each workload to the nearest healthy GPU, re-routing "
          "in real time as nodes drop and rejoin. This delivers cross-site failover and on-mesh routing "
          "with no central chokepoint, and it is what lets a small site carry Platinum-class workloads: "
          "when a node degrades, the workload moves rather than fails. Storage is erasure-coded across "
          "sites for the same reason, so the loss of any one node is a routing event, not a data-loss event.")

h2(doc, "2.3 Grid hierarchy: translation to GPU configuration")
table(doc, [
    ["Grid layer", "Unit", "What it is", "GPU configuration"],
    ["Grid cell", "Tenant domain", "Smallest independently schedulable, isolated compute island", "8-GPU NVLink island (or 4-GPU NVL4 slices, or MIG partitions)"],
    ["Module", "EC500 / EC1000", "A power-bound block of grid cells plus storage, network, and support x86", "27 domains (EC500); 54 (EC1000)"],
    ["Site", "Facility", "One or more modules; a configurable mix of the four domains, expandable to 20 MW", "Domain ratio set by the control plane, rebalanced quarterly"],
    ["Mesh", "Network", "Hundreds of sites peering as a graph; self-routing and sovereign", "Workload routed to the nearest healthy GPU"],
], weights=[1.0, 1.2, 2.6, 2.2], size=8.5)

# =========================================================================
h1(doc, 3, "Module definitions")
lead(doc, "Two predefined modules underpin every site. A facility starts small and expands toward "
          "20 MW as demand is contracted, using multiples of these blocks.")
table(doc, [
    ["Parameter", "EC500", "EC1000"],
    ["Module power (total)", "500 kW", "1 MW"],
    ["Usable IT capacity (liquid, PUE ≈ 1.15)", "≈ 435 kW", "≈ 870 kW"],
    ["Primary workloads", "Edge inference, model refinement, SLM training", "Same, plus larger fine-tunes and multi-node SLM training"],
    ["GPU accelerators (GB200 NVL72, primary)", "216 (3 × NVL72)", "432 (6 × NVL72)"],
    ["Pooled GPU HBM (GB200, 192 GB per GPU)", "≈ 41 TB", "≈ 83 TB"],
    ["Storage per module", "3 PB (hot NVMe plus warm QLC)", "3 PB (hot NVMe plus warm QLC)"],
    ["Cooling", "Direct liquid cooling standard", "Direct liquid cooling standard"],
    ["Foundation and form factor", "Relocatable precast pad; containerized", "Relocatable precast pad; containerized"],
    ["Facility expansion ceiling", "20 MW", "20 MW"],
], weights=[2.0, 2.2, 2.2], size=8.5)

# =========================================================================
h1(doc, 4, "Compute requirements")
h2(doc, "4.1 GPU platform options")
para(doc, "The module is silicon-agnostic by design; NVIDIA Grace Blackwell-class accelerators are the "
          "current standard. GB200 NVL72 is the primary platform (Section 4.2); the other rows are "
          "alternatives or supply fallbacks. The table gives GPU counts that fit each module after "
          "reserving power for cooling, storage, networking, and support x86. Counts are power-bound, "
          "so per-GPU power dominates the result.")
table(doc, [
    ["Platform", "Cooling", "x86 in compute path", "HBM per GPU", "GPUs at EC500", "GPUs at EC1000"],
    ["GB200 NVL72", "Liquid", "No (Grace)", "192 GB", "216 (3 racks)", "432 (6 racks)"],
    ["GB300 NVL72", "Liquid", "No (Grace)", "288 GB", "144 (2 racks)", "360 (5 racks)"],
    ["HGX B200 (air)", "Air", "Yes", "180 GB", "≈ 176", "≈ 360"],
    ["HGX B200 (liquid)", "Liquid", "Yes", "180 GB", "≈ 192", "≈ 392"],
    ["HGX B300 (liquid)", "Liquid", "Yes", "288 GB", "≈ 176", "≈ 368"],
], weights=[1.5, 0.9, 1.3, 1.0, 1.2, 1.2], size=8.5)

h2(doc, "4.2 Recommended configuration")
para(doc, "The primary configuration is **GB200 NVL72**. It is the most GPU-dense option per watt "
          "(216 accelerators in an EC500, 432 in an EC1000), it matches the platform Native Networks' "
          "own materials commit to, and its 72-GPU NVLink fabric can be sliced in software into the "
          "8-GPU tenant domains that edge inference and SLM training use, while retaining the option "
          "to form a larger coupled domain for an occasional full fine-tune. Direct liquid cooling is mandatory.")
callout(doc, "Not every installation is an NVL72", [
    "GB200 NVL72 is the default only where a site can house and power a full rack to NVIDIA Cloud "
    "Partner reference-architecture standards. Where a compliant NVL72 build does not fit the power "
    "and space envelope, most often at the smaller EC500 scale, the site defaults instead to the "
    "8-GPU mesh configuration (HGX B200) described in Appendix A. Platform is selected per site, "
    "not fleet-wide.",
], dark=False)
bullets(doc, [
    "**Domain topology.** Carve each 72-GPU NVL72 rack into independent 8-GPU tenant domains (or 4-GPU NVL4 slices, or MIG partitions) as the default, so inference multi-tenancy and fault isolation match the smaller-island model; form a larger domain only when a job needs more than 8-GPU tensor parallelism.",
    "**x86 requirement.** The GB200 compute path uses Grace Arm CPUs, so x86 is provided by the general-compute domain (Section 2.1, domain 01): storage controllers, head, login, and management nodes, and CPU pre- and post-processing. GB200 satisfies the accelerator requirement; x86 satisfies the support tier.",
    "**Fallback (HGX B200).** Consider HGX B200 8-GPU nodes only if GB200 NVL72 supply is unavailable or lead times are prohibitive. HGX B200 puts x86 in the compute path and can be air-cooled, at the cost of about 10 to 20% fewer GPUs per module and the loss of the large-domain option. It is a contingency, not the default.",
    "**GB300 and HGX B300.** Reserve for sites where memory-bound reasoning inference dominates; not the primary path for the inference and SLM workloads this module targets.",
])

h2(doc, "4.3 General-purpose compute")
para(doc, "Each site also carries a base of high-density general compute for containerized workloads, "
          "APIs, databases, and pipelines: Arm and x86 (EPYC, Xeon, Altra), 256 GB to 1 TB DDR5 per "
          "server, at 20 to 40 kW per rack. This tier hosts storage controllers, cluster management, "
          "scheduling, and CPU pre- and post-processing for the accelerators.")

# =========================================================================
h1(doc, 5, "Power requirements")
lead(doc, "The module is power-bound. About 85% of usable IT power is GPUs; storage, networking, and "
          "support x86 together are under 10%. The breakdown is for the EC500; the EC1000 scales proportionally.")
table(doc, [
    ["Subsystem", "Power (EC500)", "Share of module"],
    ["GPU compute (accelerators, host CPUs, in-rack NVLink)", "≈ 360 kW", "72%"],
    ["Cooling and electrical losses (PUE ≈ 1.15)", "≈ 65 kW", "13%"],
    ["Scale-out networking (leaf and spine, InfiniBand or Ethernet)", "≈ 18 kW", "3.6%"],
    ["Storage (3 PB NVMe plus QLC)", "≈ 15 kW", "3.0%"],
    ["Auxiliary x86 (head, management, CPU pre- and post-processing)", "≈ 15 kW", "3.0%"],
    ["Reserve and PDU margin", "≈ 27 kW", "5.4%"],
], weights=[3.4, 1.3, 1.3], size=8.5)
para(doc, "**Requirement notes.** Provision at least three independent power feeds (rack PDUs on separate "
          "sources) per rack. Size busbar ampacity and PDU input breakers to the platform's peak: "
          "GB300-class racks draw about 132 to 142 kW against GB200's about 120 kW and require upgraded "
          "distribution. If a site's module rating is quoted as IT-only rather than total, the usable GPU "
          "budget, and GPU count, rises by about 15%. Electrical design shall comply with NEC and UL "
          "requirements for U.S. sites and BS 7671 and UKCA requirements for UK sites; vendors shall "
          "state any design differences between the two.")

# =========================================================================
h1(doc, 6, "Cooling requirements")
bullets(doc, [
    "**Direct liquid cooling is mandatory** for the primary GB200 NVL72 configuration and for every accelerator rack; immersion is on the roadmap. Air cooling is available only on the HGX B200 supply fallback (1,000 W or less air-cooled) and is never an option on GB200, GB300, or B300 platforms.",
    "Provision in-rack CDUs sized to platform: about 120 kW for GB200 NVL72, 150 to 250 kW for GB300 NVL72; higher coolant flow and larger supply and return runs for B300-class density.",
    "If the HGX B200 fallback is ever deployed air-cooled, plan rear-door heat exchangers (about 30 to 40 kW per rack air ceiling), which spreads the same GPU count across more racks and lowers usable IT through a worse PUE (about 1.3 to 1.4). This does not apply to the primary GB200 build.",
    "**No community water draw.** Closed-loop and dry-cooler designs preserve the low-friction siting thesis. Vendors shall state the design's water use and its acoustic footprint at the site boundary.",
])

# =========================================================================
h1(doc, 7, "Storage requirements")
bullets(doc, [
    "**Capacity.** 3 PB per module, tiered as a fast NVMe hot tier of roughly 0.5 PB for active datasets and checkpoints, plus a QLC warm tier making up the balance (about 2.5 PB), on a parallel filesystem (WEKA, VAST, or Lustre-class).",
    "**Throughput over capacity.** Size the hot tier for GB/s per GPU (checkpoint and dataset I/O), which gates training and refinement, not raw petabytes.",
    "**Durability and distribution.** Erasure-coded and chunked across three or more geographically distinct sites, so no single node holds a complete copy; target 11-nines durability.",
])

# =========================================================================
h1(doc, 8, "Connectivity and networking requirements")
bullets(doc, [
    "**Intra-module fabric.** Non-blocking 100 / 400 GbE east-west; for multi-node SLM training use 400 or 800 Gb/s InfiniBand or RoCEv2 (ConnectX-7 at 400 Gb/s, or ConnectX-8 at 800 Gb/s on B300).",
    "**Carrier-neutral micro-IXP.** Each site is a miniature exchange point with direct peering to regional ISPs, CDNs, and cloud on-ramps.",
    "**Backhaul and redundancy.** 10 to 100 Gbps backhaul; minimum two carrier connections per site; redundant fiber, 5G, and LEO (bonded fiber with Starlink as diverse backup, not as the primary low-latency path).",
    "**Latency target.** Sub-20 ms intra-region engineering target through carrier-adjacent siting that removes the backhaul hop; the contracted commitment to customers is 30 ms or less at the edge of the service area and 10 ms or less inside the metro polygon.",
])

# =========================================================================
h1(doc, 9, "Multi-tenancy and orchestration requirements")
bullets(doc, [
    "**Tenant domains.** Each 8-GPU slice of a GB200 NVL72 rack (or a 4-GPU NVL4 slice) is an independent tenant domain. An EC500 provides 27 such 8-GPU domains; an EC1000 provides 54. Sub-GPU partitioning (MIG, up to 7 slices per GPU) supports far higher inference-tenant density where required. Whole-GPU tenancy is the minimum unit sold to any customer; fractional sharing is confined to one tenant's own workloads.",
    "**Isolation.** Hard multi-tenant isolation in production (network, compute, and storage) is required before the Gold and Platinum SLA classes can be sold at a site.",
    "**Mesh control plane.** Every node peers with its neighbors and at least two hubs; the control plane routes each workload to the closest GPU and re-routes on node failure (cross-site failover, on-mesh routing). The control plane rebalances the hardware ratio at each site quarterly as demand shifts.",
    "**Placement and residency.** The scheduler shall enforce placement by site, metro, and jurisdiction, and shall emit an attestation per request or per object for residency-pinned workloads.",
])

# =========================================================================
h1(doc, 10, "Deployment and siting requirements")
h2(doc, "10.1 Siting")
para(doc, "Sites are selected for scalable megawatts plus fiber density where utility capacity already "
          "exists (co-operatives, municipal utilities, cell sites, investor-owned utilities, and RTOs in the "
          "United States; distribution network operators and their equivalents in the United Kingdom), so "
          "that capacity, rate, and interconnect are locked before hardware is committed. Launch sites are "
          "Phoenix, Dallas, Newcastle, and Leeds, each an EC500 expandable to 20 MW.")
h2(doc, "10.2 Deployment channels")
bullets(doc, [
    "**Greenfield land-to-power.** Start sub-5 MW, expand to 20 MW on demand; full ownership of real estate and infrastructure; minimum two carrier connections.",
    "**Existing underutilized facilities.** 2,000 to 5,000 sq ft footprints, up to 80 racks, Tier II or III; fastest to first revenue because the shell removes the longest construction phase.",
    "**Carrier-adjacent and cell-site leasing.** Tower co-locations for latency-critical coverage where fiber and backhaul already exist.",
])
h2(doc, "10.3 Speed and capital cost")
bullets(doc, [
    "**Time to live.** 90 to 180 days from site selection, achieved by relocatable precast foundations (no concrete cure cycle), pre-engineered EC500 and EC1000 blocks, streamlined modular permitting, and parallel construction tracks. Vendors shall state the schedule to first power-on and to live for each module class and for each country.",
    "**All-in capital cost.** Vendors shall state an all-in delivered cost per module and per MW, including interconnect, civils, permitting, and security. Native Networks' objective is a materially lower installed cost and a far shorter schedule than traditional hyperscale builds, which run 36 to 60 months and $45 to 50M per MW.",
    "**Jurisdictions.** Modules shall be deliverable, certified, and permittable in both the United States and the United Kingdom. Vendors shall identify any component, certification, or design element that differs between the two.",
])

# =========================================================================
h1(doc, 11, "Use cases")
lead(doc, "Native Networks scopes its served demand as eight domains where the round trip is the problem. "
          "Each translates directly into the service levels a site must support.")
para(doc, "Latency and compliance are stated as the target profile the module must meet, not as claims of current certification.")
table(doc, [
    ["Domain", "Representative workloads", "Latency budget", "Compliance posture (target)"],
    ["AI inference", "Real-time voice, agentic sessions, conversational assistants, inline security, personalization, model refinement, and SLM serving", "Sub-20 ms", "Standard commercial; hard tenant isolation"],
    ["Public safety", "First-responder analytics, emergency communications, real-time situational awareness", "Sub-20 ms; high availability", "CJIS-aligned; government-capable; disaster recovery"],
    ["Mobility and V2X", "Vehicle-to-everything, autonomous and assisted driving, transport telemetry", "Sub-10 to 20 ms safety loop", "Functional safety; regional data residency"],
    ["Power and utilities", "Grid telemetry, predictive maintenance, digital twins, anomaly detection", "Low-ms local control", "NERC-CIP-aligned; critical infrastructure"],
    ["Healthcare", "Clinical monitoring, imaging inference, hospital disaster-recovery workloads", "Low-ms; local", "HIPAA; data residency; disaster recovery"],
    ["Web3 and validators", "Decentralized infrastructure nodes, blockchain validators", "High uptime; distributed presence", "Key custody; geographic distribution"],
    ["Smart city", "Video analytics, IoT pipelines, industrial automation, environmental monitoring", "High-bandwidth vision at source", "Municipal data governance"],
    ["Other and custom", "Robotics, physical AI, industrial vision, custom low-latency workloads (carrier, county CIO, model provider)", "Workload-defined", "Per-tenant SLO"],
], weights=[1.2, 2.8, 1.3, 1.9], size=8)
para(doc, "**Hardware-mix mapping.** Each domain leans on a different ratio of the four grid domains in "
          "Section 2.1. Inference-dominant domains (AI inference, public safety, smart city, mobility) are "
          "AI-hardware- and connectivity-heavy, served by 8-GPU inference domains with MIG partitioning for "
          "multi-tenancy. Data-gravity domains (power and utilities, healthcare) weight storage and compute "
          "alongside inference, with strong disaster recovery and data residency. Web3 and validators weight "
          "compute and connectivity with a lighter accelerator footprint. The control plane sets each site's "
          "domain ratio to the local demand mix and rebalances it quarterly.")

h2(doc, "11.1 Commercial and service-class mapping")
para(doc, "The eight domains are sold through the commercial ladder in Section 12 and delivered under the "
          "service classes below. The module must support the topology each class requires.")
table(doc, [
    ["Service class", "Monthly availability", "Topology the module must support", "Typical domains"],
    ["Bronze", "99.9%", "Single site with N+1 power, dual backhaul, on-site spares", "AI inference (self-serve)"],
    ["Silver", "99.95%", "Site plus automatic metro failover", "AI inference, smart city"],
    ["Gold", "99.99%", "Diversity-audited metro pair, drilled failover under 30 seconds", "Mobility, healthcare, power and utilities, Web3"],
    ["Platinum", "99.99% contracted, 99.999% measured", "Three or more sites across metros", "Public safety, NG911, sovereign workloads"],
], weights=[1.0, 1.4, 2.6, 2.0], size=8.5)

# =========================================================================
h1(doc, 12, "Commercial and offtake requirements")
lead(doc, "Every site launches with anchor capacity contracted before ground-break. The module's economics "
          "and the vendor's pricing must work under this ladder.")
table(doc, [
    ["Tier", "Structure", "Role in site economics"],
    ["Anchor offtake", "Agreements of five years and longer, triple-net, take-or-pay, covering about 40 to 60% of a site's capacity", "Covers facility fixed costs before a single spot GPU hour is sold; carries a contracted delivery date with liquidated damages"],
    ["Reserved capacity", "Two-year fractional reservations at mid-tier pricing; blocks reserved without a 100% utilization commitment", "Stabilizes utilization above the anchor floor"],
    ["Spot and preemptible", "On-demand GPU time at spot rates with a two-minute reclaim notice", "Fills idle capacity and maximizes revenue per deployed watt"],
], weights=[1.2, 3.0, 2.6], size=8.5)
para(doc, "Vendors shall price at program scale (a per-module price at one, ten, and one hundred modules) and "
          "shall state the earliest date by which a contracted module can be delivered against an anchor "
          "delivery-date commitment.")

# =========================================================================
h1(doc, 13, "Physical security requirements")
lead(doc, "Sites are unmanned, distributed outside-plant deployments (precast pads, existing shells, and carrier "
          "or cell-site co-locations), typically with no permanent on-site staff. Physical security must protect "
          "equipment, tenant data, and any personnel who visit.")
h2(doc, "13.1 Site and enclosure")
bullets(doc, [
    "**Enclosure hardening.** Locked, tamper-resistant modular enclosures rated for the deployment environment (NEMA or IP as applicable), with reinforced doors and panels and anti-pry, anti-drill, high-security locks.",
    "**Perimeter protection.** Fencing, bollards, and anti-vehicle measures at greenfield sites; secured cages or dedicated rooms at shared shells and cell-site co-locations.",
    "**Environmental and fire protection.** Seismic, wind, flood, and fire hardening consistent with the site risk profile in Section 10; fire detection and clean-agent (or equivalent) suppression that does not endanger equipment.",
    "**Tamper detection.** On all doors, panels, and equipment cabinets, alarming immediately to the network operations center.",
])
h2(doc, "13.2 Access control")
bullets(doc, [
    "**Multi-factor access.** Badge plus PIN or biometric at every entry point, with per-person, per-site authorization and full audit logging.",
    "**Least privilege.** Role-based, time-bound access grants for remote-hands, vendor, and third-party technicians; no shared credentials; immediate revocation on role change or departure.",
    "**Escort and logging.** Escort requirements for third parties; visitor and maintenance logs retained for a defined period.",
    "**Credential lifecycle.** Centralized issuance, rotation, and revocation of physical credentials, integrated with the electronic identity system (Section 14).",
])
h2(doc, "13.3 Surveillance and detection")
bullets(doc, [
    "**Video surveillance.** 24/7 CCTV covering the perimeter, entry points, and equipment aisles, with motion-triggered recording and a minimum 90-day retention.",
    "**Intrusion detection.** Door, motion, and enclosure sensors integrated with the NOC and with local audible and visible alarms.",
    "**Environmental monitoring.** Continuous temperature, humidity, smoke, water and leak, and door-state monitoring with automated alerting.",
    "**Correlation.** Physical access and video events correlated with electronic security monitoring (Section 14) for unified incident response.",
])

# =========================================================================
h1(doc, 14, "Electronic (cyber) security requirements")
lead(doc, "Because sites are unmanned and carrier-adjacent, the attack surface spans the network, the management "
          "plane, and the physical device. A zero-trust posture is required across compute, storage, network, and orchestration.")
h2(doc, "14.1 Platform and supply-chain integrity")
bullets(doc, [
    "**Hardware root of trust.** Secure and measured boot on all host platforms, management controllers, and network devices.",
    "**Signed firmware and software.** A verified supply chain with a software bill of materials; no unsigned or unverified components; secure firmware update with rollback protection.",
    "**Secure onboarding.** Zero-touch device provisioning with cryptographic attestation; tamper-evident hardware.",
])
h2(doc, "14.2 Network and data protection")
bullets(doc, [
    "**Segmentation.** Network and micro-segmentation isolating tenant, management, storage, and out-of-band planes; default-deny east-west controls across the mesh.",
    "**Encryption.** In transit (TLS 1.3, IPsec, or MACsec) and at rest (AES-256) for all tenant and management data, with per-tenant key isolation and customer-managed keys where a tenant requires them.",
    "**Key management.** Centralized, HSM-backed key management with rotation and revocation.",
    "**Edge defense.** DDoS protection, stateful firewalling, and intrusion detection and prevention at each site.",
])
h2(doc, "14.3 Identity, access, and monitoring")
bullets(doc, [
    "**Zero-trust identity.** Multi-factor authentication and short-lived credentials for all administrative access; no standing administrative access.",
    "**Logging and SIEM.** Centralized, tamper-evident audit logging with security telemetry streamed to a NOC or SOC.",
    "**Vulnerability management.** Continuous scanning and patching against the remediation service levels in Section 16.",
    "**Tenant isolation.** Validated to production standard (consistent with Section 9), with confidential-computing options (SEV-SNP, TDX, GPU confidential mode) where a tenant requires them.",
])
h2(doc, "14.4 Compliance and certification")
bullets(doc, [
    "**Frameworks.** The solution shall support SOC 2 Type II and ISO/IEC 27001 at the platform level, and shall be able to meet NIST 800-53, FedRAMP Moderate, CJIS, HIPAA, and NERC-CIP controls in the United States and Cyber Essentials Plus and UK GDPR obligations in the United Kingdom where a tenant workload requires (see Section 11).",
    "**Assurance.** Independent third-party penetration testing and audit evidence, provided on request and refreshed at least annually.",
])

# =========================================================================
h1(doc, 15, "OAM requirements")
lead(doc, "Sites are lights-out. Routine operations must be performed remotely, with rare, well-orchestrated field visits.")
h2(doc, "15.1 Remote operations and monitoring")
bullets(doc, [
    "**Single-pane management.** A DCIM or element-management system giving unified monitoring of power, cooling, environment, compute, network, and security across all sites.",
    "**Out-of-band management.** A dedicated, isolated management plane reachable even when the primary network is down, with cellular or LEO backup.",
    "**Telemetry and alarms.** Full telemetry (power, thermal, coolant flow and leak, GPU and node health, link state, security events) with severity classification and automated escalation to the NOC.",
    "**Remote control.** Per-rack and per-PDU remote power cycling and remote console and BMC access to all devices.",
])
h2(doc, "15.2 Administration and provisioning")
bullets(doc, [
    "**Zero-touch provisioning.** Automated configuration and infrastructure-as-code with golden images and drift detection.",
    "**Asset and configuration management.** A centralized inventory and configuration database across the fleet.",
    "**Change management.** Staged rollout, rollback, and full audit, with administrative access integrated with the security model (Section 14). Every automated action shall run through a policy engine with typed, audited, reversible steps.",
])
h2(doc, "15.3 Maintenance and field service")
bullets(doc, [
    "**Predictive maintenance.** Telemetry-driven preventive maintenance of cooling, power, pumps, fans, and filters.",
    "**Remote and smart hands.** Field service with defined dispatch and response times (Section 16) and on-site or nearby spares kits at each site.",
    "**Lifecycle management.** Staged, scheduled firmware and software maintenance with no single point of failure; spare-parts logistics and RMA with target replacement times; end-of-life and refresh planning.",
])
h2(doc, "15.4 Reporting and integration")
bullets(doc, [
    "**Dashboards and reports.** Real-time dashboards and periodic reporting on availability, capacity, energy (PUE), incidents, and security posture.",
    "**APIs.** Programmatic access to telemetry and events for integration with the Native Networks orchestration and control plane, the public status page, and customer portals.",
])

# =========================================================================
h1(doc, 16, "Service level requirements")
lead(doc, "Vendors shall commit to at least the following service levels, measured per site and across the fleet, "
          "with service credits for breaches. Final targets and the credit schedule are agreed in contract; the "
          "values below are the minimum Native Networks expects vendors to meet or exceed.")
h2(doc, "16.1 Availability and performance")
table(doc, [
    ["Measure", "Minimum", "Measured"],
    ["Site power availability", "99.99% (Tier III-equivalent)", "Monthly, per site"],
    ["Infrastructure and service availability", "99.99%", "Monthly, per site"],
    ["Network availability to carrier handoff", "99.99%", "Monthly"],
    ["Edge latency", "Sub-20 ms intra-region (Section 8)", "Continuously"],
    ["Network quality", "Packet loss under 0.1%; jitter under 2 ms", "Continuously"],
    ["Thermal compliance", "Within the equipment thermal envelope 100% of operating time", "Continuously"],
], weights=[2.2, 2.6, 1.4], size=8.5)
h2(doc, "16.2 Incident response and restoration")
table(doc, [
    ["Severity", "Definition", "Response", "Restoration target"],
    ["1", "Site down, safety, or security breach", "15 minutes", "4 hours"],
    ["2", "Degraded service or lost redundancy", "30 minutes", "8 hours"],
    ["3", "Partial issue, no customer impact", "2 hours", "2 business days"],
    ["4", "Informational or service request", "1 business day", "Scheduled"],
], weights=[0.7, 3.0, 1.2, 1.5], size=8.5)
h2(doc, "16.3 Security and maintenance service levels")
bullets(doc, [
    "**Security incident notification.** To Native Networks within 1 hour of detection.",
    "**Critical vulnerability remediation.** Within 72 hours of a validated critical finding; high severity within 7 days.",
    "**Field-service arrival for Severity 1.** Within [X] hours of dispatch, set per site distance and risk.",
    "**Scheduled maintenance.** Advance notice and approved windows only. Single sites: one weekly window. Metro pairs: rolling zero-downtime updates with no tenant-visible downtime.",
])
h2(doc, "16.4 Reporting and service credits")
bullets(doc, [
    "**SLA reporting.** Monthly reports measuring actual performance against every target above, in a form that feeds the Native Networks public status page.",
    "**Service credits.** Credits applied for missed targets per an agreed schedule; chronic or repeated breach triggers a remediation plan and Native Networks termination rights. Vendor credits shall be at least sufficient to fund the customer credits Native Networks pays automatically under its own SLA classes.",
])

# =========================================================================
h1(doc, 17, "Vendor response requirements")
lead(doc, "Native Networks invites qualified vendors to design, supply, integrate, and deliver the edge modules "
          "specified in this document. Sections 2 to 16 define the requirements; a proposal is evaluated on how "
          "fully and credibly it meets them.")
h2(doc, "17.1 Proposal contents")
bullets(doc, [
    "**Company profile.** Relevant experience delivering modular or edge datacenters, GPU platform integration, and direct-liquid-cooled deployments, with at least three references, including any UK deliveries.",
    "**Compliance matrix.** A point-by-point response to Sections 2 to 16 marking each requirement as met, partially met, or proposed alternative, with supporting notes.",
    "**Platform and configuration.** The proposed GPU platform(s) per module class (NVL72 metro hub and 8-GPU mesh, per Section 4 and Appendix A), including sourcing, allocation, and lead times.",
    "**Power and cooling.** The direct-liquid-cooling design, CDU sizing, water use, acoustic footprint, and a committed PUE for the EC500 and EC1000.",
    "**Storage, networking, orchestration.** How the 3 PB tiered storage, the connectivity fabric, and production multi-tenant isolation are delivered.",
    "**Delivery.** The schedule to first power-on and to live in each country, and the plan to meet the 90 to 180 day deployment target.",
    "**Pricing.** Itemized all-in cost per module and per MW (compute, storage, networking, cooling, integration, logistics), plus warranty, support and SLA terms, and pricing at one, ten, and one hundred modules.",
])
h2(doc, "17.2 Evaluation criteria")
para(doc, "Proposals are evaluated against the following, with weightings published in the final RFP.")
table(doc, [
    ["Criterion", "What is assessed"],
    ["Technical compliance", "Coverage of Sections 2 to 16 in the compliance matrix"],
    ["Deployment speed and schedule certainty", "Committed dates, critical path, and evidence from prior deliveries"],
    ["Total installed cost and cost of ownership", "All-in price per module and per MW, energy, maintenance, and refresh"],
    ["Supply security", "GPU allocation, lead times, and second-source options"],
    ["Support, SLA, and serviceability", "Service levels in Section 16, spares, and field coverage in both countries"],
    ["Sustainability", "PUE, water use, acoustic footprint, and embodied carbon"],
    ["Track record and references", "Comparable modular, edge, and liquid-cooled deployments"],
], weights=[1.8, 4.2], size=8.5)
h2(doc, "17.3 Submission and timeline")
bullets(doc, [
    "**Format.** A single consolidated proposal including the compliance matrix, all supporting documentation, and a named primary contact for negotiations.",
    "**Key dates.** Vendor questions due [insert date]; proposals due [insert date]; shortlist [insert date]; award [insert date].",
    "**Submission.** Send to [insert RFP contact and address], quoting reference [insert RFP number].",
    "**Status.** This RFP is confidential and does not constitute an offer or a commitment to contract; Native Networks may amend, extend, or withdraw it at any time.",
])

# =========================================================================
page_break(doc)
eyebrow(doc, "APPENDIX A · REFERENCE MESH TOPOLOGY")
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
p.paragraph_format.keep_with_next = True
set_font(p.add_run("Appendix A. Reference mesh topology"), 15, INK, True)
from nn_docx import hrule
hrule(doc).paragraph_format.keep_with_next = True
note(doc, "For consideration and further exploration only. The topology below is an exploratory reference "
          "architecture, not a committed requirement. It sketches how a heterogeneous, memory-tiered fleet "
          "could operate under the AI grid, and is offered as a starting point for design discussion with "
          "Native Networks. The segment classes, the fleet mix, and the routing rule are open questions.")
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(10)
p.add_run().add_picture(TOPOLOGY, width=Inches(6.2))
para(doc, "**Segments and GPU classes.** The metro hub runs GB300 NVL72 (72-GPU coupled fabric, about 20.7 TB "
          "HBM): the memory tier, a few per metro, for 2 to 3T models, long context, and high-concurrency "
          "serving plus mesh spill-over. The edge mesh runs B200 8×8 FP4 (8-GPU NVLink domain, about 1.44 TB "
          "HBM): the workhorse, many per region, near the signal, serving small models multi-tenanted plus any "
          "model up to about 1.8T FP4 at sub-20 ms. The optional regional node runs GB300 8×8 (about 2.3 TB "
          "HBM): a heavier mesh node for regions with enough 3T-class traffic to serve in-mesh rather than "
          "routing to the hub.")
para(doc, "**Draft placement rule.** Weights plus peak KV cache of about 1.3 TB or less and latency-critical "
          "stays on the nearest mesh node; 2 to 3T or long-context routes inward to the hub. Solid links carry "
          "hub traffic and spill-over; the dashed ring is mesh-to-mesh peering (a graph, not a spoke), so a "
          "request re-routes to a neighbor if a node drops rather than failing.")
para(doc, "**Open questions for further exploration.**", after=4)
bullets(doc, [
    "Fleet mix (the hub-to-mesh ratio) is unset, and it drives blended capital cost per MW. A fleet of mostly B200 8×8 mesh with a few GB300 NVL72 hubs prices very differently from an all-NVL72 build.",
    "Whether GB200 NVL72 or GB300 NVL72 is the right hub silicon, which depends on the actual 2 to 3T and long-context volume per metro.",
    "Whether any regions justify the GB300 8×8 regional node, or whether all large-model traffic should simply route to the hub.",
    "The KV-aware placement threshold needs validation against real model and context profiles, since context and concurrency, not weights alone, set the true per-domain ceiling.",
])
note(doc, "Issued by Native Networks (ANDD.ai) as a Request for Proposal. This document is confidential and is "
          "provided solely to support vendor proposals. It does not constitute an offer or a commitment to "
          "contract, and Native Networks may amend or withdraw it at any time.")

doc.save(OUT)
print("Wrote", OUT)
