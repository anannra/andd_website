# ANDD Engineering Build Plan
**Prepared by: VP Engineering / Chief Architect**
**Date: August 2026**
**Status: Internal — feasibility-graded build plan aligned to published company phases**

---

## 0. Framing and ground rules

This document translates ANDD's product ambitions into an engineering plan with explicit build-vs-buy calls, honest SLA math, a sequenced 36-month roadmap, a risk register, and the minimal public interface surface. Three principles govern everything below:

1. **We are a platform company that owns datacenters, not a datacenter company that dabbles in software.** The differentiated IP is the AI control plane, the metering/settlement pipeline, and the mesh scheduler. Everything else — hypervisors, object storage engines, billing rating engines, KYC — should be OSS or vendor unless it touches our moat.
2. **Never sell an SLA the physics can't back.** SLA tiers are gated on node count per metro, not on marketing calendars. The gating table in Section 2 is a hard release criterion.
3. **AI-operated does not mean AI-invented.** Every AI-agent actuation path (provisioning, billing, SLA credits) runs through a deterministic policy engine with typed, audited, reversible actions. The agent proposes; the policy layer disposes. This is the only way to pass SOC 2/FedRAMP audits with autonomous ops.

Effort units: **team-quarters (TQ)** = one squad of ~5 engineers for one quarter. Estimates include design, build, test, and productionization to "sellable" quality — roughly 2× a naive prototype estimate.

---

## 1. Platform Capability Map

### 1.1 Serverless inference gateway (per-token, OpenAI-compatible)

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| OpenAI-compatible API front door | **OSS + build** | vLLM's OpenAI server per node; our own gateway (Envoy + custom Go/Rust control plane) for auth, quotas, routing. Do NOT hand-roll the model server. | 2 TQ |
| Model serving runtime | **OSS** | vLLM (primary, NVIDIA + ROCm), SGLang for structured output, TensorRT-LLM only where perf justifies the ops burden. llama.cpp variants are not production-grade for us. | 1 TQ (integration/hardening) |
| Model catalog & registry | **Build (thin)** | Postgres + object store of weights; per-node model placement manifest; signed weights (cosign). Buying nothing here — it's small and central to routing. | 1 TQ |
| Multi-node inference routing | **BUILD — core IP** | Latency-aware, capacity-aware router: anycast/GeoDNS to nearest healthy node, spill to metro peer <2ms away, spill to hub for 70B-class. This is where "sub-10ms service area" becomes real. | 3 TQ initial, ongoing |
| Token metering | **BUILD — core IP** | Usage events emitted by the serving layer (prompt/completion tokens, model, tenant, node), signed at source, streamed to metering pipeline (§1.4). Accuracy is a revenue-integrity problem — see Risk R3. | 1.5 TQ (shared with §1.4) |
| Cold-start / model residency mgmt | **Build** | Weight caching on local NVMe, predictive pre-warm from traffic forecasts (the one place early "AI ops" earns its keep), scale-to-zero policies per node class. | 2 TQ |

**Feasibility: HIGH.** This is a well-trodden path in 2026 (Together, Fireworks, Groq all proved the category). Our twist — routing across many small pools instead of one big pool — is the hard 20%. **Total: ~10 TQ.**

### 1.2 Dedicated endpoints & GPU orchestration

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Cluster substrate | **OSS** | Kubernetes (k3s/RKE2 at edge nodes for footprint; full k8s at hubs), Cluster API for fleet lifecycle, GitOps (Flux/Argo) for config. One cluster per site, fleet-managed. | 2 TQ |
| GPU partitioning | **OSS + vendor** | NVIDIA GPU Operator, MIG on supported SKUs, time-slicing/vGPU (licensed) for L4/L40S (no MIG — plan accordingly); AMD MI300X partitioning via ROCm SR-IOV. HAMi or Nebuly-style soft isolation as stopgap only for trusted tiers. | 2 TQ |
| VM-grade isolation for untrusted multi-tenant | **OSS** | Kata Containers / cloud-hypervisor with VFIO GPU passthrough for tenant boundaries; plain namespaces only for single-tenant dedicated SKUs. | 2 TQ |
| Scheduler / quota / spot & preemption | **BUILD on OSS** | Kueue + Volcano as base; our fleet-level "global scheduler" (Tier 3 control plane) does placement across sites; local schedulers own the node. Preemption tiers: reserved > on-demand > spot; spot is how we monetize stranded capacity (Risk R10). | 3 TQ |
| Fleet provisioning / bare metal | **OSS** | Tinkerbell or Metal³ + our prefab site bring-up automation ("node-in-a-box" image, TPM-attested first boot). | 2 TQ |

**Feasibility: HIGH,** with one asterisk: secure multi-tenant GPU sharing at the edge is genuinely hard (Risk R1). Year-1 answer: dedicated-GPU tenancy only (whole GPU or MIG slice with VM isolation); no fractional soft-sharing for untrusted tenants. **Total: ~11 TQ.**

### 1.3 Tenant portal + AI onboarding agent

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Portal (console) | **Build (standard)** | Next.js console: org/project/API-key model, usage dashboards, spend alerts. Table stakes, no magic. | 2 TQ |
| Identity | **Buy** | WorkOS or Auth0 for SSO/SAML/SCIM; Keycloak self-hosted becomes mandatory inside the FedRAMP boundary later. | 0.5 TQ |
| KYC/KYB | **Buy** | Persona or Alloy (individuals + business verification), Chainalysis/TRM for crypto-payer screening (OFAC). Never build. | 0.5 TQ |
| AI onboarding agent | **BUILD — differentiator** | Conversational signup that ends in a provisioned, billable tenant in minutes. Architecture: LLM agent with a **typed tool belt** (create_org, run_kyb, quote_capacity, provision_endpoint, set_budget), every action gated by the policy engine, human-escalation path for KYB edge cases. | 3 TQ |
| Policy/actuation engine | **BUILD — core IP** | OPA-based deterministic guardrails: what an agent may do, limits, dual-control thresholds, full audit log. Shared by onboarding, billing, and SLA agents. This is the "AI-native ops" keystone. | 3 TQ |

**Feasibility: HIGH for the portal, MEDIUM for the agent** — instant provisioning is easy for serverless keys, harder for dedicated capacity (inventory checks). Ship "instant serverless, <1hr dedicated" and be honest about it. **Total: ~9 TQ.**

### 1.4 Metering & billing pipeline

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Usage event collection | **BUILD** | Signed usage events at source (gateway, kubelet device plugin, Ceph), local write-ahead spool (survive-in-place: nodes buffer usage during partitions and reconcile), Kafka/Redpanda into hubs. | 2 TQ |
| Metering/aggregation | **OSS + build** | OpenMeter or ClickHouse-based aggregation; exactly-once-ish semantics via idempotent event IDs; dual-path reconciliation (real-time stream vs. hourly batch recount) to bound drift. | 2 TQ |
| Rating & invoicing | **Buy** | Metronome or Orb for rating/invoicing/price-plans; Stripe Billing acceptable at pilot scale but will not survive our SKU complexity. Building a rating engine is a classic startup death march — don't. | 1 TQ (integration) |
| Fiat settlement | **Buy** | Stripe (CC/ACH), Modern Treasury for wires/NET-terms enterprise flows. | 0.5 TQ |
| Stablecoin settlement | **Build on vendor rails** | Coinbase Prime/Circle for custody+offramp; our own smart contracts for payment→provisioning trigger (watch USDC transfer, credit tenant within one confirmation); Solana + Base as first chains (cheap, fast finality). | 2 TQ |
| Micro-transaction channels | **BUILD — Phase 3** | State-channel style per-request debits with periodic on-chain batch settlement. Defer until DePIN demand proves out; design the metering event schema now so channels bolt on. | 3 TQ (Phase 3) |

**Feasibility: HIGH for fiat path, MEDIUM for channels.** The critical insight: **metering pipeline v1 is on the critical path for every consumption product** — it ships before serverless GA or we're giving compute away. **Total: ~10.5 TQ (7.5 pre-Phase-3).**

### 1.5 SLA measurement & smart-contract credit system

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Measurement plane | **BUILD** | Synthetic probes (external: Catchpoint/ThousandEyes buy; internal: our probe mesh between nodes), per-tenant real-user p99 from gateway telemetry, both feeding an SLA ledger (immutable, append-only). | 2 TQ |
| SLA Guardian agent | **BUILD — differentiator** | Watches error budgets per tenant SLO, triggers remediation (reroute, failover, pre-warm) *before* breach, files credit computation on breach. Actuation via policy engine only. | 2 TQ |
| Oracle layer | **Build + partner** | Publish signed SLA measurements on-chain via our own attestation feed **plus** a third-party verifier (Chainlink Functions or an independent probe vendor co-signing) — a two-of-two design so credits don't rest on "trust ANDD's own numbers" (Risk R4). | 2 TQ |
| Credit smart contracts | **Build (audited)** | Simple, boring Solidity/Anchor: escrowed credit pool per contract, proportional payout formula, dispute window. External audit mandatory (2 firms). Composability = standardized breach-event schema DePIN customers can subscribe to. | 2 TQ + audits |

**Feasibility: MEDIUM.** Nothing here is technically exotic; the risk is legal/regulatory (auto-paying credits in stablecoin) and oracle trust. Phase it: internal SLA ledger + manual fiat credits (Phase 1) → dashboard-verifiable automated fiat credits (Phase 2) → on-chain automated stablecoin credits (Phase 3). **Total: ~8 TQ.**

### 1.6 Storage products

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Object/block/file engine | **OSS** | Ceph (RGW for S3, RBD block, CephFS) as the one engine — resist running MinIO *and* Ceph; two storage stacks is an ops tax we can't afford at 1 human/20 nodes. | 2 TQ |
| Multi-tenant hardening | **Build** | RGW tenant isolation, per-tenant encryption keys (KMS-integrated, tenant-managed-key option for gov/fintech), QoS/IOPS caps per tenant, noisy-neighbor throttling. | 2 TQ |
| Cross-node erasure coding | **Build on Ceph** | Stretch/multi-site EC across 3+ nodes within a metro mesh (<2ms makes synchronous EC feasible — this is a genuine edge differentiator); async replication between metros. 11-nines claim requires ≥3 sites per placement group — gate the durability SKU on site count. | 2 TQ |
| Residency policy engine | **BUILD — differentiator** | Declarative placement policy per tenant/bucket ("data never leaves Ohio", "US-persons-only sites"), enforced at placement time and continuously audited; produces compliance evidence automatically. Nobody sells this well today. | 2 TQ |

**Feasibility: HIGH** (Ceph is mature) but operationally heavy — Ceph at 100 sites with minimal humans demands serious automation investment (rolled into AI-ops). **Total: ~8 TQ.**

### 1.7 Network products

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Mesh fabric | **OSS + build** | WireGuard/IPsec mesh with SR/SD-WAN overlay (VPP/FRR based), BGP to upstreams, anycast announcement automation. | 2 TQ |
| Automated peering | **Build (thin)** | PeeringDB integration, automated BGP session config + RPKI, IX presence at hubs. "Automated" year-1 means templated-and-reviewed, not fully autonomous. | 1.5 TQ |
| Private interconnect provisioning | **Buy + build** | Megaport/PacketFabric APIs for virtual cross-connects to customer sites and cloud on-ramps; our portal orchestrates. Physical cross-connects at hubs stay a ticketed process year 1–2. | 1.5 TQ |
| Tenant networking | **OSS** | Cilium (eBPF, network policy, egress control), per-tenant VPC-like abstraction across the mesh (this "distributed VPC" is a Phase 2–3 product, not MVP). | 2 TQ (Phase 2) |

**Feasibility: HIGH for connectivity basics, MEDIUM for distributed VPC.** **Total: ~7 TQ.**

### 1.8 Gov/compliance stack

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Compliance automation | **Buy** | Vanta/Drata for SOC 2; Paramify or RegScale for FedRAMP OSCAL SSP tooling. | 0.5 TQ |
| FedRAMP boundary | **Build (architecture)** | Dedicated enclave at 1–2 hubs + designated Gov-profile edge nodes; separate control plane instance inside boundary; FIPS-validated crypto everywhere in-boundary; US-persons ops. Target **FedRAMP Moderate via agency sponsorship or 20x pilot pathway**; 18–24 months realistic from start to ATO. | 4 TQ + program mgmt |
| Audit tooling / evidence | **Build on OSS** | Continuous-compliance evidence pipeline (OSQuery, Falco, our config attestation) feeding OSCAL artifacts; the AI compliance-reporting agent drafts, humans sign. | 2 TQ |
| Air-gap / survive-in-place mode | **Build** | Already an architecture requirement (Tier 3 "survive in place"); gov air-gap mode = that plus offline update path (signed bundles), local identity, deferred billing reconciliation. | 2 TQ |
| Confidential computing | **OSS + vendor** | SEV-SNP/TDX VM attestation (Kata + attestation service), NVIDIA Hopper/Blackwell CC-mode for GPU confidentiality at hubs. GA this only when hardware fleet supports it uniformly — Phase 3. | 3 TQ (Phase 3) |

**Feasibility: MEDIUM — the constraint is program/audit calendar, not code.** No gov SKU revenue before ATO; sell "FedRAMP-in-process + state/local (StateRAMP, CJIS-adjacent)" in Phase 2. **Total: ~11.5 TQ.**

### 1.9 DePIN APIs

| Component | Build/Buy/OSS | Choice & rationale | Effort |
|---|---|---|---|
| Verifiable compute attestations | **BUILD — differentiator** | TPM/measured-boot chain + workload attestation (what ran, where, when) signed per node; published as verifiable claims DePIN protocols can consume. TEE-backed where hardware allows. Not full zkML — attestation-based ("trusted-hardware proofs"), stated honestly. | 3 TQ |
| Programmatic settlement API | **Build** | Streaming usage → per-epoch settlement objects → stablecoin payout/charge; webhook + on-chain event parity. | 2 TQ |
| Capacity market primitives | **Build (Phase 3)** | Reserve/auction APIs for third-party protocols to buy guaranteed capacity; composable SLA pass-through (§1.5). | 2 TQ (Phase 3) |

**Feasibility: MEDIUM.** Small market today but strategically aligned; keep it thin and schema-first. **Total: ~7 TQ (5 in Phase 2–3).**

### 1.10 Capability map summary

| Capability | Verdict | Pre-GA effort | Differentiator? |
|---|---|---|---|
| Inference gateway | Build core, OSS serving | 10 TQ | Routing across mesh = yes |
| GPU orchestration | OSS-heavy | 11 TQ | No (table stakes) |
| Portal + AI onboarding | Build agent + policy engine | 9 TQ | **Yes — flagship** |
| Metering/billing | Build collection, buy rating | 10.5 TQ | Partially (crypto rails) |
| SLA + smart contracts | Build, phased | 8 TQ | **Yes** |
| Storage | Ceph + residency engine | 8 TQ | Residency engine = yes |
| Network | OSS + thin build | 7 TQ | Metro mesh = yes |
| Gov/compliance | Program-driven | 11.5 TQ | Yes (with ATO) |
| DePIN APIs | Thin build | 7 TQ | Yes (niche) |

**Grand total ≈ 82 TQ over 36 months** → sustained average of ~7 squads (~35 platform engineers) at steady state, ramping from ~3 squads in year 1. That is consistent with the team plan in Section 3.

---

## 2. SLA Engineering Reality Check

### 2.1 What the physics and math allow

Availability compounds from power, network, hardware, and software. For a **single edge node** (sub-2MW, prefab, N+1 UPS/genset, 10–100G backhaul, likely 2 carriers at best):

| Layer | Realistic availability (single edge node) |
|---|---|
| Utility power + N+1 UPS/genset | 99.98% |
| Backhaul (dual-carrier, shared conduit risk in OZ locations) | 99.95–99.98% |
| Hardware (GPU/server failures, small pool = big blast radius) | 99.95% |
| Platform software + maintenance | 99.95% |
| **Compound** | **≈99.85–99.9%** |

**Honest single-node ceiling: 99.9% monthly (43.8 min/mo error budget).** Anyone promising 99.99% from one small site with one genset is lying or lucky. Rural/OZ backhaul variability makes the network line the dominant risk (Risk R5).

| Topology | Promisable uptime SLA | Error budget | Preconditions |
|---|---|---|---|
| Single edge node | **99.9%** | 43.8 min/mo | N+1 power, dual backhaul, spare parts on site |
| Metro pair (2 nodes <2ms) | **99.99%** | 4.4 min/mo | Automated failover <30s, synchronous state where needed, independent power feeds/carriers verified (not just assumed) |
| Metro mesh 3+ nodes, anycast | **99.99% contractual, 99.999% engineering target** | 26 s/mo at 5-nines | BGP anycast with fast withdrawal, capacity headroom ≥ N-1 (one node's full load absorbable), tested (chaos-drilled) quarterly |
| Hub-backed region | 99.99% | — | Hub adds capacity depth, not a magic availability tier |

**Do not contract 99.999%.** Sell it as a measured, published achievement ("trailing 12-month measured availability"), contract at 99.99%. Five-nines contractually requires operational maturity we won't have before year 3+, and one bad BGP day erases a year of budget.

**Correlated-failure caveat:** metro math above assumes independence. Two nodes fed by the same substation, same carrier conduit, or same software rollout are not independent. Engineering requirement: **diversity audit per metro pair** (power feed, carrier path via traceroute+contract verification, staggered software rollout waves) before the 99.99% SKU is enabled for that metro.

### 2.2 Latency SLAs

Latency is our headline differentiator, so measure it like we mean it:

- **What we promise:** p99 network RTT from defined eligibility zones (customer must be within a published service polygon) to the serving node — e.g., "p99 ≤ 10ms RTT within service area." For inference, separately: **TTFT p99 per model class** (e.g., ≤150ms for 7–13B chat on L40S) — never a blended "AI latency" number.
- **Methodology:** (1) synthetic probe mesh — probes in-region (3rd-party vantage points: Catchpoint/ThousandEyes + RIPE Atlas corroboration) hitting every node every 10s; (2) per-tenant real-user telemetry at the gateway (server-side timestamping, exported to tenant dashboards); (3) monthly SLA computation uses **real-tenant p99 primary, synthetic as fallback** when tenant volume is too low for stable p99 (<10k requests/mo → synthetic governs).
- **Third-party verification:** the SLA ledger is co-signed by an independent probe vendor; both feeds go to the oracle (§1.5). Publish methodology publicly on the status page — auditable SLAs are a sales weapon against hyperscalers' vague ones.
- **Exclusions, stated plainly:** last-mile beyond our service polygon, tenant client-side stalls, DDoS events beyond mitigation capacity (with mitigation SLO stated separately), model cold-starts on scale-to-zero tiers (or price the no-cold-start tier explicitly).

### 2.3 Year-1 vs Year-3 promises

| | Year 1 (pilot, 3–5 sites) | Year 2 | Year 3 (100+ nodes) |
|---|---|---|---|
| Uptime | 99.9% single-site; **beta terms** (service credits capped at 1 month fees) | 99.99% in metros with verified pairs; 99.9% elsewhere | 99.99% standard; 99.999% *measured & published*, not contracted |
| Latency | Published targets, monitored, **not credited** | p99 latency SLA with credits in mesh metros | Full latency SLA portfolio incl. TTFT per model class |
| Credits | Manual, fiat, human-approved | Automated fiat credits, dashboard-verifiable | Smart-contract stablecoin credits, oracle-fed |
| Maintenance | Weekly window (Tue 02:00–06:00 local), excluded from SLA | Monthly window, rolling zero-downtime updates in mesh metros (maintenance no longer excluded there) | No-exclusion SLAs in mesh metros — maintenance inside the error budget |

### 2.4 Error budgets and the AI SLA Guardian

- Every SKU has an internal SLO **one notch tighter** than the contractual SLA (contract 99.99% → internal SLO 99.995%), so the Guardian acts before money is owed.
- **Guardian enforcement loop:** consume budget-burn-rate alerts (multi-window: 5m/1h/6h) → automated actions in escalating order: shift anycast weight away from degrading node → pre-warm capacity at peer → drain and failover → open incident + page the (few) humans. All actions typed, policy-gated, logged; the Guardian can *spend* error budget (e.g., proceed with a risky rollout) only below 25% budget consumption.
- **Release gating:** if a metro's monthly budget is >75% consumed, the Guardian freezes non-security rollouts there automatically. This rule is what makes 1-human-per-20-nodes survivable.
- Budget accounting is per-tenant-SKU, not just per-node — a node can be "up" while one tenant's endpoint breaches; tenant-level SLIs are the billable truth.

---

## 3. Sequenced Engineering Roadmap (12 / 24 / 36 months)

### Phase alignment recap
- **Mo 1–12:** 3–5 pilot sites, SOC 2 Type I, beta customers in 3+ segments.
- **Mo 12–24:** 20–50 nodes, 2–3 hubs, >90% AI ops autonomy, fiat+stablecoin rails, FedRAMP Moderate *in process*.
- **Mo 24–36:** 100+ nodes, smart-contract SLAs live, micro-channels, federal pipeline.

### 3.1 Months 1–12 — "Make it real" (3–5 pilot sites)

**Platform milestones (in dependency order):**

| Quarter | Milestone | Gate/dependency |
|---|---|---|
| Q1 | Fleet substrate v1: site bring-up automation, k8s per site, GitOps fleet mgmt, observability (Prometheus/Grafana/Loki + fleet rollup) | First pilot site powered |
| Q1–Q2 | **Metering pipeline v1** (signed events → aggregation → Metronome/Orb → Stripe) | **Blocks all consumption GA** |
| Q2 | Inference gateway **beta**: OpenAI-compatible, 5–8 curated models (7–13B + embeddings + Whisper-class), single-node routing | Metering v1 |
| Q2 | Portal v1 + manual-assisted onboarding; policy/actuation engine v0 (audit-everything) | — |
| Q3 | **Serverless inference GA** with per-token billing; dedicated GPU endpoints GA (whole-GPU/MIG, K8s-native) | Metering v1 + billing GA |
| Q3 | Storage beta: S3-compatible object, single-site + async replica; residency policy v0 (site pinning) | ≥2 sites live |
| Q4 | AI onboarding agent GA (instant serverless signup); AI ops agents v1 (predictive maintenance advisory, auto-remediation for a whitelist of runbooks) | Policy engine v1 |
| Q4 | Status/SLA transparency page public; internal SLA ledger; 99.9% SLA contractual on all GA SKUs | Probe mesh live |
| Q4 | SOC 2 Type I complete; FedRAMP program kickoff (SSP drafting, boundary design) | — |

**Explicitly NOT in year 1:** smart-contract credits, micro-channels, confidential computing GA, distributed VPC, marketplace listings, fine-tuning service, >2 hardware profiles per product line (see Risk R6).

**Team: ~18–24 engineers** — Fleet/Infra squad (5), Inference/Serving squad (5), Billing/Metering squad (4), Portal/Agents squad (4), Security/Compliance (2–3), SRE embedded (2–3). One VP Eng, one principal architect, tech-lead-heavy hiring.

**Critical path:** site bring-up → metering v1 → serverless GA. If metering slips, everything consumption-priced slips.

### 3.2 Months 12–24 — "Make it repeatable" (20–50 nodes, 2–3 hubs)

| Quarter | Milestone | Gate/dependency |
|---|---|---|
| Q5 | Hub platform live: 70B-class serving, training-class dedicated clusters (H200/B200) as **reserved SKUs** | First hub energized |
| Q5 | Stablecoin payment rail GA (USDC on Base + Solana; pay → provision in one confirmation) | Custody vendor + compliance sign-off |
| Q5–Q6 | **Metro-pair failover GA → 99.99% SLA** in qualifying metros | ≥2 diversity-audited nodes per metro; chaos drills passed |
| Q6 | Multi-site erasure-coded storage GA (3-node EC, durability SKU); residency policy engine GA with audit evidence | ≥3 nodes per region |
| Q6 | Automated fiat SLA credits (no claims process, dashboard-verifiable) | SLA ledger + 2 quarters of clean measurement |
| Q7 | DePIN API beta: attestations v1 + programmatic settlement, 2–3 design partners | Stablecoin rail |
| Q7 | AI ops autonomy >90%: closed-loop remediation for top-20 runbooks, capacity forecasting, Guardian enforcing error budgets fleet-wide | Policy engine maturity + 12 months of incident data |
| Q8 | Fine-tuning service beta (LoRA on hub GPUs, deploy-to-edge pipeline); marketplace groundwork (AWS/Azure marketplace listings for resell) | Hub capacity |
| Q8 | FedRAMP Moderate: boundary implemented, 3PAO assessment underway; StateRAMP/state-local sales enabled | Agency sponsor secured |
| Q8 | Anycast across 3+ node metros (beta) — engineering toward 99.999% measured | ≥3 nodes in ≥2 metros |

**Team: ~40–55 engineers** — add Storage squad, Network squad, Gov/Compliance squad, Data/ML-ops squad; SRE org formalized (follow-the-sun eventually, but year-2 is US-hours + Guardian coverage). First dedicated PM org (3–4 PMs).

**Critical path:** hub energization → 70B/fine-tuning; metro density → 99.99% SKU; FedRAMP boundary → any federal revenue (18–24 mo from kickoff → ATO lands early Phase 3 at best).

### 3.3 Months 24–36 — "Make it a network" (100+ nodes)

| Quarter | Milestone | Gate/dependency |
|---|---|---|
| Q9 | **Smart-contract SLA GA**: oracle-fed, dual-attested, automatic stablecoin credits; composable breach-event feed for DePIN customers | 2 external audits; legal opinion on auto-settlement; 4 quarters of dual-feed SLA data |
| Q9 | Multi-region anycast GA; 99.999% *measured* availability published for flagship metros | 3+ nodes × 5+ metros, chaos program mature |
| Q10 | Micro-transaction channels GA (per-request stablecoin debits, batch settlement) | Smart-contract SLA infra + DePIN demand validated |
| Q10 | **Confidential computing GA** (SEV-SNP/TDX VMs fleet-wide; GPU CC at hubs) — unlocks healthcare/fintech/gov premium SKUs | Uniform CC-capable hardware at hubs |
| Q11 | FedRAMP Moderate **ATO** → federal SKUs on sale; CJIS/HIPAA attestations on gov/health profiles; air-gap mode GA for enhanced sites | ATO granted |
| Q11 | Distributed VPC GA (tenant private networks spanning mesh); private interconnect self-service (Megaport-integrated) | Cilium mesh maturity |
| Q12 | Capacity market APIs (reservation auctions, third-party pass-through SLAs); token evaluation *analysis only* per roadmap | Regulatory review |
| Q12 | AI ops at target ratio: 1 human per 20–50 nodes demonstrated over 2 consecutive quarters with SLA attainment ≥ contract | Autonomy metrics audited |

**Team: ~70–90 engineers** (~12–14 squads). Growth concentrated in SRE/fleet automation (the ratio target is an engineering deliverable, not an ops wish) and solutions engineering for gov/fintech.

### 3.4 Cross-phase dependency ladder (the rules we will not break)

1. No consumption-priced SKU before **metering v1** (mo ~6).
2. No 99.99% contract in a metro before **2 diversity-audited nodes + passed failover drill** in that metro.
3. No federal SKU before **ATO** (realistically mo 30+). State/local under StateRAMP earlier.
4. No smart-contract credits before **2 audits + 4 quarters of dual-attested SLA data**.
5. No fractional GPU sharing for untrusted tenants before **VM-grade isolation GA**.
6. No 5-nines contracts, period, in this plan horizon.
7. No token launch work — evaluation memo only, per published roadmap.

---

## 4. Technical Risks & Mitigations (Top 10)

| # | Risk | Why it bites | Mitigation |
|---|---|---|---|
| R1 | **Multi-tenant GPU isolation at the edge.** L4/L40S lack MIG; time-slicing leaks side-channels and QoS; a noisy or malicious tenant on a shared GPU at a 4-GPU site is a big blast radius. | Security incident or SLA cascade on tiny pools | Year 1: whole-GPU or MIG-slice tenancy only, VM isolation (Kata+VFIO) for all untrusted tenants; fractional sharing only within a single tenant's own workloads. Revisit with Blackwell-gen MIG at edge refresh. |
| R2 | **Cold-start economics of serverless on small GPU pools.** A 300kW node holds ~16–40 GPUs; keeping 10 models warm strands capacity, scale-to-zero kills TTFT. | Serverless gross margin or latency SLA, pick one | Curated small catalog per node (5–8 models), traffic-forecast pre-warming, metro-level model placement (each model warm somewhere <2ms away), explicit pricing tiers: "warm-pool" (premium, TTFT SLA) vs "flex" (cheap, cold-start allowed). Don't chase long-tail model catalogs — that's a hub/aggregator game we lose. |
| R3 | **Metering accuracy for micro-billing.** Fractions-of-a-cent billing with lost events during partitions = revenue leakage or customer disputes; both are trust killers. | Revenue integrity + DePIN credibility | Signed idempotent events, local WAL spool with reconciliation on rejoin, dual-path (stream vs batch) counting with <0.1% drift alerting, monthly third-party-auditable usage exports to tenants. Under-bill on ambiguity, always. |
| R4 | **Oracle trust for SLA smart contracts.** "ANDD measures ANDD and pays itself" convinces nobody; a bad feed auto-drains the credit pool. | Product credibility + direct financial loss | Dual attestation (our feed + independent probe vendor co-sign), capped per-epoch payout, dispute window before settlement finality, publish raw measurement data. Start fiat/manual, graduate to on-chain only after 4 clean quarters. |
| R5 | **Backhaul variability breaking latency SLAs.** OZ sites skew rural/underserved; carrier diversity is often fictional (shared conduit), microwave/FWA backup adds jitter. | Latency SLA breaches concentrated at exactly our differentiator | Pre-signing site survey includes independent path verification (KMZ-level conduit maps, not carrier marketing); minimum 2 physically diverse paths or the site sells uptime-only SKUs (no latency SLA); mesh reroute via adjacent node as third path; latency SLA polygons drawn from measured data, not radius circles. |
| R6 | **Too many SKUs too early.** 6 hardware profiles × 9 product classes × 6 constituencies = a combinatorial support surface a 20-person team cannot GA. | Everything ships at beta quality; nothing is sellable | Year-1 catalog frozen at: serverless inference, dedicated GPU, object storage, colo-style dedicated node. Two hardware profiles procured (General Purpose, AI Inference Heavy) until node 20. Product council owns a one-in-one-out rule until Phase 3. |
| R7 | **AI-agent actuation safety (billing/provisioning/SLA).** An agent that can provision, bill, and pay credits can also mis-provision, mis-bill, and drain funds — at machine speed. | Financial loss, audit failure, headline risk | All actuation through the typed policy engine: allow-listed actions, per-action rate & value limits, dual-control above thresholds (e.g., credits >$1k), full replayable audit log, kill-switch per agent class, chaos-testing of agent failure modes. Agents draft; deterministic code executes. This is also our FedRAMP story for autonomous ops. |
| R8 | **Capacity stranding from wrong hardware mix.** GPUs bought for demand that shows up elsewhere (or not at all); edge sites can't be re-racked cheaply; GPU generations depreciate ~30–40%/yr. | Cash death by idle silicon | Order in tranches gated on utilization (>60% sustained triggers next tranche); standardized sleds so profiles are field-convertible; spot/preemptible tier + DePIN wholesale as demand sponge for stranded capacity; scheduler treats the whole metro (not the node) as the sellable pool. |
| R9 | **Distributed control plane complexity (BFT across hubs, survive-in-place).** Split-brain during partitions → double-provisioning, billing divergence, or fleet-wide bad rollout. | Correctness bugs that only appear at scale/partition | Year 1: boring primary/standby control plane (single logical brain, regional read replicas); BFT-style multi-hub consensus introduced in Phase 2 behind the same APIs; partition behavior contract per subsystem (provisioning: fail closed; serving: fail open; billing: spool locally); Jepsen-style partition test suite in CI from day one. |
| R10 | **FedRAMP/compliance calendar risk.** ATO slips are the norm (sponsor churn, 3PAO findings); revenue plans keyed to ATO dates fail. | Phase 3 federal revenue slips 2–4 quarters | Compliance engineering embedded from Q1 (evidence pipeline, FIPS crypto, boundary-aware architecture so nothing is retrofitted); pursue StateRAMP/state-local revenue that doesn't need ATO; treat 20x/agency-sponsor paths in parallel; keep the boundary small (gov enclave, not whole platform). |

---

## 5. Interface Contracts

Minimal public surface — every API below is versioned, and nothing else is public until it has a deprecation policy.

| Interface | Contract | Compatibility commitment |
|---|---|---|
| **Inference API** | `POST /v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/audio/*` — OpenAI-compatible wire format, plus ANDD extensions under `x-andd-*` headers/namespaced fields only (e.g., `x-andd-region-pin`, `x-andd-residency`). | **OpenAI-compat is a hard contract**: we track the OpenAI spec; extensions never break drop-in clients. Model deprecations: 6-month notice, aliased successor. |
| **Capacity API** | `andd.v1` REST+gRPC: sites, offers (GPU type, region, price), reservations, dedicated endpoints; K8s-native option — CRDs (`GPUPool`, `Endpoint`, `ResidencyPolicy`) + cluster-API-style lifecycle for BYO-cluster tenants. | K8s objects follow K8s deprecation conventions (GA CRDs supported ≥12 mo after successor). REST: `v1` stable, additive-only; breaking → `v2` with 12-mo overlap. |
| **Storage API** | S3-compatible endpoint (RGW), documented compatibility matrix (we do not claim 100% S3 — we publish exactly which operations are supported, as MinIO/Ceph do); block via CSI; residency policy attached at bucket/volume creation. | **S3-compat is a hard contract** for the documented subset; residency policy schema versioned independently (`residency.v1`). |
| **Billing/Usage API** | `GET /v1/usage` (line-item events, hourly rollups, exportable raw), `GET /v1/invoices`, budgets/alerts CRUD, price-sheet endpoint (machine-readable pricing — DePIN customers demand this). Signed usage exports for third-party audit. | Additive-only within v1; usage event schema (`usage-event.v1`) is the shared spine of billing, DePIN settlement, and SLA credits — changes gated by internal schema review board. |
| **Status/SLA transparency page** | Public: per-metro measured availability (trailing 30d/12mo), latency percentiles per service polygon, incident history, maintenance calendar, **published SLA measurement methodology**, and the raw signed SLA ledger feed (JSON + on-chain pointer once live). | Methodology changes announced 90 days ahead; historical data never restated silently. |
| **DePIN settlement API** | `settlement.v1`: usage attestations (signed, TPM-rooted), per-epoch settlement objects, webhook + on-chain event parity, SLA breach-event stream (composable pass-through), stablecoin payout instructions. | Attestation format versioned with dual-publish overlap ≥2 epochs; on-chain contract upgrades via timelocked proxy with published audit. |

**Versioning & compatibility policy (uniform):**
1. **Three anchors, never ours to break:** OpenAI wire format, S3 semantics (documented subset), Kubernetes API conventions. We conform; we do not fork.
2. All ANDD-native APIs: URL-versioned major (`/v1/`), additive-only minors, 12-month minimum deprecation window with `Sunset` headers and dashboard notices.
3. One shared schema registry (usage events, attestation claims, SLA breach events) — these schemas are contracts between our own subsystems *and* customers; a single review board owns them.
4. SDKs (Python/TS/Go) generated from OpenAPI/proto, published same-day as API changes; the OpenAI-compatible surface needs no SDK — that's the point.

---

## 6. Bottom line

The plan is feasible with disciplined sequencing: ~82 team-quarters of platform work over 36 months, a team ramping 20 → 50 → 85 engineers, and hard gates tying every SLA and SKU promise to physical network density and audit calendars. The moats worth building by hand are five: the mesh-aware inference router, the policy-gated AI actuation engine, the residency policy engine, the signed metering/attestation spine, and the dual-attested SLA ledger. Everything else we assemble from Kubernetes, Ceph, vLLM, and bought billing/KYC rails — and we say no, loudly and often, to SKU sprawl until the fleet earns it.
