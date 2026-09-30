# ANDD Commercialization Engine
**Office of the Chief Commercialization Officer — August 2026**
**Status: Phase 1→2 transition (pilot sites live; scaling to 20–50 nodes; fiat + stablecoin rails coming online)**

---

## 0. Commercial Thesis

ANDD's commercial engine must exploit three structural facts that no hyperscaler and no GPU-cloud can copy simultaneously:

1. **AI-native zero-touch operations** collapse the cost of selling and serving small customers to near zero. The same autonomy that runs the datacenters runs the funnel. Our AI onboarding agent is not a chatbot bolted onto a sales team — it *is* the sales team for the bottom 80% of deals, executing conversational quote-to-provision in minutes. This gives us hyperscaler-grade self-serve economics at edge-cloud scale, and it means our CAC curve bends down as the network grows instead of up.
2. **Capacity is pre-sellable before it exists.** Because nodes deploy in 60–90 days via prefab modules and sit in known metros, each node is a discrete, financeable, pre-sellable unit. Anchor-tenant pre-commits (40–60% of node capacity sold before ground-break) convert GTM wins directly into de-risked capex — sales and site development are the same flywheel.
3. **Programmable money and programmable SLAs** turn billing and trust into product features. Smart-contract SLAs with automatic credits are a closing weapon, not an ops nicety; stablecoin settlement and micro-transaction channels open segments (DePIN, agentic workloads, per-call inference) that fiat-only clouds structurally cannot bill.

The engine below is organized so that **usage revenue seeds demand, committed revenue funds nodes, and reserved/contracted revenue (off-takers, gov, telco) anchors the balance sheet.**

---

## 1. Go-to-Market Motions by Segment

### Summary Matrix

| Segment | Motion | Primary Discovery Channels | Sales Cycle | CAC Target | Who Sells |
|---|---|---|---|---|---|
| Spot/consumer developers | Pure PLG self-serve | Model hubs (Hugging Face, OpenRouter), dev communities, SEO on latency benchmarks, hackathons | Minutes–days | <$50 blended (near-zero marginal) | AI onboarding agent, 100% |
| Startups | PLG + AI-assisted upsell | YC/accelerator perks, cloud-credit programs, GitHub/framework integrations (vLLM, LangChain, Ray) | Days–4 wks | $500–2,000 | AI agent; human touch only >$100k ARR |
| Mid-market / regional fintech | AI-qualified, human-closed | Compliance/latency content, core-banking ISV partners (Jack Henry, Fiserv ecosystem), regional banking associations, fintech conferences | 2–4 months | $8k–20k | AI agent qualifies + drafts; 1 AE closes; solutions engineering by AI copilots |
| Commercial off-takers (enterprise/telco capacity) | Named-account enterprise + structured finance | Direct exec outreach, cloud marketplaces (private offers), infrastructure bankers, telco wholesale desks | 4–9 months | $50k–150k | VP-level human team; AI builds capacity models, contract drafts, TCO decks |
| State/local government | Channel + cooperative purchasing | NASCIO, state CIO offices, public-safety associations (APCO/NENA for NG911), OZ economic-development offices, SLED-focused VARs | 6–12 months | $30k–80k | SLED channel partners + 1 gov capture lead; AI generates RFP responses |
| Federal/defense | Capture + contract vehicles | GSA MAS, NASA SEWP, OTAs (DIU, AFWERX), FedRAMP Marketplace listing, SI primes | 12–24 months | $150k–400k per program | Dedicated capture team + prime/sub relationships; AI drafts compliance artifacts |
| DePIN projects | Protocol BD + programmatic | Protocol governance forums, DePIN conferences/hackathons, direct integrations (SDK), crypto-native content | 1–3 months to integrate | $5k–15k | Protocol BD lead + AI agent handles technical onboarding and settlement setup |
| Municipalities/communities | Anchor-tenant-led site launches | OZ investor networks, mayors/economic-dev councils, community broadband groups, QOF co-marketing | 6–12 months (paired to site dev) | Absorbed into site-dev cost | Site-development team + gov capture; AI produces community-impact and jobs models |

### 1.1 Spot/Consumer Developers — Pure PLG, Zero Human Touch

**Motion.** Credit card or USDC in, API key out, tokens flowing in under five minutes. No sales team will ever touch this segment. The AI onboarding agent handles signup, KYC-lite, workload profiling ("what are you building?"), model/region recommendation, and first-call success. Free tier: enough serverless inference to run a demo, hard-capped.

**Discovery.** This segment is won where developers already are: (a) **model-hub integrations** — ANDD listed as an inference provider on OpenRouter and Hugging Face endpoints, where routing is won on price+latency, not brand; (b) latency-benchmark content ("p99 under 20ms from Kansas City — here's the trace"); (c) OSS framework adapters (vLLM, LiteLLM, LangChain provider plugins) so switching cost is one config line; (d) hackathon credit drops in metros where nodes exist — the "compute in *your* city" story is unique and demoable.

**Economics.** Sales cycle: minutes. CAC: marginal cost approaches $0 (agent inference + credit incentives); blended target <$50. This segment is deliberately low-margin — its job is utilization fill, word-of-mouth, and graduating users into startups.

### 1.2 Startups — PLG With AI-Driven Expansion

**Motion.** Same self-serve front door, but the AI agent runs an *expansion* playbook: it watches usage patterns and proactively offers the next commercial step ("you spent $4,100 last month on on-demand; a 1-year commit on 2× L40S saves you 31% — sign here, provisioned now"). Quote-to-provision conversationally, in minutes — the agent generates the order form, applies the discount schedule, executes the commit, and re-provisions, with a human countersignature required only above $250k TCV.

**Discovery.** Accelerator credit programs (YC, Techstars deal books), cloud-credit-matching offers for startups graduating off hyperscaler credits, and integration marketplaces. Positioning: "the edge cloud that onboards like Stripe."

**Cycle/CAC.** Days to 4 weeks; CAC $500–2,000 including credits. First human involvement threshold: $100k ARR trajectory, and even then the human is an account *advisor*, not a quota-carrying gatekeeper — the agent still executes the paperwork.

### 1.3 Mid-Market / Regional Fintech — AI-Qualified, Human-Closed

**Motion.** Sales-assisted, but inverted from the traditional model: the AI agent runs discovery, technical qualification, architecture recommendation, security-questionnaire completion (SOC 2 evidence auto-served), pricing scenarios, and contract drafting. The human AE enters only for the trust-and-negotiation layer — typically 2–3 meetings instead of 10. Fraud-detection latency (<50ms) and data-residency-by-construction are the wedge products; a live proof-of-latency demo from the node nearest the prospect's datacenter is the signature sales moment.

**Discovery.** Compliance/residency content marketing; partnerships with core-banking ISVs and payment processors who embed ANDD as their low-latency inference substrate; regional banking associations; state fintech sandboxes.

**Cycle/CAC.** 2–4 months (the compliance review is the long pole — pre-answered questionnaires and the FedRAMP-track story compress it). CAC $8k–20k. One AE should carry 3–4× a traditional pipeline because AI does everything except the handshake.

### 1.4 Commercial Off-Takers (Enterprises/Telcos Committing to Capacity)

**Motion.** Named-account, executive-led, structured-finance-adjacent. These are not cloud sales; they are **capacity origination deals** — an enterprise, telco, or AI company commits to blocks of future node capacity (see §2.4–2.5). The sale is run like a project-finance placement: capacity model, delivery schedule, take-or-pay terms, SLA schedule. AI's role: builds the TCO models, generates the site-delivery Gantt, drafts the capacity reservation agreement, and — post-signature — gives the off-taker a real-time dashboard of their reserved capacity's build status and utilization.

**Discovery.** Direct executive outreach; **cloud marketplace private offers** (AWS/Azure/GCP Marketplace lets enterprises burn committed cloud spend on ANDD — see §3.5); telco wholesale desks; infrastructure/datacenter bankers who see off-take demand they can't place into hyperscale queues.

**Cycle/CAC.** 4–9 months; CAC $50k–150k, justified by $2M–$50M TCVs. This is where human sales talent concentrates — perhaps 4–6 people company-wide even at Phase 3.

### 1.5 State/Local Government

**Motion.** Channel-led via SLED VARs and **state cooperative purchasing** agreements (NASPO ValuePoint, OMNIA, Sourcewell), which let one contract vehicle serve hundreds of municipalities without individual RFPs. Wedge use cases: NG911 call-routing and transcription, public-safety video analytics, smart-city sensor fusion — all latency- and residency-sensitive, all mapped to our published constituency #1. The OZ story is a differentiated door-opener: mayors get jobs, tax base, and digital infrastructure in the same conversation.

**Cycle/CAC.** 6–12 months; CAC $30k–80k per state entry, then near-zero for piggyback purchases on the cooperative vehicle. AI drafts RFP responses from a curated compliance corpus (target: 80% of proposal volume machine-generated, human-reviewed).

### 1.6 Federal/Defense

**Motion.** Classic capture discipline, sequenced to compliance milestones: FedRAMP Moderate (Phase 2 target) unlocks civilian agencies via the **FedRAMP Marketplace**; **OTAs** (DIU, AFWERX/SpaceWERX) are the fast path to defense pilots without full FAR procurement; **GSA MAS** (Special Item Numbers for cloud/IaaS) and **NASA SEWP** ride-along via an established contract-holder reseller before we hold our own vehicles. Prime through SIs (Booz, Leidos, CACI-class) for large programs; sell direct on OTAs. The sovereign-mesh story — distributed, survive-in-place, SCIF-compatible enhanced sites — is a genuinely differentiated defense narrative versus centralized clouds.

**Cycle/CAC.** 12–24 months per program; CAC $150k–400k. Do not staff this ahead of FedRAMP Moderate; one capture lead in FY26, a team of 3–4 by Phase 3.

### 1.7 DePIN Projects

**Motion.** Protocol partnership BD, then fully programmatic. The deal: the protocol routes demand (storage, bandwidth, compute verification, inference) to ANDD nodes; settlement is stablecoin, per-epoch, via payment channels; **composable SLAs** let the protocol cascade our uptime guarantees into their own token-holder promises — a capability literally no other infrastructure provider offers them. After integration, zero human involvement: demand routing, metering, settlement, and SLA credits are all machine-to-machine.

**Discovery.** Protocol governance forums (we show up with a draft integration proposal, not a pitch deck), DePIN-focused events, and reference integrations (Phase 2 target: 2–3 protocols; Phase 3: 10+).

**Cycle/CAC.** 1–3 months to integration; CAC $5k–15k. Watch-item: revenue quality varies with token markets — cap DePIN at ~15% of revenue mix and require stablecoin (not native-token) settlement.

### 1.8 Municipalities/Communities — Anchor-Tenant-Led Site Launches

**Motion.** This is GTM and site development fused. Each new metro launch is a **coalition sale**: OZ investors fund the node (QOF structure), the municipality provides site/permitting/sometimes an anchor workload (public safety), a telco or regional enterprise takes an anchor block, and local startups get launch credits. The commercial team's product here is *the node itself* — sold before it's built (§2.5). AI produces the community-impact models (jobs, tax revenue, digital-inclusion metrics) that make the municipal side of the coalition move.

**The AI onboarding agent as the signature differentiator (all segments).** Across segments 1.1–1.3 and post-integration 1.7 — the bottom 80% of deals by count — no human touches the transaction. The agent: profiles the workload conversationally → recommends node/region/hardware → generates a firm quote with live capacity check → executes payment (card, ACH, USDC) → provisions within minutes → schedules its own follow-up based on usage telemetry. Target: **80%+ of new logos and 40%+ of new ARR closed with zero human involvement by end of Phase 2**, rising to 60% of ARR by Phase 3. This is the demo we lead every enterprise meeting with, because it *proves* the AI-native ops claim commercially before we ever discuss infrastructure.

---

## 2. Offer & Deal Structures — The Commercial Menu

| # | Offer | Target Segments | Term | Discount vs List | Key Mechanics |
|---|---|---|---|---|---|
| 1 | On-demand (list) | All | None | 0% | Per-second GPU, per-token inference, per-GB storage/egress |
| 2 | Prepaid credit packs | Devs, startups, DePIN | Credits expire 12 mo | 5–15% by pack size | Fiat or USDC; instant via AI agent; non-refundable |
| 3 | Committed-use discounts | Startups → enterprise | 1 yr / 3 yr | 25–35% / 40–50% | Resource- or spend-based; AI agent right-sizes and auto-proposes |
| 4 | Capacity reservation (take-or-pay) | Off-takers, gov, telco | 3–7 yr | Custom (floor pricing) | Reserved kW/GPU blocks; take-or-pay 70–85%; resale/remarketing rights |
| 5 | Anchor tenant (new-site) | Off-takers, gov, telco, fintech | 3–7 yr, pre-ground-break | Best pricing in book + naming/priority rights | 40–60% of node pre-sold; milestone-based commitment |
| 6 | Revenue share | Telcos, municipalities | 5–10 yr | n/a (partner economics) | Partner contributes site/power/fiber/demand; 10–25% of node net revenue |
| 7 | Wholesale/reseller | Telcos, MSPs, SIs, VARs | 1–3 yr | 20–35% off list | White-label or co-brand; committed minimums; partner-of-record billing |
| 8 | DePIN protocol partnership | DePIN | Protocol-term | Volume-tiered | Programmatic demand routing; stablecoin epoch settlement; composable SLAs |
| 9 | Gov contract vehicles | SLED, federal | Per vehicle | Per GSA/coop schedules | GSA MAS, SEWP (via reseller first), OTAs, NASPO/OMNIA/Sourcewell |

### 2.1 On-Demand List Pricing
The reference price for everything. Per-second GPU billing, per-token serverless inference, per-GB-month storage, per-GB egress (priced aggressively low — egress gouging is the hyperscaler wound we salt). List prices are public, published, and machine-readable (an API endpoint), because agentic buyers — AI agents purchasing compute for their principals — are an emerging channel we intend to own.

### 2.2 Prepaid Credit Packs
$500 / $5k / $50k packs at 5/10/15% discount, purchasable in one conversational turn with the AI agent, settled in fiat or USDC. Prepaid is our default risk posture for unproven accounts (see §3.3) and is working capital positive. Credits expire in 12 months (breakage is margin; recognize per §3.7).

### 2.3 Committed-Use Discounts (1/3-Year)
The workhorse mid-funnel instrument. Two flavors: **resource commits** (specific GPUs at a specific node — deeper discount, because it lets our scheduler plan) and **spend commits** (flexible across the fabric — shallower discount). 1-yr: 25–35%; 3-yr: 40–50%. Signature move: the AI agent *initiates* commit conversations from usage telemetry and can execute the entire upgrade autonomously below $250k TCV. Commit revenue is the primary NRR engine.

### 2.4 Capacity Reservation Contracts (Take-or-Pay)
For off-takers reserving whole capacity blocks (e.g., 100kW of inference capacity across 3 named nodes, or 500 L40S-equivalents fabric-wide):
- **Take-or-pay floor at 70–85%** of reserved capacity — the off-taker pays for the floor whether consumed or not; usage above floor bills at the committed rate.
- **Remarketing clause**: unconsumed reserved capacity may be resold by ANDD into the spot pool, with 50% of spot proceeds credited back to the off-taker — softens take-or-pay optics while protecting our floor, and keeps physical utilization high.
- **Cancellation terms**: no termination for convenience in years 1–2; thereafter, termination on 12 months' notice plus a fee equal to 40% of remaining contract value, stepping down 5 points per year. Government contracts substitute standard termination-for-convenience clauses priced into the rate.
- **Delivery SLAs on us**: if a contracted node/hub is late, the off-taker receives equivalent capacity elsewhere on the fabric plus service credits — enforced by the same smart-contract SLA machinery, which is a *remarkable* trust signal in a capacity negotiation.

### 2.5 Anchor Tenant Deals — The Node-Launch Flywheel (Signature Mechanic)
Every new node launches with **40–60% of its sellable capacity pre-committed before ground-break.** Mechanics:

1. **Site selection triggers origination.** When site development shortlists a metro, the commercial team opens an "anchor book" for that node: capacity blocks offered at the best pricing that node will ever see (typically 45–55% below list on a 5-yr term).
2. **Anchor composition target** for a 300kW inference-heavy node: one telco or enterprise block (25–35% of capacity), one gov/public-safety block (10–15%), one fintech or ISV block (5–10%). Diversification rule: no single anchor >40% of any node.
3. **Milestone-gated commitment**: anchor obligation activates at node acceptance testing; anchors pay a reservation deposit (5–10% of year-1 value, creditable) at signing, which funds pre-construction. Anchors get delivery-date SLAs with automatic credits, priority provisioning, optional naming/co-marketing, and first-refusal on expansion capacity.
4. **Financing effect**: a node with 50% pre-sold capacity at contracted rates presents to QOF investors and lenders as an infrastructure asset with contracted cash flows, not a speculative build — materially lowering cost of capital and making the OZ raise faster. **Rule: no ground-break without ≥40% pre-commit coverage** (board may waive for strategic/first-in-market sites).
5. The remaining 40–60% of capacity is the high-margin merchant layer sold via PLG and commits — this is where blended margin is made.

### 2.6 Revenue-Share Deals (Telcos & Municipal Partners)
When a partner contributes an ingredient we'd otherwise pay for — telco central-office space, power, fiber backhaul, or a municipality's land/permits/anchor demand — we trade capex/opex for revenue share: **10–25% of node net revenue** depending on contribution, 5–10 year terms, with a minimum-revenue guarantee to the partner only in exceptional strategic cases. Telco variant adds mutual channel rights: they resell our edge capacity to their enterprise base (at wholesale terms, §2.7); we buy their backhaul at preferred rates. Municipal variant is politically potent: the city literally shares in the datacenter's revenue — an OZ story with a recurring check attached.

### 2.7 Wholesale/Reseller Pricing
20–35% off list, tiered by committed volume; white-label API available (the reseller's brand, our fabric). Resellers own billing and first-line support for their end customers — but crucially, we license them **the AI onboarding agent itself** (their branding, our engine), so channel deals inherit our zero-touch economics rather than reintroducing human-heavy sales. Rules of engagement: named-account registration, no resale into federal without our compliance sign-off.

### 2.8 DePIN Protocol Partnership Deals
Structure: (a) integration agreement (SDK, demand-routing spec, oracle feeds); (b) volume-tiered pricing settled in USDC per epoch via payment channels; (c) composable SLA schedule the protocol can pass through to its users; (d) optional co-marketing and joint grants to protocol developers. Settlement must be stablecoin; we do not take protocol-native tokens as payment (treasury policy), though we may accept them as *incentive grants* held separately. Future network utility token interactions (staking for reserved capacity) remain contemplated-only, per regulatory analysis.

### 2.9 Government Contract Vehicles
Sequenced acquisition of vehicles: **Year 1 (now)**: ride existing vehicles via reseller/SI partners (SEWP contract holders, GSA Schedule holders); pursue **OTA** pilots directly (DIU/AFWERX) — fast, prototype-friendly, no vehicle needed. **Year 2**: own GSA MAS award (cloud SINs); NASPO/Sourcewell/OMNIA cooperative agreements for SLED scale-out; FedRAMP Marketplace listing at Moderate. **Year 3+**: pursue positions as sub on major IDIQs; evaluate SEWP VI direct. Pricing on vehicles reflects the discount schedules above with GSA-compliant price lists; TAA/BAA compliance flows from our US-based prefab supply chain (verify per SKU).

---

## 3. Billing & Monetization Architecture (Commercial View)

The unifying policy: **one meter, one ledger, many settlement rails.** Every product emits usage events to a single metering pipeline; the AI billing agent rates, aggregates, and settles across fiat, stablecoin, and channel rails according to the customer's tier — and the customer experiences it as one coherent account regardless of how money moves.

### 3.1 Metering Granularity per Product

| Product | Meter | Granularity | Rail Fit |
|---|---|---|---|
| Serverless inference | Tokens in/out per model per region | Per request | Micro-tx channels or aggregated fiat |
| Dedicated GPU | GPU-seconds per SKU | Per second, billed per minute | Fiat monthly or prepaid |
| General compute | vCPU-s, GB-s RAM | Per second | Fiat monthly or prepaid |
| Object/block storage | GB-month, ops, egress GB | Hourly snapshots | Fiat monthly |
| Mesh networking / private interconnect | Gbps-hours, GB transferred | Per hour | Fiat monthly / included in reservation |
| Capacity reservations | Reserved kW or GPU-block per month | Monthly | Invoice (wire/ACH), multi-year |
| DePIN demand routing | Protocol-defined work units | Per epoch | Stablecoin channel settlement |
| SLA credits (outbound) | Breach-minutes × affected spend | Per incident, oracle-fed | Auto-credit in customer's settlement currency |

### 3.2 Invoicing Cadence
- **Self-serve (Starter)**: real-time balance decrement against prepaid credits or card-on-file weekly sweeps; monthly statement.
- **Professional**: monthly postpaid invoice, NET 30, ACH/wire; annual-prepay option at 15–20% discount (per published architecture).
- **Enterprise/off-taker**: monthly invoice for reservation fixed fee + usage overage, NET 45–60; annual true-ups on committed-use shortfalls.
- **Government**: per vehicle terms (NET 30 under Prompt Payment Act); milestone or monthly-in-arrears per CLIN structure.
- **DePIN/crypto**: continuous — payment channels settle per epoch (hours), batch option daily. Provisioning within one block confirmation of stablecoin receipt, as architected.

### 3.3 Prepaid vs Postpaid by Risk Tier (AI-Automated Credit Policy)
The AI billing agent runs a live risk score per account (payment history, usage volatility, entity verification, funding signals for startups) and assigns tier automatically:

| Risk Tier | Who (typically) | Policy |
|---|---|---|
| T0 — Anonymous/new | Spot devs, new signups | Prepaid only (card/USDC); hard spend caps; auto-suspend at zero balance |
| T1 — Verified, <6 mo history | Startups | Prepaid or card postpaid to a dynamic credit limit ($5–25k), limit raised algorithmically with on-time payment |
| T2 — Established | Mid-market, fintech | Postpaid NET 30, credit limit from score; deposits waived at 12 mo clean history |
| T3 — Contracted | Enterprise, off-takers, gov | Postpaid NET 45–60 under MSA; reservation deposits per §2.5 |
| Crypto-settled | DePIN, crypto-native | Effectively prepaid by construction (channel collateral); zero credit risk |

**Collections are fully AI-automated through day 60**: dunning sequences, self-serve payment-plan offers, service throttling (graceful degradation before suspension — inference rate-limits first, storage read-only at day 45, deletion never before day 120 with export window). Human review only for T3 accounts and disputes >$25k. Target: DSO <35 days blended; bad debt <0.5% of revenue (structurally low because ~half the base is prepaid/crypto-collateralized).

### 3.4 Taxes
Automated tax engine (Avalara/Anrok-class) at the metering layer: US sales-tax nexus tracking as nodes create physical presence state-by-state (each new node is a nexus event — the AI compliance agent flags registrations as site development commits); cloud services taxability varies by state and product classification, so SKUs carry tax codes from birth. Stablecoin payments are taxed identically to fiat (settlement currency doesn't change taxability); invoices denominate in USD with USDC as a payment method. Government sales: exemption-certificate handling automated.

### 3.5 Marketplace Billing — Tapping Committed Cloud Spend
List on **AWS Marketplace, Azure Marketplace, and Google Cloud Marketplace** with private-offer capability by Phase 2 end. Rationale: enterprises hold billions in committed hyperscaler spend (EDP/MACC agreements) that marketplace purchases draw down — a private offer lets a CIO buy ANDD capacity using budget *already committed to AWS*, neutralizing the "we're all-in on our cloud" objection. Costs 1.5–5% marketplace fees — cheap CAC for enterprise deals that would otherwise stall in procurement. Also list in **FedRAMP Marketplace** (compliance listing) and pursue SLED marketplaces via cooperative contracts. Marketplace-transacted revenue target: 15–20% of enterprise ARR by Phase 3.

### 3.6 Smart-Contract SLAs as a Sales Weapon
Reframe from ops feature to **the trust product**:
- **In the pitch**: "Our SLA is code. If we breach, credits appear in your account automatically — no ticket, no claims process, no arguing with support. Here's the contract address; here's the oracle feed; audit it yourself." No hyperscaler can say this; their SLA credits require the *customer* to detect the breach and file a claim within a window.
- **In negotiation**: kills the SLA-redline phase of enterprise deals (weeks of legal time) because remedies are deterministic and pre-agreed in code. Offer a fiat mirror for customers who don't want on-chain settlement: same oracle, same math, credit lands on the invoice.
- **In the product**: public, real-time SLA performance page per node (uptime, latency percentiles, credits paid) — transparency as marketing. "Credits paid automatically to date: $X" is a counterintuitive but devastating trust stat.
- **For DePIN**: composability (they cascade our guarantees into theirs) is the closing feature — it lets a protocol make hard promises to its token holders that are actuarially backed by our infrastructure.
- **For gov**: the immutable, oracle-fed performance record doubles as continuous compliance evidence — QASP reporting nearly free.

### 3.7 Revenue Recognition Considerations
- **Usage/on-demand**: recognized as consumed (point-in-time series). Straightforward.
- **Prepaid credits**: contract liability at sale; recognized on consumption; **breakage** recognized proportionally based on expected forfeiture (estimate from cohort data; expect 5–10%).
- **Committed-use**: recognize as consumed; shortfall/true-up amounts recognized when the commitment period expires and make-up rights lapse.
- **Capacity reservations (take-or-pay)**: the fixed reservation fee is a stand-ready obligation — recognized **ratably over the reservation period** regardless of consumption; usage above floor recognized as consumed. Deposits are contract liabilities. If a reservation conveys the right to a *specific identified* capacity block the customer controls, assess embedded-lease treatment (ASC 842) — structure contracts to retain substitution rights (fabric-level fulfillment) to keep them service contracts, which is also operationally what we want.
- **Anchor deals**: same as reservations; delivery-delay credits are variable consideration (estimate, constrain).
- **SLA credits**: variable consideration reducing revenue in the period of breach — the smart-contract automation actually makes accrual estimation *cleaner* (perfect data).
- **Revenue-share nodes**: gross-vs-net analysis per ASC 606 principal/agent — ANDD controls the service and is principal (gross revenue, partner share as cost) in standard structures.
- **Stablecoin receipts**: revenue measured in USD at receipt; USDC held is a financial asset — treasury policy: sweep to fiat/T-bills weekly, no speculative holding.

---

## 4. Pricing Strategy & Unit Economics

### 4.1 Pricing Posture by Product Line

| Product Line | Posture | Logic |
|---|---|---|
| Edge inference (<10ms service area) | **Premium: +25–60% vs region-agnostic inference** | No substitute exists; price against the value of latency (fraud caught, frame rendered), not against GPU cost |
| Sovereignty/residency products (pinned placement, compliance bundles) | **Premium: +20–40%** | Priced against the cost of the customer building compliant infra themselves; gov/CJIS/HIPAA bundles carry the compliance premium |
| Commodity GPU-hours (batch, training at hubs) | **Parity: within ±5% of GPU-cloud market (CoreWeave/Lambda-class)** | We can't win commodity on price at our scale; we win it on adjacency (data already on-fabric) — price to not lose, don't chase to the bottom |
| Serverless inference (open-weights, per-token) | **Aggressive: bottom-quartile per-token pricing** | Loss-leader to seed demand, fill idle capacity (marginal cost near zero on owned hardware), and feed the PLG→commit funnel |
| Storage | Parity on GB-month, **aggressive on egress (≤$0.01/GB or free intra-fabric)** | Egress pricing is the hyperscaler pain point; cheap egress is a switching incentive and honest at the edge (short haul) |
| Mesh networking/interconnect | Premium-lite | Unique fabric capability, priced for margin but not so high it discourages multi-node architectures (which increase stickiness) |

### 4.2 Price Fences — Protecting the Edge Premium from Cannibalization
The core hazard: aggressive serverless pricing eats the premium latency product. Fences:

1. **Latency-class SKUs**: serverless inference sells in three classes — *Standard* (fabric-routed, no latency guarantee, cheapest), *Regional* (sub-50ms, mid), *Edge-Pinned* (named node, sub-10ms, premium). Same silicon, different scheduling priority and guarantee. The cheap class is explicitly preemptible by the premium class.
2. **SLA as the fence**: only Edge-Pinned and Regional carry smart-contract latency SLAs. Standard has uptime SLA only. Customers who need the guarantee must buy the class that has it.
3. **Placement control as the fence**: data-residency pinning, compliance attestations, and dedicated tenancy are exclusive to premium tiers.
4. **Volume path crosses tiers**: discounts deepen with commitment, never by dropping tier — a big Standard buyer gets cheaper Standard, not free Edge-Pinned.
5. **No arbitrage**: Standard-class capacity is preemptible and unpinned, so it cannot be repackaged by resellers as guaranteed-latency service (wholesale contracts prohibit SLA misrepresentation; our oracles would expose it anyway).

### 4.3 Unit Economics — 300kW AI-Inference-Heavy Edge Node (Illustrative)

Assumptions: 300kW IT load; ~220kW to GPU inference (≈180 L40S-class accelerators), remainder to CPU/storage/network; capex ≈ $4.5M (prefab shell, power, cooling, network) + $3.5M IT hardware ≈ **$8.0M**; opex: power at $0.08/kWh blended, backhaul, insurance, security, allocated human cost at 1:30 nodes, AI-ops compute ≈ **$95k/month ≈ $1.14M/yr**. Sellable revenue potential at 100% utilization across the blended product mix (edge-premium inference, standard serverless, compute, storage) ≈ **$420k/month**.

| Metric | 40% util | 60% util | 80% util |
|---|---|---|---|
| Monthly revenue | $168k | $252k | $336k |
| Monthly cash opex | $95k | $101k (power scales) | $107k |
| **Node cash margin** | **$73k (43%)** | **$151k (60%)** | **$229k (68%)** |
| Annual node EBITDA | $0.88M | $1.81M | $2.75M |
| Cash-on-cash yield on $8M | 11% | 23% | 34% |
| Simple payback | ~9 yrs | ~4.4 yrs | ~2.9 yrs |

Readings:
- **Breakeven utilization is ~23–25%** — an anchor book at 40–60% pre-commit means every node is cash-positive from acceptance testing. This is the whole point of the anchor mechanic.
- The merchant layer (capacity above the anchor floor) is where margin expands violently: moving 60→80% utilization adds $78k/month at ~90% incremental margin.
- Anchor capacity is sold at ~45–55% off list, so a 50%-anchored node at 75% total utilization yields blended revenue ≈ $265–285k/month — model conservatively at the low end.
- Depreciation (5-yr IT, 15-yr shell) ≈ $87k/month — so full P&L profitability arrives around 45–50% utilization; the commercial target of 65%+ blended fabric utilization (see §6) puts mature nodes solidly profitable on a GAAP basis.

### 4.4 Blended Margin Targets

| Line | Gross Margin Target (mature) |
|---|---|
| Edge-premium inference & sovereignty products | 70–80% |
| Standard serverless inference | 35–50% (deliberately thin) |
| Commodity GPU / hub training | 30–40% |
| Storage | 60–70% |
| Reservations/anchor (fixed fees) | 55–65% (discounted but zero sales cost + guaranteed) |
| **Blended fabric target** | **Phase 2: 45–50% → Phase 3: 55–60% → Phase 4: 60%+** |

Margin expands with: utilization (operating leverage), mix shift toward premium/sovereignty products as compliance certifications land, and AI-ops ratio improving from 1:20 to 1:50 nodes.

---

## 5. Partnerships & Ecosystem

| Partnership Class | What They Bring | What We Bring | Commercial Structure | Priority |
|---|---|---|---|---|
| **Telco wholesale** (regional carriers, fiber operators, tower cos) | Backhaul, central-office/tower real estate, enterprise sales channel, spectrum-adjacent edge use cases (MEC) | Carrier-neutral edge capacity they can't build economically; new revenue per site | Rev-share nodes (§2.6) + mutual wholesale (§2.7) | **P0** — every node needs backhaul anyway; make the fiber vendor a partner |
| **ISV / model providers** (open-weights labs, vertical AI ISVs, core-banking/healthcare ISVs) | Demand gravity — their users need low-latency serving; distribution | Preferred serving infrastructure, per-token rev-share or co-sell, model-hub listings | Co-sell + marketplace rev-share; "Powered by ANDD" latency badge | **P0** — this is the PLG demand engine |
| **SI/VAR channel for gov** (SLED VARs, federal SIs, SEWP/GSA contract holders) | Contract vehicles today, capture muscle, agency relationships | Differentiated sovereign-edge offering they can prime with | Reseller (20–35%) + teaming agreements; migrate to direct vehicles over time | **P1** — mandatory until we hold our own vehicles |
| **OZ fund investor network as customer channel** | QOF LPs are often family offices, regional banks, healthcare systems, real-estate operators — i.e., *prospective customers* in the very metros they're funding | Dual-sided offer: invest in the node QOF *and* anchor its capacity — aligned returns | Cross-introduction program; anchor pricing for investor-affiliated off-take (arm's-length, documented) | **P1** — unique to ANDD; nobody else's cap table doubles as a demand pipeline |
| **DePIN protocol alliances** | Programmatic demand, crypto-native distribution, validation of programmable-payment rails | Enterprise-grade physical backbone + composable SLAs (unique) | §2.8 structures; joint grants for protocol devs | **P1** — 2–3 flagship integrations in Phase 2, 10+ by Phase 3 |
| **Cloud marketplaces** (AWS/Azure/GCP) | Access to committed enterprise spend, procurement fast-path | Marketplace fees, co-sell registrations | Private offers (§3.5) | **P1** |
| **Hardware/prefab partners** (GPU vendors, modular DC builders) | Supply priority, financing programs, co-marketing (e.g., NVIDIA/AMD partner programs) | Volume, reference architecture for edge inference | Procurement + co-marketing; explore vendor financing on IT capex | P2 |
| **Universities/public safety associations** (APCO/NENA, community colleges in OZ metros) | SLED credibility, workforce pipeline for the human 5% | Training partnerships, NG911 pilots | MOU + pilot pricing | P2 |

Ecosystem sequencing note: telco + ISV partnerships compound the fastest and require no compliance gates — execute now. Gov channel scales with FedRAMP milestones. The OZ-investor-as-customer channel should be formalized as a named program ("Anchor Investor Program") with clean arm's-length pricing documentation, because it is both a genuine differentiator and an obvious diligence question.

---

## 6. Commercial Metrics & Targets

### 6.1 KPI Tree

```
NORTH STAR: Contracted + Consumed Revenue per Deployed kW ($/kW/mo)
│
├── NEW REVENUE ENGINE
│   ├── Zero-touch ARR % (deals closed by AI agent, no human) — signature metric
│   ├── Time-to-first-dollar per customer (signup → paid usage): target <1 hr self-serve
│   ├── CAC by segment / CAC payback (target <12 mo blended, <3 mo PLG)
│   ├── Pipeline coverage per node launch (anchor book $ vs node capacity $)
│   └── Marketplace-sourced enterprise ARR %
│
├── NODE ECONOMICS ENGINE
│   ├── Pre-commit coverage per new node (% capacity sold at ground-break): floor 40%, target 55%
│   ├── Time-to-first-dollar per NODE (acceptance test → first revenue): target <7 days
│   ├── Node utilization % (by class: anchored / committed / merchant) — fabric target 65%+
│   ├── Node cash-margin ramp (months to 60% cash margin): target <12 mo
│   └── $/kW/mo realized vs model
│
├── RETENTION & EXPANSION ENGINE
│   ├── NRR (target 115–125% commercial; 100–105% gov)
│   ├── Gross revenue retention (>92%)
│   ├── Commit conversion rate (on-demand → committed within 6 mo of $2k+/mo spend): target 35%
│   ├── SLA credit rate (credits paid / revenue): target <0.5% — also a trust KPI we publish
│   └── DSO / bad debt (<35 days / <0.5%)
│
└── MIX & QUALITY
    ├── ARR mix by segment (see 6.2) and by offer type (usage / commit / reservation)
    ├── Contracted revenue backlog ($ TCV, weighted)
    ├── Blended gross margin (see 4.4)
    └── Revenue per human FTE (AI-native leverage metric)
```

### 6.2 Directional Revenue-Mix & Scale Targets

Aligned to the published roadmap (Phase 2 underway: 20–50 nodes by mid-2027).

| Metric | **+12 mo (Aug 2027)** — late Phase 2 | **+24 mo (Aug 2028)** — Phase 3 | **+36 mo (Aug 2029)** — late Phase 3 |
|---|---|---|---|
| Deployed nodes / hubs | 30–50 / 2–3 | 100–150 / 5–8 | 250–300 / 10+ |
| Run-rate revenue (directional) | $25–45M | $120–200M | $350–550M |
| **Mix: Spot/PLG (devs+startups)** | 30% | 25% | 20% |
| **Mix: Mid-market/fintech commits** | 20% | 20% | 20% |
| **Mix: Off-taker reservations/anchors** | 30% | 30% | 28% |
| **Mix: SLED gov** | 8% | 10% | 12% |
| **Mix: Federal/defense** | 2% | 5% | 10% |
| **Mix: DePIN** | 8% | 8% | 8% (capped ~15%) |
| **Mix: Telco/wholesale/rev-share** | 2% | 2% | 2% |
| Zero-touch ARR share | 40% of new logos' ARR | 50% | 60% |
| NRR (commercial) | 110% | 118% | 122% |
| Fabric utilization | 45–55% | 55–65% | 65%+ |
| Pre-commit coverage on new nodes | ≥40% | ≥50% | ≥55% |
| Contracted backlog (TCV) | $60–100M | $300–500M | $1B+ |
| Blended gross margin | 45–50% | 52–58% | 58–62% |

Interpretation of the mix strategy: usage/PLG deliberately shrinks as a *share* while growing absolutely — it is the demand-seeding and margin-fill layer. Reserved/contracted revenue (off-takers + gov + telco ≈ 40–50% at maturity) is what finances the node-build flywheel and stabilizes the P&L. Gov mix grows on compliance milestones, not wishes: FedRAMP Moderate gates the federal line, and the SLED cooperative-purchasing vehicle gates municipal scale-out.

### 6.3 Operating Cadence
- **Weekly**: zero-touch close rate, utilization by node, anchor-book status per site in development, DSO alerts (all AI-generated; the commercial team reviews exceptions, not reports).
- **Monthly**: mix vs targets, NRR cohorts, node margin ramp curves, SLA credit rate.
- **Quarterly**: pricing review (the AI agent proposes reprices from win/loss + utilization elasticity data; humans approve), price-fence integrity audit (is Standard-class leaking into premium use cases?), partner channel QBRs.
- **Per node launch**: post-launch commercial review at day 90 — time-to-first-dollar, coverage vs anchor book, merchant fill rate — feeding the site-selection model.

---

## Appendix: Ten Commercial Rules (the doctrine, in one place)

1. No ground-break below 40% pre-commit coverage.
2. The AI agent sells everything below $250k TCV end-to-end; humans advise, they don't gatekeep.
3. Publish list prices, machine-readable; never publish reservation floors.
4. Discounts buy commitment or term — never given without one.
5. Premium tiers are fenced by guarantees and placement rights, never by artificial throttling of the cheap tier's *quality* — only its *certainty*.
6. Stablecoin settlement for DePIN always; native tokens never as payment.
7. Every SLA is code; every credit is automatic; every performance record is public.
8. Egress stays cheap forever — it's the moat-builder against hyperscaler lock-in.
9. DePIN revenue capped at ~15% of mix; gov mix grows only as fast as compliance certifications.
10. Every partner deal must inherit zero-touch economics (licensed AI agent) or it dilutes the model.
