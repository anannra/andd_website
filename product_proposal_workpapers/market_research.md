# ANDD Market Comparables Analysis: Edge AI Compute, DePIN, and Sovereign Infrastructure

**Prepared:** August 2026 | **Analyst role:** Market research for ANDD product offering design
**Method:** Live web research (August 2026). Every price/SLA claim carries a source URL and, where the data predates mid-2026, an as-of date. Aggregator-sourced numbers (pricing trackers) are flagged as such; official-page numbers are noted.

---

## 1. Edge AI Inference / GPU Cloud Comparables

### 1.1 Serverless per-token inference (the "API tier")

This is the most price-transparent, most deflationary segment. All providers below are self-serve signup (credit card, prepaid credits or postpaid billing), typically with a free tier.

| Provider | Representative per-token pricing (per 1M tokens, in/out) | Product forms | Billing mechanics | SLA | Onboarding |
|---|---|---|---|---|---|
| **Together AI** | DeepSeek V4 Flash $0.14/$0.28; Llama 3.3 70B $1.04/$1.04; Qwen3.5 9B $0.17/$0.25; DeepSeek R1 ~$3.00/$7.00 | Serverless per-token; dedicated endpoints ($5.49/hr H100, $8.99/hr B200); GPU clusters ($3.99/hr H100 on-demand, $3.19–$7.99 reserved); provisioned-throughput units (~$0.05/PTU-min); batch at discount; fine-tuning $0.48–$8.00/1M training tokens | Usage-based, prepaid credits for self-serve; invoicing for enterprise | Enterprise SLA negotiated; no strong public uptime % on self-serve | Fully self-serve; sales for reserved clusters |
| **Fireworks AI** | Llama 3.1 8B $0.15 in; Llama 3.1 405B up to $3.00 out; size-tiered: dense >16B $0.90/MTok flat; MoE ≤176B $1.20/MTok flat. Three serving tiers (Standard / Priority / Fast 100+ tok/s), each with own rate | Serverless; dedicated GPU endpoints: H100 & H200 $7.00/hr, B200 $10.00/hr, B300 $12.00/hr, billed per GPU-second; batch at 50% of serverless; cached-input discounts | Postpaid usage + enterprise contracts; "Fire Pass" prepaid product launched Jul 2026 | **Published 99.9% uptime SLA** on inference API | Self-serve; enterprise tier via sales |
| **Groq** | $0.05–$3.00/1M tokens; Llama 3.1 8B $0.05 in; Llama 3.3 70B $0.59/$0.79; Kimi K2 ~$1.00 | Per-token only on GroqCloud (LPU hardware, 280–1,000 tok/s); batch API −50%; prompt caching −50% on repeated prefixes; enterprise dedicated instances via sales | Prepaid credits self-serve; enterprise invoicing | No public numeric SLA on self-serve; enterprise negotiated | Self-serve, generous free tier |
| **Cerebras** | GPT-OSS-120B $0.35/$0.75; ZAI-GLM-4.7 $2.25/$2.75; reserved capacity $0.25–$0.60/MTok for volume batch | Per-token pay-as-you-go (new in 2025–26); reserved capacity contracts; wafer-scale dedicated systems via sales | Prepaid/pay-per-token; 1M free tokens/day free tier | Enterprise negotiated | Self-serve free tier is the funnel |
| **SambaNova** | Llama 3.1 8B $0.10/$0.20; range free–$4.50/MTok (as of May 2026); largest models ~$6/MTok out | Managed inference API on RDU hardware; dedicated rack deals via sales | Usage-based | Enterprise negotiated | Self-serve API; racks via sales |
| **Cloudflare Workers AI** | Neuron-based: $0.011/1,000 Neurons after 10k/day free. Llama 3.1 70B ≈ 26,668 N/M input + 204,805 N/M output ≈ **$0.29 in / $2.25 out per 1M tokens**; Mistral 7B ≈ $0.11/$0.19 | Serverless at 200+ edge cities; bundled with Workers/CDN platform; pricing revamp to per-task units announced | Postpaid on Cloudflare account | Cloudflare enterprise SLA applies at platform level; no per-inference latency SLA | Fully self-serve |

Sources: [Together AI official pricing](https://www.together.ai/pricing) (fetched Aug 2026); [CloudZero Together guide](https://www.cloudzero.com/blog/together-ai-pricing/); [Morph Fireworks pricing](https://www.morphllm.com/fireworks-ai-pricing); [UsagePricing Fireworks](https://www.usagepricing.com/blueprint/fireworks-ai); [eesel Groq pricing](https://www.eesel.ai/blog/groq-pricing); [costbench Groq](https://costbench.com/software/llm-api-providers/groq/); [Cerebras pricing](https://www.cerebras.ai/pricing); [pricepertoken Cerebras](https://pricepertoken.com/endpoints/cerebras); [pricepertoken SambaNova](https://pricepertoken.com/endpoints/sambanova); [eesel SambaNova](https://www.eesel.ai/blog/sambanova-cloud-pricing); [Cloudflare Workers AI pricing docs](https://developers.cloudflare.com/workers-ai/platform/pricing/); [pricepertoken Cloudflare](https://pricepertoken.com/endpoints/cloudflare); [Fireworks SLA / GMI SLA comparison](https://www.gmicloud.ai/en/blog/most-reliable-inference-provider-sla).

**Key observations for ANDD:**
- **7–13B-class models — ANDD's edge sweet spot — now clear at $0.05–$0.30/1M tokens.** Nobody pays a premium for raw tokens on commodity open models; the premium attaches to *speed tiers* (Fireworks "Fast" 100+ tok/s, Groq/Cerebras speed positioning), *priority under load*, and *dedicated/isolated capacity*.
- **The industry has converged on a 3-tier menu:** (1) serverless per-token, (2) dedicated endpoint per-GPU-hour, (3) reserved cluster with committed-term discount. ANDD's offering should mirror this shape to be legible to buyers.
- **Batch −50% is now standard** (Groq, Fireworks, Together, Anthropic/OpenAI all do it). Cached-input discounts are standard. Any ANDD serverless product without these looks dated.
- **No serverless provider sells latency-by-geography.** Pricing is identical whether the request is served 5ms or 80ms away. This is ANDD's structural opening.

### 1.2 GPU-hour rental and dedicated capacity (the "infrastructure tier")

| Provider | H100 $/GPU-hr | H200 | B200 | Other | Billing | SLA / notes |
|---|---|---|---|---|---|---|
| **RunPod** | $2.89 (PCIe, Secure Cloud); $3.19 NVL; serverless H100 ≈$4.55/hr-equivalent | $4.39 | $5.89 (B300 $7.39) | Serverless flex $0.58–$9.98/hr-equivalent per class; per-second billing | Prepaid credits, per-second | No formal published uptime SLA; Community Cloud cheaper but unpublished rates |
| **Lambda** | $3.99 SXM ($3.29 PCIe); cluster reserved $5.54–$6.16 (1-Click Clusters incl. fabric) | — | $6.69 on-demand; $8.87–$9.86 in 1-Click Clusters | 1–3 yr reserved saves ~$0.86/hr/H100 | Per-minute, postpaid; no egress fees; no spot | **No numeric public SLA in cloud ToS** (as of mid-2026) |
| **CoreWeave** | $4.25 PCIe; $6.15–$6.16 HGX (8-GPU nodes) | $6.31 (8-GPU bundles only) | GB200 ≈$10.50/GPU-hr (from $42/hr NVL node ÷4) | Kubernetes-native; reserved contracts dominate revenue | Enterprise contracts | 99% **rack-level** uptime with penalties on GB200 NVL72 — negotiated, not published |
| **Nebius** | $2.15 on-demand ($3.85 premium tier) | $2.45 ($4.50 premium) | — | Aggressive pricing, EU+US regions | Self-serve + sales | ~99.9% typical claim (aggregator) |
| **Crusoe** | Specialty-cloud median ~$7.00/hr basket (aggregator; direct rate is sales-quoted) | — | — | Energy-first DCs (stranded gas/renewables) | Sales-led | Enterprise negotiated |
| **Vast.ai** | **from $0.90/hr** (marketplace, unverified hosts) | — | — | Configs from $0.02/hr; interruptible auctions | Prepaid credits | None. Marketplace: no security perimeter, unsuitable for regulated/user-facing prod |
| **Fluidstack** | base rates $0.50–$1.50/hr (older cards) → sales-quoted for large H100 blocks | — | — | Aggregates DC capacity for 100+ GPU deals; targets $10k+/mo teams | Contract | Uptime claims contractual |
| **Baseten** | $6.50/hr (per-replica; per-minute rates published, e.g., H100 $0.10833/min) | — | $9.98/hr | L4 $0.8484/hr, A10G $1.21/hr; autoscaling replicas | Per-minute per active replica | **99.99% claim** (active-active); enterprise SLA contracts |
| **Modal** | ≈$3.95/hr **only while executing** (per-second billing, scale-to-zero) | — | — | True usage-based serverless containers | Per-second, prepaid credits | Enterprise tier SLA |
| **Replicate** | $5.49/hr ($0.001525/s) | — | — | L40S $3.51/hr ($0.000975/s); A100 80GB $5.04/hr; billed only for active processing | Per-second, postpaid CC | No formal SLA on public models |

Sources: [RunPod pricing](https://www.runpod.io/pricing); [Spheron RunPod H100](https://www.spheron.network/blog/runpod-h100-pricing-2026/); [Spheron Lambda H100](https://www.spheron.network/blog/lambda-cloud-h100-pricing-2026/); [costbench Lambda](https://costbench.com/software/ai-gpu-cloud/lambda-labs/); [Thunder Compute CoreWeave guide, Aug 2026](https://www.thundercompute.com/blog/coreweave-gpu-pricing-review); [Spheron CoreWeave](https://www.spheron.network/blog/coreweave-h100-h200-pricing-2026/); [Nebius official prices](https://nebius.com/prices); [Spheron GPU comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/); [GPUnex Vast.ai review](https://www.gpunex.com/blog/vast-ai-review-2026/); [gpuperhour Fluidstack vs Vast](https://gpuperhour.com/compare/fluidstack-vs-vastai); [Blaxel Modal pricing](https://blaxel.ai/blog/modal-pricing-alternatives-guide); [UsagePricing Baseten](https://www.usagepricing.com/blueprint/baseten); [Replicate pricing](https://replicate.com/pricing); [Spheron SLA guide](https://www.spheron.network/blog/gpu-cloud-sla-guarantees-2026/).

**Key observations:**
- **H100 on-demand band in mid-2026: $2.15 (Nebius) → $6.16 (CoreWeave HGX)**, with marketplace floors at $0.90–$1.50 (Vast, io.net). L40S-class — ANDD Tier 1's workhorse — rents for **$0.90–$3.51/hr** depending on trust tier (Vultr low end, Replicate serverless high end). This gives ANDD a wide corridor: an L40S at an ANDD edge node priced at $1.75–$2.50/hr is credible if paired with locality + SLA value.
- **SLA reality check: the GPU-cloud mid-market largely does NOT publish numeric SLAs.** Lambda's ToS has no numeric uptime; RunPod has none; CoreWeave's 99% rack-level penalty terms are negotiated. Only the platform layer (Baseten 99.99%, Fireworks 99.9%) and hyperscalers publish. **ANDD's programmable, automatically-paying smart-contract SLA is genuinely differentiated — nobody in this table auto-pays credits without a claims process.**
- Billing mechanics cluster into: per-second/per-minute metering (RunPod, Modal, Replicate, Fireworks dedicated), prepaid credit wallets (RunPod, Modal, Groq, Vast), and committed-term reserved (everyone, 15–45% discounts, e.g., Together clusters $3.99→$3.19).
- **Newer edge-inference entrants exist but are tiny** — e.g., Cyborg Network's Oxlo.ai (distributed inference, 1,500 users across 75 countries in 2025; adding SLAs/enterprise features in 2026) — validating demand but posing no incumbent threat ([STL Partners 50 edge companies 2026](https://stlpartners.com/articles/edge-computing/50-edge-computing-companies-to-watch-in-2026/)). NVIDIA's $1B investment into Nokia for AI-native RAN/edge inference signals where the majors think this goes ([RD World](https://www.rdworldonline.com/2026-ai-story-inference-at-the-edge-not-just-scale-in-the-cloud/)).

---

## 2. DePIN Compute Comparables

| Network | Pricing (2026) | Payment/settlement | Supply incentives | Utilization/reliability reality |
|---|---|---|---|---|
| **Akash** | H100 PCIe $2.09/hr, SXM5 $2.69/hr live marketplace (reverse-auction leases) | Any IBC token incl. **USDC**; since Mar 23 2026, Burn-Mint-Equilibrium: tenant payment burns AKT → mints dollar-pegged ACT credit → provider redeems to AKT; USDC leases carry a higher take-rate than AKT leases | Staking/inflation rewards + lease revenue; community-pool take rate | **Supply contraction**: from ~897 aggregated GPUs (2025 peak) to ~250–334 active in Q1–Q2 2026, with only ~84 in use — GPU capacity fell >57% QoQ as rewards tightened |
| **io.net** | H100 ~$1.47–$1.49/hr | Solana-native; $IO token + USDC | Token emissions to suppliers | Verified GPU count fell in down-token quarters; supplier churn tracks token price |
| **Render** | GPU rendering jobs; H100-class claimed 18–30x below AWS | RNDR/RENDER burn-mint on Solana | Render job fees | Solana-version render jobs grew QoQ in Q1 2026 but **paying revenue remains modest vs $1.65B market cap** |
| **Aethir** | Enterprise-focused new-GPU procurement; sales-led | ATH token; enterprise contracts | Checker-node + operator rewards | Positions above retail DePIN on quality; enterprise deals opaque |
| **Golem** | From $0.10/hr (RTX 3090 class); 30–60% below hyperscalers on batch tasks | GLM | Marketplace fees | Pioneer (2016) but niche; batch/rendering only |

Sources: [Messari State of Akash Q1 2026](https://messari.io/report/state-of-akash-q1-2026-final); [Akash BME review](https://ownyourmind.ai/projects/akash/); [cache256 Akash business](https://www.cache256.com/ecosystem/akash-network-depin-gpu-marketplace-business/); [buildmvpfast DePIN inference](https://www.buildmvpfast.com/blog/depin-gpu-inference-io-net-akash-below-aws-2026); [DEXTools io.net guide](https://www.dextools.io/tutorials/what-is-io-net-decentralized-gpu-ai-depin-solana-guide-2026); [Disruption Banking on Render](https://www.disruptionbanking.com/2026/02/19/can-render-ride-the-ai-wave-in-2026/); [ComputeStacker Golem](https://computestacker.com/providers/golem-network/).

**The DePIN lesson for ANDD (critical):**
1. **DePIN's discount is real (60–80% below AWS) but its reliability ceiling is ~99.7%** — ~26 hrs/yr downtime vs AWS's 99.99% target ([buildmvpfast](https://www.buildmvpfast.com/blog/depin-gpu-inference-io-net-akash-below-aws-2026)). Enterprises won't run regulated or user-facing workloads there. **ANDD can be the first network that offers DePIN-style programmable payments ON TOP of datacenter-grade physical infrastructure** — the combination doesn't exist today.
2. **Token-emission-funded supply is unstable**: Akash and io.net both bled physical supply when token prices fell. ANDD owns its nodes (QOF-financed), so its supply doesn't churn with a token — a durable structural advantage worth stating explicitly to DePIN customers burned by capacity evaporation.
3. **Akash's BME and USDC-lease mechanics are the closest working model to ANDD's stablecoin rails** — study its take-rate split (lower for native token, higher for USDC) when designing ANDD's fee schedule, but note ANDD can skip token complexity entirely at launch (stablecoin-only), per its roadmap.
4. DePIN networks are ANDD's *customers* as much as competitors (constituency #3): they need reliable "backbone" nodes to meet their own SLAs. ANDD's composable smart-contract SLA (cascade guarantees downstream) is precisely the product Aethir/io.net-class networks lack.

---

## 3. Hyperscaler & CDN Edge

| Offering | Model & pricing | SLA | Discovery/buying | Gap ANDD exploits |
|---|---|---|---|---|
| **AWS Local Zones** (33 zones) | Same EC2 API; compute priced **~25% above parent region**; limited instance families, few/no modern GPUs at most zones | Standard EC2 SLA (99.99% region-level; zone-level weaker) | AWS console self-serve | Latency only to ~33 metros; thin GPU availability; 25% premium **validates that buyers pay a locality premium** |
| **AWS Outposts** | Customer-premises racks, 3-yr committed, capex-like (six figures per rack over term); customer supplies power/space | AWS-managed hardware | Sales-led, long cycle | No inference-optimized economics; customer bears facility burden — ANDD's "we own the facility near you" inverts this |
| **AWS Wavelength** (30 zones) | Compute embedded in carrier 5G edge; EC2-style pricing with premium | Standard | Via AWS + carrier | Tied to one carrier's network; not carrier-neutral; enterprise uptake weak |
| **Azure Local / Arc** (ex-Azure Stack) | On-prem/sovereign; Apr 27 2026: scales to **thousands of servers** in a single Sovereign Private Cloud — aimed at governments/defense | Azure hybrid SLAs | Enterprise/gov sales | Software-defined sovereignty on *customer* hardware; ANDD sells sovereignty **as a service** with no customer capex |
| **Google Distributed Cloud** | GDC air-gapped (Google-supplied hardware, fully disconnected) + GDC connected (customer hardware); Gemini on-prem push at Next '26 | Negotiated | Gov/telco partners | Same gap: hardware lands on customer's premises and budget; 6+ month deployments vs ANDD's 60–90-day prefab |
| **Cloudflare Workers AI** | $0.011/1k Neurons (≈$0.11–$2.25/M tokens depending on model); 200+ cities; pricing revamp pending | Platform SLA (enterprise) | Fully self-serve | **Small models only, no dedicated GPUs, no residency guarantees per-request, no heavy inference** — Cloudflare proves edge-inference demand but can't serve 70B-class, storage-heavy, or compliance-bound workloads |

Sources: [Art of Infra on Local/Wavelength Zones](https://artofinfra.com/local-and-wavelength-zones-in-aws/); [Box Piper AWS zone list](https://www.boxpiper.com/posts/complete-list-of-aws-regions-wavelength-zones-and-local-zones-globally/); [Microsoft Azure Local sovereign-scale announcement](https://techcommunity.microsoft.com/blog/azurearcblog/azure-local-expands-to-sovereign-scale-infrastructure-with-disaggregated-deploym/4514338); [Google Distributed Cloud at Next '26](https://cloud.google.com/blog/topics/hybrid-cloud/google-distributed-cloud-at-next26); [Cloudflare Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

**The structural gap:** hyperscaler edge products make the *customer* host the hardware (Outposts, Azure Local, GDC) or restrict the edge to thin compute (Local Zones' 25% premium with limited GPUs; Cloudflare's small-model serverless). **Nobody offers hyperscaler-grade GPUs, in a provider-owned facility, within ~10ms of mid-size American metros, purchasable self-serve.** That's the ANDD wedge, and AWS's own 25% Local Zone uplift is the market's proof that locality carries a paid premium.

---

## 4. Colocation / Bare Metal / Sovereign Cloud / Government Buying

### 4.1 Bare metal market shakeup
- **Equinix Metal shuts down June 30, 2026 (confirmed)** — sales stopped, platform sunsets 6/30/26, console (billing history) until 12/31/26 ([DCD](https://www.datacenterdynamics.com/en/news/equinix-to-kill-off-metal-by-june-2026/); [SDxCentral](https://www.sdxcentral.com/news/equinix-officially-retires-bare-metal-offering/)). Displaced customers are being courted by OVHcloud, Latitude.sh, Servers.com, NovoServe, RedSwitches, IBM Cloud ([Cherry Servers roundup](https://www.cherryservers.com/blog/equinix-metal-alternatives)). **A cohort of automated-bare-metal buyers is homeless in exactly ANDD's Phase 1–2 window — a concrete near-term demand pocket for API-provisioned dedicated hardware.**
- **Vultr** (2026): HGX H100 ~$2.30–$2.60/GPU-hr; L40S ~$0.90–$1.20/hr; GH200 $1.99/hr; 8×H100 bare metal $23.92/hr (~$2.99/GPU-hr); hourly billing with prepaid/reserved discounts ([DeployBase Vultr guide, Mar 2026](https://deploybase.ai/articles/vultr-gpu-cloud-pricing-complete-guide-vs-hr-for-every-gpu)).
- **OVHcloud**: GPU cloud from $0.50/hr (A100 class); spot at 30–70% off; positions on data sovereignty + free bandwidth ([GPU Finder OVH](https://gpufinder.dev/providers/ovhcloud); [OVH's own Equinix-migration pitch](https://us.ovhcloud.com/resources/blog/equinix-metal-shutdown-why-ovhcloud-is-your-best-path-forward/)).

### 4.2 How government actually buys compute
- **Federal:** FedRAMP authorization is the gate; the **FedRAMP 20x** reform is live (first pilot authorizations Mar 6, 2026; six more by Apr 27, 2026; consolidated certification rules due June 2026, FedRAMP Ready designation retiring) — meaningfully faster/cheaper path to Moderate for new entrants like ANDD ([fedramp.gov/20x](https://www.fedramp.gov/20x/); [Winvale](https://info.winvale.com/blog/gsa-plans-release-consolidated-fedramp-program-certification-rules-june-2026)). Agencies discover via the FedRAMP Marketplace and buy via GSA schedules, GWACs, and resellers (Carahsoft-type aggregators are the practical storefront: [Carahsoft FedRAMP portal](https://www.carahsoft.com/solve/fedramp-technologies)). DoD multi-vendor IDIQs (JWCC → JWCC-Next) established that defense buys cloud from a pre-approved multi-award pool — ANDD's realistic entry is as a specialized edge/sovereign capability under a prime or follow-on vehicle.
- **State/local:** the **NASPO ValuePoint Cloud Solutions** cooperative (lead-state model aggregating all 50 states + territories + political subdivisions) is how cities/counties buy without running their own RFPs; the 2016–2026 vehicle is rolling into new awards (CAI Mar 2026, Presidio Feb 2026) explicitly framed around AI-enabled tech adoption ([NASPO ValuePoint Cloud portfolio](https://www.naspovaluepoint.org/portfolios/cloud-solutions-2016-2026/); [Presidio award](https://www.presidio.com/news/presidio-awarded-naspo-valuepoint-cloud-and-audio-visual-contracts-for-state-and-local-governments/)). **Action: ANDD should target a NASPO ValuePoint listing (directly or via an awarded reseller) in Phase 2 — it converts every OZ-adjacent municipality into an eligible buyer with no procurement cycle.**
- **Sovereign cloud demand driver:** Azure Local's sovereign-scale push and GDC air-gapped confirm hyperscalers see sovereign/private AI as a 2026 battleground — but both put hardware on the customer's premises and budget. Regional sovereign "GPU-cloud-in-country" plays are proliferating; in the U.S. domestic context, "sovereign" translates to FedRAMP/CJIS/ITAR + guaranteed U.S. persons + physical locality, which is ANDD's designed-in posture.

---

## 5. Market Sizing & Trends

| Metric | Figure | Source (date) |
|---|---|---|
| Edge AI market, 2026 | **$30.0–$37.5B** | [Grand View Research](https://www.grandviewresearch.com/industry-analysis/edge-ai-market-report); [DataM Intelligence](https://www.datamintelligence.com/research-report/edge-ai-market) (2026) |
| Edge AI market, 2030–2033 | $103B (2030, 28.7% CAGR) to $118.7B (2033, 21.7% CAGR) | same |
| Edge AI hardware | $26.1B (2025) → $58.9B (2030), 17.6% CAGR | [MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/edge-ai-hardware-market-158498281.html) |
| Inference share of edge-AI chips | 86.5% of segment (2025) | [Grand View](https://www.grandviewresearch.com/industry-analysis/edge-artificial-intelligence-chips-market) |
| Inference share of total AI compute | **~two-thirds in 2026** (vs ~1/3 in 2023, ~1/2 in 2025); 60–70% of ~$400B accelerator market | [AgentMarketCap, Apr 2026](https://agentmarketcap.ai/blog/2026/04/17/ai-inference-overtakes-training-two-thirds-2026-compute); [Computerworld CES 2026](https://www.computerworld.com/article/4114579/ces-2026-ai-compute-sees-a-shift-from-training-to-inference.html) |
| Lifetime compute split | inference 80–90% of a model's lifecycle compute dollars | [Introl](https://introl.com/blog/ai-inference-vs-training-infrastructure-economics-diverging) |
| Token price deflation | GPT-4-class: $30/M (Mar 2023) → ~$0.10–$0.40/M equivalents (2026), ≈99%+ decline; ~10x/yr 2021–25, moderating to 3–5x/yr through 2027, then 1.5–2x | [TokenCost index](https://tokencost.app/blog/ai-price-index); [a16z LLMflation](https://a16z.com/llmflation-llm-inference-cost/); [Axis Intelligence](https://axis-intelligence.com/ai-inference-cost-statistics/) |
| Gartner forecast | 1T-param inference cost falls >90% (2025→2030) | [Gartner, Mar 2026](https://www.gartner.com/en/newsroom/press-releases/2026-03-25-gartner-predicts-that-by-2030-performing-inference-on-an-llm-with-1-trillion-parameters-will-cost-genai-providers-over-90-percent-less-than-in-2025) |

**2026 table stakes** (what a credible offering must have on day one): self-serve signup with free tier; per-token serverless with published in/out rates and cached-input discount; batch tier at −50%; per-second/minute metered dedicated GPUs; committed-use discounts (15–45%); OpenAI-compatible API; usage dashboards with budget alerts; for enterprise, ≥99.9% uptime SLA with credits. (Synthesis of §1 sources.)

**Strategic implication of deflation:** never anchor ANDD's economics to raw $/token — that curve only goes down. Anchor to the things that *don't* deflate: milliseconds (physics), jurisdiction (law), reliability (engineering), and compliance (regulation). Sell tokens as the on-ramp, sell locality/sovereignty/SLA as the margin.

---

## 6. Synthesis: Gaps, Whitespace, Pricing Anchors

### 6.1 Gaps-and-opportunities table

| ANDD differentiator | Inference clouds (Together/Fireworks/Groq…) | GPU clouds (RunPod/Lambda/CoreWeave…) | DePIN (Akash/io.net…) | Hyperscaler/CDN edge | Colo/bare metal | **ANDD opportunity** |
|---|---|---|---|---|---|---|
| Latency / physical proximity | ✗ centralized DCs; no geo-SLA | ✗ few regions | ✗ random node placement | ◐ Local Zones (25% uplift, thin GPUs); Cloudflare (small models only) | ◐ colo is where it is | **Only provider with heavy GPUs <10ms from mid-size metros; sell latency as a priced tier** |
| Sovereignty / residency by construction | ✗ | ✗ | ✗ (worst: unknown hosts) | ◐ on-prem variants shift capex to customer | ◐ location known, no compliance stack | **US-soil, per-jurisdiction placement policies as a checkbox, not a consulting project** |
| AI-native zero-touch ops | ◐ good self-serve APIs | ◐ self-serve VMs | ◐ | ✗ sales-led for edge products | ✗ (Equinix Metal, the best attempt, is dead 6/30/26) | **Instant provisioning of *dedicated physical* capacity — the thing Metal proved demand for, then abandoned** |
| Mesh resilience / survive-in-place | ✗ | ✗ | ◐ (decentralized but unreliable) | ◐ | ✗ | **Only network combining datacenter reliability with partition-tolerant distribution — public-safety/NG911 grade** |
| Programmable smart-contract SLAs | ✗ (99.9–99.99% with claims process at best; most publish nothing) | ✗ mostly no numeric SLA at all | ✗ (ironically, none has automated SLAs) | ◐ credits require claims | ✗ | **Auto-paying, oracle-fed, composable SLA credits — category-creating; no claims process anywhere in market** |
| Micro-transaction billing | ◐ per-token is micro-ish, settlement isn't | ✗ | ◐ Akash BME/USDC leases closest | ✗ | ✗ | **Per-request stablecoin channels + one-block provisioning — DePIN-grade rails on enterprise-grade infra** |
| OZ economics | ✗ | ✗ | ✗ | ✗ | ✗ | **Unique cost-of-capital advantage → sustainable price aggression where chosen + community/gov procurement goodwill** |

### 6.2 The 5–7 whitespace positions ANDD should claim

1. **Latency-tiered inference** — the first per-token API with an explicit proximity tier ("Metro" <10ms / "Regional" <25ms / "Standard") and a *latency SLA*, not just uptime. No serverless provider prices geography today; AWS's 25% Local Zone premium proves willingness to pay.
2. **Sovereignty-as-a-service** — per-tenant data-residency placement policies (state-level pinning, CJIS/HIPAA/ITAR paths) sold self-serve, vs hyperscalers' put-hardware-on-your-premises model and DePIN's know-nothing hosting.
3. **Self-executing SLAs** — smart-contract uptime/latency guarantees with automatic proportional stablecoin credits, composable so DePIN and telco customers cascade them into their own SLAs. Zero incumbents; most GPU clouds publish *no* numeric SLA at all.
4. **The Equinix Metal succession** — API-provisioned dedicated bare metal/GPU nodes with 2026-grade automation; a displaced customer base exists right now with a hard 6/30/26 deadline.
5. **DePIN enterprise backbone** — guaranteed-tier physical nodes DePIN networks rent (paid in stablecoins, settled per-block) to stabilize their own supply, fixing the documented Akash/io.net capacity-churn problem.
6. **Gov-ready edge via cooperative vehicles** — FedRAMP 20x fast-path + NASPO ValuePoint listing = the only sub-10ms GPU capacity a county or state agency can buy off a pre-competed contract.
7. **Micro-billed spot inference** — per-request payment channels (fractions of a cent, batch-settled) for agentic/IoT workloads where card-based prepaid credit models break down.

### 6.3 Pricing anchor recommendations

| ANDD product line | Anchor vs market | Rationale & reference points |
|---|---|---|
| Serverless per-token (standard, 7–13B open models) | **Parity to −10%** vs Together/Fireworks (e.g., Llama-8B-class ~$0.10–$0.15/M; 70B-class at hubs ~$0.85–$1.00/M blended) | Deflating commodity; use as acquisition funnel; batch −50% and cached-input discounts are mandatory table stakes |
| **Latency-tier serverless (Metro <10ms, latency-SLA'd)** | **+25–40% premium** over own standard tier | Mirrors AWS's proven 25% Local Zone uplift; competitors cannot follow without building physical presence |
| Dedicated inference endpoints (L40S/MI300X at edge nodes) | **Parity with platform tier**: L40S $1.90–$2.40/hr (between Vultr's $0.90–$1.20 bare rate and Replicate's $3.51 serverless rate); H100-class at hubs $3.50–$4.50/hr | Buyers compare against RunPod $2.89/Lambda $3.99/Together $5.49; ANDD adds locality + auto-SLA at platform-tier price |
| Reserved / committed capacity | Market-standard **15–45% discount curve** (matches Together $3.99→$3.19, Lambda reserved, annual = 15–20% per existing ANDD plan) | Deviating from the standard curve creates friction; the differentiator is *staked-reservation option via stablecoin*, not the % |
| Sovereign/compliance tier (Gov/Secure profiles, CJIS/ITAR paths) | **+50–100% premium** over commercial dedicated | Comps are Outposts/GDC air-gapped (capex-heavy, 6-month deployments) and GovCloud uplifts; ANDD is still cheaper *all-in* because customer buys no hardware |
| DePIN backbone nodes (guaranteed tier) | **Premium to DePIN spot (~2× Akash's $2.09 H100 ≈ their reliability-adjusted true cost), discount to CoreWeave-class contracts** | Price against the *cost of unreliability*: 99.7% → 99.95%+ uptime is worth more than the spread |
| Micro-billed spot / consumer API | Parity per-token with **zero minimums, per-request settlement** | Win on billing mechanics and instant onboarding, not price |
| Storage (S3-compatible, 3-site erasure-coded) | Parity with regional-cloud object storage; premium for residency-pinned placement | Together charges $0.16/GiB-mo for adjacent storage — ANDD's multi-site durability + residency justifies the same or slightly above |

**Overall posture: premium where physics/law/reliability bind (latency tiers, sovereignty, auto-SLAs — the non-deflating goods); parity on commodity tokens and GPU-hours (funnel); discount only tactically via OZ cost-of-capital when landing anchor tenants in a new metro.**

---

## Appendix: Data caveats
- Aggregator-tracker prices (Spheron, costbench, gpuperhour, computeprices, checkthat, DeployBase, etc.) lag official pages by days-to-weeks; Together AI numbers were verified on the official pricing page Aug 2026; Groq's official page no longer exposes public rates (marketing page only — rates live in console), so Groq figures are tracker-sourced (May–Jun 2026).
- Crusoe publishes no rate card; its figure is a specialty-cloud median (indicative only).
- DePIN utilization figures are from Messari quarterly reporting (Q1 2026) and may have shifted.
- CoreWeave GB200 per-GPU figure is derived (node price ÷ 4) and indicative.
- Market-size figures vary by firm because "edge AI" scope definitions differ; ranges are presented rather than a single point.
