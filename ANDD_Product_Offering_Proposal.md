# ANDD Product Offering Proposal

**How customers discover, sign up for, and consume the ANDD network: offers, billing, SLAs, go-to-market, and the 12/24/36-month roadmap**

**ANDD Network, Product Proposal v1.0 | August 2026**

*Prepared through a four-desk process: market research (live comparables, August 2026), product management, commercialization, and engineering. Where the desks disagreed, engineering's physical gates won. Nothing in this proposal promises what the network's density cannot yet deliver.*

---

## 1. Executive summary

ANDD sells three things nobody else can bundle: proximity (heavy GPUs within about 10ms of mid-size American metros), sovereignty (data residency built into placement, not bolted on through a consulting engagement), and zero-touch operations (the AI that runs the datacenters also runs the funnel, taking a customer from quote to provisioned workload in minutes). Every offer in this proposal is a packaging of those three assets.

The core findings from market analysis:

Raw inference token prices have fallen roughly 99% since 2023 and will keep falling. ANDD must never anchor margin to $/token. The durable premiums attach to what does not deflate: milliseconds (physics), jurisdiction (law), reliability (engineering), and compliance (regulation). Tokens bring customers onto the network; locality, sovereignty, and SLAs carry the margin.

The SLA whitespace is wide open. Most GPU clouds publish no numeric SLA at all. The best publish 99.9-99.99% with a manual claims process. Nobody pays credits automatically. ANDD's oracle-fed, self-crediting SLA has no competitor, and it is a sales weapon as much as an ops feature.

No provider prices latency by geography, yet AWS's 25% Local Zone uplift proves buyers pay for proximity. ANDD launches the first latency-tiered inference API.

The commercial engine and the site-development engine are the same flywheel. Every new node launches with 40-60% of capacity pre-sold to anchor tenants before ground-break. Since breakeven utilization is roughly 23-25%, each node is cash-positive from acceptance testing and financeable as contracted infrastructure rather than a speculative build.

The commercial strategy runs in three phases. Phase 1 is off-take: committed capacity contracts from enterprises, telcos, and government anchor every node before ground-break and underwrite the buildout. Phase 2 is verticals: depth in the segments where sovereignty and latency premiums live, such as public safety, fintech, healthcare, and DePIN. Phase 3 is spot: the posted-price exchange and PLG merchant layer that monetize whatever capacity the anchors and verticals leave idle. Phases 2 and 3 are sequenced by market conditions; they may be executed in parallel, or swapped outright if merchant demand outruns vertical sales.

Directional targets: $25-45M run-rate revenue at 12 months, $120-200M at 24, $350-550M at 36, with reserved and contracted revenue reaching about half the mix, blended gross margin climbing from 45-50% to about 60%, and 60% of new ARR closed with no human involvement by month 36.

---

## 2. Market context and comparables (August 2026)

### 2.1 What the market charges today

Serverless inference (per 1M tokens, open models): 7-13B-class models clear at $0.05-$0.30 (Groq $0.05 in for Llama-8B; Together $0.14-$0.28 for DeepSeek-class; Fireworks $0.15 in for Llama-8B). 70B-class runs about $0.59-$1.04. Batch at half price and cached-input discounts are table stakes everywhere.

GPU-hours (mid-2026 corridor): H100 on-demand runs from $2.15 (Nebius) to $6.16 (CoreWeave HGX), with marketplace floors at $0.90-$1.50 (Vast.ai, io.net). The L40S, ANDD's edge workhorse, rents for $0.90-$3.51/hr depending on trust tier (Vultr bare metal at $0.90-$1.20; Replicate serverless at $3.51). Dedicated endpoints: Together $5.49/hr H100, Fireworks $7/hr H100/H200, Baseten $6.50/hr.

Committed-use discounts of 15-45% are the standard curve industry-wide.

On SLAs: Lambda and RunPod publish no numeric SLA. CoreWeave's 99% rack-level penalties are negotiated, not published. Best in class is Baseten at 99.99% (active-active) and Fireworks at 99.9%, both with manual claims. No one pays credits automatically, and no one offers a latency SLA tied to geography.

### 2.2 The structural gaps ANDD exploits

| ANDD differentiator | State of the market | ANDD opportunity |
|---|---|---|
| Latency / proximity | No serverless provider prices geography; AWS Local Zones charge +25% but carry thin GPU inventory; Cloudflare edge serves small models only | The only provider with heavy GPUs under 10ms from mid-size metros; latency becomes a priced, SLA-backed tier |
| Sovereignty / residency | Hyperscalers put hardware on the customer's premises and budget (Outposts, Azure Local, GDC); DePIN can't even say where a workload ran | Jurisdiction-pinned placement as a checkbox, not a consulting project |
| Zero-touch dedicated capacity | Equinix Metal, the best attempt at API-provisioned bare metal, shuts down June 30, 2026, orphaning its customers | Instant provisioning of dedicated physical capacity, with a displaced buyer cohort in-market right now |
| Reliability plus programmable payments | DePIN discounts are real (60-80% below AWS) but reliability ceilings sit near 99.7%; Akash GPU supply fell over 57% QoQ as token rewards tightened | The first network with DePIN-grade programmable settlement on datacenter-grade infrastructure; ANDD's QOF-financed supply doesn't churn with a token price |
| Self-executing SLAs | Manual claims processes everywhere, or no SLA at all | Oracle-fed, self-paying, composable SLA credits, which no competitor offers |
| Gov procurement | FedRAMP 20x fast-track authorizations began March 2026; NASPO ValuePoint makes every state and county an eligible buyer with no RFP | The only sub-10ms GPU capacity purchasable off a pre-competed cooperative contract |
| Micro-billing | Per-token is micro-ish but settlement isn't; card-based prepaid breaks down for agentic and IoT per-request payment | Payment channels settling fractions of a cent per request |

### 2.3 Demand tailwind

Inference is now about two-thirds of all AI compute (up from one-third in 2023) and 80-90% of a model's lifetime compute spend. The edge AI market is $30-37B in 2026, growing at 22-29% CAGR toward $100B+ by 2030. NVIDIA's $1B investment into Nokia for AI-native RAN and edge signals where the majors believe this goes. Nobody has yet built the provider-owned, mid-metro, heavy-GPU layer.

---

## 3. Product catalog

### 3.1 Product philosophy

ANDD sells proximity, sovereignty, and zero-touch operations rather than raw GPUs. Every SKU is designed so the AI ops layer can quote it, provision it, meter it, and enforce its SLA without a sales or solutions team in the loop. All SKUs carry machine-readable metadata (metering unit, SLA class, residency capability, tier placement) so the provisioning agent and the SLA engine can compose them without human intervention. List prices are public and machine-readable, because agentic buyers, meaning AI agents purchasing compute for their principals, are an emerging channel ANDD intends to own.

### 3.2 Eight product lines

| Line | Product line | One-liner |
|---|---|---|
| AI | Inference & AI Services | Serverless tokens, dedicated endpoints, fine-tuning |
| CMP | Compute | GPU-hours, VMs, containers, bare metal, spot |
| STO | Storage | Object/block/file, residency-pinned, backup/archive |
| NET | Network | Interconnect, peering, CDN/cache, wavelengths, cheap egress |
| SOV | Sovereign | Gov/compliance bundles, cages, air-gap, survive-in-place |
| DPN | DePIN & Web3 | Validators, verifiable compute, programmable SLA APIs |
| NOD | Whole-Node | Node lease, private node, Node-as-a-Service |
| MKT | Marketplace | Per-call APIs, prepaid credits, spot exchange, model hub |

### 3.3 AI: inference and AI services (the wedge)

AI-Serverless is an OpenAI-compatible API over a curated catalog of open-weight models (7-70B chat, embeddings, ASR, image), routed to the nearest edge node with the model warm; 70B and larger serve from hubs. Four variants define the latency and sovereignty ladder:

| Variant | What it adds | Price vs Standard |
|---|---|---|
| Std | Fabric-routed, best-effort placement | Baseline (bottom-quartile market pricing) |
| Metro | Latency-pinned to a named metro, with a p99 latency SLA | +15-40% |
| Resident | Jurisdiction-pinned ("process only in Ohio"), attested | +20-30% |
| Batch | 24h async window; fills idle edge capacity | Half price |

Metered per 1M input/output tokens (plus per-second audio and per-image), with per-request micro-billing down to $0.000001 via payment channels. This is the first revenue SKU. It needs only one pilot site.

AI-Dedicated is a single-tenant model endpoint on named GPUs (catalog or bring-your-own-weights and LoRA), with guaranteed tokens/sec, p99 latency, autoscaling floor and ceiling, and placement control. Variants: Edge (L40S/MI300X, 7-34B), Hub (H100/H200/B200, 70B+), and Confidential (SEV-SNP/TDX attested serving, +15-25%). Billed per GPU-replica-hour; commit discounts of 20% monthly and 40% annual.

AI-Tune is managed fine-tuning (SFT/DPO/LoRA) and mid-scale training at hubs, with conversational job launch ("tune Llama-8B on this bucket, budget $400") and one-click deploy to a dedicated endpoint. It is hub-gated and arrives in Phase 2.

### 3.4 CMP: compute

CMP-GPU covers on-demand, reserved, spot, and fractional GPU access with per-minute billing. Reserved runs 30-55% off. Spot runs 60-75% off with a 2-minute reclaim notice; it is the mechanism that monetizes idle edge capacity, with prices set per-node by the AI capacity agent.

CMP-Edge covers managed K8s namespaces, scale-to-zero serverless containers billed per 100ms, VMs (x86 and ARM, with confidential variants), and dedicated bare metal. The bare metal SKU is the Equinix Metal succession product, aimed squarely at that displaced cohort.

### 3.5 STO: storage

S3-compatible object storage, erasure-coded across three or more geographically distinct nodes for 11-nines durability (the SKU is gated on having at least 3 nodes per region). STO-Object-Resident adds cryptographically attested jurisdiction pinning at +25-40%. Block (NVMe), file (NFS/SMB), archive (about a fifth of the object price), and managed backup with residency guarantees round out the family. Egress is deliberately priced at $0.01/GB or less, free intra-fabric. Egress gouging is the hyperscaler wound ANDD salts.

### 3.6 NET: network

Private interconnect ports into customer premises and cloud on-ramps (AWS DX, Azure ER, GCP at hubs), carrier-neutral peering at Connectivity-Hub nodes, metro wavelengths, a CDN with semantic AI-response caching, and a zero-trust mesh VPN across a customer's ANDD footprint.

### 3.7 SOV: sovereign and government

SOV-Cage is a dedicated secure cage or suite in Gov/Secure-profile sites, with customer-controlled access, attestation reports, and 12-60-month terms.

SOV-Bundle-FedMod, -CJIS, -HIPAA, and -ITAR wrap any base SKU in the relevant control set with auto-generated boundary documentation and continuous-monitoring feeds the customer's auditors can subscribe to, at a 15-35% uplift. These are never sold before the underlying authorization exists; in the interim the compliance agent sells the path on SOC 2 evidence.

SOV-AirGap is a node or cage that runs disconnected or intermittently connected (the survive-in-place control plane is native to the architecture), with an optional SCIF-compatible build.

SOV-Resilience-911 is packaged NG911 continuity: call processing, records, and AI dispatch-assist pinned to in-county nodes, sold as an annual subscription per PSAP.

SOV-Model-Enclave is sovereign inference in confidential-compute enclaves with attested no-egress reports.

### 3.8 DPN: DePIN and Web3

Validator hosting with anti-correlation placement guarantees (no two validators share a node or power region), managed RPC and indexers, verifiable compute with TEE-backed execution attestations, and the flagship DPN-SLA-API: programmable SLAs a customer can compose into their own downstream commitments, with automatic stablecoin credits on breach (a 5%-of-resource attach fee, included in Enterprise and Gov tiers). DPN-Backbone bundles metal, peering, and the SLA API as the wholesale land vehicle for DePIN networks whose own token-incentivized supply keeps evaporating. Any network-native consensus capability is referenced only as "network-native consensus protocol, evaluating options including licensing partnerships."

### 3.9 NOD: whole-node products

Whole-node leases (36-60-month terms, build-to-suit with take-or-pay), private nodes on customer campuses such as hospitals and utilities, Node-as-a-Service for telcos (white-label portal and API, MEC-ready, revenue-share or wholesale), Node-as-a-Service for municipalities (QOF-financeable, 5-10-year terms, bundled with public-safety workloads and community pricing for schools and clinics), and fractional nodes with guaranteed slices of 25% and up.

### 3.10 MKT: marketplace and spot consumer

Prepaid credits from $5 to $50k (card, ACH, or USDC/USDT, with provisioning within one block confirmation), per-API-call pay-as-you-go with no subscription or minimum, a posted-price spot exchange with a public machine-readable price feed, and, in Phase 3, a third-party model hub (publisher sets the markup, ANDD takes 15-20%) and an agent-template store.

---

## 4. Customer journeys: discovery to signup to consumption

The shared spine, stated once: every journey replaces sales-qualification calls with an AI Concierge that quotes real prices instantly, manual account review with KYC/KYB in minutes, capacity-planning meetings with autonomous capacity negotiation against live node telemetry, and SLA claims with automatic credits. Time-to-first-workload (TTFW) is a tracked product KPI per persona.

| Persona | Discovery | Signup | TTFW target | Core consumption | Growth path |
|---|---|---|---|---|---|
| Spot developer | Model hubs (OpenRouter, HF endpoints), latency-benchmark SEO, framework adapters (vLLM/LiteLLM/LangChain), hackathon credit drops in node metros | GitHub OAuth to API key plus $5 free credits, no card; or wallet plus USDC, provisioned in one block | Under 3 min | Serverless PAYG, playground with latency map | PAYG, then auto-top-up, then Starter, then a dedicated endpoint |
| Startup | Accelerator credit programs, "onboards like Stripe" positioning, Terraform/Pulumi registries | Self-serve org; KYB in minutes; startup credits auto-adjudicated in under an hour | Under 10 min first call; under 1 day production | Serverless, then a dedicated endpoint, K8s, object storage, spot for CI | Agent-proposed commits ("this endpoint on a 12-mo commit saves $1,340/mo"), multi-metro |
| Mid-market / fintech | Compliance and residency content, core-banking ISV partners, regional banking associations | Hybrid: sandbox same-day self-serve; production MSA/DPA e-signed, security questionnaire auto-answered by the compliance agent in hours | Sandbox same day; production under 2 weeks | Resident and Confidential inference (sub-50ms fraud), residency-pinned storage, private interconnect | Per-state residency expansion, custom models at hub, multi-year commit |
| Commercial off-taker (enterprise/telco) | Direct exec origination, cloud-marketplace private offers, telco wholesale desks, infrastructure bankers | Contracted, but compressed: the negotiation agent produces a binding term sheet (sites, kW, GPU mix, delivery dates, take-or-pay) in days; humans handle legal and the relationship | Existing capacity under 30 days; build-to-suit 60-90 days | Capacity blocks, node leases, wavelengths, white-label portal | 2-node pilot, then metro cluster, then statewide; quarterly flex of 15% either way without amendment cycles |
| Government (state/federal) | NASCIO and state CIOs, APCO/NENA for NG911, NASPO ValuePoint, FedRAMP Marketplace once listed, SI primes, the OZ economic-development narrative | Contracted per procurement regs; the compliance agent auto-generates SSPs and control matrices, compressing ATO timelines; OTAs for defense pilots | Pilot enclave under 60 days post-award | SOV bundles, cages, air-gap, NG911 continuity, private nodes | County PSAP pilot, statewide NG911, state AI enclave, then federal after ATO |
| DePIN project | Protocol governance forums (arrive with a draft integration proposal, not a deck), DePIN events, on-chain SLA registry discoverability | Wallet-based auth plus automated foundation KYB; pay USDC; provisioned in one block | Under 1 hour | Anti-correlated validators, RPC, verifiable compute, cascading SLA API, per-request channels | 5 validators, then protocol backbone, then their end-users consuming ANDD inference through the protocol's own app |
| Municipality / community | OZ economic-development offices, state broadband programs, county associations, groundbreaking press | Contracted (council approval, QOF financing); ANDD supplies model ordinance language and AI-drafted grant applications | Node live 90 days from executed agreement; first public-safety workload the same week | NaaS-Muni plus Resilience-911, smart-city analytics, community rates for schools and clinics, county-records residency | One node, then a county cluster, then a regional consortium; the municipality becomes a channel for local business onboarding |

---

## 5. Packaging, tiers, and pricing

### 5.1 Tiers

| | Free | Starter | Pro | Enterprise | Gov |
|---|---|---|---|---|---|
| Platform fee | $0 | $49/mo | $499/mo | Custom annual (about $60k/yr minimum) | Contract vehicle |
| Included credits | $5 expiring | $60 | $650 | Negotiated pool | Negotiated |
| Rate limits (serverless) | 20 RPM | 600 RPM | 6,000 RPM | Custom | Custom |
| SKU access | Serverless, PAYG, sandbox | Adds K8s/VM, storage, spot, CDN | Adds Dedicated, Tune, reserved, interconnect, DPN | Adds NOD, wavelengths, backbone, white-label | Adds all SOV |
| Default SLA class | Best-effort | Bronze 99.9% | Silver 99.95% | Gold 99.99% | Gold/Platinum-track |
| Auto-credit SLA | None | Attach option | Attach option | Included | Included where permitted |
| Residency pinning | None | Metro | State | State/county plus attestation | Full sovereign controls |
| Support (sev-1) | Community plus AI | AI plus 24h email | 24/7, 1-4h human | TAM-lite, 1h | Cleared personnel, 15 min |
| Billing | Prepaid only | Monthly CC/ACH, NET 30 | Monthly/annual ACH/wire | Annual, NET 45-60 | Per procurement, multi-year |

The free tier is permanent and hard-capped (no card on file, so no overage is possible), which costs almost nothing on idle edge capacity. Trials: 14 days with $500 in credits; the startup program grants $5-25k, auto-adjudicated. Gov and enterprise pilots are paid by design ($10-50k fixed scope) because free pilots don't test procurement.

### 5.2 Overage and spend protection

Base allocations draw down first; overage meters at list. Alerts fire at 50/75/90/100% with one-click actions: raise the cap, buy a discounted credit pack, or convert to a commit. Customer-set hard caps default to on for Free and Starter, so workloads throttle rather than surprise-bill. Pro and above get anomaly detection that freezes runaway patterns pending confirmation ("this batch job would cost $18k, confirm to proceed").

### 5.3 Commitment ladder

| Instrument | Term | Discount | Mechanics |
|---|---|---|---|
| Prepaid credit packs | 12-mo expiry | 5-15% by size | Fiat or USDC, one conversational turn; breakage is margin |
| Committed-use | 1 yr / 3 yr | 25-35% / 40-50% | Resource commits (deeper, because the scheduler can plan) or spend commits (flexible); fungible by design, committing dollars rather than hardware; the agent auto-proposes from telemetry and executes below $250k TCV |
| Capacity Block | 12-60 mo | Custom floor | Reserved kW plus GPU mix at named nodes; quarterly flex of 15% either way via the negotiation agent |
| Take-or-pay | 24-60 mo | Floor pricing | A 70-85% floor billed regardless; a remarketing clause resells unconsumed capacity into spot with half the proceeds credited back |
| Build-to-suit (NOD) | 36-120 mo | Contracted | NRC plus node-month; the take-or-pay floor covers financing; QOF-structurable |
| Forward capacity options | 6-36 mo | Option premium of 3-8% of strike | Callable future capacity, tradeable back to ANDD |
| Staked reservation (token) | n/a | n/a | Contemplated only, pending regulatory analysis; nothing customer-facing before the Phase 3 evaluation completes |

### 5.4 Pricing posture by line (anchored to August 2026 market data)

| Product line | Posture | Anchor |
|---|---|---|
| Serverless tokens (standard) | Aggressive: bottom quartile | Llama-8B-class around $0.10-$0.15/M; 70B around $0.85-$1.00/M blended; batch at half price and cached-input discounts are mandatory. A loss leader that fills idle capacity and feeds the funnel |
| Metro / latency-tiered inference | Premium: 25-40% over our own standard | Mirrors AWS's proven 25% Local Zone uplift; competitors can't follow without pouring concrete |
| Dedicated endpoints | Platform-tier parity | L40S at $1.90-$2.40/hr (between Vultr's $0.90 bare rate and Replicate's $3.51 serverless rate); H100-class at hubs at $3.50-$4.50/hr against RunPod $2.89, Lambda $3.99, Together $5.49, with locality and the auto-credit SLA included at the same price |
| Commodity GPU-hours / hub training | Parity within 5% | Price to not lose; win on adjacency, since the data is already on-fabric |
| Sovereignty / compliance | Premium: 20-100% | Priced against the customer building compliant infrastructure themselves; still cheaper all-in than Outposts or GDC because the customer buys no hardware |
| DePIN backbone | About twice DePIN spot, at a discount to CoreWeave-class contracts | Price against the cost of unreliability (99.7% versus 99.95%+) |
| Storage | Parity on GB-month; premium for residency; egress at $0.01/GB or less | Cheap egress is the switching incentive, and edge cost structure sustains it |

### 5.5 Price fences (protecting the premium from the funnel)

1. Latency-class SKUs: Standard (unpinned, preemptible, cheapest), Regional (sub-50ms), and Edge-Pinned (sub-10ms, premium). Same silicon, different scheduling certainty.
2. The SLA is a fence: only Regional and Edge-Pinned carry latency SLAs; Standard carries uptime only.
3. Placement control is a fence: residency pinning, attestation, and dedicated tenancy are premium-exclusive.
4. Volume never crosses tiers: a big Standard buyer gets cheaper Standard, never free Edge-Pinned.
5. No arbitrage: Standard is preemptible and unpinned, so resellers can't repackage it as guaranteed-latency service, and the public oracles would expose the attempt anyway.

---

## 6. Billing and monetization architecture

The unifying policy is one meter, one ledger, many settlement rails. Every product emits signed usage events into a single metering pipeline; the AI billing agent rates, aggregates, and settles across fiat, stablecoin, and channel rails, and the customer experiences one coherent account regardless of how the money moves.

### 6.1 Rails by customer

| Customer | Primary rail | Cadence |
|---|---|---|
| Self-serve | Prepaid credits or card sweeps | Real-time decrement; monthly statement |
| Professional | Postpaid ACH/wire | Monthly, NET 30; annual prepay saves 15-20% |
| Enterprise / off-taker | Invoice (reservation fee plus overage) | Monthly, NET 45-60; annual true-ups |
| Government | Per vehicle (Prompt Payment Act) | Milestone or monthly-in-arrears per CLIN |
| DePIN / crypto | USDC/USDT payment channels | Per-epoch (hours) or daily batch; provisioned within one block confirmation |

### 6.2 AI-automated credit policy

The billing agent runs a live risk score per account and assigns prepaid or postpaid automatically. Anonymous accounts are prepaid-only with hard caps. Verified startups earn dynamic credit limits of $5-25k, raised algorithmically. Contracted accounts get NET 45-60 under MSA. Crypto-settled accounts are prepaid by construction, since channel collateral carries zero credit risk. Collections are fully AI-automated through day 60: dunning, self-serve payment plans, and graceful degradation (rate limits first, storage read-only at day 45, deletion never before day 120 with an export window). Targets: DSO under 35 days and bad debt under 0.5%, which is structurally low because roughly half the base is prepaid or collateralized.

### 6.3 Cloud marketplaces: tapping committed spend

List on the AWS, Azure, and GCP marketplaces with private-offer capability by the end of Phase 2. Enterprises can then burn committed hyperscaler spend (EDP/MACC) on ANDD capacity, which neutralizes the "we're all-in on our cloud" objection at a 1.5-5% fee. That is cheap CAC for deals that otherwise stall in procurement. Target: 15-20% of enterprise ARR marketplace-transacted by Phase 3, plus a FedRAMP Marketplace compliance listing and SLED cooperative catalogs.

### 6.4 Revenue recognition (the load-bearing points)

Usage is recognized as consumed. Prepaid credits are contract liabilities, with breakage (estimated 5-10%) recognized proportionally. Take-or-pay reservation fees are stand-ready obligations recognized ratably. Contracts retain fabric-level substitution rights to stay service contracts and avoid ASC 842 embedded-lease treatment, which is also what the scheduler wants operationally. SLA credits are variable consideration, and the smart-contract automation makes accrual estimation cleaner, not messier. Stablecoin receipts are measured in USD at receipt and swept to fiat and T-bills weekly, with no speculative holding.

---

## 7. SLA framework

### 7.1 Engineering reality first (what the physics allow)

A single sub-2MW edge node, with N+1 power, dual backhaul of sometimes-fictional diversity, and a small hardware pool, compounds to an honest ceiling of about 99.9% monthly. Availability above that is bought with node density, not promises:

| Topology | Contractible SLA | Error budget | Hard preconditions |
|---|---|---|---|
| Single edge node | 99.9% | 43.8 min/mo | N+1 power, dual backhaul, on-site spares |
| Metro pair (2 nodes, under 2ms apart) | 99.99% | 4.4 min/mo | Diversity audit passed (power feeds, conduit-level carrier paths, staggered rollout waves) plus automated failover under 30s, chaos-drilled |
| Metro mesh (3+ nodes, anycast) | 99.99% contractual; 99.999% measured and published, never contracted in this horizon | 26 s/mo at five nines | N-1 capacity headroom, quarterly chaos drills, BGP fast withdrawal |

The governing rule: SLA tiers are gated on node count and audit status per metro, not on marketing calendars. No 99.99% SKU is sold in a metro until two diversity-audited nodes pass failover drills there. Five nines is never contracted within the 36-month horizon; it is published as measured trailing performance.

### 7.2 SLA classes and credit schedules

| Class | Availability | Scope | Default for |
|---|---|---|---|
| Best-effort | n/a | n/a | Free, Spot, Batch |
| Bronze | 99.9% | Single node | Starter |
| Silver | 99.95% | Node plus metro auto-failover | Pro |
| Gold | 99.99% | Multi-node metro | Enterprise, dedicated endpoints, validators, object storage |
| Platinum | 99.99% contracted with a 99.999% engineering target, multi-metro mesh | 3+ nodes across metros | SOV bundles, NG911, DePIN backbone (available Phase 3) |

Credits, as a percentage of the affected resource's monthly charge: the first breach band pays 10-25%, deepening to 100% below 99.0% on Gold, and Platinum pays double the Bronze rate at every band. For latency, any hour where p99 exceeds target by 20% or more is a breach-hour, paying 5% per breach-hour capped at 30% per month on Gold and 50% on Platinum. Confirmed object-storage data loss pays 12 months of storage fees for the affected data. Any confirmed residency boundary violation pays 100% of the monthly charge plus notification within 24 hours.

Beyond availability, the framework covers latency SLAs (p99 of 10ms or less network RTT within published service polygons, drawn from measured data rather than radius circles, and TTFT per model class rather than a blended "AI latency" number), throughput floors in tokens/sec on dedicated endpoints, 11-nines durability, recovery targets of RPO 15 min and RTO 4h, and delivery-date SLAs with liquidated damages on capacity contracts.

### 7.3 Measurement customers can audit

Dual attestation: ANDD's probe mesh and gateway-side real-user telemetry, co-signed by an independent third-party probe vendor, in a two-of-two oracle design. "ANDD grading ANDD's homework" convinces nobody. Real-tenant p99 governs when volume suffices; synthetic probes govern below 10k requests per month. The methodology is published on the status page, and historical data is never silently restated. Exclusions are stated plainly: last-mile beyond the polygon, client-side stalls, and cold starts on scale-to-zero tiers (the no-cold-start warm tier is priced explicitly).

### 7.4 The differentiated product: self-executing SLAs

Every SLA runs in one of two enforcement modes.

Classic auto-credit, from Phase 1 onward: ANDD measures, and the credit lands on the invoice automatically. There is no claims form and no filing window, which by itself beats every incumbent.

Programmable, in beta during Phase 2 and GA in Phase 3: SLA terms are encoded on-chain, telemetry is oracle-fed, and stablecoin credits stream automatically and proportionally on breach. It is composable: a DePIN protocol or SaaS vendor can reference ANDD's SLA contract inside its own customer SLAs, cascading credits downstream. No infrastructure provider offers this.

As a sales weapon: "Our SLA is code. If we breach, credits appear in your account. No ticket, no claim, no arguing with support. Here's the contract address; audit it yourself." It removes the SLA-redline phase of enterprise negotiations, feeds a public per-node performance page (where "credits paid automatically to date: $X" is an unusually persuasive trust stat), and doubles as nearly free QASP evidence for government contracts. A fiat mirror serves customers who want the math without the chain.

### 7.5 SLA promises by year

| | Year 1 (3-5 sites) | Year 2 (20-50 nodes) | Year 3 (100+ nodes) |
|---|---|---|---|
| Uptime | 99.9%, beta terms | 99.99% in diversity-audited metros | 99.99% standard; 99.999% measured and published |
| Latency | Published targets, monitored, not credited | p99 credits in mesh metros | Full portfolio including TTFT per model class |
| Credits | Automatic on invoice, fiat | Automated fiat, dashboard-verifiable, oracle beta | Smart-contract stablecoin credits GA |
| Maintenance | Weekly window, excluded | Rolling zero-downtime in mesh metros | No-exclusion SLAs in mesh metros |

Internally, every SKU carries an SLO one notch tighter than its contract. The AI SLA Guardian acts on multi-window burn-rate alerts (reroute, pre-warm, failover, then page a human) before money is owed, and automatically freezes non-security rollouts in any metro that has consumed more than 75% of its monthly error budget. That rule is what makes one human per 20 nodes survivable.

---

## 8. Go-to-market and commercial model

### 8.1 The commercial thesis

First, the AI onboarding agent is the sales team for the bottom 80% of deals. It runs conversational quote-to-provision in minutes and executes everything below $250k TCV end to end, with humans advising rather than approving each step. Targets: 80%+ of new logos and 40% of new ARR closed with no human involvement by the end of Phase 2, and 60% of ARR by Phase 3. This is the demo that opens every enterprise meeting, because it proves the AI-native claim commercially before infrastructure comes up.

Second, capacity is pre-sellable before it exists. Nodes deploy in 60-90 days into known metros, so each one is a discrete, financeable, pre-sellable unit.

Third, programmable money and programmable SLAs are closing weapons; they open segments (DePIN, agentic workloads, per-call inference) that fiat-only clouds cannot bill at all.

The engine layers by phase. Phase 1, off-take: reserved and contracted revenue from off-takers, government, and telcos anchors the balance sheet and funds nodes. Phase 2, verticals: segment-deep motions convert the sovereignty and latency premiums into committed revenue. Phase 3, spot: usage revenue from the exchange and PLG funnel seeds future demand and fills idle hours. Phases 2 and 3 are ordered by what the market gives us; they can run in parallel or trade places without changing the underwriting logic, because anchor off-take alone carries every node past breakeven.

### 8.2 Motions by segment

| Segment | Motion | Cycle | CAC target | Who sells |
|---|---|---|---|---|
| Spot developers | Pure PLG | Minutes to days | Under $50 | The AI agent, 100% |
| Startups | PLG plus an AI expansion playbook | Days to 4 weeks | $500-2k | AI agent; a human advisor only above $100k ARR |
| Mid-market / fintech | AI-qualified, human-closed (2-3 meetings, not 10) | 2-4 months | $8-20k | The agent qualifies and drafts; one AE closes |
| Off-takers (enterprise/telco) | Capacity origination, adjacent to structured finance | 4-9 months | $50-150k | VP-level humans; AI builds the models, contracts, and dashboards |
| State/local gov | Channel plus cooperative purchasing (NASPO, OMNIA, Sourcewell) | 6-12 months | $30-80k per state entry, then near zero for piggyback purchases | SLED VARs plus one capture lead; AI drafts 80% of proposal volume |
| Federal / defense | Capture discipline sequenced to compliance: OTAs (DIU, AFWERX), then GSA MAS and SEWP via resellers, then our own vehicles | 12-24 months | $150-400k per program | A capture team, staffed only after FedRAMP progress |
| DePIN | Protocol BD, then fully programmatic | 1-3 months to integrate | $5-15k | A BD lead; the agent handles onboarding and settlement |
| Municipalities | Anchor-tenant-led site launches (coalition sales) | 6-12 months, paired to site development | Absorbed in site development | The site team plus gov capture; AI produces the jobs and impact models |

### 8.3 The signature mechanic: anchor-tenant node launches

Every new node launches with 40-60% of sellable capacity pre-committed before ground-break. The hard floor is 40%; the board may waive it for strategic first-in-market sites.

1. Site shortlisting opens an "anchor book" at the best pricing that node will ever see, typically 45-55% off list on 5-year terms.
2. Target composition for a 300kW inference node: one telco or enterprise block (25-35%), one gov or public-safety block (10-15%), one fintech or ISV block (5-10%). No single anchor takes more than 40% of any node.
3. Anchors pay a creditable 5-10% reservation deposit at signing; obligations activate at node acceptance. Anchors get delivery-date SLAs enforced by the same smart-contract machinery, which is a strong trust signal inside a capacity negotiation.
4. A node with half its capacity pre-sold at contracted rates presents to QOF investors and lenders as infrastructure with contracted cash flows rather than a speculative build, which materially lowers the cost of capital.
5. The remaining 40-60% is the high-margin merchant layer sold through PLG and commits, where blended margin is made.

### 8.4 Partnerships (sequenced by compliance gates)

P0 now: telco wholesale, since every node needs backhaul anyway and the fiber vendor should be a partner (revenue-share nodes at 10-25% of node net, 5-10-year terms), and ISV and model-provider co-sell, the PLG demand engine, with a "Powered by ANDD" latency badge.

P1: the SLED VAR and SI channel (mandatory until ANDD holds its own contract vehicles), cloud marketplaces, DePIN protocol alliances (2-3 flagship integrations in Phase 2 growing to 10+ in Phase 3, settled in stablecoin always, native tokens never accepted as payment), and the Anchor Investor Program. QOF LPs (family offices, regional banks, healthcare systems) are prospective customers in the very metros they fund; they can invest in the node and anchor its capacity, at documented arm's-length pricing. No one else's cap table doubles as a demand pipeline.

The channel rule: every partner deal must inherit zero-touch economics. Resellers get the AI onboarding agent white-labeled (their brand, ANDD's engine), or the deal dilutes the model.

### 8.5 Unit economics: a 300kW inference-heavy edge node (illustrative)

Assumptions: about $8.0M all-in ($4.5M shell, power, cooling, and network plus $3.5M IT, roughly 180 L40S-class accelerators); about $95k/mo cash opex (power at $0.08/kWh, backhaul, insurance, allocated human cost at one person per 30 nodes); about $420k/mo sellable revenue at 100% utilization across the blended mix.

| | 40% util | 60% util | 80% util |
|---|---|---|---|
| Monthly revenue | $168k | $252k | $336k |
| Node cash margin | $73k (43%) | $151k (60%) | $229k (68%) |
| Cash-on-cash yield on $8M | 11% | 23% | 34% |

Breakeven utilization is about 23-25%, so a 40-60% anchor book makes every node cash-positive from acceptance testing. GAAP profitability, after about $87k/mo of depreciation, arrives around 45-50% utilization; the fabric target of 65%+ puts mature nodes solidly profitable. The blended gross margin path runs 45-50% in Phase 2, 55-60% in Phase 3, and 60%+ in Phase 4, expanding with utilization, the premium and sovereignty mix, and the ops ratio improving from 1:20 toward 1:50.

---

## 9. Unified 12/24/36-month roadmap

Each horizon integrates the product wave, the commercial motion, and the engineering critical path. The horizons carry the commercial phases: months 1-12 are dominated by Phase 1 off-take anchoring, months 12-24 by Phase 2 vertical depth, and months 24-36 by the Phase 3 spot layer maturing into a public capacity market. The phase labels describe the dominant motion, not a wall: the spot exchange opens as early as fleet scale allows, and Phases 2 and 3 may run in parallel or swap order if merchant demand outruns vertical sales. The dependency rules are hard gates: no consumption SKU before metering v1; no 99.99% contract before a diversity-audited metro pair; no federal SKU before ATO; no smart-contract credits before two external audits plus four quarters of dual-attested SLA data; no fractional GPU sharing for untrusted tenants before VM-grade isolation; no five-nines contracts, period; and no token launch work beyond an evaluation memo.

### Months 1-12, Phase 1 off-take: "Anchor the nodes, prove ops" (3-5 pilot sites)

| Track | Milestones |
|---|---|
| Product | Launch AI-Serverless (Std, Metro, Batch, plus metro-level Resident), prepaid credits and PAYG (fiat first, USDC fast-follow), AI-Dedicated-Edge, GPU on-demand and fractional, K8s/VMs, object storage (sold as single-metro replication until 3+ nodes enable geo-EC), Free/Starter/Pro tiers, classic auto-credit SLAs (Bronze through Gold), and AI Concierge v1. Two strategic anchors: one municipal NG911 pilot county (NaaS-Muni plus Resilience-911) and one design-partner fintech on Resident inference. The catalog is otherwise frozen: no training clusters, no FedRAMP-branded SKUs, no token products, no whole-node leases beyond the muni anchor. Two hardware profiles only (General Purpose, AI Inference Heavy) until node 20 |
| Engineering | Q1: fleet substrate and site bring-up automation. Q1-Q2: metering pipeline v1, which blocks everything consumption-priced. Q2: inference gateway beta with 5-8 curated models. Q3: serverless GA and dedicated endpoints GA. Q4: AI onboarding agent GA, policy and actuation engine v1, public status and SLA page, SOC 2 Type I, FedRAMP program kickoff. Team of about 18-24 engineers (4 squads plus security and SRE) |
| Commercial | The PLG engine goes live (model-hub listings, framework adapters, hackathon drops in node metros); anchor books open per pilot site; ride SEWP and GSA via resellers; pursue OTA defense pilots; convert telco backhaul partners into revenue-share prospects. Targets: paying logos in 3+ segments, 60%+ of edge GPU-hours monetized, zero-touch on 90%+ of signups |
| Exit criteria | A $25-45M run-rate trajectory by month 12; TTFW p50 under 3 minutes for developers; token gross margin of 55%+; 1-2 anchor contracts signed; SOC 2 Type I complete |

### Months 12-24, Phase 2 verticals: "Add depth, land segments" (20-50 nodes, 2-3 hubs)

| Track | Milestones |
|---|---|
| Product | Hubs unlock AI-Tune, 70B-class serving, training-class reserved SKUs, and storage cache. Fleet scale unlocks GPU spot plus the public spot exchange, the full storage family, interconnect, peering, CDN, and DePIN validator/RPC/backbone with 2-3 flagship protocols. Enterprise and Gov tiers, CUDs, and the first Capacity Blocks arrive. SOV-Bundle-FedMod and cages are sold only as FedRAMP progresses; StateRAMP and state/local sales bridge gov revenue in the meantime |
| Engineering | Q5: hub platform and stablecoin rail GA (USDC on Base and Solana; pay, then provision in one confirmation). Q5-Q6: metro-pair failover GA, enabling the 99.99% SLA in qualifying metros. Q6: 3-node erasure-coded storage GA, residency policy engine GA, automated fiat SLA credits. Q7: DePIN API beta (attestations plus programmatic settlement); AI ops autonomy above 90% with the top-20 runbooks closed-loop. Q8: fine-tuning beta, AWS and Azure marketplace listings, the FedRAMP boundary under 3PAO assessment, anycast beta in 3+ node metros. Team of about 40-55 |
| Commercial | Marketplace private offers go live; a NASPO ValuePoint listing (directly or via an awarded reseller) converts every municipality into an eligible buyer; the capacity-origination desk stands up; the Anchor Investor Program is formalized; DePIN revenue is capped near 15% of mix and settled in stablecoin, always |
| Exit criteria | 99.99% SKUs live in audited metros; the first $1M+ TCV gov and capacity-block contracts; 2-3 DePIN backbones live; zero-touch at 40% of new ARR; spot clearing 70%+ of idle hours; NRR of 110%+; pre-commit coverage of 40%+ on every new node |

### Months 24-36, Phase 3 spot: "Open the market, lock in the moat" (100-300 nodes, 10+ hubs)

| Track | Milestones |
|---|---|
| Product | The moat products ship: smart-contract SLA GA (oracle-fed, dual-attested, auto-streaming stablecoin credits, with a composable breach-event feed), micro-transaction channels, verifiable compute, whole-node leases and telco NaaS and fractional nodes (the footprint now supports them without starving self-serve), wavelengths, air-gap plus CJIS/HIPAA bundles, federal SKUs on ATO, the model hub marketplace, the Platinum multi-metro class, and forward capacity options. Token staked reservations remain an evaluation memo only |
| Engineering | Q9: smart-contract SLA GA (after 2 audits plus 4 clean quarters of dual-feed data); multi-region anycast GA; 99.999% measured availability published for flagship metros. Q10: micro-channels GA; confidential computing GA (fleet-wide SEV-SNP/TDX, GPU CC at hubs), unlocking healthcare, fintech, and gov premium SKUs. Q11: FedRAMP Moderate ATO (realistically around month 30 at best), putting federal SKUs on sale; distributed VPC GA; self-service interconnect. Q12: capacity-market APIs; one human per 20-50 nodes demonstrated over two consecutive audited quarters. Team of about 70-90 |
| Commercial | Our own GSA MAS award; 10+ DePIN protocols; a federal capture team of 3-4; telco white-label retail launches; quarterly price-fence integrity audits asking whether Standard is leaking into premium use cases |
| Exit criteria | A $350-550M run rate; 25%+ of revenue under multi-year commit; contracted backlog above $1B TCV; on-chain SLA attach at 30%+ of DePIN revenue; the NOD line at 20%+ of revenue without merchant starvation (under 80% sustained utilization); blended gross margin of 58-62%; zero-touch at 60% of new ARR |

---

## 10. Top risks and mitigations

| # | Risk | Mitigation |
|---|---|---|
| 1 | Multi-tenant GPU isolation at the edge (L4/L40S lack MIG; small pools mean a big blast radius) | Year 1: whole-GPU or MIG-slice tenancy only, VM isolation (Kata plus VFIO) for all untrusted tenants; fractional sharing only within one tenant's own workloads |
| 2 | Serverless cold-start economics on small pools (a 300kW node holds roughly 16-40 GPUs) | A curated 5-8 model catalog per node, metro-level warm placement so every model is warm somewhere under 2ms away, and explicit warm-pool (TTFT SLA) versus flex (cheap, cold starts allowed) tiers. Don't chase long-tail catalogs; that is a hub and aggregator game ANDD loses |
| 3 | Metering accuracy for micro-billing (lost events during partitions mean leakage or disputes) | Signed idempotent events, a local write-ahead spool with rejoin reconciliation, dual-path counting with drift alerts below 0.1%, and auditable usage exports. Under-bill on ambiguity, always |
| 4 | Oracle trust for SLA contracts ("ANDD measures ANDD" convinces nobody, and a bad feed drains the credit pool) | Two-of-two attestation (ANDD plus an independent probe vendor), capped per-epoch payouts, a dispute window, published raw data; fiat and manual first, on-chain only after 4 clean quarters |
| 5 | Backhaul diversity is often fictional at OZ sites (shared conduit), breaking latency SLAs at exactly the differentiator | Pre-signing conduit-level path verification (KMZ maps, not carrier marketing); sites failing the diversity audit sell uptime-only SKUs; mesh reroute as a third path; SLA polygons drawn from measured data |
| 6 | SKU sprawl (6 profiles times 9 product classes times 6 constituencies is a support surface a 20-person team can't GA) | The year-1 catalog is frozen; two hardware profiles until node 20; a product council runs a one-in-one-out rule until Phase 3 |
| 7 | AI-agent actuation safety (an agent that can provision, bill, and pay credits can mis-do all three at machine speed) | Agents propose; a deterministic OPA policy engine executes. Typed allow-listed actions, per-action rate and value limits, dual control above thresholds (credits over $1k), a replayable audit log, and per-agent-class kill switches. This architecture is also the FedRAMP story for autonomous ops |
| 8 | Capacity stranding from the wrong hardware mix (GPUs depreciate 30-40% per year) | Tranche ordering gated on 60%+ sustained utilization; field-convertible standardized sleds; spot plus DePIN wholesale as the demand sponge; the metro, not the node, is the sellable pool |
| 9 | DePIN revenue quality tracks token markets | Cap it near 15% of mix; stablecoin settlement always; native tokens never accepted as payment |
| 10 | FedRAMP calendar risk (ATO slips are the norm) | Compliance engineering embedded from Q1 so nothing is retrofitted; a small boundary (a gov enclave, not the whole platform); StateRAMP and SLED revenue in parallel; pursue the 20x and agency-sponsor paths simultaneously; never key revenue plans to ATO dates |

---

## 11. KPI tree (abbreviated)

North star: contracted plus consumed revenue per deployed kW ($/kW/mo).

New revenue: zero-touch ARR share (the signature metric), time to first dollar (under 1 hour self-serve), CAC payback (under 12 months blended, under 3 months PLG), anchor-book coverage per node launch, and marketplace-sourced enterprise ARR share.

Node economics: pre-commit coverage (floor 40%, target 55%), node time to first dollar (under 7 days from acceptance), fabric utilization (65%+ at maturity), and months to a 60% node cash margin (under 12).

Retention: NRR of 115-125% commercial, GRR above 92%, commit conversion of 35%+ among accounts crossing $2k/mo, an SLA credit rate under 0.5% of revenue (published, since it doubles as a trust stat), DSO under 35 days, and bad debt under 0.5%.

Mix and quality: ARR by segment and offer type, weighted contracted backlog, blended gross margin, and revenue per human FTE, the AI-native leverage metric.

| Directional mix | +12 mo | +24 mo | +36 mo |
|---|---|---|---|
| Nodes / hubs | 30-50 / 2-3 | 100-150 / 5-8 | 250-300 / 10+ |
| Run-rate revenue | $25-45M | $120-200M | $350-550M |
| Spot / PLG | 30% | 25% | 20% |
| Mid-market commits | 20% | 20% | 20% |
| Off-taker reservations / anchors | 30% | 30% | 28% |
| SLED plus federal | 10% | 15% | 22% |
| DePIN (capped near 15%) | 8% | 8% | 8% |
| Telco / wholesale | 2% | 2% | 2% |
| Zero-touch share of new ARR | 40% | 50% | 60% |
| Contracted backlog (TCV) | $60-100M | $300-500M | $1B+ |

PLG deliberately shrinks as a share while growing absolutely; it is the demand-seeding and margin-fill layer. Reserved and contracted revenue finances the node-build flywheel. Government mix grows on compliance milestones, not wishes.

---

## 12. The ten commercial rules

1. No ground-break below 40% pre-commit coverage.
2. The AI agent sells everything below $250k TCV end to end; humans advise, they don't gatekeep.
3. Publish list prices, machine-readable; never publish reservation floors.
4. Discounts buy commitment or term, and are never given without one.
5. Premium tiers are fenced by guarantees and placement rights, never by throttling the cheap tier's quality, only its certainty.
6. Stablecoin settlement for DePIN always; native tokens never as payment.
7. Every SLA is code; every credit is automatic; every performance record is public.
8. Egress stays cheap forever. It is the moat-builder against hyperscaler lock-in.
9. DePIN revenue is capped near 15% of mix; gov mix grows only as fast as certifications.
10. Every partner deal must inherit zero-touch economics or it dilutes the model.

---

*Market data as of August 2026; sources and per-claim citations are maintained in the underlying market research working paper. Pricing figures for comparables are drawn from official provider pages where available and aggregator trackers otherwise (which lag by days to weeks). This document contains forward-looking statements; directional revenue and margin figures are planning targets, not forecasts.*
