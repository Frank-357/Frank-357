"""Generate the profile's SVG banner and diagrams into ../assets/.

Every number and label below comes from Frank's resume (2026-10-28) or his
bullet bank. Edit the text here and re-run:  python3 scripts/build_assets.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Avenir Next','Avenir','Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',Times,serif"
MONO = "'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# Card palette: one dark surface so the images read the same in GitHub light and dark mode.
SURFACE = "#0f1626"
BORDER = "#24304a"
TEXT = "#e8eef5"
TEXT2 = "#aab6c8"
MUTED = "#7c8aa0"
# Categorical slots (validated on #0f1626: CVD ΔE 8.4, normal-vision ΔE 19.8, all ≥ 3:1).
BLUE, ORANGE, AQUA, GOLD = "#3987e5", "#d95926", "#199e70", "#c98500"
MAROON = "#800000"
ROSE = "#e07a8a"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", OUT / name)


def card_open(w, h, title, desc, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title>
<desc id="d">{esc(desc)}</desc>
<style>
text{{font-family:{SANS}}}
.h{{font-size:24px;font-weight:600;fill:{TEXT}}}
.sub{{font-size:15px;fill:{MUTED};letter-spacing:.4px}}
.lbl{{font-size:15px;fill:{TEXT}}}
.lbl2{{font-size:13px;fill:{TEXT2}}}
.cap{{font-size:12px;fill:{MUTED};letter-spacing:1.4px;text-transform:uppercase}}
.mono{{font-family:{MONO};font-size:13px;fill:{TEXT2}}}
{extra_css}
{REDUCED}
@media (prefers-reduced-motion: reduce){{.flow{{display:none}}}}
</style>
<defs>
<linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0c1322"/><stop offset=".7" stop-color="{SURFACE}"/><stop offset="1" stop-color="#1c1020"/>
</linearGradient>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M0,0 L10,5 L0,10 z" fill="{TEXT2}"/></marker>
<clipPath id="cardclip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#cardbg)"/>
<rect x="0" y="0" width="{w}" height="5" fill="{MAROON}" clip-path="url(#cardclip)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
"""


def box(x, y, w, h, title, lines=(), color=BLUE, title_size=15):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#131d31" stroke="{color}" stroke-width="1.6"/>',
           f'<rect x="{x}" y="{y+10}" width="4" height="{h-20}" rx="2" fill="{color}"/>',
           f'<text x="{x+16}" y="{y+26}" style="font-size:{title_size}px;font-weight:600;fill:{TEXT}">{esc(title)}</text>']
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x+16}" y="{y+48+i*19}" class="lbl2">{esc(ln)}</text>')
    return "\n".join(out)


def arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="5 5"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TEXT2}" stroke-width="1.6"{d} marker-end="url(#arr)"/>'


# --------------------------------------------------------------------------- banner
def banner():
    W, H = 1600, 500
    rnd = random.Random(357)
    ox, oy = W + 10, 262  # fibers converge at the right edge, like light leaving a cable
    fibers, pulses, dots = [], [], []
    for i in range(46):
        ex = rnd.uniform(820, 1480)
        ey = rnd.uniform(-40, H + 40)
        c1x, c1y = rnd.uniform(1250, 1500), oy + rnd.uniform(-30, 30)
        c2x, c2y = rnd.uniform(800, 1300), ey + rnd.uniform(-120, 120)
        d = f"M{ox:.0f},{oy:.0f} C{c1x:.0f},{c1y:.0f} {c2x:.0f},{c2y:.0f} {ex:.0f},{ey:.0f}"
        op = rnd.uniform(.10, .32)
        fibers.append(f'<path d="{d}" stroke="#ffc9d1" stroke-opacity="{op:.2f}" stroke-width="{rnd.uniform(.6,1.3):.2f}" fill="none"/>')
        if i % 3 == 0:
            dur = rnd.uniform(5, 11)
            delay = rnd.uniform(0, 8)
            pulses.append(f'<path d="{d}" class="pulse" style="animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s" fill="none"/>')
        if i % 2 == 0:
            t = rnd.uniform(.45, .9)
            # point on the cubic at t
            mt = 1 - t
            px = mt**3*ox + 3*mt*mt*t*c1x + 3*mt*t*t*c2x + t**3*ex
            py = mt**3*oy + 3*mt*mt*t*c1y + 3*mt*t*t*c2y + t**3*ey
            dots.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(1.6,3):.1f}" class="dot" style="animation-delay:-{rnd.uniform(0,6):.1f}s"/>')

    # faint candlestick strip — a finance motif, not data
    candles = []
    price = 0.0
    for k in range(64):
        x = 70 + k * 22
        o = price
        price += rnd.gauss(0.1, 1.0)
        c = price
        hi = max(o, c) + abs(rnd.gauss(0, .6))
        lo = min(o, c) - abs(rnd.gauss(0, .6))
        sy = lambda v: 470 - (v + 6) * 4.2
        up = c >= o
        col = "#7fb3ff" if up else "#ff8a98"
        candles.append(f'<line x1="{x+4}" y1="{sy(hi):.1f}" x2="{x+4}" y2="{sy(lo):.1f}" stroke="{col}"/>'
                       f'<rect x="{x}" y="{sy(max(o,c)):.1f}" width="8" height="{max(abs(sy(o)-sy(c)),1.2):.1f}" fill="{col}"/>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Zijie (Frank) Guo — Quantitative research × data science</title>
<desc id="d">Banner: Zijie (Frank) Guo, MS Applied Data Science at the University of Chicago, expected June 2028. Dongxing Securities, Financial Street Securities, George Washington University, CFA Level I passed.</desc>
<style>
text{{font-family:{SANS}}}
.pulse{{stroke:#fff;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:60 1400;stroke-dashoffset:1460;animation:flow linear infinite;opacity:.75}}
@keyframes flow{{to{{stroke-dashoffset:0}}}}
.dot{{fill:#ffd9df;animation:tw 4.5s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.95}}}}
.spark{{animation:tw 6s ease-in-out infinite}}
.fade{{opacity:0;animation:in 1.2s ease-out forwards}}
@keyframes in{{to{{opacity:1}}}}
{REDUCED}
@media (prefers-reduced-motion: reduce){{.fade{{opacity:1}}}}
</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#060a17"/><stop offset=".5" stop-color="#140c1d"/><stop offset=".82" stop-color="#3a0712"/><stop offset="1" stop-color="#5c0d1a"/>
</linearGradient>
<radialGradient id="glow" cx="1" cy=".52" r=".55">
<stop offset="0" stop-color="#ff9aa8" stop-opacity=".55"/><stop offset=".25" stop-color="#b3172e" stop-opacity=".35"/><stop offset="1" stop-color="#800000" stop-opacity="0"/>
</radialGradient>
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
<stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset=".78" stop-color="#fff" stop-opacity="1"/>
</linearGradient>
<mask id="fiberMask"><rect width="{W}" height="{H}" fill="url(#fadeL)"/></mask>
<linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="84" y1="0" x2="1520" y2="0"><stop offset="0" stop-color="#c9d6e6" stop-opacity=".55"/><stop offset="1" stop-color="#c9d6e6" stop-opacity=".15"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<g opacity=".07">{''.join(candles)}</g>
<g mask="url(#fiberMask)">{''.join(fibers)}{''.join(pulses)}{''.join(dots)}</g>

<g class="fade">
<text x="1530" y="74" text-anchor="end" style="font-family:{SERIF};font-size:21px;letter-spacing:2.2px;fill:#f3f5f8">THE UNIVERSITY OF</text>
<text x="1530" y="128" text-anchor="end" style="font-family:{SERIF};font-size:54px;letter-spacing:1.5px;fill:#f3f5f8">CHICAGO</text>
<line x1="1262" y1="146" x2="1530" y2="146" stroke="#f3f5f8" stroke-opacity=".7"/>
<text x="1530" y="176" text-anchor="end" style="font-size:20px;font-weight:700;letter-spacing:1.2px;fill:#f3f5f8">MS–APPLIED DATA SCIENCE</text>
</g>

<g class="fade" style="animation-delay:.2s">
<text x="80" y="262" style="font-size:94px;font-weight:300;letter-spacing:3px;fill:#e4f1f4">ZIJIE (FRANK) GUO</text>
<text x="84" y="322" style="font-size:29px;font-weight:400;letter-spacing:3.2px;fill:#d7e2ea">QUANTITATIVE RESEARCH × DATA SCIENCE × AI ENGINEERING</text>
<text x="84" y="364" style="font-size:29px;font-weight:400;letter-spacing:3.2px;fill:#d7e2ea">MS APPLIED DATA SCIENCE – UNIVERSITY OF CHICAGO, 2028</text>
</g>
<line x1="84" y1="408" x2="1520" y2="408" stroke="url(#rule)" stroke-width="1.6"/>
<path class="spark" d="M1490,388 q4,16 20,20 q-16,4 -20,20 q-4,-16 -20,-20 q16,-4 20,-20z" fill="#d8dee8" fill-opacity=".55"/>
<text x="84" y="452" class="fade" style="animation-delay:.45s;font-size:20px;letter-spacing:2.4px;fill:#c5d0dc">DONGXING SECURITIES  |  FINANCIAL STREET SECURITIES  |  GEORGE WASHINGTON UNIVERSITY  |  CFA LEVEL I</text>
</svg>"""
    write("banner.svg", svg)


# --------------------------------------------------------------------------- stats
def stats():
    W, H = 1200, 330
    tiles = [
        ("80+", "alpha factors analyzed across", "IF / IC / IM equity-index futures", "Dongxing Securities · CTA desk", BLUE),
        ("4,622", "cloud trials across", "19 signal families", "Autonomous Factor Research Harness", AQUA),
        ("197", "sign-flipped factors removed by", "schema validation (30% of archive)", "Autonomous Factor Research Harness", AQUA),
        ("~120 s → <1 s", "recurring-query latency after the", "hybrid LangGraph re-architecture", "Procurement Pilot", ORANGE),
        ("¥1.45B", "bond underwriting supported; due", "diligence on 30+ enterprises", "Financial Street Securities", GOLD),
        ("Faculty Choice", "Award, GW Business Analytics", "Capstone (four-person team)", "Procurement Pilot", ORANGE),
    ]
    css = (".big{font-size:40px;font-weight:600;fill:%s;letter-spacing:.5px}"
           ".tile{opacity:0;animation:in .8s ease-out forwards}"
           "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
           "@media (prefers-reduced-motion: reduce){.tile{opacity:1}}") % TEXT
    out = [card_open(W, H, "At a glance", "Six headline numbers from Frank's resume.", css)]
    tw, th, gx, gy, x0, y0 = 373, 132, 16, 16, 24, 30
    for i, (big, l1, l2, src, col) in enumerate(tiles):
        cx, cy = x0 + (i % 3) * (tw + gx), y0 + (i // 3) * (th + gy)
        size = 40 if len(big) < 8 else 30
        out.append(f'<g class="tile" style="animation-delay:{i*.12:.2f}s">'
                   f'<rect x="{cx}" y="{cy}" width="{tw}" height="{th}" rx="12" fill="#131d31" stroke="{BORDER}"/>'
                   f'<rect x="{cx}" y="{cy+16}" width="4" height="{th-32}" rx="2" fill="{col}"/>'
                   f'<text x="{cx+22}" y="{cy+50}" class="big" style="font-size:{size}px">{esc(big)}</text>'
                   f'<text x="{cx+22}" y="{cy+78}" class="lbl2">{esc(l1)}</text>'
                   f'<text x="{cx+22}" y="{cy+96}" class="lbl2">{esc(l2)}</text>'
                   f'<text x="{cx+22}" y="{cy+120}" class="cap" style="font-size:11px">{esc(src)}</text></g>')
    out.append("</svg>")
    write("stats.svg", "\n".join(out))


# --------------------------------------------------------------------------- harness
def harness():
    W, H = 1200, 470
    css = (".flow{stroke:%s;stroke-width:3;stroke-linecap:round;stroke-dasharray:14 900;animation:run 4s linear infinite}"
           "@keyframes run{from{stroke-dashoffset:914}to{stroke-dashoffset:0}}") % ROSE
    o = [card_open(W, H, "Autonomous Factor Research Harness",
                   "An LLM agent proposes factor expressions; a fixed, agent-immutable evaluator applies discovery 2021, "
                   "validation 2022 and holdout 2023 gates plus correlation de-duplication. 4,622 cloud trials across 19 signal families; "
                   "schema-level validation removed 197 sign-flipped factors, 30% of the archive.", css)]
    o.append(f'<text x="32" y="50" class="h">Autonomous Factor Research Harness</text>')
    o.append(f'<text x="32" y="74" class="sub">Microsoft Qlib · Karpathy\'s autoresearch loop adapted to factor research · Feb 2026 – present</text>')

    o.append(f'<path d="M137,168 L1095,168" class="flow" fill="none"/>')
    # agent
    o.append(box(32, 116, 210, 104, "LLM agent", ["proposes factor", "expressions"], ROSE))
    # evaluator frame
    o.append(f'<rect x="282" y="98" width="700" height="140" rx="14" fill="none" stroke="{TEXT2}" stroke-opacity=".5" stroke-dasharray="6 6"/>')
    o.append(f'<text x="298" y="120" class="cap">Fixed, agent-immutable evaluator</text>')
    gates = [("Discovery", "2021", BLUE), ("Validation", "2022", BLUE), ("Holdout", "2023", BLUE), ("Correlation", "de-dup", AQUA)]
    gx = 300
    for i, (a, b, col) in enumerate(gates):
        o.append(box(gx, 136, 150, 84, a, [b], col))
        if i < 3:
            o.append(arrow(gx + 150, 178, gx + 172, 178))
        gx += 172
    o.append(arrow(242, 168, 298, 168))
    o.append(box(1022, 116, 146, 104, "Factor", ["archive"], GOLD))
    o.append(arrow(982, 168, 1020, 168))
    # loop back
    o.append(f'<path d="M1095,220 C1095,280 137,280 137,222" fill="none" stroke="{TEXT2}" stroke-width="1.4" stroke-dasharray="5 6" marker-end="url(#arr)"/>')
    o.append(f'<text x="600" y="276" text-anchor="middle" class="lbl2">results feed the next proposal</text>')

    # findings
    finds = [
        ("Scale", ["4,622 cloud trials", "across 19 signal families"], AQUA),
        ("Audit", ["A documented holdout gate was never", "enforced in code → added schema-level", "validation; removed 197 sign-flipped", "factors (30% of the archive)"], ORANGE),
        ("Attribution", ["Lead strategy showed a significant", "cash/beta contribution, not pure alpha", "→ repositioned as a reproducible", "research platform"], GOLD),
    ]
    fx = 32
    widths = [318, 418, 418]
    for (t, lines, col), w in zip(finds, widths):
        o.append(box(fx, 308, w - 16, 136, t, lines, col))
        fx += w + 2
    o.append("</svg>")
    write("harness.svg", "\n".join(o))


# --------------------------------------------------------------------------- walk-forward
def walkforward():
    W, H = 1200, 450
    css = (".scan{fill:#fff;opacity:.10;animation:scan 6s ease-in-out infinite}"
           "@keyframes scan{0%{transform:translateX(0)}50%{transform:translateX(150px)}100%{transform:translateX(0)}}")
    o = [card_open(W, H, "CTA factor research at Dongxing Securities",
                   "80+ alpha factors on IF, IC and IM futures; XGBoost with 5-fold rolling validation, ranked by mean feature importance "
                   "and cross-fold stability to select the top 30. Sliding-window out-of-sample validation with 12-month training and 3-month "
                   "validation windows, net of costs.", css)]
    o.append('<text x="32" y="50" class="h">CTA factor research — Dongxing Securities</text>')
    o.append('<text x="32" y="74" class="sub">Quantitative Research Intern, CTA Desk · Shanghai · Jul – Aug 2025 · Python, XGBoost</text>')

    # funnel (left)
    steps = [("80+ candidate factors", "price · volume · order flow · market depth", 400, BLUE),
             ("Lag-only feature pipeline", "per-window transforms · NaN-preserving + is_active", 360, BLUE),
             ("XGBoost · 5-fold rolling", "rank by mean importance + cross-fold stability", 320, AQUA),
             ("Top 30 factors", "carried into out-of-sample testing", 280, GOLD)]
    y = 104
    for t, s, w, col in steps:
        x = 32 + (400 - w) / 2
        o.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="62" rx="10" fill="#131d31" stroke="{col}" stroke-width="1.6"/>')
        o.append(f'<text x="232" y="{y+26}" text-anchor="middle" style="font-size:15px;font-weight:600;fill:{TEXT}">{esc(t)}</text>')
        o.append(f'<text x="232" y="{y+46}" text-anchor="middle" class="lbl2" style="font-size:12px">{esc(s)}</text>')
        if y < 104 + 3 * 80:
            o.append(arrow(232, y + 62, 232, y + 78))
        y += 80

    # walk-forward windows (right): 12m train + 3m validation, step 3m
    gx0, gy0, mpx = 480, 128, 14.0  # px per month
    o.append(f'<text x="{gx0}" y="112" class="cap">Sliding-window out-of-sample test · net of costs (schematic)</text>')
    for r in range(6):
        x = gx0 + r * 3 * mpx
        yy = gy0 + r * 40
        o.append(f'<text x="{gx0-8}" y="{yy+19}" text-anchor="end" class="mono" style="font-size:11px">w{r+1}</text>' if False else "")
        o.append(f'<rect x="{x:.1f}" y="{yy}" width="{12*mpx-2:.1f}" height="26" rx="4" fill="{BLUE}"/>')
        o.append(f'<rect x="{x+12*mpx:.1f}" y="{yy}" width="{3*mpx-2:.1f}" height="26" rx="4" fill="{ORANGE}"/>')
        if r == 0:
            o.append(f'<text x="{x+8:.1f}" y="{yy+18}" style="font-size:13px;font-weight:600;fill:#08101f">train · 12 months</text>')
            o.append(f'<text x="{x+15*mpx+10:.1f}" y="{yy+18}" class="lbl2">validate · 3 months</text>')
    axy = gy0 + 6 * 40 + 6
    o.append(f'<line x1="{gx0}" y1="{axy}" x2="{gx0+30*mpx}" y2="{axy}" stroke="{MUTED}" marker-end="url(#arr)"/>')
    o.append(f'<text x="{gx0+30*mpx+12}" y="{axy+4}" class="lbl2">time</text>')
    # legend + notes
    lx = 950
    o.append(f'<rect x="{lx}" y="132" width="14" height="14" rx="3" fill="{BLUE}"/><text x="{lx+22}" y="144" class="lbl2">training window</text>')
    o.append(f'<rect x="{lx}" y="158" width="14" height="14" rx="3" fill="{ORANGE}"/><text x="{lx+22}" y="170" class="lbl2">validation window</text>')
    notes = ["Each window steps forward; the", "model never sees its validation", "period during training.", "",
             "Reported: total & annualized", "return, Sharpe, max drawdown,", "win rate.", "",
             "Delivered scripts, notebooks,", "dashboards and documentation."]
    for i, n in enumerate(notes):
        o.append(f'<text x="{lx}" y="{210+i*20}" class="lbl2">{esc(n)}</text>')
    o.append("</svg>")
    write("walkforward.svg", "\n".join(o))


# --------------------------------------------------------------------------- procurement
def procurement():
    W, H = 1200, 480
    css = (".flow{stroke:%s;stroke-width:3;stroke-linecap:round;stroke-dasharray:14 1400;animation:run 5s linear infinite}"
           "@keyframes run{from{stroke-dashoffset:1414}to{stroke-dashoffset:0}}") % ROSE
    o = [card_open(W, H, "Procurement Pilot architecture",
                   "Hybrid LangGraph system: pre-execution request review, an LLM for open-ended intent and task planning, deterministic "
                   "parsers and direct analytics tools for decision-critical workflows, a Streamlit decision workflow and post-solve "
                   "approve, modify or discard controls, with execution traces. Recurring query execution went from about 120 seconds to sub-second.", css)]
    o.append('<text x="32" y="50" class="h">Procurement Pilot — hybrid LangGraph decision system</text>')
    o.append('<text x="32" y="74" class="sub">System Architect · four-person GW Business Analytics capstone · Jan – May 2026 · Faculty Choice Award</text>')

    o.append(f'<path d="M120,192 L440,192 L470,280 L740,280 L780,214 L1010,192" class="flow" fill="none"/>')
    o.append(box(32, 150, 170, 84, "User request", ["planning question"], TEXT2))
    o.append(box(232, 150, 180, 84, "Pre-execution", ["request review"], GOLD))
    o.append(arrow(202, 192, 230, 192))
    o.append(arrow(412, 192, 440, 192))
    # router frame
    o.append(f'<rect x="442" y="104" width="300" height="236" rx="14" fill="none" stroke="{TEXT2}" stroke-opacity=".5" stroke-dasharray="6 6"/>')
    o.append(f'<text x="458" y="126" class="cap">LangGraph router</text>')
    o.append(box(458, 138, 268, 84, "LLM", ["open-ended intent + task planning"], ROSE))
    o.append(box(458, 238, 268, 84, "Deterministic parsers", ["decision-critical workflows"], BLUE))
    # tools
    tools = ["Demand forecasting", "BOM requirements", "Inventory triggers", "Supplier risk scoring", "Executive summary"]
    o.append(f'<text x="782" y="126" class="cap">Analytics &amp; optimization modules (team-built)</text>')
    for i, t in enumerate(tools):
        yy = 138 + i * 40
        o.append(f'<rect x="782" y="{yy}" width="200" height="32" rx="8" fill="#131d31" stroke="{AQUA}" stroke-width="1.3"/>')
        o.append(f'<text x="796" y="{yy+21}" class="lbl" style="font-size:14px">{esc(t)}</text>')
    o.append(arrow(742, 222, 780, 222))
    o.append(box(1012, 150, 156, 84, "Streamlit", ["decision workflow"], ORANGE))
    o.append(arrow(982, 222, 1010, 200))
    # post-solve controls
    for i, (t, col) in enumerate([("Approve", AQUA), ("Modify", GOLD), ("Discard", ORANGE)]):
        yy = 254 + i * 30
        o.append(f'<rect x="1012" y="{yy}" width="156" height="24" rx="12" fill="none" stroke="{col}" stroke-width="1.4"/>')
        o.append(f'<text x="1090" y="{yy+17}" text-anchor="middle" class="lbl2">{t}</text>')
    o.append(f'<text x="1090" y="{254+3*30+10}" text-anchor="middle" class="cap" style="font-size:10px">post-solve human review</text>')

    # bottom: traces + latency hero
    o.append(f'<rect x="32" y="372" width="700" height="80" rx="12" fill="#131d31" stroke="{BORDER}"/>')
    o.append(f'<text x="50" y="400" class="cap">Execution traces</text>')
    o.append(f'<text x="50" y="428" class="lbl">agent selection · parameters · outputs · latency — kept auditable</text>')
    o.append(f'<rect x="752" y="372" width="416" height="80" rx="12" fill="#131d31" stroke="{BORDER}"/>')
    o.append(f'<text x="770" y="400" class="cap">Recurring query execution</text>')
    o.append(f'<text x="770" y="436" style="font-size:28px;font-weight:600;fill:{TEXT}">~120 s → sub-second</text>')
    o.append("</svg>")
    write("procurement.svg", "\n".join(o))


# --------------------------------------------------------------------------- timeline
def timeline():
    W, H = 1200, 400
    x0, x1 = 150, 1160
    y_start, y_end = 2023.0, 2029.0
    X = lambda t: x0 + (t - y_start) / (y_end - y_start) * (x1 - x0)
    m = lambda y, mo: y + (mo - 1) / 12  # month start
    css = ".now{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}"
    o = [card_open(W, H, "Path, 2023 to 2028",
                   "Financial Street Securities Jul–Aug 2023; Dongxing Securities Jul–Aug 2025; Procurement Pilot Jan–May 2026; "
                   "Factor Research Harness Feb 2026 to present; B.S. George Washington University May 2026; CFA Level I passed Aug 2026; "
                   "MS Applied Data Science University of Chicago through June 2028; seeking a Summer 2027 internship.", css)]
    o.append('<text x="32" y="50" class="h">Path</text>')
    lanes = [("Experience", 104), ("Projects", 172), ("Education", 240), ("Credentials", 296)]
    for name, y in lanes:
        o.append(f'<text x="32" y="{y+18}" class="cap">{name}</text>')
        o.append(f'<line x1="{x0}" y1="{y+13}" x2="{x1}" y2="{y+13}" stroke="{BORDER}"/>')
    for yr in range(2023, 2029):
        x = X(yr)
        o.append(f'<line x1="{x:.1f}" y1="92" x2="{x:.1f}" y2="330" stroke="{BORDER}" stroke-dasharray="2 4"/>')
        o.append(f'<text x="{x+4:.1f}" y="350" class="mono" style="font-size:13px">{yr}</text>')

    def bar(a, b, y, col, label, anchor="start", lx=None, h=26, ink=None):
        xa, xb = X(a), X(b)
        o.append(f'<rect x="{xa:.1f}" y="{y}" width="{max(xb-xa-2,6):.1f}" height="{h}" rx="4" fill="{col}"/>')
        tx = lx if lx is not None else xb + 8
        o.append(f'<text x="{tx:.1f}" y="{y+h/2+5:.0f}" text-anchor="{anchor}" class="lbl" style="font-size:13px{';font-weight:600;fill:' + ink if ink else ''}">{esc(label)}</text>')

    def milestone(t, y, col, label, anchor="start", dx=12):
        x = X(t)
        o.append(f'<path d="M{x:.1f},{y} l9,13 l-9,13 l-9,-13z" fill="{col}"/>')
        o.append(f'<text x="{x+dx if anchor=="start" else x-dx:.1f}" y="{y+18}" text-anchor="{anchor}" class="lbl" style="font-size:13px">{esc(label)}</text>')

    bar(m(2023, 7), m(2023, 9), 104, BLUE, "Financial Street Securities · fixed income")
    bar(m(2025, 7), m(2025, 9), 104, BLUE, "Dongxing Securities · CTA desk")
    # the two projects overlap in time, so they get two thin rows in one lane
    bar(m(2026, 1), m(2026, 6), 160, AQUA, "Procurement Pilot", anchor="end", lx=X(m(2026, 1)) - 8, h=18)
    bar(m(2026, 2), m(2026, 11), 184, AQUA, "Factor Research Harness → present", h=18)
    milestone(m(2026, 5), 240, ORANGE, "B.S. Business Analytics · GWU", anchor="end")
    bar(m(2026, 9), m(2028, 7), 240, ORANGE, "M.S. Applied Data Science · UChicago", lx=X(m(2026, 11)) + 4, ink="#08101f")
    milestone(m(2026, 8), 296, GOLD, "CFA Level I passed")
    # target internship
    xa, xb = X(m(2027, 6)), X(m(2027, 9))
    o.append(f'<rect x="{xa:.1f}" y="104" width="{xb-xa:.1f}" height="26" rx="4" fill="none" stroke="{ROSE}" stroke-width="1.8" stroke-dasharray="5 4"/>')
    o.append(f'<text x="{xb+8:.1f}" y="122" style="font-size:13px;font-weight:600;fill:{TEXT}">Seeking: Summer 2027 internship</text>')
    # today marker
    xn = X(m(2026, 10) + 28 / 365)
    o.append(f'<line x1="{xn:.1f}" y1="88" x2="{xn:.1f}" y2="326" stroke="{ROSE}" stroke-width="1.6" class="now"/>')
    o.append(f'<text x="{xn:.1f}" y="84" text-anchor="middle" class="cap" style="fill:{ROSE}">Oct 2026</text>')
    o.append(f'<text x="32" y="380" class="lbl2" style="font-size:12px">Bars show dated periods from the resume; diamonds are completion dates.</text>')
    o.append("</svg>")
    write("timeline.svg", "\n".join(o))


# --------------------------------------------------------------------------- divider
def divider():
    W, H = 1200, 18
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
<style>.g{{animation:slide 7s ease-in-out infinite alternate}}@keyframes slide{{from{{transform:translateX(-500px)}}to{{transform:translateX(900px)}}}}{REDUCED}</style>
<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#800000" stop-opacity="0"/><stop offset=".5" stop-color="#800000"/><stop offset="1" stop-color="#800000" stop-opacity="0"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="{ROSE}" stop-opacity="0"/><stop offset=".5" stop-color="#ffd9df"/><stop offset="1" stop-color="{ROSE}" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="8" width="{W}" height="2" fill="url(#l)"/>
<rect class="g" x="0" y="7" width="300" height="4" rx="2" fill="url(#s)"/>
</svg>"""
    write("divider.svg", svg)


if __name__ == "__main__":
    banner(); stats(); harness(); walkforward(); procurement(); timeline(); divider()
