#!/usr/bin/env python3
"""Generate the three Native Networks homepage proposals into proposals/."""
import pathlib

OUT = pathlib.Path('/home/anoop/git/anannra/andd_website/proposals')
OUT.mkdir(exist_ok=True)

MARK = '''<svg class="mark" viewBox="-8 -8 246 206" fill="none" aria-hidden="true">
  <g stroke="#1E2F72" stroke-width="2" stroke-linecap="round">
    <path d="M77 9 L43.5 94.5 M77 9 L111.5 94.5 M77 9 L77 179 M43.5 94.5 L77 179 M111.5 94.5 L77 179 M111.5 94.5 L145 179 M9.5 179.5 L145 179"/>
    <path d="M179 9 L179 179 M179 9 L221 50 M221 50 L221 140 M179.5 94.5 L221 140 M221 140 L179 179"/>
  </g>
  <path class="signal" d="M9.5 179.5 L43.5 94.5 L179.5 94.5 L221 50" stroke="#38BDF8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="#4C6FFF"><circle cx="77" cy="9" r="5.5"/><circle cx="179" cy="9" r="5.5"/><circle cx="77" cy="179" r="5.5"/><circle cx="145" cy="179" r="5.5"/><circle cx="179" cy="179" r="5.5"/><circle cx="221" cy="140" r="5.5"/></g>
  <g fill="#38BDF8"><circle cx="9.5" cy="179.5" r="7.5"/><circle cx="43.5" cy="94.5" r="7.5"/><circle cx="111.5" cy="94.5" r="7.5"/><circle cx="179.5" cy="94.5" r="7.5"/></g>
  <circle cx="221" cy="50" r="7" fill="#0A0E1A" stroke="#38BDF8" stroke-width="5"/>
</svg>'''

LOGO = f'<a class="logo" href="#top" aria-label="Native Networks home">{MARK}<span class="wordmark">Native Networks</span></a>'

FORM_ACTION = 'https://docs.google.com/forms/d/e/1FAIpQLSfHtd4u5kRASwOWJgg4-gr2M3eRRhZLNxL5clJcXSxOrmuCtw/formResponse'

FORM = f'''
<form id="lead-form" class="lead-form" action="{FORM_ACTION}" method="POST" target="nn-form-sink" novalidate>
  <div class="frow">
    <div class="field"><label for="lf-name">Full name</label><input id="lf-name" name="entry.761505288" type="text" autocomplete="name" required></div>
    <div class="field"><label for="lf-email">Work email</label><input id="lf-email" name="entry.906364280" type="email" autocomplete="email" required></div>
  </div>
  <div class="frow">
    <div class="field"><label for="lf-org">Organization</label><input id="lf-org" name="entry.528269525" type="text" autocomplete="organization"></div>
    <div class="field"><label for="lf-audience">I am a</label>
      <select id="lf-audience" name="entry.445405568" required>
        <option value="" selected disabled>Choose one</option>
        <option>Customer</option><option>Partner</option><option>Developer</option><option>Investor</option>
      </select></div>
  </div>
  <div class="frow">
    <div class="field"><label for="lf-region">Region or market</label><input id="lf-region" name="entry.936819366" type="text" placeholder="Texas, North East England, Arizona"></div>
    <div class="field"><label for="lf-workload">Workload</label>
      <select id="lf-workload" name="entry.496908603">
        <option value="" selected disabled>Choose one</option>
        <option>AI inference</option><option>Public safety</option><option>Mobility &amp; V2X</option><option>Power &amp; Utilities</option><option>Healthcare</option><option>DePIN / validators</option><option>Smart city</option><option>Other</option>
      </select></div>
  </div>
  <div class="field full"><label for="lf-message">What do you need to run, and where?</label><textarea id="lf-message" name="entry.1983684791" required placeholder="Workload, region, latency budget, and any compliance requirements."></textarea></div>
  <input type="hidden" name="emailAddress" value=""><input type="hidden" name="fvv" value="1"><input type="hidden" name="pageHistory" value="0">
  <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="actions"><button type="submit" class="btn btn-primary">Send inquiry</button><span class="privacy">We reply within two business days.</span></div>
</form>
<div id="form-success" class="form-success" role="status" aria-live="polite">
  <h3>Inquiry sent</h3>
  <p>We'll review the workload and region and reply within two business days at the address you gave.</p>
</div>
<iframe name="nn-form-sink" class="form-sink" title="form submission target"></iframe>
'''

FORM_JS = '''
(function(){
  const form = document.getElementById('lead-form');
  const success = document.getElementById('form-success');
  if (!form || !success) return;
  form.addEventListener('submit', function(e){
    const hp = form.querySelector('.hp');
    if (hp && hp.value) { e.preventDefault(); return; }
    if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
    const emailField = document.getElementById('lf-email');
    const emailAddr = form.querySelector('input[name="emailAddress"]');
    if (emailField && emailAddr) emailAddr.value = emailField.value;
    setTimeout(function(){
      form.hidden = true;
      success.hidden = false;
      success.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 120);
  });
})();
'''

# Shared form CSS, expressed through tokens each page defines.
FORM_CSS = '''
.lead-form { display: grid; gap: 22px; }
.lead-form .frow { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
.field { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.field.full { grid-column: 1 / -1; }
.field label { font-size: 0.85rem; color: var(--ink-2); }
.field input, .field select, .field textarea {
  width: 100%; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  color: var(--ink-0); font: inherit; font-size: 0.95rem; line-height: 1.4; padding: 12px 14px;
  transition: border-color 160ms;
}
.field input::placeholder, .field textarea::placeholder { color: var(--ink-3); }
.field textarea { resize: vertical; min-height: 120px; }
.field input:focus, .field select:focus, .field textarea:focus { outline: none; border-color: var(--sky); }
.field select { appearance: none; -webkit-appearance: none; cursor: pointer; padding-right: 38px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239AA4BD' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 14px center; }
.lead-form .actions { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.lead-form .privacy { font-size: 0.85rem; color: var(--ink-3); }
.lead-form .hp { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
.form-sink { display: none; }
.form-success { border: 1px solid var(--line); border-radius: var(--radius); padding: 28px 30px; }
.form-success h3 { margin: 0 0 6px; font-size: 1.3rem; color: var(--ink-0); }
.form-success p { margin: 0; color: var(--ink-2); }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 20px; border-radius: var(--radius); border: 1px solid var(--line); color: var(--ink-0); font: inherit; font-weight: 500; font-size: 0.95rem; cursor: pointer; background: transparent; transition: border-color 160ms, background 160ms; }
.btn:hover { border-color: var(--sky); }
.btn-primary { background: var(--indigo); border-color: var(--indigo); color: #fff; }
.btn-primary:hover { background: var(--indigo-hi); border-color: var(--indigo-hi); }
:focus-visible { outline: 2px solid var(--sky); outline-offset: 3px; }
@media (max-width: 640px) { .lead-form .frow { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
'''

HEAD = '''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Native Networks builds and operates small modular AI datacenters, 500 kW to 20 MW, sited where power and fiber already exist. Inference runs locally instead of round-tripping to a distant cloud.">
<meta name="theme-color" content="#0A0E1A">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fonts}&display=swap" rel="stylesheet">
'''

# ----------------------------------------------------------------------------
# A. SIGNAL — deck-literal
# ----------------------------------------------------------------------------
SIGNAL = HEAD.format(title='Native Networks', fonts='Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400') + '''
<style>
:root {
  --bg: #0A0E1A; --surface: #111A30; --surface-2: #19223E;
  --line: #24305A; --line-soft: #1A2447;
  --indigo: #4C6FFF; --indigo-hi: #6383FF; --indigo-fill: #454FC4; --sky: #38BDF8; --navy: #1E2F72;
  --ink-0: #FFFFFF; --ink-1: #C8CEE0; --ink-2: #9AA4BD; --ink-3: #6B7488;
  --radius: 8px; --font: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif;
  --pad: clamp(4rem, 8vw, 7.5rem);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink-1); font-family: var(--font); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { color: var(--ink-0); margin: 0; font-weight: 600; letter-spacing: -0.02em; text-wrap: balance; }
p { margin: 0; }
.wrap { width: min(1180px, calc(100% - 2 * clamp(1.25rem, 4vw, 3rem))); margin-inline: auto; }

/* Nav */
.nav { position: sticky; top: 0; z-index: 10; background: rgba(10,14,26,0.82); backdrop-filter: blur(14px); border-bottom: 1px solid var(--line-soft); }
.nav .wrap { display: flex; align-items: center; justify-content: space-between; height: 68px; gap: 24px; }
.logo { display: inline-flex; align-items: center; gap: 12px; }
.logo .mark { width: 40px; height: 34px; }
.wordmark { font-weight: 700; font-size: 1.15rem; color: var(--ink-0); letter-spacing: -0.01em; white-space: nowrap; }
.nav-links { display: flex; gap: 28px; font-size: 0.92rem; color: var(--ink-2); }
.nav-links a:hover { color: var(--ink-0); }
.nav .btn { padding: 9px 16px; font-size: 0.9rem; }

/* Hero */
.hero { position: relative; overflow: hidden; border-bottom: 1px solid var(--line-soft); }
.hero .wrap { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr); gap: 48px; align-items: center; min-height: 560px; }
.hero-copy { padding: clamp(3.5rem, 7vw, 6rem) 0; }
.hero h1 { font-size: clamp(2.4rem, 4.6vw, 3.9rem); line-height: 1.05; max-width: 14ch; margin-bottom: 26px; }
.hero .dek { font-size: 1.12rem; color: var(--ink-2); max-width: 46ch; margin-bottom: 36px; }
.hero .ctas { display: flex; gap: 12px; flex-wrap: wrap; }
.hero-art { position: relative; align-self: stretch; min-height: 420px; }
.hero-art img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 22%, #000 100%), linear-gradient(to bottom, transparent, #000 12%, #000 90%, transparent);
  -webkit-mask-composite: source-in; mask-image: linear-gradient(to right, transparent, #000 22%), linear-gradient(to bottom, transparent, #000 12%, #000 90%, transparent); mask-composite: intersect; }

/* Facts strip */
.facts { border-bottom: 1px solid var(--line-soft); }
.facts .wrap { display: grid; grid-template-columns: repeat(4, 1fr); }
.fact { padding: 26px 0; border-left: 1px solid var(--line-soft); padding-left: 22px; }
.fact:first-child { border-left: 0; padding-left: 0; }
.fact b { display: block; color: var(--ink-0); font-size: 1.45rem; font-weight: 600; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.fact span { color: var(--ink-2); font-size: 0.9rem; }

/* Sections */
section.block { padding: var(--pad) 0; border-bottom: 1px solid var(--line-soft); }
.sec-head { max-width: 720px; margin-bottom: 44px; }
.sec-head h2 { font-size: clamp(1.8rem, 3vw, 2.5rem); line-height: 1.12; margin-bottom: 14px; }
.sec-head p { color: var(--ink-2); font-size: 1.05rem; max-width: 60ch; }
.cards { display: grid; gap: 18px; }
.cards.c2 { grid-template-columns: repeat(2, 1fr); }
.cards.c3 { grid-template-columns: repeat(3, 1fr); }
.card { border: 1px solid var(--indigo); border-radius: var(--radius); padding: 28px 28px 30px; background: var(--surface); }
.card h3 { font-size: 1.25rem; margin-bottom: 12px; line-height: 1.25; }
.card p { color: var(--ink-2); font-size: 0.98rem; }
.card.filled { background: var(--indigo-fill); border-color: var(--indigo-fill); }
.card.filled p { color: #DDE2FA; }
.card.filled.wide { grid-column: 1 / -1; }
.note { margin-top: 24px; color: var(--ink-2); font-size: 1rem; max-width: 70ch; }
.band { margin-top: 36px; background: var(--indigo-fill); border-radius: var(--radius); padding: 30px; text-align: center; color: #fff; font-size: clamp(1.2rem, 2.2vw, 1.6rem); font-weight: 600; letter-spacing: -0.01em; }

/* Tiers */
.tiers { display: grid; gap: 14px; }
.tier { display: grid; grid-template-columns: 220px 1fr; gap: 24px; align-items: baseline; border: 1px solid var(--line); border-radius: var(--radius); padding: 24px 28px; }
.tier h3 { font-size: 1.15rem; }
.tier .term { color: var(--sky); font-size: 0.88rem; display: block; margin-top: 4px; font-weight: 500; }
.tier p { color: var(--ink-2); }

/* Where */
.where { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: start; }
.sites { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 14px 24px; }
.sites li { border-top: 1px solid var(--line); padding-top: 12px; }
.sites b { display: block; color: var(--ink-0); font-weight: 600; font-size: 1.1rem; }
.sites span { color: var(--ink-3); font-size: 0.9rem; }
.where p { color: var(--ink-2); font-size: 1.05rem; max-width: 46ch; }

/* Contact */
.contact { display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 56px; align-items: start; }
.contact h2 { font-size: clamp(1.8rem, 3vw, 2.5rem); line-height: 1.12; margin-bottom: 14px; }
.contact .lead { color: var(--ink-2); font-size: 1.05rem; margin-bottom: 20px; }
.contact .mail { color: var(--sky); font-weight: 500; }

footer .wrap { display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; padding: 34px 0; color: var(--ink-3); font-size: 0.88rem; }
footer .logo .mark { width: 30px; height: 26px; }
footer .wordmark { font-size: 1rem; }
footer nav { display: flex; gap: 20px; }
footer nav a:hover { color: var(--ink-0); }
''' + FORM_CSS + '''
@media (max-width: 960px) {
  .nav-links { display: none; }
  .hero .wrap { grid-template-columns: 1fr; min-height: 0; }
  .hero-art { min-height: 320px; margin-inline: calc(-1 * clamp(1.25rem, 4vw, 3rem)); }
  .hero-art img { mask-image: linear-gradient(to bottom, transparent, #000 25%); -webkit-mask-image: linear-gradient(to bottom, transparent, #000 25%); }
  .facts .wrap { grid-template-columns: 1fr 1fr; }
  .fact:nth-child(3) { border-left: 0; padding-left: 0; }
  .cards.c2, .cards.c3, .where, .contact { grid-template-columns: 1fr; }
  .tier { grid-template-columns: 1fr; gap: 8px; }
}
@media (max-width: 520px) { .facts .wrap { grid-template-columns: 1fr; } .fact { border-left: 0; padding-left: 0; padding: 16px 0; border-top: 1px solid var(--line-soft); } .sites { grid-template-columns: 1fr; } }
</style>

<a id="top"></a>
<header class="nav"><div class="wrap">
  ''' + LOGO + '''
  <nav class="nav-links"><a href="#why">Why now</a><a href="#build">What we build</a><a href="#buy">How you buy</a><a href="#where">Where</a></nav>
  <a class="btn btn-primary" href="#contact">Talk to us</a>
</div></header>

<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <h1>The distributed layer between the hyperscale core and the device.</h1>
    <p class="dek">We build and operate small modular AI datacenters, 500 kW to 20 MW, sited where power and fiber already exist. Rapidly deployed, and inference runs locally instead of round-tripping to a distant cloud.</p>
    <div class="ctas"><a class="btn btn-primary" href="#contact">Talk to us</a><a class="btn" href="#build">See what we build</a></div>
  </div>
  <div class="hero-art"><img src="assets/tower.jpg" alt="Illustration of radio towers at night linked by a glowing signal path" width="1068" height="1600"></div>
</div></section>

<div class="facts"><div class="wrap">
  <div class="fact"><b>500 kW to 20 MW</b><span>per site, expanded as demand is contracted</span></div>
  <div class="fact"><b>90 to 180 days</b><span>from site selection to live</span></div>
  <div class="fact"><b>Under 30 ms</b><span>round trip at the edge</span></div>
  <div class="fact"><b>1 GW and more</b><span>land-to-power pipeline today</span></div>
</div></div>

<section class="block" id="why"><div class="wrap">
  <div class="sec-head"><h2>Inference is moving to the edge. Latency tolerance is gone.</h2>
    <p>The shift from building models to deploying them is structural, and it is colliding with a hard constraint: existing megawatts at the right location.</p></div>
  <div class="cards c2">
    <div class="card"><h3>Inference dominates compute</h3><p>Inference is now the majority of AI compute and growing faster than training. The shift from model-building to model-deployment is structural and accelerating.</p></div>
    <div class="card"><h3>Latency tolerance is gone</h3><p>Real-time voice, agentic sessions, inline security, and physical AI cannot tolerate a distant round trip. A rising share of workloads demands local, sub-20 ms response.</p></div>
  </div>
  <div class="cards c2" style="margin-top:18px">
    <div class="card filled"><h3>Hyperscale is the wrong architecture</h3><p>Hyperscale was engineered for centralized, batch-oriented training, not for distributed, low-latency inference. Repurposing it is not a retrofit. It is a rebuild.</p></div>
    <div class="card filled"><h3>Hyperscale supply has stalled</h3><p>Power and water scarcity, permitting backlogs, and community opposition stall large builds for years. New capacity cannot arrive in time to meet the inference wave.</p></div>
    <div class="card filled wide"><h3>The edge layer is unowned</h3><p>The distributed, low-latency inference layer does not exist yet. Real-time voice, agentic AI, inline security, and physical AI have nowhere to run at the edge. That is what we build.</p></div>
  </div>
</div></section>

<section class="block" id="build"><div class="wrap">
  <div class="sec-head"><h2>Modular, low-friction AI datacenters sited where power already exists.</h2></div>
  <div class="cards c3">
    <div class="card"><h3>AI-native modular design</h3><p>Sub-20 MW datacenters built from two pre-defined modules: the EC500 at 500 kW and the EC1000 at 1 MW. A facility starts small and expands to 20 MW as demand is contracted. Capital follows commitment, not speculation.</p></div>
    <div class="card"><h3>Sited on existing and stranded power</h3><p>We site where utility capacity already exists: co-ops, municipals, cell sites, investor-owned utilities, and RTOs. Rates are locked and interconnect expedited before a single rack is deployed.</p></div>
    <div class="card"><h3>Minimal friction</h3><p>No community water draw. Minimal noise profile. Expedited permitting through relocatable precast foundations. The form factor removes the slow parts by engineering them out.</p></div>
  </div>
  <div class="band">Land-to-power pipeline exceeds 1 GW today</div>
</div></section>

<section class="block"><div class="wrap">
  <div class="sec-head"><h2>Faster, quieter, closer, and cheaper. With a mechanism behind each claim.</h2></div>
  <div class="cards c2">
    <div class="card"><h3>Live in 90 to 180 days</h3><p>Relocatable precast foundations eliminate the concrete cure cycle. EC500 and EC1000 blocks arrive pre-engineered. No long-lead custom construction. The design is the speed.</p></div>
    <div class="card"><h3>No community conflict</h3><p>Zero community water draw. Minimal acoustic footprint. Expedited permitting through relocatable structures. We do not need years of community relations before breaking ground.</p></div>
    <div class="card"><h3>Under 30 ms at the edge</h3><p>Carrier-adjacent siting removes the backhaul hop. Bonded fiber with Starlink as diverse backup delivers the latency profile real-time AI workloads require.</p></div>
    <div class="card"><h3>Lower capital, leaner operations</h3><p>Roughly half the capital per megawatt of a traditional hyperscale build, delivered five to ten times faster. AI-native operations keep the operator-to-site ratio lean.</p></div>
  </div>
</div></section>

<section class="block" id="buy"><div class="wrap">
  <div class="sec-head"><h2>Three ways to buy capacity.</h2><p>Anchor agreements cover a facility's fixed costs before a single spot GPU hour is sold.</p></div>
  <div class="tiers">
    <div class="tier"><div><h3>Anchor offtake</h3><span class="term">5 years and longer, take-or-pay</span></div><p>Dedicated capacity under a long-term NNN agreement. The anchor tenant's commitment sets the site's expansion path.</p></div>
    <div class="tier"><div><h3>Reserved capacity</h3><span class="term">2 years, fractional</span></div><p>Reserve blocks of a site at mid-tier pricing without committing to 100% utilization.</p></div>
    <div class="tier"><div><h3>Spot and preemptible</h3><span class="term">On demand</span></div><p>GPU time on idle capacity at spot rates. Best for batch inference, evaluation runs, and bursty workloads.</p></div>
  </div>
</div></section>

<section class="block" id="where"><div class="wrap">
  <div class="where">
    <div><div class="sec-head" style="margin-bottom:22px"><h2>Four launch sites. Then 20 MW per state.</h2></div>
      <p>The first facilities go live in the United States and the United Kingdom. From there the template repeats: 20 MW per state across 30 U.S. states, with the orchestration layer routing work across sites.</p></div>
    <ul class="sites">
      <li><b>Phoenix</b><span>Arizona, 500 kW</span></li>
      <li><b>Dallas</b><span>Texas, 500 kW</span></li>
      <li><b>Newcastle</b><span>England, 500 kW</span></li>
      <li><b>Leeds</b><span>England, 500 kW</span></li>
    </ul>
  </div>
</div></section>

<section class="block" id="contact"><div class="wrap contact">
  <div><h2>Tell us the workload, the region, and the latency budget.</h2>
    <p class="lead">Carriers, utilities, AI model providers, and enterprises with real-time workloads: we will come back with a site plan.</p>
    <a class="mail" href="mailto:contact@andd.ai">contact@andd.ai</a></div>
  <div>''' + FORM + '''</div>
</div></section>

<footer><div class="wrap">
  ''' + LOGO + '''
  <nav><a href="#why">Why now</a><a href="#build">What we build</a><a href="#buy">How you buy</a><a href="#contact">Contact</a></nav>
  <span>© 2026 Native Networks · andd.ai</span>
</div></footer>
<script>''' + FORM_JS + '''document.getElementById('form-success').hidden = true;</script>
'''

# ----------------------------------------------------------------------------
# B. MESH — typographic, the mark is the hero
# ----------------------------------------------------------------------------
MESH = HEAD.format(title='Native Networks', fonts='Schibsted+Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400') + '''
<style>
:root {
  --bg: #0A0E1A; --surface: #0E1426;
  --line: #1E2F72; --line-soft: #172250;
  --indigo: #4C6FFF; --indigo-hi: #6383FF; --sky: #38BDF8; --navy: #1E2F72;
  --ink-0: #FFFFFF; --ink-1: #C8CEE0; --ink-2: #9AA4BD; --ink-3: #6B7488;
  --radius: 4px; --font: 'Schibsted Grotesk', 'Helvetica Neue', Arial, sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink-1); font-family: var(--font); font-size: 17px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { color: var(--ink-0); margin: 0; font-weight: 500; letter-spacing: -0.025em; text-wrap: balance; }
p { margin: 0; }
.wrap { width: min(1240px, calc(100% - 2 * clamp(1.25rem, 5vw, 4rem))); margin-inline: auto; }

.nav .wrap { display: flex; align-items: center; justify-content: space-between; height: 80px; }
.logo { display: inline-flex; align-items: center; gap: 12px; }
.logo .mark { width: 42px; height: 36px; }
.wordmark { font-weight: 700; font-size: 1.15rem; color: var(--ink-0); white-space: nowrap; }
.nav-links { display: flex; gap: 32px; font-size: 0.95rem; color: var(--ink-2); }
.nav-links a:hover { color: var(--ink-0); }

.hero { padding: clamp(2rem, 6vw, 5rem) 0 clamp(3rem, 7vw, 6rem); }
.hero .wrap { display: grid; grid-template-columns: minmax(0, 1fr) minmax(280px, 0.8fr); gap: clamp(2rem, 6vw, 6rem); align-items: center; }
.hero h1 { font-size: clamp(2.6rem, 5.4vw, 4.8rem); line-height: 1.02; max-width: 13ch; }
.hero .dek { margin-top: 30px; font-size: 1.2rem; color: var(--ink-2); max-width: 44ch; }
.hero .dek a { color: var(--sky); border-bottom: 1px solid currentColor; }
.hero-mark { width: 100%; max-width: 540px; margin-inline: auto; }
.hero-mark .mark { width: 100%; height: auto; display: block; }
.hero-mark .signal.draw { stroke-dasharray: 320; stroke-dashoffset: 320; animation: draw 1.4s cubic-bezier(.4,0,.2,1) 0.2s forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) { .hero-mark .signal.draw { animation: none; stroke-dashoffset: 0; } }

.rule { border: 0; border-top: 1px solid var(--line-soft); margin: 0; }
.row { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 40px; padding: clamp(3rem, 6vw, 5.5rem) 0; }
.row .k { color: var(--sky); font-size: 1rem; font-weight: 500; padding-top: 0.45em; }
.row h2 { font-size: clamp(1.8rem, 3.4vw, 2.9rem); line-height: 1.1; max-width: 22ch; }
.row .body { margin-top: 26px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 40px; }
.row .body p { color: var(--ink-2); max-width: 46ch; }
.row .body p b { color: var(--ink-0); font-weight: 500; display: block; margin-bottom: 4px; }
.row .body.one { grid-template-columns: minmax(0, 1fr); }

/* Numbers as type, not tiles */
.numbers { display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; margin-top: 34px; }
.numbers div { border-top: 1px solid var(--line); padding-top: 14px; }
.numbers b { display: block; color: var(--ink-0); font-size: clamp(1.6rem, 2.6vw, 2.2rem); font-weight: 500; letter-spacing: -0.03em; line-height: 1.1; font-variant-numeric: tabular-nums; }
.numbers span { color: var(--ink-2); font-size: 0.95rem; }

/* Scale rail: EC500 -> EC1000 -> 20 MW */
.rail { margin-top: 36px; }
.rail svg { width: 100%; height: auto; display: block; overflow: visible; }
.rail text { font-family: var(--font); fill: var(--ink-2); font-size: 13px; }
.rail text.big { fill: var(--ink-0); font-size: 16px; font-weight: 500; }

.tiers { display: grid; gap: 0; margin-top: 26px; }
.tier { display: grid; grid-template-columns: 240px 1fr; gap: 24px; padding: 20px 0; border-top: 1px solid var(--line-soft); }
.tier:last-child { border-bottom: 1px solid var(--line-soft); }
.tier h3 { font-size: 1.1rem; font-weight: 500; }
.tier .term { color: var(--sky); font-size: 0.9rem; display: block; margin-top: 2px; }
.tier p { color: var(--ink-2); max-width: 60ch; }

.sites { list-style: none; padding: 0; margin: 26px 0 0; display: flex; gap: 40px; flex-wrap: wrap; }
.sites li { display: flex; align-items: center; gap: 10px; color: var(--ink-0); font-size: 1.05rem; }
.sites li::before { content: ''; width: 10px; height: 10px; border-radius: 50%; background: var(--sky); }
.sites span { color: var(--ink-3); font-size: 0.9rem; }

.contact-wrap { max-width: 720px; }
.contact-wrap .mail { color: var(--sky); border-bottom: 1px solid currentColor; }
.contact-wrap .lead-form { margin-top: 30px; }

footer .wrap { display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; padding: 36px 0; color: var(--ink-3); font-size: 0.9rem; }
footer nav { display: flex; gap: 22px; }
footer nav a:hover { color: var(--ink-0); }
''' + FORM_CSS + '''
@media (max-width: 900px) {
  .nav-links { display: none; }
  .hero .wrap { grid-template-columns: 1fr; }
  .hero-mark { max-width: 360px; margin: 0; }
  .row { grid-template-columns: 1fr; gap: 14px; }
  .row .body, .numbers { grid-template-columns: 1fr 1fr; }
  .tier { grid-template-columns: 1fr; gap: 6px; }
}
@media (max-width: 560px) { .row .body, .numbers { grid-template-columns: 1fr; } }
</style>

<a id="top"></a>
<header class="nav"><div class="wrap">
  ''' + LOGO + '''
  <nav class="nav-links"><a href="#why">Why now</a><a href="#build">What we build</a><a href="#buy">How you buy</a><a href="#contact">Contact</a></nav>
</div></header>

<section class="hero"><div class="wrap">
  <div>
    <h1>The distributed layer between the hyperscale core and the device.</h1>
    <p class="dek">Small modular AI datacenters, 500 kW to 20 MW, sited where power and fiber already exist. Inference runs locally instead of round-tripping to a distant cloud. <a href="#contact">Talk to us</a></p>
  </div>
  <div class="hero-mark">''' + MARK + '''</div>
</div></section>

<hr class="rule">
<section id="why"><div class="wrap row">
  <div class="k">Why now</div>
  <div>
    <h2>Inference is moving to the edge, and latency tolerance is gone.</h2>
    <div class="body">
      <p><b>Inference dominates compute.</b> It is now the majority of AI compute and growing faster than training. The shift from building models to deploying them is structural.</p>
      <p><b>Real time cannot round-trip.</b> Voice, agentic sessions, inline security, and physical AI need local, sub-20 ms response. A distant cloud cannot deliver it.</p>
      <p><b>Hyperscale is the wrong shape.</b> It was engineered for centralized, batch-oriented training. Repurposing it for distributed inference is a rebuild, not a retrofit.</p>
      <p><b>And it is stalled.</b> Power and water scarcity, permitting backlogs, and community opposition hold large builds for years. The distributed inference layer remains unowned.</p>
    </div>
  </div>
</div></section>

<hr class="rule">
<section id="build"><div class="wrap row">
  <div class="k">What we build</div>
  <div>
    <h2>Two modules. One site that grows from 500 kW to 20 MW.</h2>
    <div class="body">
      <p><b>EC500 and EC1000.</b> Pre-engineered 500 kW and 1 MW blocks on relocatable precast foundations. A facility starts with one and expands as demand is contracted. Capital follows commitment.</p>
      <p><b>Sited on existing power.</b> Co-ops, municipals, cell sites, investor-owned utilities, and RTOs where capacity already exists. Rates locked and interconnect expedited before a rack ships.</p>
      <p><b>Nothing the neighbors object to.</b> No community water draw. Minimal noise. Permitting expedited because the structure is relocatable.</p>
      <p><b>Carrier-adjacent.</b> Siting next to the carrier removes the backhaul hop. Bonded fiber with Starlink as diverse backup.</p>
    </div>
    <div class="rail" aria-label="Site scale from EC500 to a 20 MW facility">
      <svg viewBox="0 0 1000 110">
        <line x1="20" y1="60" x2="980" y2="60" stroke="#1E2F72" stroke-width="2"/>
        <line x1="20" y1="60" x2="180" y2="60" stroke="#38BDF8" stroke-width="6" stroke-linecap="round"/>
        <circle cx="20" cy="60" r="8" fill="#38BDF8"/><circle cx="180" cy="60" r="8" fill="#38BDF8"/>
        <circle cx="500" cy="60" r="6" fill="#4C6FFF"/><circle cx="740" cy="60" r="6" fill="#4C6FFF"/>
        <circle cx="980" cy="60" r="8" fill="#0A0E1A" stroke="#38BDF8" stroke-width="5"/>
        <text x="20" y="34" class="big">EC500</text><text x="20" y="92">500 kW · first module</text>
        <text x="180" y="34" class="big">EC1000</text><text x="180" y="92">1 MW block</text>
        <text x="500" y="34" text-anchor="middle" class="big">5 MW</text><text x="500" y="92" text-anchor="middle">anchor offtake expansion</text>
        <text x="740" y="34" text-anchor="middle" class="big">10 MW</text>
        <text x="980" y="34" text-anchor="end" class="big">20 MW</text><text x="980" y="92" text-anchor="end">full site envelope</text>
      </svg>
    </div>
    <div class="numbers">
      <div><b>90–180 days</b><span>to live</span></div>
      <div><b>Under 30 ms</b><span>at the edge</span></div>
      <div><b>Zero</b><span>community water draw</span></div>
      <div><b>1 GW+</b><span>land-to-power pipeline</span></div>
    </div>
  </div>
</div></section>

<hr class="rule">
<section id="buy"><div class="wrap row">
  <div class="k">How you buy</div>
  <div>
    <h2>Anchor, reserve, or spot.</h2>
    <div class="tiers">
      <div class="tier"><div><h3>Anchor offtake</h3><span class="term">5 years and longer, take-or-pay</span></div><p>Dedicated capacity under a long-term NNN agreement. Covers the facility's fixed costs before a single spot GPU hour is sold.</p></div>
      <div class="tier"><div><h3>Reserved capacity</h3><span class="term">2 years, fractional</span></div><p>Reserve blocks at mid-tier pricing without committing to 100% utilization.</p></div>
      <div class="tier"><div><h3>Spot and preemptible</h3><span class="term">On demand</span></div><p>GPU time on idle capacity at spot rates. For batch inference, evaluation, and bursty work.</p></div>
    </div>
  </div>
</div></section>

<hr class="rule">
<section id="where"><div class="wrap row">
  <div class="k">Where</div>
  <div>
    <h2>Four launch sites, then 20 MW per state.</h2>
    <ul class="sites">
      <li>Phoenix <span>Arizona</span></li><li>Dallas <span>Texas</span></li><li>Newcastle <span>England</span></li><li>Leeds <span>England</span></li>
    </ul>
    <div class="body one" style="margin-top:22px"><p>The first four facilities are 500 kW each. From there the template repeats across 30 U.S. states and the United Kingdom, with an orchestration layer that routes work across sites and fails over between them.</p></div>
  </div>
</div></section>

<hr class="rule">
<section id="contact"><div class="wrap row">
  <div class="k">Contact</div>
  <div class="contact-wrap">
    <h2>Tell us the workload, the region, and the latency budget.</h2>
    <p style="margin-top:18px;color:var(--ink-2)">Or write to <a class="mail" href="mailto:contact@andd.ai">contact@andd.ai</a>.</p>
    ''' + FORM + '''
  </div>
</div></section>

<hr class="rule">
<footer><div class="wrap">
  ''' + LOGO + '''
  <nav><a href="#why">Why now</a><a href="#build">What we build</a><a href="#buy">How you buy</a><a href="#contact">Contact</a></nav>
  <span>© 2026 Native Networks · andd.ai</span>
</div></footer>
<script>''' + FORM_JS + '''document.getElementById('form-success').hidden = true;
(function(){ const p = document.querySelector('.hero-mark .signal'); if (!p) return; if (matchMedia('(prefers-reduced-motion: reduce)').matches) return; p.classList.add('draw'); })();</script>
'''

# ----------------------------------------------------------------------------
# C. FIELD — map first, data forward
# ----------------------------------------------------------------------------

US_PATH = "M 125,491 L 564,491 L 680,559 L 722,551 L 752,567 L 758,620 L 763,626 L 926,568 L 965,521 L 1002,572 L 944,608 L 954,632 L 893,650 L 869,676 L 862,723 L 811,778 L 777,838 L 791,878 L 797,924 L 797,931 L 785,941 L 779,941 L 752,897 L 731,850 L 677,845 L 654,866 L 625,868 L 577,859 L 540,885 L 530,930 L 496,918 L 461,858 L 437,871 L 383,819 L 353,819 L 313,828 L 255,801 L 216,805 L 161,766 L 134,705 L 102,656 L 97,504 L 125,491 Z"
US_BBOX = (97, 491, 1002, 943)
UK_PATH = "M 1219,331 L 1298,331 L 1349,411 L 1344,459 L 1359,518 L 1325,560 L 1359,596 L 1366,621 L 1364,629 L 1348,639 L 1345,658 L 1360,673 L 1380,669 L 1387,672 L 1463,769 L 1465,830 L 1536,853 L 1531,905 L 1516,931 L 1520,968 L 1501,977 L 1520,994 L 1480,1021 L 1408,1021 L 1277,1038 L 1236,1066 L 1192,1083 L 1159,1083 L 1215,1043 L 1234,983 L 1254,983 L 1258,979 L 1230,951 L 1195,951 L 1195,947 L 1212,939 L 1178,923 L 1211,900 L 1238,837 L 1233,826 L 1217,814 L 1217,807 L 1213,803 L 1209,806 L 1204,798 L 1286,789 L 1291,781 L 1294,755 L 1289,744 L 1264,729 L 1273,665 L 1265,661 L 1194,669 L 1185,622 L 1181,618 L 1163,624 L 1175,597 L 1180,607 L 1186,603 L 1180,596 L 1180,587 L 1188,568 L 1171,510 L 1153,420 L 1179,357 L 1219,331 Z"
UK_BBOX = (1153, 331, 1536, 1083)

def node(x, y, name, dx=18, dy=6, anchor='start'):
    return f'''<g class="site"><circle cx="{x}" cy="{y}" r="34" class="halo"/><circle cx="{x}" cy="{y}" r="13" fill="#38BDF8"/><circle cx="{x}" cy="{y}" r="6" fill="#0A0E1A"/>
<text x="{x+dx}" y="{y+dy}" text-anchor="{anchor}">{name}</text></g>'''

FIELD = HEAD.format(title='Native Networks', fonts='IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500') + '''
<style>
:root {
  --bg: #0A0E1A; --surface: #111A30; --surface-2: #19223E;
  --line: #24305A; --line-soft: #1A2447;
  --indigo: #4C6FFF; --indigo-hi: #6383FF; --indigo-fill: #454FC4; --sky: #38BDF8; --navy: #1E2F72;
  --ink-0: #FFFFFF; --ink-1: #C8CEE0; --ink-2: #9AA4BD; --ink-3: #6B7488;
  --radius: 6px; --font: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif; --mono: 'IBM Plex Mono', ui-monospace, Menlo, monospace;
  --pad: clamp(3.5rem, 7vw, 6.5rem);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink-1); font-family: var(--font); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { color: var(--ink-0); margin: 0; font-weight: 500; letter-spacing: -0.02em; text-wrap: balance; }
p { margin: 0; }
.wrap { width: min(1200px, calc(100% - 2 * clamp(1.25rem, 4vw, 3rem))); margin-inline: auto; }
.data { font-family: var(--mono); font-variant-numeric: tabular-nums; }

.nav { border-bottom: 1px solid var(--line-soft); }
.nav .wrap { display: flex; align-items: center; justify-content: space-between; height: 70px; gap: 24px; }
.logo { display: inline-flex; align-items: center; gap: 12px; }
.logo .mark { width: 40px; height: 34px; }
.wordmark { font-weight: 600; font-size: 1.12rem; color: var(--ink-0); white-space: nowrap; }
.nav-links { display: flex; gap: 28px; font-size: 0.92rem; color: var(--ink-2); }
.nav-links a:hover { color: var(--ink-0); }
.nav .btn { padding: 9px 16px; font-size: 0.9rem; }

.hero { padding: clamp(3rem, 6vw, 5rem) 0 0; }
.hero .top { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); gap: 48px; align-items: end; margin-bottom: 40px; }
.hero h1 { font-size: clamp(2.3rem, 4.4vw, 3.7rem); line-height: 1.06; max-width: 15ch; }
.hero .dek { color: var(--ink-2); font-size: 1.1rem; max-width: 44ch; }
.hero .dek .ctas { margin-top: 22px; display: flex; gap: 10px; flex-wrap: wrap; }

.map { border: 1px solid var(--line); border-radius: var(--radius); background: var(--surface); padding: 26px 28px 18px; display: grid; grid-template-columns: minmax(0, 1.7fr) minmax(0, 0.55fr); gap: 24px; align-items: end; position: relative; }
.map .region { position: relative; }
.map .region h3 { font-size: 0.8rem; color: var(--ink-3); font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 8px; }
.map svg { width: 100%; height: auto; display: block; overflow: visible; }
.map .land { fill: var(--surface-2); stroke: #2F4290; stroke-width: 2; stroke-linejoin: round; }
.map .site text { font-family: var(--font); font-size: 26px; fill: var(--ink-0); font-weight: 500; }
.map .uk .site text { font-size: 30px; }
.map .halo { fill: #38BDF8; opacity: 0.16; transform-origin: center; transform-box: fill-box; animation: pulse 3.2s ease-in-out infinite; }
.map .site:nth-child(2) .halo { animation-delay: 0.8s; }
@keyframes pulse { 0%, 100% { transform: scale(0.7); opacity: 0.18; } 50% { transform: scale(1.15); opacity: 0.05; } }
.map .legend { grid-column: 1 / -1; display: flex; gap: 32px; flex-wrap: wrap; border-top: 1px solid var(--line-soft); padding-top: 14px; font-size: 0.85rem; color: var(--ink-2); }
.map .legend b { color: var(--ink-0); font-weight: 500; }
.map .legend .dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--sky); margin-right: 8px; vertical-align: 1px; }

.strip { margin-top: 18px; display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--line); border-radius: var(--radius); }
.strip div { padding: 18px 22px; border-left: 1px solid var(--line-soft); }
.strip div:first-child { border-left: 0; }
.strip b { display: block; color: var(--ink-0); font-weight: 500; font-size: 1.35rem; letter-spacing: -0.01em; }
.strip span { color: var(--ink-2); font-size: 0.86rem; }

section.block { padding: var(--pad) 0; border-top: 1px solid var(--line-soft); }
section.block.first { border-top: 0; }
.sec-head { max-width: 700px; margin-bottom: 36px; }
.sec-head h2 { font-size: clamp(1.7rem, 2.9vw, 2.4rem); line-height: 1.12; margin-bottom: 12px; }
.sec-head p { color: var(--ink-2); font-size: 1.05rem; }

.split { display: grid; grid-template-columns: minmax(0, 0.7fr) minmax(0, 1.3fr); gap: 48px; align-items: center; }
.split figure { margin: 0; border-radius: var(--radius); overflow: hidden; border: 1px solid var(--line-soft); aspect-ratio: 3 / 4; max-height: 520px; }
.split figure img { width: 100%; height: 100%; object-fit: cover; display: block; }
.points { display: grid; gap: 22px; }
.points p { color: var(--ink-2); max-width: 56ch; }
.points p b { display: block; color: var(--ink-0); font-weight: 500; margin-bottom: 3px; }

table { width: 100%; border-collapse: collapse; font-size: 0.98rem; }
th, td { text-align: left; padding: 16px 18px; border-top: 1px solid var(--line-soft); vertical-align: top; }
thead th { color: var(--ink-3); font-weight: 500; font-size: 0.82rem; letter-spacing: 0.04em; text-transform: uppercase; border-top: 0; padding-top: 0; }
tbody th { color: var(--ink-1); font-weight: 400; width: 26%; }
td { color: var(--ink-2); }
td.us { color: var(--ink-0); background: rgba(76,111,255,0.08); }
thead th.us { color: var(--sky); }
.table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); padding: 18px 4px 4px; background: var(--surface); }
tbody tr:last-child td, tbody tr:last-child th { border-bottom: 0; }

.tiers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.tier { border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; }
.tier h3 { font-size: 1.1rem; margin-bottom: 4px; }
.tier .term { color: var(--sky); font-size: 0.88rem; display: block; margin-bottom: 12px; }
.tier p { color: var(--ink-2); font-size: 0.95rem; }

.contact { display: grid; grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr); gap: 56px; align-items: start; }
.contact h2 { font-size: clamp(1.7rem, 2.9vw, 2.4rem); line-height: 1.12; margin-bottom: 14px; }
.contact .lead { color: var(--ink-2); font-size: 1.05rem; margin-bottom: 20px; }
.contact .mail { color: var(--sky); font-weight: 500; }

footer { border-top: 1px solid var(--line-soft); }
footer .wrap { display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; padding: 34px 0; color: var(--ink-3); font-size: 0.88rem; }
footer nav { display: flex; gap: 20px; }
footer nav a:hover { color: var(--ink-0); }
''' + FORM_CSS + '''
@media (max-width: 960px) {
  .nav-links { display: none; }
  .hero .top, .split, .contact, .tiers { grid-template-columns: 1fr; }
  .map { grid-template-columns: 1fr; }
  .map .uk { max-width: 240px; }
  .strip { grid-template-columns: 1fr 1fr; }
  .strip div:nth-child(3) { border-left: 0; border-top: 1px solid var(--line-soft); }
  .strip div:nth-child(4) { border-top: 1px solid var(--line-soft); }
  .split figure { max-height: 380px; aspect-ratio: 4 / 3; }
}
@media (max-width: 520px) { .strip { grid-template-columns: 1fr; } .strip div { border-left: 0; border-top: 1px solid var(--line-soft); } .strip div:first-child { border-top: 0; } }
</style>

<a id="top"></a>
<header class="nav"><div class="wrap">
  ''' + LOGO + '''
  <nav class="nav-links"><a href="#why">Why now</a><a href="#modules">Modules</a><a href="#compare">Compare</a><a href="#buy">How you buy</a></nav>
  <a class="btn btn-primary" href="#contact">Talk to us</a>
</div></header>

<section class="hero"><div class="wrap">
  <div class="top">
    <h1>The distributed layer between the hyperscale core and the device.</h1>
    <div class="dek"><p>Small modular AI datacenters, 500 kW to 20 MW, sited where power and fiber already exist. Inference runs locally instead of round-tripping to a distant cloud.</p>
      <div class="ctas"><a class="btn btn-primary" href="#contact">Talk to us</a><a class="btn" href="#modules">See the modules</a></div></div>
  </div>
  <div class="map" aria-label="Launch sites in the United States and the United Kingdom">
    <div class="region us"><h3>United States</h3>
      <svg viewBox="70 470 960 500"><path class="land" d="''' + US_PATH + '''"/>
        ''' + node(297, 785, 'Phoenix', dx=-20, dy=-30, anchor='start') + node(535, 797, 'Dallas', dx=26, dy=8) + '''
      </svg></div>
    <div class="region uk"><h3>United Kingdom</h3>
      <svg viewBox="1130 310 440 790"><path class="land" d="''' + UK_PATH + '''"/>
        ''' + node(1367, 650, 'Newcastle', dx=-22, dy=-26, anchor='end') + node(1370, 755, 'Leeds', dx=-24, dy=10, anchor='end') + '''
      </svg></div>
    <div class="legend"><span><span class="dot"></span><b>Four launch sites</b>, 500 kW each</span><span><b>1 GW and more</b> of land-to-power pipeline under development</span><span>Next: <b>20 MW per state</b> across 30 U.S. states</span></div>
  </div>
  <div class="strip">
    <div><b class="data">500 kW – 20 MW</b><span>per site, grown as demand is contracted</span></div>
    <div><b class="data">90 – 180 days</b><span>from site selection to live</span></div>
    <div><b class="data">&lt; 30 ms</b><span>round trip at the edge</span></div>
    <div><b class="data">0 water</b><span>drawn from the community</span></div>
  </div>
</div></section>

<section class="block" id="why"><div class="wrap split">
  <figure><img src="assets/rack.jpg" alt="Illustration of an empty server rack in a dark room" width="1068" height="1600"></figure>
  <div>
    <div class="sec-head"><h2>Inference is moving to the edge, and the edge layer is unowned.</h2></div>
    <div class="points">
      <p><b>Inference dominates compute.</b> It is now the majority of AI compute and growing faster than training. The shift from model-building to model-deployment is structural and accelerating.</p>
      <p><b>Latency tolerance is gone.</b> Real-time voice, agentic sessions, inline security, and physical AI cannot tolerate a distant round trip. A rising share of workloads demands local, sub-20 ms response.</p>
      <p><b>Hyperscale cannot fill the demand.</b> It was engineered for centralized, batch-oriented training, and new capacity is stalled by power and water scarcity, permitting backlogs, and community opposition.</p>
      <p><b>So the layer does not exist yet.</b> Real-time voice, agentic AI, inline security, and physical AI have nowhere to run at the edge. That is what we build.</p>
    </div>
  </div>
</div></section>

<section class="block" id="modules"><div class="wrap">
  <div class="sec-head"><h2>Two modules, one template, sited on existing power.</h2>
    <p>A facility starts with a single module and expands to 20 MW as demand is contracted. Capital follows commitment, not speculation.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th></th><th class="us">EC500</th><th class="us">EC1000</th></tr></thead>
    <tbody>
      <tr><th>Capacity</th><td class="us data">500 kW</td><td class="us data">1 MW</td></tr>
      <tr><th>Accelerator racks</th><td class="us">3 NVL72-class racks</td><td class="us">6 NVL72-class racks</td></tr>
      <tr><th>Foundation</th><td class="us">Relocatable precast, no cure cycle</td><td class="us">Relocatable precast, no cure cycle</td></tr>
      <tr><th>Power</th><td class="us">Existing utility capacity: co-ops, municipals, cell sites, IOUs, RTOs</td><td class="us">Existing utility capacity, rates locked before deployment</td></tr>
      <tr><th>Connectivity</th><td class="us">Carrier-adjacent, bonded fiber, Starlink backup</td><td class="us">Carrier-adjacent, bonded fiber, Starlink backup</td></tr>
      <tr><th>Water and noise</th><td class="us">No community water draw, minimal noise</td><td class="us">No community water draw, minimal noise</td></tr>
      <tr><th>Time to live</th><td class="us data">90 – 180 days</td><td class="us data">90 – 180 days</td></tr>
    </tbody>
  </table></div>
</div></section>

<section class="block" id="compare"><div class="wrap">
  <div class="sec-head"><h2>Cheaper and faster, by design.</h2>
    <p>The same inference capacity for roughly half the capital, delivered five to ten times faster.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th></th><th>Traditional hyperscale</th><th class="us">Native Networks modular</th></tr></thead>
    <tbody>
      <tr><th>Time to deployment</th><td class="data">36 – 60 months</td><td class="us data">90 – 180 days</td></tr>
      <tr><th>Capital per megawatt</th><td>Baseline</td><td class="us">About half, all-in: interconnect, civils, permitting, security</td></tr>
      <tr><th>Foundations</th><td>Poured concrete, long cure cycles</td><td class="us">Relocatable precast, no cure cycle</td></tr>
      <tr><th>Permitting</th><td>12 to 18 month queues</td><td class="us">Streamlined through modular classification</td></tr>
      <tr><th>Construction</th><td>Linear, no parallelism</td><td class="us">Parallel tracks compress the schedule</td></tr>
      <tr><th>Community</th><td>Water draw, noise, years of opposition</td><td class="us">No water draw, minimal noise</td></tr>
    </tbody>
  </table></div>
</div></section>

<section class="block" id="buy"><div class="wrap">
  <div class="sec-head"><h2>Three ways to buy capacity.</h2></div>
  <div class="tiers">
    <div class="tier"><h3>Anchor offtake</h3><span class="term">5 years and longer, take-or-pay</span><p>Dedicated capacity under a long-term NNN agreement. Covers the facility's fixed costs before a single spot GPU hour is sold.</p></div>
    <div class="tier"><h3>Reserved capacity</h3><span class="term">2 years, fractional</span><p>Reserve blocks at mid-tier pricing without committing to 100% utilization.</p></div>
    <div class="tier"><h3>Spot and preemptible</h3><span class="term">On demand</span><p>GPU time on idle capacity at spot rates. For batch inference, evaluation, and bursty work.</p></div>
  </div>
</div></section>

<section class="block" id="contact"><div class="wrap contact">
  <div><h2>Tell us the workload, the region, and the latency budget.</h2>
    <p class="lead">Carriers, utilities, AI model providers, and enterprises with real-time workloads: we will come back with a site plan.</p>
    <a class="mail" href="mailto:contact@andd.ai">contact@andd.ai</a></div>
  <div>''' + FORM + '''</div>
</div></section>

<footer><div class="wrap">
  ''' + LOGO + '''
  <nav><a href="#why">Why now</a><a href="#modules">Modules</a><a href="#compare">Compare</a><a href="#contact">Contact</a></nav>
  <span>© 2026 Native Networks · andd.ai</span>
</div></footer>
<script>''' + FORM_JS + '''document.getElementById('form-success').hidden = true;</script>
'''

DOCTYPE = '<!DOCTYPE html>\n<html lang="en">\n<head>\n'

def wrap(body):
    # Split head (meta/link/title/style) from body content at the first <a id="top">
    head, rest = body.split('<a id="top"></a>', 1)
    return DOCTYPE + head + '</head>\n<body>\n<a id="top"></a>' + rest + '\n</body>\n</html>\n'

for name, html in [('signal', SIGNAL), ('mesh', MESH), ('field', FIELD)]:
    (OUT / f'{name}.html').write_text(wrap(html))
    # Artifact version: no doctype/html/head/body wrappers
    (OUT / f'{name}.artifact.html').write_text(html)
    print('wrote', name)
