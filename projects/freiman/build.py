"""Build article.html (preview with inline charts) from article.md."""
import re
from pathlib import Path

HERE = Path(__file__).parent
md = (HERE / "article.md").read_text(encoding="utf-8")


def fig1():
    # London: two bars to one scale. Baseline y=300, 2.6M -> 230px.
    base, h = 300, 230
    s = lambda v: h * v / 2.6
    ticks = "".join(
        f'<line class="grid" x1="70" x2="650" y1="{base - s(v):.1f}" y2="{base - s(v):.1f}"/>'
        f'<text class="tick" x="60" y="{base - s(v) + 5:.1f}" text-anchor="end">{lbl}</text>'
        for v, lbl in [(1, "1 מיליון"), (2, "2 מיליון")]
    )
    small = s(0.1)
    return f'''
<svg class="fit" viewBox="0 0 680 370" role="img" aria-labelledby="f1t">
  <title id="f1t">מגרש ליד תחנת סאות'וורק: 100 אלף ליש"ט ב־1980, 2.6 מיליון ליש"ט שנה אחרי פתיחת הקו</title>
  {ticks}
  <line class="axis" x1="70" x2="650" y1="{base}" y2="{base}"/>
  <text class="tick" x="60" y="{base + 5}" text-anchor="end">0</text>
  <g class="hit"><title>1980: 100,000 ליש"ט</title>
    <rect class="bar-muted" x="160" y="{base - small:.1f}" width="130" height="{small:.1f}" rx="3"/>
    <text class="val" x="225" y="{base - small - 12:.1f}" text-anchor="middle">£100,000</text>
  </g>
  <g class="hit"><title>שנה אחרי פתיחת הקו: 2,600,000 ליש"ט</title>
    <rect class="bar" x="430" y="{base - h}" width="130" height="{h}" rx="3"/>
    <text class="val" x="495" y="{base - h - 12}" text-anchor="middle">£2,600,000</text>
  </g>
  <text class="lbl" x="225" y="{base + 28}" text-anchor="middle">1980</text>
  <text class="sub" x="225" y="{base + 50}" text-anchor="middle">לפני שהיה קו</text>
  <text class="lbl" x="495" y="{base + 28}" text-anchor="middle">שנה אחרי הפתיחה</text>
  <text class="sub" x="495" y="{base + 50}" text-anchor="middle">התחנה פועלת</text>
  <path class="arrow" d="M300 {base - 30} C 360 {base - 60}, 380 {base - 150}, 420 {base - 190}" marker-end="url(#ah)"/>
  <text class="big" x="330" y="{base - 130}" text-anchor="middle">פי 26</text>
  <defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ahead" d="M0 0L10 5L0 10z"/></marker></defs>
</svg>'''


def fig2():
    x = lambda t: 50 + (t - 2022.0) * 141.7
    a, b, c = x(2022 + 2 / 12), x(2024 + 11 / 12), x(2025 + 4 / 12)
    y = 150
    MAY = 'מאי 2025: אישור תמ"א 70'
    return f'''
<svg viewBox="0 0 720 250" role="img" aria-labelledby="f2t">
  <title id="f2t">ציר זמן: הסכם במרץ 2022, החלטת ממשלה בדצמבר 2024, אישור תמ"א 70 במאי 2025. השלב הבא ללא מועד.</title>
  <line class="axis-strong" x1="50" x2="{x(2025.75):.1f}" y1="{y}" y2="{y}"/>
  <line class="axis-dash" x1="{x(2025.75):.1f}" x2="700" y1="{y}" y2="{y}"/>
  {"".join(f'<line class="yr" x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{y - 5}" y2="{y + 5}"/><text class="tick" x="{x(t):.1f}" y="{y + 22}" text-anchor="middle">{t}</text>' for t in (2022, 2023, 2024, 2025))}

  <line class="lead" x1="{a:.1f}" x2="{a:.1f}" y1="{y}" y2="94"/>
  <text class="lbl" x="{a + 70:.1f}" y="70" text-anchor="middle">מרץ 2022</text>
  <text class="sub" x="{a + 70:.1f}" y="90" text-anchor="middle">הסכם עם דירה להשכיר</text>

  <line class="lead" x1="{b:.1f}" x2="{b:.1f}" y1="{y}" y2="54"/>
  <text class="lbl" x="{b - 40:.1f}" y="30" text-anchor="middle">דצמבר 2024</text>
  <text class="sub" x="{b - 40:.1f}" y="50" text-anchor="middle">החלטת ממשלה: תמ"ל 3015</text>

  <line class="lead" x1="{c:.1f}" x2="{c:.1f}" y1="{y}" y2="114"/>
  <text class="lbl" x="{c + 45:.1f}" y="90" text-anchor="middle">מאי 2025</text>
  <text class="sub" x="{c + 45:.1f}" y="110" text-anchor="middle">תמ"א 70 מאושרת</text>

  {"".join(f'<g class="hit"><title>{t}</title><circle class="dot" cx="{p:.1f}" cy="{y}" r="7"/></g>' for p, t in ((a, "מרץ 2022: הסכם העירייה ודירה להשכיר"), (b, "דצמבר 2024: החלטת ממשלה"), (c, MAY)))}
  <circle class="dot-open" cx="700" cy="{y}" r="7"/>
  <text class="lbl" x="640" y="{y + 50}" text-anchor="middle">השלב הבא</text>
  <text class="sub" x="640" y="{y + 72}" text-anchor="middle">תכנית מפורטת. מועד: ?</text>

  <path class="brace" d="M{a:.1f} {y + 38} v8 H{b - 2:.1f} v-8"/>
  <text class="span" x="{(a + b) / 2:.1f}" y="{y + 70}" text-anchor="middle">33 חודשים</text>
  <path class="brace hot" d="M{b + 2:.1f} {y + 38} v8 H{c:.1f} v-8"/>
  <text class="span hot-t" x="{(b + c) / 2:.1f}" y="{y + 70}" text-anchor="middle">5 חודשים</text>
</svg>'''


def fig3():
    # Before: 6 parcels (2x3). After: public strip + 6 smaller plots, shuffled.
    cls = {"א": "o1", "ב": "o2", "ג": "o3"}
    def cell(x, y, w, h, l):
        k = cls.get(l, "o0")
        return (f'<g class="hit"><title>חלקה של בעלים {l}</title>'
                f'<rect class="{k}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'
                f'<text class="cell-t {k}-t" x="{x + w / 2}" y="{y + h / 2 + 7}" text-anchor="middle">{l}</text></g>')
    before_order = ["ג", "ב", "א", "ו", "ה", "ד"]  # RTL rows
    after_order = ["ה", "א", "ד", "ב", "ו", "ג"]
    W, H, g = 62, 62, 4
    out = []
    bx, by = 500, 70
    for i, l in enumerate(before_order):
        r, col = divmod(i, 3)
        out.append(cell(bx + col * (W + g), by + r * (H + g), W, H, l))
    ax, ay = 40, 70
    out.append(f'<g class="hit"><title>שטח ציבורי: כבישים, פארק, מבני ציבור</title><rect class="pub" x="{ax}" y="{ay}" width="{3 * W + 2 * g}" height="40" rx="3"/>'
               f'<text class="sub" x="{ax + (3 * W + 2 * g) / 2}" y="{ay + 26}" text-anchor="middle">שטח ציבורי</text></g>')
    h2 = (2 * H + g - 40 - g) / 2
    for i, l in enumerate(after_order):
        r, col = divmod(i, 3)
        out.append(cell(ax + col * (W + g), ay + 40 + g + r * (h2 + g), W, h2, l))
    sx, sy = bx + 2 * (W + g) + W - 6, by + 6
    return f'''
<svg viewBox="0 0 720 260" role="img" aria-labelledby="f3t">
  <title id="f3t">איחוד וחלוקה: שש חלקות נכנסות לסל אחד ומחולקות מחדש למגרשי תמורה במיקומים אחרים, לצד שטח ציבורי</title>
  <text class="lbl" x="{bx + (3 * W + 2 * g) / 2}" y="40" text-anchor="middle">1. לפני</text>
  <text class="lbl" x="360" y="40" text-anchor="middle">2. סל אחד</text>
  <text class="lbl" x="{ax + (3 * W + 2 * g) / 2}" y="40" text-anchor="middle">3. אחרי</text>
  {"".join(out)}
  <g><title>תחנת מטרו</title><circle class="stn" cx="{sx}" cy="{sy + 4}" r="11"/><text class="stn-t" x="{sx}" y="{sy + 9}" text-anchor="middle">M</text></g>
  <path class="arrow" d="M490 136 H425" marker-end="url(#ah3)"/>
  <circle class="pool" cx="360" cy="136" r="52"/>
  <text class="sub" x="360" y="131" text-anchor="middle">כל הקרקע</text>
  <text class="sub" x="360" y="151" text-anchor="middle">לפי שווי יחסי</text>
  <path class="arrow" d="M300 136 H252" marker-end="url(#ah3)"/>
  <text class="note" x="{bx + (3 * W + 2 * g) / 2}" y="225" text-anchor="middle">חלקה א צמודה לתחנה</text>
  <text class="note" x="{ax + (3 * W + 2 * g) / 2}" y="225" text-anchor="middle">מגרש התמורה של א במקום אחר</text>
  <defs><marker id="ah3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path class="ahead" d="M0 0L10 5L0 10z"/></marker></defs>
</svg>'''


def fig4():
    cols, rows, cw, ch, g = 5, 3, 84, 56, 3
    gw = cols * cw + (cols - 1) * g
    gh = rows * ch + (rows - 1) * g
    x0, y0 = (520 - gw) / 2, 96
    cells = []
    for r in range(rows):
        for c in range(cols):
            hl = (r, c) == (0, cols - 1)
            cx, cy = x0 + c * (cw + g), y0 + r * (ch + g)
            cells.append(
                f'<g class="hit"><title>יחידה תבעית: כ־67 מ"ר קרקע</title>'
                f'<rect class="{"bar" if hl else "plot"}" x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="2"/>'
                + (f'<text class="cell-t on-bar" x="{cx + cw / 2}" y="{cy + ch / 2 + 6}" text-anchor="middle">67 מ"ר</text>' if hl else "")
                + "</g>")
    return f'''
<svg class="fit" viewBox="0 0 520 330" role="img" aria-labelledby="f4t">
  <title id="f4t">דונם אחד, 1,000 מ"ר, מחולק ל־15 יחידות תבעיות של כ־67 מ"ר כל אחת</title>
  <text class="big" x="{x0 + gw}" y="58" text-anchor="start">15</text>
  <text class="sub" x="{x0 + gw - 52}" y="40" text-anchor="start">יחידות לדונם ברוטו,</text>
  <text class="sub" x="{x0 + gw - 52}" y="62" text-anchor="start">לפי דוחות השמאי</text>
  <text class="note" x="{x0}" y="58" text-anchor="start" style="direction:ltr">1,000 ÷ 15 ≈ 67</text>
  {"".join(cells)}
  <path class="brace" d="M{x0} {y0 + gh + 14} v8 H{x0 + gw} v-8"/>
  <text class="lbl" x="260" y="{y0 + gh + 46}" text-anchor="middle">דונם אחד = 1,000 מ"ר</text>
</svg>'''


FIGS = {
    "1": (fig1, "גרף 1", "אותו מגרש ליד תחנת סאות'וורק בלונדון, שני מחירים, אותו קנה מידה. מקור: המחקר של דון ריילי."),
    "2": (fig2, "גרף 2", "ההחלטות שהזיזו את פריימן, על ציר זמן בקנה מידה. מהחלטת הממשלה ועד תמ\"א 70 עברו חמישה חודשים."),
    "3": (fig3, "גרף 3", "איחוד וחלוקה, בפשטות. המיקום של החלקה שקניתם לא קובע את המיקום של מגרש התמורה. איור להמחשה בלבד."),
    "4": (fig4, "גרף 4", "כמה קרקע שקולה ליחידת דיור אחת, לפי צפיפות של 15 יחידות לדונם ברוטו. בחלקה עם הפקעה צריך יותר."),
}


def inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s


body, lst, lst_tag = [], [], None
title = lede = ""


def flush():
    global lst, lst_tag
    if lst:
        body.append(f"<{lst_tag}>" + "".join(f"<li>{inline(i)}</li>" for i in lst) + f"</{lst_tag}>")
        lst, lst_tag = [], None


for line in md.splitlines():
    t = line.strip()
    if not t:
        flush(); continue
    if t.startswith("# "):
        title = t[2:]; continue
    if t.startswith("**") and not lede and not body:
        lede = t.strip("*"); continue
    if t == "---":
        flush(); continue
    m = re.match(r"> \*\*\[גרף (\d)", t)
    if m:
        flush()
        fn, lab, cap = FIGS[m.group(1)]
        body.append(f'<figure id="fig{m.group(1)}"><div class="fig-scroll">{fn()}</div>'
                    f'<figcaption><span class="fig-n">{lab}</span> {cap}</figcaption></figure>')
        continue
    if t.startswith("## "):
        flush(); body.append(f"<h2>{inline(t[3:])}</h2>"); continue
    m = re.match(r"(\d+)\. (.*)", t)
    if m:
        lst_tag = "ol"; lst.append(m.group(2)); continue
    if t.startswith("- "):
        lst_tag = "ul"; lst.append(t[2:]); continue
    if t.startswith("*") and t.endswith("*") and not t.startswith("**"):
        flush(); body.append(f'<p class="disclaimer">{t.strip("*")}</p>'); continue
    flush(); body.append(f"<p>{inline(t)}</p>")
flush()

kicker, headline = "קרקעות להשקעה", title

html = f'''<title>פריימן: האדמה שחיכתה לרכבת</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700;900&family=Assistant:wght@400;600;700&display=swap">
<style>
/* Layout: one reading column, newspaper feature. Land tones for the page, metro blue for data. */
:root {{
  --bg: #f4f5f1;
  --paper: #fbfbf8;
  --ink: #17201d;
  --muted: #5b6561;
  --rule: #d6dad3;
  --metro: #2a78d6;
  --metro-ink: #1c4f8f;
  --land: #eb6834;
  --aqua: #1baf7a;
  --plot: #e3e6df;
  --plot-ink: #46504c;
  --font-display: "Frank Ruhl Libre", "David Libre", "Times New Roman", serif;
  --font-body: "Assistant", "Segoe UI", Arial, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #121614; --paper: #181d1b; --ink: #edf0eb; --muted: #a7b0ab; --rule: #333b37;
  --metro: #3987e5; --metro-ink: #8fbaf0; --land: #d95926; --aqua: #199e70; --plot: #2a312e; --plot-ink: #c9d0cb;
  color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #121614; --paper: #181d1b; --ink: #edf0eb; --muted: #a7b0ab; --rule: #333b37;
  --metro: #3987e5; --metro-ink: #8fbaf0; --land: #d95926; --aqua: #199e70; --plot: #2a312e; --plot-ink: #c9d0cb;
  color-scheme: dark; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--font-body); font-size: 1.15rem; line-height: 1.75; }}
.wrap {{ max-width: 44rem; margin: 0 auto; padding-inline: 16px; padding-block: 2.5rem 4rem; }}
.kicker {{ font-weight: 700; font-size: .85rem; letter-spacing: .04em; color: var(--metro-ink); display: flex; gap: .6rem; align-items: center; }}
.kicker::before {{ content: ""; width: 1.6rem; height: 4px; border-radius: 2px; background: var(--metro); }}
h1 {{ font-family: var(--font-display); font-weight: 900; font-size: clamp(2rem, 6vw, 3.1rem); line-height: 1.15; margin: .6rem 0 1rem; text-wrap: balance; }}
.lede {{ font-size: 1.3rem; line-height: 1.6; color: var(--muted); margin: 0 0 2rem; padding-bottom: 1.6rem; border-bottom: 1px solid var(--rule); }}
h2 {{ font-family: var(--font-display); font-weight: 700; font-size: 1.7rem; line-height: 1.3; margin: 2.6rem 0 .6rem; text-wrap: balance; }}
p {{ margin: 0 0 1.1rem; }}
a {{ color: var(--metro-ink); text-decoration-thickness: 2px; text-underline-offset: 3px; }}
a:focus-visible {{ outline: 2px solid var(--metro); outline-offset: 2px; }}
strong {{ font-weight: 700; }}
ol, ul {{ padding-inline-start: 1.4rem; margin: 0 0 1.2rem; display: grid; gap: .5rem; }}
ol li::marker {{ font-family: var(--font-display); font-weight: 700; color: var(--metro-ink); }}
figure {{ margin: 2rem 0; background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: 1rem; }}
.fig-scroll {{ overflow-x: auto; }}
.fig-scroll svg {{ display: block; width: 100%; min-width: 34rem; height: auto; direction: rtl; }}
.fig-scroll svg.fit {{ min-width: 0; }}
figcaption {{ font-size: .95rem; line-height: 1.55; color: var(--muted); margin-top: .6rem; }}
.fig-n {{ font-weight: 700; color: var(--ink); }}
.disclaimer {{ font-size: .9rem; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 1rem; margin-top: 2.5rem; }}
/* chart parts */
svg text {{ font-family: var(--font-body); fill: var(--ink); }}
.tick {{ font-size: 14px; fill: var(--muted); }}
.lbl {{ font-size: 17px; font-weight: 700; }}
.sub {{ font-size: 15px; fill: var(--muted); }}
.note {{ font-size: 15px; font-weight: 600; fill: var(--land); }}
.val {{ font-size: 18px; font-weight: 700; direction: ltr; }}
.big {{ font-family: var(--font-display); font-size: 44px; font-weight: 900; fill: var(--metro-ink); }}
.span {{ font-size: 16px; font-weight: 700; fill: var(--muted); }}
.hot-t {{ fill: var(--land); }}
.grid {{ stroke: var(--rule); stroke-width: 1; stroke-dasharray: 3 4; }}
.axis {{ stroke: var(--muted); stroke-width: 1.5; }}
.axis-strong {{ stroke: var(--metro); stroke-width: 4; stroke-linecap: round; }}
.axis-dash {{ stroke: var(--metro); stroke-width: 3; stroke-dasharray: 2 8; stroke-linecap: round; opacity: .6; }}
.yr {{ stroke: var(--paper); stroke-width: 2; }}
.lead {{ stroke: var(--rule); stroke-width: 1.5; }}
.dot {{ fill: var(--metro); stroke: var(--paper); stroke-width: 3; }}
.dot-open {{ fill: var(--paper); stroke: var(--metro); stroke-width: 3; }}
.brace {{ fill: none; stroke: var(--muted); stroke-width: 1.5; }}
.brace.hot {{ stroke: var(--land); stroke-width: 2.5; }}
.bar {{ fill: var(--metro); }}
.bar-muted {{ fill: var(--muted); }}
.arrow {{ fill: none; stroke: var(--muted); stroke-width: 2; }}
.ahead {{ fill: var(--muted); }}
.plot, .o0 {{ fill: var(--plot); }}
.o1 {{ fill: var(--land); }} .o2 {{ fill: var(--metro); }} .o3 {{ fill: var(--aqua); }}
.pub {{ fill: none; stroke: var(--muted); stroke-width: 1.5; stroke-dasharray: 5 4; }}
.pool {{ fill: var(--plot); stroke: var(--rule); stroke-width: 1.5; }}
.cell-t {{ font-size: 20px; font-weight: 700; }}
.o0-t {{ fill: var(--plot-ink); }}
.o1-t, .o2-t, .o3-t, .on-bar {{ fill: #ffffff; }}
.on-bar {{ font-size: 16px; }}
.stn {{ fill: var(--ink); stroke: var(--paper); stroke-width: 3; }}
.stn-t {{ fill: var(--paper); font-size: 13px; font-weight: 700; direction: ltr; }}
.hit {{ cursor: default; }}
.hit:hover rect, .hit:hover circle {{ filter: brightness(1.08); }}
</style>
<main class="wrap" dir="rtl" lang="he">
  <div class="kicker">נדל"ן · {kicker}</div>
  <h1>{headline}</h1>
  <p class="lede">{lede}</p>
  {"".join(body)}
</main>
'''
(HERE / "article.html").write_text(html, encoding="utf-8")
print("ok", len(html))
