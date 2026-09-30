# ANDD Product Offering Catalog & Customer Journeys

**Author:** Senior Product Manager, ANDD
**Date:** August 2026
**Status:** v1.0 — for exec review; aligned to published company roadmap (Phase 1: mo 1–12 pilot sites → Phase 4: mo 48–72 full autonomy)
**Inputs:** ANDD Context Brief (architecture, payment rails, constituencies, hard constraints)

---

## 0. Product Philosophy & Naming System

ANDD is not selling GPUs; it is selling **proximity, sovereignty, and zero-touch operations**. Every SKU below is designed so the AI ops layer — not a sales/solutions team — can quote it, provision it, meter it, and enforce its SLA. That is the structural cost advantage (1 human per 20–50 nodes) and the experiential differentiator (minutes, not weeks, to first workload).

**Catalog hierarchy (top-level product lines):**

| Line code | Product line | One-liner |
|---|---|---|
| **AI** | ANDD Inference & AI Services | Serverless tokens → dedicated endpoints → fine-tuning |
| **CMP** | ANDD Compute | GPU-hour, VMs, containers, bare metal, spot |
| **STO** | ANDD Storage | Object/block/file, residency-pinned, backup/archive |
| **NET** | ANDD Network | Interconnect, peering, CDN/cache, wavelengths |
| **SOV** | ANDD Sovereign | Gov/compliance-bundled, cages, air-gap, survive-in-place |
| **DPN** | ANDD DePIN & Web3 | Validators, verifiable compute, programmable SLA APIs |
| **NOD** | ANDD Whole-Node | Node lease, private node, Node-as-a-Service |
| **MKT** | ANDD Marketplace | Per-call APIs, prepaid credits, spot consumer |

Naming convention: `LINE-Family-Variant` (e.g., `AI-Serverless-Std`, `NOD-NaaS-Telco`). All SKUs carry machine-readable metadata (metering unit, SLA class, residency capability, tier placement) so the AI provisioning agent and the smart-contract SLA engine can compose them without human intervention.

**Two placement tiers serve products:** Edge Nodes (T1, 200–500kW; L4/L40S/MI300X-class, sub-10ms service areas) and Regional Hubs (T2, 1–2MW; H100/H200/B200-class, compliance boundary, dense peering). Every SKU declares placement; the scheduler enforces it.

---

## 1. Product Catalog (Exhaustive)

### 1.1 AI — Inference & AI Services

#### AI-Serverless — Serverless AI Inference
- **Description:** Multi-tenant, OpenAI-compatible API (`/v1/chat/completions`, `/v1/embeddings`, `/v1/audio`, `/v1/images`) over a curated catalog of open-weight models (Llama-3.x/4 class 7B–70B, Mistral/Mixtral, Qwen, DeepSeek distills, Whisper-class ASR, SDXL-class image, embedding/reranker models). Requests routed to the nearest edge node with the model warm; 70B+ models served from hubs. Latency-aware routing is the headline feature: **sub-10ms network RTT for users inside a node's metro service area**.
- **Variants:**
  - `AI-Serverless-Std` — best-effort placement, cheapest per token.
  - `AI-Serverless-Metro` — latency-pinned to a named metro (p99 latency SLA attached).
  - `AI-Serverless-Resident` — jurisdiction-pinned (e.g., "process only in Ohio nodes"): the sovereignty-by-construction differentiator, priced at a premium.
  - `AI-Serverless-Batch` — 24h-window async batch at ~50% discount (fills idle edge capacity).
- **Segments:** spot developers, startups, fintech (fraud/RAG), DePIN apps.
- **Unit of sale / metering:** per 1M input/output tokens (LLM); per-second audio; per image; per 1k embeddings. Per-request minimum billing increment $0.000001 via payment channels (crypto) or aggregated cents (fiat).
- **Pricing model:** pure usage; price sheet per model tier (S: ≤8B, M: 9–34B, L: 35–72B, XL: hub-only frontier open weights). Batch −50%; Resident +20–30%; Metro +15%.
- **Tier:** Edge (S/M), Hub (L/XL, spillover).
- **Dependencies:** model catalog + serving stack (vLLM/SGLang-class), API gateway, metering pipeline, prepaid credits (MKT-Credits). This is the **first revenue SKU** — needs only 1 pilot site.

#### AI-Dedicated — Dedicated Inference Endpoints
- **Description:** Single-tenant model endpoint reserved on named GPUs; customer picks model (catalog or bring-your-own-weights, incl. fine-tuned LoRAs), autoscaling floor/ceiling, placement (metro, node, or "any edge in state X"). Guaranteed throughput (tokens/sec) and p99 latency SLA. Private networking (VPC peering / private interconnect) optional.
- **Variants:** `AI-Dedicated-Edge` (L40S/MI300X units, 7–34B models), `AI-Dedicated-Hub` (H100/H200/B200 units, 70B+, high-QPS), `AI-Dedicated-Confidential` (SEV-SNP/TDX attested serving — weights and prompts encrypted in use).
- **Segments:** startups in production, fintech, healthcare, gov (via SOV bundles), telcos.
- **Unit of sale:** GPU-replica-hour (min 1 hr on-demand; discounts at monthly/annual commit).
- **Metering:** GPU-replica-hours + optional per-token telemetry for chargeback.
- **Pricing:** on-demand hourly; 1-mo commit −20%; 12-mo −40%.
- **Tier:** Edge and Hub.
- **Dependencies:** AI-Serverless stack, tenant isolation (MIG/SR-IOV), BYO-weights registry with license attestation.

#### AI-Tune — Fine-Tuning & Training
- **Description:** Managed fine-tuning (SFT, DPO, LoRA/QLoRA) and small/mid-scale training jobs at hubs on H100/H200/B200 pods. Job API + conversational launcher ("tune Llama-3-8B on this S3 bucket, budget $400" → AI agent proposes recipe, cost estimate, ETA). Output weights deploy 1-click to AI-Dedicated or serve via AI-Serverless private model slot.
- **Variants:** `AI-Tune-LoRA` (per-job), `AI-Tune-Full` (per GPU-hour), `AI-Tune-Reserved` (dedicated training pod, weekly/monthly), `AI-Eval` (managed eval harness, per-run).
- **Segments:** startups, mid-market, fintech (fraud models), gov (mission models via SOV).
- **Unit of sale / metering:** per training GPU-hour; LoRA jobs flat-rate by tokens processed.
- **Pricing:** usage; reserved pods at committed rates.
- **Tier:** Hub only (training-class GPUs).
- **Dependencies:** first regional hub live (Phase 2); STO-Object for datasets; job scheduler.

### 1.2 CMP — Compute

#### CMP-GPU — GPU Capacity
- **Description:** Raw GPU access when customers want their own stack.
- **Variants:**
  - `CMP-GPU-OnDemand` — per GPU-hour, L4/L40S/MI300X at edge; H100/H200/B200 at hubs; per-minute billing.
  - `CMP-GPU-Reserved` — 1/6/12/36-mo reservations, capacity guaranteed.
  - `CMP-GPU-Spot` — preemptible edge GPUs at 60–75% off; 2-min reclaim notice; the mechanism that monetizes idle edge capacity and powers Batch pricing. Spot prices set per-node by the AI capacity agent (real supply/demand).
  - `CMP-GPU-Fractional` — MIG slices / time-sliced fractions for small workloads.
- **Segments:** startups, ML teams, DePIN compute networks, researchers.
- **Unit/metering:** GPU-minute (billed per-minute, quoted per-hour).
- **Pricing:** on-demand; reserved −30–55%; spot dynamic.
- **Tier:** Edge (inference GPUs) + Hub (training GPUs).
- **Dependencies:** virtualization/isolation layer, image service; spot requires capacity-forecasting agent.

#### CMP-Edge — Edge Compute (Containers / K8s / VMs / Bare Metal)
- **Description:** General compute at the edge with residency and latency placement.
  - `CMP-K8s` — managed Kubernetes namespaces (vCluster-style) on shared edge clusters; per-vCPU/GB-hour; the fastest path for startups.
  - `CMP-Container` — serverless containers (Cloud-Run-style): deploy an OCI image, scale-to-zero, per-100ms billing.
  - `CMP-VM` — VMs (EPYC/Xeon/Ampere ARM shapes, incl. confidential-VM variants), per-second billing.
  - `CMP-Metal` — dedicated bare-metal servers (hourly/monthly), incl. GPU-attached metal; required for telco NFV, DePIN validators wanting no hypervisor, and some compliance regimes.
- **Segments:** all; CMP-Metal skews telco/DePIN/gov.
- **Unit/metering:** vCPU-hr + GB-hr (K8s/VM); vCPU-100ms (Container); server-hour/month (Metal).
- **Pricing:** usage; monthly commit −20%; annual −35%.
- **Tier:** Edge primarily; Hub for large shapes.
- **Dependencies:** SDN/tenant networking, image registry, metering. CMP-VM/K8s are Phase-1 launchable.

### 1.3 STO — Storage

| SKU | Description | Unit of sale | Metering | Pricing | Tier | Depends on |
|---|---|---|---|---|---|---|
| `STO-Object` | S3-compatible object storage, erasure-coded across 3+ geographically distinct nodes, 11-nines durability | GB-month | GB-mo, PUT/GET ops, egress GB | Tiered $/GB-mo + ops + egress (egress cheap vs hyperscalers — a wedge) | Edge + Hub (EC spans nodes) | ≥3 nodes in region |
| `STO-Object-Resident` | Object storage with **jurisdiction-pinned placement policy** (state/county-level), policy cryptographically attested | GB-month | same | +25–40% premium | Edge | STO-Object + placement policy engine |
| `STO-Block` | NVMe block volumes for VMs/metal, 3-replica within node/metro | GB-month, IOPS tier | GB-mo, provisioned IOPS | Provisioned | Edge | CMP-VM |
| `STO-File` | POSIX NFS/SMB shares (medical imaging, media) | GB-month | GB-mo, throughput | Provisioned | Edge | STO-Block |
| `STO-Cache` | Regional read cache / dataset staging at hubs (training data, model weights) | GB-month | GB-mo + hits | Usage | Hub | Hub live |
| `STO-Archive` | Cold/archive class on HDD tier, 12h retrieval | GB-month | GB-mo + retrieval GB | ~1/5 of Object price | Storage-Dense edge nodes | Storage-Dense profile deployed |
| `STO-Backup` | Managed backup-as-a-service (VM/K8s/DB snapshots, cross-node) with residency guarantee | Protected-GB-month | protected GB | Per-protected-GB | Edge | STO-Object |

### 1.4 NET — Network & Connectivity

| SKU | Description | Segments | Unit of sale | Metering | Pricing | Tier | Depends on |
|---|---|---|---|---|---|---|---|
| `NET-Interconnect` | Private L2/L3 interconnect into a customer's premises, colo cage, or cloud (AWS DX / Azure ER / GCP on-ramp cross-connect at hubs) | fintech, telco, enterprise, gov | Port (1/10/100G) | Port-month + data | Monthly port fee | Hub (cloud on-ramps), Edge (last-mile) | Hub peering fabric |
| `NET-Peering` | Carrier-neutral peering ports at Connectivity-Hub edge nodes and hubs; public + private VLAN | telcos, ISPs, CDNs, DePIN | Port | Port-month | Monthly | Connectivity-Hub nodes | Connectivity-Hub profile |
| `NET-Wave` | Metro/regional wavelengths & dark-fiber-lit services between ANDD nodes and customer sites | telcos, gov | Wavelength (10/100G) | Circuit-month | MRC + NRC, 12–36mo | Both | Fiber build/IRU per metro |
| `NET-CDN` | Edge cache/CDN: static + streaming + **AI response cache** (semantic cache for repeated inference) | media, startups, DePIN | — | GB egress + requests | Usage | Edge | ≥10 nodes for meaningful footprint |
| `NET-Mesh-VPN` | Zero-trust private network fabric across customer's ANDD footprint (mTLS mesh, managed) | all multi-node customers | Per node-attachment | attachment-month + GB | Monthly | Both | 2+ customer locations |
| `NET-Egress` | Metered internet egress (deliberately priced ~50–70% below hyperscaler egress as an acquisition wedge) | all | GB | GB | Usage | Both | — |

### 1.5 SOV — Sovereign & Government

- `SOV-Cage` — **Dedicated secure cage/suite** inside a Government/Secure-profile edge node or hub: physically partitioned racks, customer-controlled access list, TPM/measured-boot attestation reports, video/audit trail via compliance agent. Unit: cage-month (by rack count + kW). Contracted pricing, 12–60 mo. Tier: Gov/Secure nodes + hubs. Depends: Gov/Secure hardware profile, SOC 2 (Phase 1), then FedRAMP Moderate (Phase 2).
- `SOV-Bundle-FedMod` / `SOV-Bundle-CJIS` / `SOV-Bundle-HIPAA` / `SOV-Bundle-ITAR` — **compliance-bundled SKUs**: any AI/CMP/STO SKU wrapped with the relevant control set, boundary documentation auto-generated by the compliance agent, personnel/citizenship guarantees, and continuous-monitoring feeds the customer's auditors can subscribe to. Unit: base SKU + compliance uplift (15–35%). Depends: respective authorizations (FedRAMP Mod in Phase 2; CJIS/HIPAA Phase 2–3; ITAR Phase 3).
- `SOV-AirGap` — **Air-gapped / survive-in-place node service**: a node (or cage) that runs disconnected or intermittently connected; local AI control plane operates autonomously; data never leaves site; optional SCIF-compatible enhanced build. Sells as node-month or cage-month, multi-year. Segments: defense, intelligence-adjacent, critical infrastructure, NG911 continuity. Depends: NOD-Private + Gov/Secure profile + "survive in place" control-plane feature (native to T3 design).
- `SOV-Resilience-911` — packaged **public-safety continuity**: NG911 call-processing workloads + records + local AI dispatch-assist pinned to in-county nodes with survive-in-place guarantee. Sold to counties/municipalities as annual subscription per PSAP. Depends: SOV-AirGap features + municipal reference architecture.
- `SOV-Model-Enclave` — sovereign AI inference: named open-weight models running in confidential-compute enclaves inside the compliance boundary, with attested "no data egress" reports. Uplift on AI-Dedicated. Depends: AI-Dedicated-Confidential + FedRAMP.

### 1.6 DPN — DePIN & Web3

- `DPN-Validator` — validator/RPC node hosting for major L1/L2s: bare-metal or dedicated-VM SKUs with 99.99% availability class, slashing-protection runbooks automated by ops agents, geographic distribution across ANDD mesh (anti-correlation guarantees — "no two validators in the same node/power region"). Unit: validator-month. Segments: DePIN projects, staking providers, DAOs. Tier: DePIN-Backbone edge nodes. Depends: CMP-Metal/VM + monitoring agents.
- `DPN-RPC` — managed blockchain RPC/indexer endpoints, per-request metered (pairs naturally with MKT-Credits and payment channels). Unit: 1M requests.
- `DPN-VerifiableCompute` — compute jobs with **cryptographic execution attestation** (TEE quotes from SEV-SNP/TDX, signed job receipts, optional zk-proof-friendly output commitments) so DePIN protocols can verify off-chain work done on ANDD. Unit: attested GPU-/CPU-hour, +10–20% over standard. Depends: confidential computing GA + receipt/oracle service.
- `DPN-SLA-API` — **programmable SLA-as-a-product**: API + smart contracts letting a customer (1) query live oracle-fed SLA telemetry per resource, (2) compose ANDD's SLA guarantees into their own downstream SLAs ("cascading SLAs"), (3) receive automatic stablecoin credits on breach with no claims process. Sold as a per-resource attach fee (5% of underlying SKU) + free read-only telemetry tier. Segments: DePIN (headline), fintech, enterprises with strict vendor SLAs. Depends: smart-contract SLA engine (Phase 3 GA; Phase 2 beta), oracle infrastructure, stablecoin rails.
- `DPN-Backbone` — wholesale "enterprise-grade backbone for DePIN networks": bundles CMP-Metal + NET-Peering + DPN-SLA-API + geographic-distribution scheduling for a DePIN project's own node fleet. Contracted, per-node-month. This is the "2–3 DePIN projects in Phase 2" land vehicle.
- `DPN-Channels` — payment-channel micro-transaction rails as a metering feature across all usage SKUs (fractions of a cent per request, batch settlement). Not separately priced; a payments capability that makes MKT and DPN SKUs possible. Depends: stablecoin rails (Phase 2), channels (Phase 3).
- *Note:* any network-native consensus capability is referenced only as "network-native consensus protocol (evaluating options incl. licensing partnerships)" — **not** an ANDD product line.

### 1.7 NOD — Whole-Node Products

- `NOD-Lease` — **Dedicated Edge Node Lease**: an entire 200–500kW node (existing or build-to-suit in a chosen OZ metro) leased to one customer; ANDD's AI ops layer still operates it (that's the product — "your node, zero ops staff"). Unit: node-month; 36–60-mo terms; build-to-suit carries NRC + take-or-pay. Segments: large enterprise off-takers, hyperscaler overflow, CDN/AI labs wanting metro presence.
- `NOD-Private` — private node inside customer perimeter or campus (hospital, utility, base-adjacent): ANDD deploys prefab module on customer land/power, operates remotely, survive-in-place native. Unit: node-month + deployment NRC. Segments: gov, healthcare systems, utilities.
- `NOD-NaaS-Telco` — **Node-as-a-Service for telcos**: carrier-neutral edge extension at/near CO or tower aggregation sites; telco resells ANDD compute under its brand (white-label portal + API), rev-share or wholesale node-month pricing; MEC-ready (UPF/RAN-adjacent latency). Depends: NET-Peering + multi-tenant reseller billing.
- `NOD-NaaS-Muni` — Node-as-a-Service for municipalities/communities: county sponsors an in-community node (often OZ-financed); bundle includes SOV-Resilience-911 option, smart-city workload catalog, local-hiring commitments, and community pricing for local institutions (schools, clinics). Unit: node-month, 5–10-yr municipal terms; QOF-financeable.
- `NOD-Fractional` — guaranteed fraction of a node (e.g., 25% of a node's GPU + storage, physically pinned) for customers who want dedicated-but-smaller. Unit: node-fraction-month.
- **Dependencies (all NOD):** site pipeline + prefab supply chain (60–90-day deploys), remote-ops maturity; NOD-NaaS variants need reseller/white-label billing.

### 1.8 MKT — Marketplace & Spot Consumer

- `MKT-Credits` — **Prepaid credits**: buy $5–$50k of credits by card, ACH, or USDC/USDT (Ethereum L1/L2, Solana); crypto payment → provisioning within one block confirmation. Credits are the universal currency across all usage SKUs; auto-top-up optional. Free-tier grants issue as expiring credits.
- `MKT-API-PAYG` — per-API-call consumption with **no subscription and no monthly minimum**, billed via payment channels (crypto) or credit drawdown (fiat) down to fractions of a cent. The spot-developer front door.
- `MKT-Spot-Exchange` — posted-price spot marketplace for `CMP-GPU-Spot` and off-peak `AI-Serverless-Batch`; prices set autonomously per node by the capacity agent; public price feed API (also feeds DPN-SLA-API oracles).
- `MKT-Model-Hub` — third-party model publishers list fine-tuned/specialized models served on ANDD; publisher sets per-token markup, ANDD takes 15–20% rev share. Depends: AI-Serverless + BYO-weights + payout rails. Phase 3.
- `MKT-Agent-Store` (Phase 3+) — deployable agent/workflow templates (e.g., "fraud-scoring pipeline," "RAG stack") that provision underlying SKUs in one click; rev-share with authors.

### 1.9 Cross-cutting platform features (not SKUs, but sellable attach)

| Feature | Attach | Notes |
|---|---|---|
| AI Concierge (conversational provisioning, instant quotes, cost forecasting) | Free, all tiers | The signature demo; drives conversion |
| Smart-contract SLA (auto-credit) | `DPN-SLA-API` attach fee or bundled in Enterprise+/Gov | Differentiator vs. every incumbent's claims process |
| Residency policy engine | Premium variants (`-Resident`) | Sovereignty by construction |
| Confidential computing | `-Confidential` variants, +15–25% | SEV-SNP/TDX |
| Carbon/energy telemetry + VPP participation reporting | Free reports; Phase 4 grid-services rev share | Supports OZ/ESG narratives |

---

## 2. Customer Journeys (Discovery → Signup → Consumption → Growth)

A shared spine, then per-persona specifics. **The AI-native difference, stated once:** every journey below replaces (a) sales-qualification calls with an **AI Concierge** that quotes real prices instantly, (b) manual account review with **KYC/KYB-in-minutes** (doc upload → automated verification → risk-tiered limits), (c) capacity planning meetings with **autonomous capacity negotiation** (the customer's stated need is matched against live node telemetry; the agent proposes placement + price + SLA and can commit inventory), and (d) SLA claims with **automatic credits**. Time-to-first-workload (TTFW) is a tracked product KPI per persona.

### 2a. Individual / Spot Developer
- **Discovery:** model benchmarks & price/latency leaderboards (SEO), Hacker News/X launches, OpenAI-compatible drop-in guides ("change one base URL"), latency map showing their metro, MKT-Spot-Exchange public price feed, hackathon credits.
- **Signup:** email or GitHub OAuth → instant API key with $5 free credit; **no card required for free tier**; card or USDC top-up unlocks higher rate limits (KYC-light: automated sanctions screen only). Crypto path: connect wallet, pay USDC, provisioned within one block.
- **TTFW target:** **< 3 minutes** (signup → first successful completion call).
- **Consumption:** `MKT-API-PAYG` on AI-Serverless; playground + latency dashboard showing which node served them; spot GPUs for side projects.
- **AI-native difference:** Concierge answers "cheapest way to run Llama-8B at <80ms from Columbus?" with a live quote and a copy-paste snippet; per-request micro-billing means no $50 surprise minimum.
- **Growth path:** PAYG → `MKT-Credits` auto-top-up → Starter tier when they form a team → AI-Dedicated when an app gets traction. Signals watched by the growth agent: sustained QPS, org-domain emails, model diversity.

### 2b. Startup Engineering Team
- **Discovery:** dev-community content, "egress is cheap here" comparisons, YC/accelerator credit programs ($5–25k), founder networks in OZ metros, Terraform/Pulumi providers in registries.
- **Signup:** self-serve org account; KYB-in-minutes (EIN + doc upload, automated); Startup Credits application auto-adjudicated by the onboarding agent in <1 hr.
- **TTFW target:** **< 1 day** for a production-ish deployment (K8s namespace or dedicated endpoint), **< 10 min** for first API call.
- **Consumption:** AI-Serverless → `AI-Dedicated-Edge` for their product's model; `CMP-K8s` + `STO-Object` for the app; `NET-CDN`; spot for CI/experiments.
- **AI-native difference:** conversational infra ("we need a 13B endpoint at 200 QPS in Texas, budget $3k/mo") returns three placement/price options with SLA classes; the cost-forecast agent flags projected overage at 50/75/90/100% and proposes reserved conversion with one-click savings ("switching this endpoint to 12-mo commit saves $1,340/mo").
- **Growth path:** Starter → Pro; on-demand → 12-mo commits; single metro → multi-metro latency footprint; eventually `NOD-Fractional` when they saturate shared capacity.

### 2c. Mid-Market / Regional Fintech
- **Discovery:** state banking/fintech associations, compliance-focused content ("data residency by construction," SOC 2 → FedRAMP path), core-banking vendor partnerships, regional conferences, referrals from pilot-phase design partners.
- **Signup:** hybrid — self-serve KYB (minutes) opens a sandbox immediately; production requires a light-touch contracted step (MSA + DPA e-signed; security questionnaire answered **automatically by the compliance agent** from the live controls library — hours, not weeks). NET 30 fiat billing.
- **TTFW target:** sandbox **same day**; production fraud-scoring workload **< 2 weeks** (vs. 3–6 months at incumbents, mostly their own change-management).
- **Consumption:** `AI-Serverless-Resident` and `AI-Dedicated-Confidential` for fraud/risk models (<50ms budget), `STO-Object-Resident`, `NET-Interconnect` into their core processor, `STO-Backup`. SLA class Gold with p99 latency SLA in-metro.
- **AI-native difference:** continuous compliance reporting feed (auditor-subscribable), residency attestations per object/inference, and the smart-contract SLA (auto-credit) removing vendor-management overhead; instant quotes let their procurement compare against cloud line-by-line.
- **Growth path:** one metro → all operating states (`-Resident` in each); add AI-Tune for custom fraud models at hub; multi-year committed-use agreement; candidate for `NOD-Fractional`/`NOD-Lease` at scale.

### 2d. Commercial Off-Taker (Large Enterprise / Telco Capacity Commitments)
- **Discovery:** direct BD + exec network, capacity-shortage narrative (grid-constrained hyperscaler regions), carrier-neutrality pitch to telcos, infra analysts, co-build conversations with fiber/power partners.
- **Signup:** contracted — but radically compressed: the **autonomous capacity-negotiation agent** produces a binding term sheet (sites, kW, GPU mix, delivery dates, take-or-pay schedule, pricing curve) from live inventory + build pipeline in **days**; humans handle legal review and relationship. Multi-year MSA, NET 45–60, annual = 15–20% discount per payment architecture.
- **TTFW target:** existing-node capacity live **< 30 days** from signature; build-to-suit nodes in **60–90 days** (prefab).
- **Consumption:** `NOD-Lease` / `NOD-NaaS-Telco`, `CMP-GPU-Reserved` blocks, `NET-Wave` + `NET-Peering`, white-label portal (telco).
- **AI-native difference:** the off-taker gets a real-time capacity book (delivered vs. contracted, utilization, forward availability) and can flex ±15% quarter-to-quarter via the negotiation agent without an amendment cycle; SLA credits settle automatically.
- **Growth path:** 2-node pilot → metro cluster → statewide footprint; telcos expand from wholesale to white-label MEC retail; option-to-expand rights priced into capacity blocks.

### 2e. Government Agency (State & Federal)
- **Discovery:** state CIO/NASCIO channels, public-safety associations (NG911), cooperative purchasing vehicles (NASPO, GSA schedules once listed), primes/SI partnerships, OZ/economic-development narrative with legislators, FedRAMP Marketplace listing (Phase 2+).
- **Signup:** fully contracted per procurement regs (RFP/RFI, sole-source justifications where applicable, multi-year). ANDD's compression play: the **compliance agent auto-generates** SSPs, control matrices, and continuous-monitoring artifacts, cutting ATO timelines; pilot vehicles (OTAs, state pilot programs) for Phase 2 entry.
- **TTFW target:** pilot enclave **< 60 days** post-award; ATO-dependent production per authorization timeline.
- **Consumption:** `SOV-Bundle-FedMod/CJIS`, `SOV-Cage`, `SOV-AirGap`, `SOV-Model-Enclave`, `SOV-Resilience-911` (state/local), `NOD-Private` on gov campuses.
- **AI-native difference:** continuous compliance telemetry instead of annual audit theater; survive-in-place autonomy as a mission-assurance feature no hyperscaler region offers; sovereign inference with attested no-egress.
- **Growth path:** county PSAP pilot → statewide NG911 continuity → state agency AI enclave → federal (Phase 3) via FedRAMP Mod and prime partnerships.

### 2f. DePIN Project
- **Discovery:** crypto-native channels (governance forums, ETH/Solana conferences, DePIN researcher networks), the public smart-contract SLA registry itself (on-chain discoverability), integrations/co-marketing with L2s, `MKT-Spot-Exchange` price feed consumed by their protocols.
- **Signup:** self-serve with wallet-based auth + KYB for the foundation/labs entity (minutes, automated); pay in USDC/USDT; provisioning within one block confirmation. Larger backbone deals via `DPN-Backbone` contract, still agent-quoted.
- **TTFW target:** first validator or attested-compute job **< 1 hour**.
- **Consumption:** `DPN-Validator` (geo-anti-correlated), `DPN-RPC`, `DPN-VerifiableCompute`, `DPN-SLA-API` (cascading SLAs into their own token-holder commitments), `CMP-Metal`, payment channels for per-request settlement.
- **AI-native difference:** machine-consumable everything — price feeds, SLA oracles, provisioning API — lets their protocol treat ANDD as a composable primitive; auto-credit SLAs match their trust-minimized ethos; anti-correlation placement is a scheduler feature nobody else sells.
- **Growth path:** 5 validators → protocol backbone (50–500 nodes' worth of workloads) → their end-users consuming ANDD inference via the project's app → co-developed `MKT-Model-Hub`/agent listings.

### 2g. Municipality / Community
- **Discovery:** OZ economic-development channels, state broadband/digital-equity offices, county associations, public-safety grant consultants, local press from pilot-site groundbreakings ("jobs + resilience + AI in your county").
- **Signup:** contracted (council approval, sometimes bond/QOF financing); ANDD provides a standard municipal package (model ordinance language, grant-application support drafted by the AI concierge, QOF structure). Timeline governed by public process, not ANDD.
- **TTFW target:** from executed agreement, node live in **90 days** (prefab); first public-safety workload same week as node-live.
- **Consumption:** `NOD-NaaS-Muni` anchor; `SOV-Resilience-911`; smart-city workloads (traffic/video analytics on AI-Serverless-Metro); community rates for schools/clinics/local startups on the same node; `STO-Object-Resident` for county records.
- **AI-native difference:** a county of 80k people cannot staff a datacenter — AI ops is the *only* model where an in-community node is viable; the community dashboard (uptime, local jobs, local workloads served, energy telemetry) is auto-published.
- **Growth path:** one node → county cluster → regional consortium (multi-county shared hub); municipality becomes a channel: local businesses onboard self-serve onto "their" node.

---

## 3. Packaging & Tiers

### 3.1 Free tier & trial
- **Free (permanent):** $5/mo equivalent in expiring credits usable on AI-Serverless-Std + MKT-API-PAYG; 1 K8s sandbox namespace (0.5 vCPU / 1GB, scale-to-zero); 10GB STO-Object; community support; hard-capped (no card, no overage possible). Purpose: developer top-of-funnel; near-zero marginal cost on idle edge capacity.
- **Trial (14-day, card or KYB on file):** $500 credits across all self-serve SKUs incl. one AI-Dedicated-Edge replica and spot GPUs; converts automatically to Starter unless cancelled. Startup/accelerator program: $5k–$25k credits, 12-mo expiry, auto-adjudicated.
- **Gov/Enterprise pilots:** paid pilots by design ($10–50k fixed-scope), because free pilots don't test procurement; credits applied to first-year commit on conversion.

### 3.2 Tier definitions

| | **Free** | **Starter** | **Pro** | **Enterprise** | **Gov** |
|---|---|---|---|---|---|
| Base price | $0 | $49/mo | $499/mo | Custom annual (min ~$60k/yr) | Contract vehicle |
| Included allocation (credits usable on any usage SKU) | $5 expiring | $60 | $650 | Negotiated pool | Negotiated |
| Rate limits (Serverless) | 20 RPM | 600 RPM | 6,000 RPM | Custom | Custom |
| SKU access | AI-Serverless, PAYG, sandbox | + CMP-K8s/VM/Container, STO, Spot, CDN | + AI-Dedicated, AI-Tune, Reserved, Interconnect, DPN self-serve | + NOD, NET-Wave, DPN-Backbone, custom SLAs, white-label | + all SOV SKUs |
| SLA class (default) | None (best effort) | Bronze 99.9% | Silver 99.95% | Gold 99.99% (Platinum optional) | Gold/Platinum + contractual |
| Smart-contract SLA (auto-credit) | — | Optional attach | Optional attach | **Included** | Included where permitted |
| Residency pinning | — | Metro | State | State/county + attestation | Full sovereign controls |
| Support | Community + AI Concierge | AI Concierge + 24h email | AI + 4h human, 24/7 sev-1 | TAM-lite (human) + 1h sev-1 | Cleared personnel options, 15-min sev-1 |
| Billing | Prepaid only | Monthly CC/ACH, NET 30 | Monthly/annual ACH/wire | Annual, NET 45–60 | Per procurement, multi-year |
| Crypto payments | USDC prepaid | ✓ | ✓ + payment channels | ✓ | Fiat only (typically) |

*(Tier fee is a platform fee that unlocks limits/SLA/support; consumption is metered on top. Annual prepay = 15–20% discount on platform fee and committed usage, per the established payment architecture.)*

### 3.3 Overage mechanics
- Base allocations draw down first; overage meters at list rates. AI billing agent alerts at **50/75/90/100%** with one-click actions: raise cap, buy credit pack (−5–10% vs list), convert to commit.
- Customer-set **hard caps** (default ON for Free/Starter): workloads throttle or scale-to-zero rather than surprise-bill. Pro+ defaults to soft caps with anomaly detection (the billing agent auto-freezes runaway spend patterns pending confirmation — "your batch job would cost $18k, confirm to proceed").
- Spot has no overage concept (prepaid credits or channels only).

### 3.4 Committed-use discounts (CUDs)

| Commitment | Discount vs on-demand | Notes |
|---|---|---|
| 1-mo rolling | 15–20% | Auto-suggested by billing agent |
| 12-mo | 30–40% | Resource-flexible within a SKU family (e.g., any edge GPU) |
| 36-mo | 45–55% | Convertible 1x/yr across families (e.g., GPU→inference tokens) |
| Spend-based (Enterprise) | 10–35% tiered on annual committed $ | Applies across the whole catalog |

CUDs are **fungible by design** (commit dollars, not specific hardware) — the scheduler monetizes flexibility, so ANDD can afford fungibility incumbents charge for.

### 3.5 Capacity reservation products for off-takers

| Product | Structure | Term | Pricing mechanics |
|---|---|---|---|
| **Capacity Block** | Reserved kW + GPU-mix block at named node(s)/metro (e.g., 250kW, 64×L40S-equiv) | 12–60 mo | Fixed $/kW-mo + usage at deep discount; ±15% quarterly flex via negotiation agent |
| **Take-or-Pay** | Minimum monthly consumption floor across catalog | 24–60 mo | Floor billed regardless; consumption above floor at CUD rates; shortfall banked 1 quarter |
| **Build-to-Suit (NOD-Lease/Private)** | New node deployed for customer | 36–120 mo | NRC + node-month; take-or-pay floor covers financing; OZ/QOF structures can lower effective cost |
| **Forward Capacity Options** | Option to call capacity at future date/price (powers telco/DePIN planning) | 6–36 mo | Option premium (3–8% of strike), tradeable back to ANDD |
| **Staked Reservation (future)** | Capacity reservation via network utility token staking | TBD | Contemplated only; subject to regulatory analysis (Phase 3+ evaluation) |

---

## 4. SLA Product Matrix

### 4.1 SLA classes

| Class | Availability (monthly) | Scope | Typical SKUs |
|---|---|---|---|
| Best-effort | none | — | Free tier, Spot, Batch |
| **Bronze** | 99.9% | single node | Starter default; CMP on-demand; STO-Block single-metro |
| **Silver** | 99.95% | node + auto-failover in metro | Pro default; AI-Serverless-Metro; CMP-K8s; NET-CDN |
| **Gold** | 99.99% | multi-node metro (2+ nodes) | AI-Dedicated, DPN-Validator, STO-Object, NET-Interconnect, Enterprise default |
| **Platinum** | 99.999% | multi-node multi-metro (3+ nodes, mesh-routed) | SOV bundles, SOV-Resilience-911, NOD-Lease option, DPN-Backbone |

### 4.2 Dimension → SKU attachment

| SLA dimension | Metric | Attaches to | Standard targets |
|---|---|---|---|
| **Availability** | Successful-minutes / total | All non-spot SKUs | Per class above |
| **Latency (metro)** | p99 network+queue ms within named metro service area | AI-Serverless-Metro/Resident, AI-Dedicated, CMP-Container, NET-CDN | p99 ≤ 10ms network RTT in-metro; p99 TTFT ≤ 200ms (S/M models), ≤ 350ms (L) |
| **Inference latency** | p99 ms/token (inter-token) | AI-Dedicated | ≤ 25ms/token (S), ≤ 50ms (M), ≤ 80ms (L) per model-tier spec |
| **Throughput** | Guaranteed tokens/sec (aggregate) or QPS floor | AI-Dedicated, AI-Tune-Reserved | Contracted per endpoint (e.g., 10k tok/s floor) |
| **Durability** | Annual object durability | STO-Object/-Resident/Archive/Backup | 11 nines (EC across 3+ geo-distinct nodes); Block 5 nines |
| **Data residency** | % of bytes/inferences inside declared boundary | All `-Resident`, SOV | 100% — breach triggers max credit tier + incident report |
| **Recovery** | RPO/RTO | STO-Backup, SOV-AirGap | RPO ≤ 15 min / RTO ≤ 4 h (standard); ≤ 1 h RTO (Platinum) |
| **Support response** | Sev-1 first response | Tier-based | Starter 24h / Pro 1–4h / Ent 1h / Gov 15 min |
| **Delivery (capacity)** | Contracted go-live date | NOD, Capacity Blocks | Liquidated-damages schedule per contract |

### 4.3 Credit schedules (monthly, % of affected resource's monthly charge)

**Availability:**

| Monthly uptime shortfall | Bronze (99.9) | Silver (99.95) | Gold (99.99) | Platinum (99.999) |
|---|---|---|---|---|
| Below target → −0.05% | 10% | 10% | 15% | 25% |
| Further −0.5% band | 25% | 25% | 30% | 50% |
| < 99.0% | 50% | 50% | 60% | 100% |
| < 95.0% | 100% | 100% | 100% | 100% |

**Latency/throughput:** any hour where p99 exceeds target ≥ 20% = "breach-hour"; credits = 5% per breach-hour up to 30%/mo (Gold), 50%/mo (Platinum). **Durability:** any confirmed data loss on STO-Object = 100% credit of 12 months' storage fees for affected data + incident RCA (durability is engineered-to-never; the credit signals confidence). **Residency:** any confirmed boundary violation = 100% monthly credit + notification within 24h.

### 4.4 The differentiated product: smart-contract SLA (auto-credit)
- Every SLA above exists in two enforcement modes: **classic** (measured by ANDD, credited on invoice, no claims form — already better than incumbents' "customer must file within 30 days") and **programmable** (`DPN-SLA-API`): SLA terms encoded in an on-chain contract, telemetry fed by oracles from ANDD's monitoring plane (and optionally third-party probes), **stablecoin credits stream automatically and proportionally on breach — no claims process, no dispute window**.
- Composable/cascading: a DePIN project or SaaS vendor can reference ANDD's SLA contract inside its own customer SLA contracts, transferring credits downstream automatically. No incumbent offers this.
- Packaging: included in Enterprise/Gov (classic mode telemetry always; on-chain where customer opts in); 5%-of-resource attach fee for Starter/Pro; free read-only telemetry API for all (marketing surface: public, verifiable uptime).
- Phasing: classic auto-credit from Phase 1 (it's just honest billing); oracle telemetry beta Phase 2; on-chain auto-credit GA Phase 3 per roadmap.

---

## 5. Prioritization & Launch Waves

### 5.1 Method
RICE-lite scoring: **Reach** (segments served × funnel width), **Impact** (revenue + strategic learning), **Confidence**, **Effort** (eng + hardware footprint + compliance prerequisite). Overriding Phase-1 principle: *maximize revenue and learning per kW deployed* — with only 3–5 pilot sites (≈1–2.5MW total), we cannot sell big blocks; we must sell **high-margin, thin-slice, self-serve usage** and **a small number of anchor contracts that finance sites**.

### 5.2 Scoring summary (5 = best; Effort inverted so higher = cheaper)

| SKU family | Reach | Impact | Conf | Effort⁻¹ | Score | Wave |
|---|---|---|---|---|---|---|
| AI-Serverless (+MKT-Credits, PAYG) | 5 | 5 | 5 | 4 | **500** | 1 |
| CMP-GPU-OnDemand/Fractional | 4 | 4 | 5 | 4 | 320 | 1 |
| CMP-K8s/VM/Container | 4 | 3 | 5 | 3 | 180 | 1 |
| STO-Object (+Resident) | 4 | 4 | 4 | 3 | 192 | 1 |
| AI-Dedicated-Edge | 3 | 5 | 5 | 4 | 300 | 1 |
| NOD-NaaS-Muni + SOV-Resilience-911 (pilot form) | 2 | 5 | 3 | 2 | 60* | 1 (1–2 anchors) |
| CMP-GPU-Spot + MKT-Spot-Exchange | 4 | 4 | 4 | 3 | 192 | 2 |
| DPN-Validator/RPC/Backbone | 3 | 4 | 4 | 3 | 144 | 2 |
| AI-Tune (hub) | 3 | 4 | 4 | 2 | 96 | 2 (needs hub) |
| NET-Interconnect/Peering/CDN | 3 | 4 | 4 | 2 | 96 | 2 |
| STO-Block/File/Backup/Archive | 3 | 3 | 4 | 3 | 108 | 2 |
| SOV-Bundle-FedMod/CJIS + SOV-Cage | 2 | 5 | 3 | 1 | 30* | 2–3 (gated on FedRAMP) |
| NOD-Lease / NaaS-Telco / Fractional | 2 | 5 | 3 | 2 | 60* | 3 |
| DPN-SLA-API (on-chain) + DPN-Channels + VerifiableCompute | 3 | 5 | 3 | 2 | 90 | 3 |
| NET-Wave, MKT-Model-Hub, Agent-Store, SOV-AirGap/ITAR | 2 | 4 | 3 | 1 | 24 | 3–4 |

\* Low arithmetic score but **strategic anchors**: they finance sites, create references, and unlock roadmap milestones (first gov customer, first DePIN projects) — promoted deliberately.

### 5.3 Launch waves

**Wave 1 — Phase 1 (months 1–12, 3–5 pilot sites): "Sell tokens, prove ops."**
Launch: `AI-Serverless` (Std/Metro/Batch; Resident-lite at metro level), `MKT-Credits` + `MKT-API-PAYG` (fiat first; USDC prepaid fast-follow), `AI-Dedicated-Edge`, `CMP-GPU-OnDemand/Fractional`, `CMP-K8s/VM`, `STO-Object` (once ≥3 nodes give geo-EC; single-metro replication before that, labeled honestly), Free/Starter/Pro tiers, classic auto-credit SLAs (Bronze/Silver/Gold), AI Concierge v1 (quote + provision + billing alerts). Plus **1–2 anchor contracts**: one `NOD-NaaS-Muni`+`SOV-Resilience-911` pilot county and one design-partner fintech on `AI-Serverless-Resident` — these are the "beta customers in 3+ segments" milestone and the OZ/QOF story.
*Rationale:* inference tokens are the highest revenue-per-kW, fully self-serve product with the shortest TTFW; it exercises the entire AI ops loop (onboarding → routing → metering → SLA) on real traffic — exactly the learning Phase 1 exists to buy. Everything here runs on inference-GPU edge nodes; nothing requires a hub, FedRAMP, or big fiber builds.

**Wave 2 — Phase 2 (months 12–24, 20–50 nodes + 2–3 hubs): "Add depth, land segments."**
Launch: `AI-Tune` + `STO-Cache` (hubs arrive), `CMP-GPU-Spot` + `MKT-Spot-Exchange` (needs fleet scale for a real spot market), full `STO` family, `NET-Interconnect/Peering/CDN` (hub on-ramps + 20+ node CDN footprint), `DPN-Validator/RPC/Backbone` with 2–3 flagship DePIN projects (roadmap milestone), stablecoin rails GA + oracle telemetry beta for SLAs, `SOV-Bundle-FedMod` + `SOV-Cage` as FedRAMP Moderate lands, first state/local production gov (expanding the Wave-1 muni pilot), Enterprise tier + CUDs + first Capacity Blocks, Gov tier.
*Rationale:* hubs unlock training-class and peering products; fleet scale unlocks spot economics and CDN credibility; FedRAMP unlocks SOV monetization of the compliance investment.

**Wave 3 — Phase 3 (months 24–48, 100–300 nodes, 10+ hubs): "Differentiate and lock in."**
Launch: on-chain `DPN-SLA-API` GA + `DPN-Channels` micro-transactions (roadmap: smart-contract SLAs live), `DPN-VerifiableCompute`, `NOD-Lease`/`NOD-NaaS-Telco`/`NOD-Fractional` (footprint now supports whole-node sales without starving self-serve), `NET-Wave`, `SOV-AirGap` + CJIS/HIPAA bundles + federal customers, `MKT-Model-Hub`, Platinum multi-metro SLA, Forward Capacity Options, token-based staked reservations **evaluation only**.
*Rationale:* these are the moat products — they require scale (multi-metro Platinum, spot depth, telco NaaS) or authorizations (federal) that only now exist; launching them earlier would over-promise.

**Wave 4 — Phase 4 (months 48+):** `MKT-Agent-Store`, VPP/grid-services revenue share reporting productized, international packaging planning, deeper white-label.

### 5.4 What we deliberately do NOT launch early
- **No training clusters in Phase 1** (no hub hardware; the market there is brutal on price anyway).
- **No FedRAMP-branded SKUs before authorization** — compliance agent sells the *path* (SOC 2 Type I evidence) honestly.
- **No token products** — contemplated only, pending regulatory analysis; nothing customer-facing until Phase 3 evaluation completes.
- **No whole-node leases in Phase 1** except the strategic muni anchor — selling 20–50% of a 5-node fleet to one tenant would kill the self-serve learning loop the whole company depends on.

### 5.5 KPIs per wave (product health)
- **W1:** TTFW p50 <3 min (dev) / <10 min (startup); ≥60% of edge GPU-hours monetized; ≥3 segments with paying logos; token gross margin ≥55%; zero-touch rate ≥90% of signups needing no human.
- **W2:** net revenue retention ≥130% self-serve; spot clearing ≥70% of idle hours; 2–3 DePIN backbones live; first $1M+ TCV gov + capacity-block contracts; AI ops autonomy >90% (roadmap).
- **W3:** ≥25% of revenue under multi-year commit; on-chain SLA attach ≥30% of DePIN revenue; ≥10 DePIN projects; NOD line ≥20% revenue without self-serve capacity starvation (<80% sustained utilization target).

---

## Appendix A — SKU quick-reference (unit & meter cheat sheet)

| SKU | Unit of sale | Meter | Pricing | Tier |
|---|---|---|---|---|
| AI-Serverless-* | 1M tokens / req / sec-audio / image | tokens, requests | usage (±variant modifiers) | Edge (S/M), Hub (L/XL) |
| AI-Dedicated-* | GPU-replica-hour | replica-hours | on-demand / commit −20/−40% | Edge + Hub |
| AI-Tune-* | GPU-hour or per-job | GPU-hrs, tokens processed | usage / reserved | Hub |
| CMP-GPU-* | GPU-hour (min-billed) | GPU-minutes | on-demand / reserved / spot | Edge + Hub |
| CMP-K8s / VM / Container | vCPU+GB-hour; vCPU-100ms | resource-seconds | usage / commit | Edge |
| CMP-Metal | server-hour/month | server-time | monthly | Edge + Hub |
| STO-* | GB-month | GB-mo, ops, egress, retrieval | tiered usage | per family |
| NET-Interconnect/Peering/Wave | port / circuit | port-month + GB | MRC (+NRC) | Hub + Conn-Hub nodes |
| NET-CDN / Egress | — | GB + requests | usage | Edge |
| SOV-Cage / AirGap | cage- / node-month | contracted | multi-year | Gov/Secure sites |
| SOV-Bundles | uplift on base SKU | base meter | +15–35% | boundary sites |
| DPN-Validator / RPC | validator-month / 1M req | uptime, requests | monthly / usage | DePIN-Backbone nodes |
| DPN-SLA-API | attach | resources covered | 5% of underlying | control plane |
| NOD-* | node(-fraction)-month | contracted | 36–120 mo, NRC options | whole sites |
| MKT-Credits / PAYG | $ credits / per call | drawdown / per-request | prepaid / channels | all |

*End of deliverable.*
