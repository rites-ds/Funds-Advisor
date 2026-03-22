import streamlit as st
import math

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RITESH FUNDS ADVISOR",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1400px; }

.stApp {
  background: #080b14;
  background-image:
    radial-gradient(ellipse 80% 40% at 50% -10%, rgba(91,106,245,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 90% 80%, rgba(16,185,129,0.08) 0%, transparent 50%);
  color: #dde1f0;
}

[data-testid="stSidebar"] {
  background: #0c0f1d !important;
  border-right: 1px solid #1e2235 !important;
}

[data-testid="stNumberInput"] > div > div > input {
  background: #10142a !important;
  border: 1px solid #252840 !important;
  border-radius: 10px !important;
  color: #dde1f0 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  padding: 10px 14px !important;
}
[data-testid="stNumberInput"] > div > div > input:focus {
  border-color: #5b6af5 !important;
  box-shadow: 0 0 0 3px rgba(91,106,245,0.15) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
  color: #6b7194 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

[data-testid="stSlider"] div[role="slider"] { background: #5b6af5 !important; }
[data-testid="stSlider"] > div > div > div > div {
  background: linear-gradient(90deg, #5b6af5, #7c3aed) !important;
}

.stButton > button {
  background: linear-gradient(135deg, #5b6af5 0%, #7c3aed 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em;
  padding: 11px 24px !important;
  text-transform: uppercase;
  width: 100%;
}

[data-testid="metric-container"] {
  background: linear-gradient(135deg, #10142a 0%, #12162e 100%) !important;
  border: 1px solid #1e2235 !important;
  border-radius: 14px !important;
  padding: 18px 20px !important;
  position: relative;
  overflow: hidden;
}
[data-testid="metric-container"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, #5b6af5, #7c3aed);
}
[data-testid="metric-container"] label {
  color: #6b7194 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: #dde1f0 !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 24px !important;
  font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { display: none; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
  color: #10b981 !important;
  font-size: 11px !important;
}

[data-testid="stSelectbox"] > div > div {
  background: #10142a !important;
  border: 1px solid #252840 !important;
  border-radius: 10px !important;
  color: #dde1f0 !important;
}

.stRadio > div { flex-direction: row !important; gap: 8px !important; flex-wrap: wrap !important; }
.stRadio > div > label {
  background: #10142a !important;
  border: 1px solid #252840 !important;
  border-radius: 20px !important;
  padding: 6px 16px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #6b7194 !important;
  cursor: pointer;
}
.stRadio > div > label[data-checked="true"] {
  background: #5b6af5 !important;
  border-color: #5b6af5 !important;
  color: #fff !important;
}

hr { border: none; border-top: 1px solid #1e2235 !important; margin: 1.5rem 0 !important; }

.sec-hdr {
  font-family: 'Syne', sans-serif;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #5b6af5;
  padding-bottom: 10px;
  border-bottom: 1px solid #1e2235;
  margin: 2rem 0 1.2rem;
}

.glass-card {
  background: linear-gradient(135deg, #10142a 0%, #0e1224 100%);
  border: 1px solid #1e2235;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 12px;
}

.pick-card {
  background: #10142a;
  border: 1px solid #1e2235;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 10px;
  height: 100%;
}
.pick-cat { font-size: 9px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 10px; border-radius: 20px; display: inline-block; margin-bottom: 9px; }
.pick-name { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #dde1f0; margin-bottom: 2px; }
.pick-ticker { font-size: 11px; color: #6b7194; margin-bottom: 7px; font-weight: 500; }
.pick-why { font-size: 12px; color: #9095b0; line-height: 1.55; }
.pick-ret { font-size: 11px; font-weight: 700; color: #10b981; margin-top: 7px; }
.pick-alloc { font-size: 11px; font-weight: 700; color: #818cf8; margin-top: 3px; }

.arow {
  display: flex; align-items: center;
  padding: 11px 0;
  border-bottom: 1px solid #131728;
  gap: 10px;
}
.arow-name { flex: 1.2; font-size: 13px; color: #b8bdd4; }
.arow-name small { font-size: 10px; color: #464c68; display: block; margin-top: 1px; }
.arow-bar { flex: 2; height: 5px; background: #191d30; border-radius: 3px; overflow: hidden; }
.arow-bar-fill { height: 5px; border-radius: 3px; }
.arow-pct { font-size: 11px; color: #6b7194; min-width: 30px; text-align: right; font-weight: 600; }
.arow-amt { font-family: 'Syne', sans-serif; font-size: 13px; color: #dde1f0; font-weight: 700; min-width: 72px; text-align: right; }

.milestone-card {
  background: #10142a;
  border: 1px solid #1e2235;
  border-radius: 12px;
  padding: 14px 12px;
  text-align: center;
}
.milestone-card.dim { opacity: .4; }

.infobox {
  background: #0d1221;
  border: 1px solid #1e2235;
  border-left: 3px solid #5b6af5;
  border-radius: 10px;
  padding: 14px 18px;
  font-size: 12px;
  color: #7880a0;
  line-height: 1.7;
  margin-top: 1.5rem;
}
.disclaimer {
  background: #130c14;
  border: 1px solid #2a1b2e;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 11px;
  color: #5a4060;
  line-height: 1.7;
  margin-top: 14px;
}
.live-dot {
  display: inline-block;
  width: 7px; height: 7px;
  background: #10b981;
  border-radius: 50%;
  margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_ALLOC = [
    {"key": "shares", "label": "Stocks",       "default": 22, "color": "#5b6af5", "desc": "Direct equity"},
    {"key": "mf",     "label": "Mutual Funds", "default": 28, "color": "#10b981", "desc": "Equity SIP"},
    {"key": "etf",    "label": "ETFs",         "default": 20, "color": "#f59e0b", "desc": "Index passive"},
    {"key": "fd",     "label": "FD / Debt",    "default": 15, "color": "#06b6d4", "desc": "Stable return"},
    {"key": "ppf",    "label": "PPF / NPS",    "default": 10, "color": "#a78bfa", "desc": "Tax-free"},
    {"key": "gold",   "label": "Gold / SGB",   "default":  5, "color": "#fb923c", "desc": "Hedge"},
]

PICKS = [
    {"cat":"shares","name":"Reliance Industries","ticker":"NSE: RELIANCE","why":"Jio + retail vertical integration fuels multi-decade compounding.","ret":"~18% CAGR (5yr)","risk":"Medium"},
    {"cat":"shares","name":"HDFC Bank",          "ticker":"NSE: HDFCBANK","why":"India's most trusted private bank. Consistent asset quality.","ret":"~14% CAGR (5yr)","risk":"Low"},
    {"cat":"shares","name":"Infosys",            "ticker":"NSE: INFY",    "why":"IT leader with global enterprise clients and growing margins.","ret":"~16% CAGR (5yr)","risk":"Low"},
    {"cat":"shares","name":"Tata Motors",        "ticker":"NSE: TATAMOTORS","why":"EV pivot + JLR Europe recovery — high conviction growth.","ret":"~22% CAGR (3yr)","risk":"High"},
    {"cat":"shares","name":"Bajaj Finance",      "ticker":"NSE: BAJFINANCE","why":"NBFC king — massive consumer lending book, fintech moat.","ret":"~20% CAGR (5yr)","risk":"Medium"},
    {"cat":"etf",   "name":"Nifty 50 ETF",       "ticker":"NSE: NIFTYBEES","why":"Track 50 blue chips passively. Expense ratio just 0.04%.","ret":"~13% CAGR (5yr)","risk":"Low"},
    {"cat":"etf",   "name":"Nifty Next 50 ETF",  "ticker":"NSE: JUNIORBEES","why":"Mid-large blend — higher growth ceiling than Nifty 50.","ret":"~15% CAGR (5yr)","risk":"Low"},
    {"cat":"etf",   "name":"Nasdaq 100 ETF",     "ticker":"NSE: MOM100",  "why":"US tech giants (Apple, Google, Nvidia) in INR.","ret":"~20% CAGR (5yr)","risk":"Medium"},
    {"cat":"mf",    "name":"Mirae Asset Large Cap","ticker":"Direct Growth","why":"Consistently 5-star rated. Top quartile large-cap performer.","ret":"~15% CAGR (5yr)","risk":"Low"},
    {"cat":"mf",    "name":"Parag Parikh Flexi Cap","ticker":"Direct Growth","why":"Flexi-cap with international allocation and very low churn.","ret":"~19% CAGR (5yr)","risk":"Low"},
    {"cat":"mf",    "name":"Axis Small Cap",     "ticker":"Direct Growth","why":"Best-in-class small cap with disciplined stock selection.","ret":"~21% CAGR (5yr)","risk":"High"},
    {"cat":"mf",    "name":"SBI Nifty Index Fund","ticker":"Direct Growth","why":"Ultra low-cost index tracking — perfect anchor for any SIP.","ret":"~13% CAGR (5yr)","risk":"Low"},
    {"cat":"fd",    "name":"SBI FD (2yr)",       "ticker":"Fixed Deposit","why":"Capital safety with ~7.25% p.a. Guaranteed and predictable.","ret":"7.25% p.a.","risk":"None"},
    {"cat":"fd",    "name":"PPF Account",        "ticker":"PPF (15yr)",   "why":"EEE tax status. 7.1% risk-free — best debt instrument in India.","ret":"7.1% tax-free","risk":"None"},
]

RISK_COLOR = {"None":"#10b981","Low":"#34d399","Low-Med":"#f59e0b","Medium":"#fb923c","High":"#f43f5e"}
CAT_META = {
    "shares": {"label":"Stock",       "bg":"#1a2550","color":"#818cf8"},
    "etf":    {"label":"ETF",         "bg":"#2d1f07","color":"#f59e0b"},
    "mf":     {"label":"Mutual Fund", "bg":"#052817","color":"#34d399"},
    "fd":     {"label":"FD / Debt",   "bg":"#062025","color":"#22d3ee"},
    "ppf":    {"label":"PPF / NPS",   "bg":"#1c1040","color":"#a78bfa"},
    "gold":   {"label":"Gold",        "bg":"#2a1505","color":"#fb923c"},
}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt(n):
    if n >= 10_000_000: return f"₹{n/10_000_000:.2f}Cr"
    if n >= 100_000:    return f"₹{n/100_000:.2f}L"
    if n >= 1_000:      return f"₹{n/1_000:.1f}K"
    return f"₹{int(n)}"

def sip_future(monthly, rate_annual, years):
    r = rate_annual / 12 / 100
    n = years * 12
    if r == 0: return monthly * n
    return monthly * (((1 + r) ** n - 1) / r) * (1 + r)

def make_donut_svg(alloc_list, invest):
    """Pure SVG donut chart — no plotly needed."""
    cx, cy, r_out, r_in = 160, 160, 130, 82
    total = sum(a["pct"] for a in alloc_list) or 1
    segments = []
    angle = -90.0
    for a in alloc_list:
        sweep = (a["pct"] / total) * 360
        segments.append((angle, sweep, a["color"], a["label"], a["pct"]))
        angle += sweep

    def arc_path(cx, cy, r, start_deg, sweep_deg):
        start = math.radians(start_deg)
        end   = math.radians(start_deg + sweep_deg)
        x1, y1 = cx + r * math.cos(start), cy + r * math.sin(start)
        x2, y2 = cx + r * math.cos(end),   cy + r * math.sin(end)
        large  = 1 if sweep_deg > 180 else 0
        return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large} 1 {x2:.2f} {y2:.2f}"

    paths = []
    for (start, sweep, color, label, pct) in segments:
        if sweep < 0.5: continue
        d_out = arc_path(cx, cy, r_out, start, sweep)
        d_in  = arc_path(cx, cy, r_in,  start + sweep, -sweep)
        d = f"{d_out} L {cx + r_in*math.cos(math.radians(start+sweep)):.2f} {cy + r_in*math.sin(math.radians(start+sweep)):.2f} {d_in} Z"
        paths.append(f'<path d="{d}" fill="{color}" stroke="#080b14" stroke-width="2.5"/>')

    # Legend rows
    legend_items = ""
    for i, a in enumerate(alloc_list):
        yy = 20 + i * 22
        legend_items += f'''
        <rect x="330" y="{yy}" width="10" height="10" rx="2" fill="{a['color']}"/>
        <text x="346" y="{yy+9}" font-size="11" fill="#9095b0" font-family="DM Sans,sans-serif">{a['label']} — {a['pct']:.0f}%</text>'''

    center_label = fmt(invest)
    svg = f'''<svg viewBox="0 0 530 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-height:320px;">
      {''.join(paths)}
      <circle cx="{cx}" cy="{cy}" r="{r_in - 2}" fill="#080b14"/>
      <text x="{cx}" y="{cy - 8}" text-anchor="middle" font-size="17" font-weight="700"
        fill="#dde1f0" font-family="Syne,sans-serif">{center_label}</text>
      <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="11" fill="#6b7194"
        font-family="DM Sans,sans-serif">per month</text>
      {legend_items}
    </svg>'''
    return svg

def make_bar_svg(alloc_list, invest):
    """Pure SVG horizontal bar chart."""
    max_amt = max(a["amt"] for a in alloc_list) or 1
    bar_max_w = 340
    row_h = 44
    pad_left = 100
    height = len(alloc_list) * row_h + 20
    rows = ""
    for i, a in enumerate(alloc_list):
        y = 10 + i * row_h
        bw = int((a["amt"] / max_amt) * bar_max_w)
        rows += f'''
        <text x="{pad_left - 8}" y="{y + 18}" text-anchor="end" font-size="12"
          fill="#9095b0" font-family="DM Sans,sans-serif">{a['label']}</text>
        <rect x="{pad_left}" y="{y + 6}" width="{bw}" height="18" rx="4" fill="{a['color']}" opacity="0.85"/>
        <text x="{pad_left + bw + 8}" y="{y + 19}" font-size="11" fill="#6b7194"
          font-family="Syne,sans-serif" font-weight="600">{fmt(a['amt'])}</text>'''

    return f'''<svg viewBox="0 0 520 {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;">
      {rows}
    </svg>'''

def make_projection_svg(invest, show_rate, inflation, proj_years):
    """Pure SVG line chart for growth projection."""
    W, H = 700, 260
    pad = {"t": 24, "b": 40, "l": 68, "r": 20}
    chart_w = W - pad["l"] - pad["r"]
    chart_h = H - pad["t"] - pad["b"]

    years = list(range(1, proj_years + 1))
    inv_total = [invest * 12 * y for y in years]
    val_sel   = [sip_future(invest, show_rate, y) for y in years]
    val_real  = [sip_future(invest, max(show_rate - inflation, 1), y) for y in years]

    max_val = max(val_sel) * 1.08
    min_val = 0

    def sx(i):
        return pad["l"] + (i / (len(years) - 1 or 1)) * chart_w

    def sy(v):
        return pad["t"] + chart_h - ((v - min_val) / (max_val - min_val)) * chart_h

    def polyline(series, color, dash=""):
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(series))
        style = f'stroke="{color}" stroke-width="2.5" fill="none"'
        if dash:
            style += f' stroke-dasharray="{dash}"'
        return f'<polyline points="{pts}" {style}/>'

    def fill_area(series, color):
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(series))
        pts += f" {sx(len(series)-1):.1f},{sy(0):.1f} {sx(0):.1f},{sy(0):.1f}"
        return f'<polygon points="{pts}" fill="{color}" opacity="0.08"/>'

    # Y-axis ticks
    y_ticks = ""
    n_ticks = 5
    for t in range(n_ticks + 1):
        v = min_val + (max_val - min_val) * t / n_ticks
        y = sy(v)
        lbl = fmt(v)
        y_ticks += f'<line x1="{pad["l"]}" y1="{y:.1f}" x2="{W - pad["r"]}" y2="{y:.1f}" stroke="#13172a" stroke-width="1"/>'
        y_ticks += f'<text x="{pad["l"] - 6}" y="{y + 4:.1f}" text-anchor="end" font-size="9" fill="#464c68" font-family="DM Sans,sans-serif">{lbl}</text>'

    # X-axis labels (show every 2nd or 3rd year)
    step = max(1, proj_years // 8)
    x_labels = ""
    for i, y in enumerate(years):
        if i % step == 0 or i == len(years) - 1:
            x = sx(i)
            x_labels += f'<text x="{x:.1f}" y="{H - pad["b"] + 16}" text-anchor="middle" font-size="9" fill="#464c68" font-family="DM Sans,sans-serif">Yr {y}</text>'

    # Legend
    legend = f'''
    <rect x="{pad["l"]}" y="4" width="10" height="3" rx="1" fill="#252840"/>
    <text x="{pad["l"]+14}" y="11" font-size="9" fill="#6b7194" font-family="DM Sans,sans-serif">Capital invested</text>
    <rect x="{pad["l"]+110}" y="4" width="10" height="3" rx="1" fill="#5b6af5"/>
    <text x="{pad["l"]+124}" y="11" font-size="9" fill="#6b7194" font-family="DM Sans,sans-serif">At {show_rate}% p.a.</text>
    <rect x="{pad["l"]+210}" y="4" width="10" height="3" rx="1" fill="#10b981"/>
    <text x="{pad["l"]+224}" y="11" font-size="9" fill="#6b7194" font-family="DM Sans,sans-serif">Real (inflation adj.)</text>'''

    svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:rgba(16,20,42,0.5);border-radius:12px;">
      {y_ticks}
      {x_labels}
      {fill_area(val_sel, "#5b6af5")}
      {polyline(inv_total, "#252840", "6,3")}
      {polyline(val_sel, "#5b6af5")}
      {polyline(val_real, "#10b981", "4,2")}
      {legend}
    </svg>'''
    return svg


# ─────────────────────────────────────────────────────────────────────────────
# LOGO / HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2rem 0 1.5rem;border-bottom:1px solid #1e2235;margin-bottom:2rem;display:flex;align-items:center;gap:18px;">
  <div style="width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#5b6af5,#7c3aed);
    display:flex;align-items:center;justify-content:center;font-size:24px;
    box-shadow:0 8px 24px rgba(91,106,245,0.4);flex-shrink:0;">💎</div>
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;letter-spacing:0.06em;
      background:linear-gradient(90deg,#818cf8 0%,#c4b5fd 50%,#f0abfc 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;">
      RITESH FUNDS ADVISOR</div>
    <div style="font-size:12px;color:#6b7194;margin-top:4px;letter-spacing:0.03em;">
      <span class="live-dot"></span>AI-Powered Portfolio Planner &nbsp;·&nbsp; India Markets
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Allocation Controls")

    risk_profile = st.selectbox("Risk Profile", ["Conservative","Balanced","Aggressive","Custom"], index=1)
    presets = {
        "Conservative": [10, 20, 15, 35, 15, 5],
        "Balanced":     [22, 28, 20, 15, 10, 5],
        "Aggressive":   [35, 35, 20,  5,  3, 2],
        "Custom":       None,
    }
    preset_vals = presets[risk_profile]

    st.markdown("---")
    st.markdown("### 📊 Adjust Split (%)")

    alloc_pcts = {}
    total_pct = 0
    for i, a in enumerate(DEFAULT_ALLOC):
        dv = preset_vals[i] if preset_vals else a["default"]
        v = st.slider(a["label"], 0, 60, dv, 1, key=f"sl_{a['key']}")
        alloc_pcts[a["key"]] = v
        total_pct += v

    ok = total_pct == 100
    col = "#10b981" if ok else "#f43f5e"
    bg  = "#052817" if ok else "#1c0812"
    st.markdown(f"""
    <div style="margin-top:14px;padding:12px 14px;border-radius:10px;
      background:{bg};border:1px solid {col};">
      <div style="font-size:10px;color:#6b7194;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Total allocation</div>
      <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:{col};">{total_pct}%</div>
      <div style="font-size:11px;color:{col};margin-top:2px;">
        {'✓ Perfect balance' if ok else f'{"▲" if total_pct>100 else "▼"} {abs(100-total_pct)}% {"over" if total_pct>100 else "under"}'}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Projection Settings")
    proj_years = st.slider("Horizon (years)", 1, 30, 10)
    show_rate  = st.slider("Expected return % p.a.", 8, 24, 13)
    inflation  = st.slider("Inflation % p.a.", 3, 10, 6)


# ─────────────────────────────────────────────────────────────────────────────
# INPUTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio Inputs</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])
with c1:
    salary = st.number_input("Monthly take-home salary (₹)", min_value=0, step=1000, value=80000, format="%d")
with c2:
    invest_raw = st.number_input("Amount you can invest (₹/mo)", min_value=0, step=500, value=25000, format="%d")
with c3:
    pct_override = st.number_input("Or set % of salary to invest", min_value=0, max_value=100, step=1, value=0, format="%d")
with c4:
    st.markdown("<br>", unsafe_allow_html=True)
    if salary > 0:
        invest = invest_raw if pct_override == 0 else int(salary * pct_override / 100)
        pct_of_sal = round(invest / salary * 100, 1)
        health = "🟢 Excellent" if pct_of_sal >= 30 else ("🟡 Good" if pct_of_sal >= 20 else "🔴 Low")
        st.markdown(f"""
        <div style="background:#10142a;border:1px solid #1e2235;border-radius:12px;padding:14px 16px;margin-top:4px;">
          <div style="font-size:9px;color:#6b7194;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px;">Invest Ratio</div>
          <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#818cf8;">{pct_of_sal}%</div>
          <div style="font-size:11px;color:#9095b0;margin-top:3px;">{health}</div>
        </div>""", unsafe_allow_html=True)
    else:
        invest = invest_raw

if salary <= 0 or invest <= 0:
    st.markdown("""<div class="infobox">
      <b>💡 Getting started:</b> Enter your monthly salary and the amount you want to invest.
      Adjust allocation sliders in the sidebar to customise your split.
    </div>""", unsafe_allow_html=True)
    st.stop()

if invest > salary:
    st.error("⚠ Investment amount cannot exceed your salary.")
    st.stop()

# Normalise allocations
if total_pct > 0:
    norm = {k: v / total_pct for k, v in alloc_pcts.items()}
else:
    norm = {a["key"]: a["default"] / 100 for a in DEFAULT_ALLOC}

ALLOC = [{**a, "pct": round(norm[a["key"]] * 100, 1), "amt": invest * norm[a["key"]]} for a in DEFAULT_ALLOC]

expenses = salary - invest
inv_pct_display = round(invest / salary * 100, 1)


# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW METRICS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio Overview</div>', unsafe_allow_html=True)

real_return  = show_rate - inflation
future_val   = sip_future(invest, show_rate, proj_years)
real_val     = sip_future(invest, max(real_return, 1), proj_years)
total_invest = invest * 12 * proj_years
wealth_gain  = future_val - total_invest

m1,m2,m3,m4,m5,m6 = st.columns(6)
m1.metric("Monthly Salary",    fmt(salary))
m2.metric("You Invest",        fmt(invest),        f"{inv_pct_display}% of salary")
m3.metric("Monthly Expenses",  fmt(expenses),      f"{100-inv_pct_display:.0f}% of salary")
m4.metric("Annual Investment",  fmt(invest*12),     "Per year")
m5.metric(f"Future Value ({proj_years}yr)", fmt(future_val), f"At {show_rate}% p.a.")
m6.metric("Wealth Gained",     fmt(wealth_gain),   f"Real: {fmt(real_val)}")


# ─────────────────────────────────────────────────────────────────────────────
# ALLOCATION BREAKDOWN + DONUT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Allocation Breakdown</div>', unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for a in ALLOC:
        bar_w = min(int(a["pct"] * 3.5), 100)
        st.markdown(f"""
        <div class="arow">
          <div class="arow-name">{a['label']}<small>{a['desc']}</small></div>
          <div class="arow-bar"><div class="arow-bar-fill" style="width:{bar_w}%;background:{a['color']};"></div></div>
          <div class="arow-pct">{a['pct']:.0f}%</div>
          <div class="arow-amt">{fmt(a['amt'])}<span style="font-size:10px;color:#464c68;font-weight:400;">/mo</span></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown(make_donut_svg(ALLOC, invest), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# GROWTH PROJECTION CHART
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="sec-hdr">Growth Projection — {proj_years}-Year Horizon</div>', unsafe_allow_html=True)
st.markdown(make_projection_svg(invest, show_rate, inflation, proj_years), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MONTHLY ALLOCATION BAR CHART
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Monthly Allocation by Category</div>', unsafe_allow_html=True)
st.markdown(make_bar_svg(ALLOC, invest), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MILESTONES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Wealth Milestones</div>', unsafe_allow_html=True)

milestones      = [10_00_000, 25_00_000, 50_00_000, 1_00_00_000, 5_00_00_000, 10_00_00_000]
milestone_labels = ["₹10L","₹25L","₹50L","₹1Cr","₹5Cr","₹10Cr"]

cols_ms = st.columns(len(milestones))
for i, (ms, lbl) in enumerate(zip(milestones, milestone_labels)):
    yr_hit = None
    for y in range(1, 51):
        if sip_future(invest, show_rate, y) >= ms:
            yr_hit = y
            break
    with cols_ms[i]:
        if yr_hit:
            st.markdown(f"""
            <div class="milestone-card">
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:#818cf8;">{lbl}</div>
              <div style="font-size:22px;font-weight:700;color:#dde1f0;margin:6px 0;">{yr_hit}<span style="font-size:12px;color:#6b7194;">yr</span></div>
              <div style="font-size:10px;color:#6b7194;">to reach</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="milestone-card dim">
              <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:#464c68;">{lbl}</div>
              <div style="font-size:14px;color:#464c68;margin:6px 0;">50yr+</div>
              <div style="font-size:10px;color:#3a3f55;">to reach</div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TOP PICKS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Top Investment Picks</div>', unsafe_allow_html=True)

filter_opt = st.radio("Filter", ["All","Stocks","ETFs","Mutual Funds","FD / Debt"], horizontal=True, label_visibility="collapsed")
cat_map = {"All":None,"Stocks":"shares","ETFs":"etf","Mutual Funds":"mf","FD / Debt":"fd"}
filtered_picks = PICKS if not cat_map[filter_opt] else [p for p in PICKS if p["cat"] == cat_map[filter_opt]]

cat_count = {}
for p in PICKS: cat_count[p["cat"]] = cat_count.get(p["cat"], 0) + 1

alloc_by_key = {a["key"]: a for a in ALLOC}
pick_cols = st.columns(3)
for i, p in enumerate(filtered_picks):
    ao = alloc_by_key.get(p["cat"])
    suggested = fmt(round(ao["amt"] / cat_count.get(p["cat"], 1))) if ao else ""
    m = CAT_META.get(p["cat"], CAT_META["shares"])
    rc = RISK_COLOR.get(p.get("risk","Medium"), "#fb923c")
    with pick_cols[i % 3]:
        st.markdown(f"""
        <div class="pick-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px;">
            <span class="pick-cat" style="background:{m['bg']};color:{m['color']}">{m['label']}</span>
            <span style="font-size:9px;font-weight:700;color:{rc};background:rgba(0,0,0,.25);
              padding:2px 7px;border-radius:20px;border:1px solid {rc}44;">{p.get('risk','—')} RISK</span>
          </div>
          <div class="pick-name">{p['name']}</div>
          <div class="pick-ticker">{p['ticker']}</div>
          <div class="pick-why">{p['why']}</div>
          <div class="pick-ret">↑ {p['ret']}</div>
          {f'<div class="pick-alloc">→ Suggested {suggested}/mo</div>' if suggested else ''}
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TIPS + DISCLAIMER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="infobox">
  💡 <b>Pro Tips from RITESH FUNDS ADVISOR:</b><br>
  • Start SIPs on the 1st of every month — consistent entry beats timing the market.<br>
  • For stocks, invest in 2–3 tranches per month. Never deploy all funds in a single day.<br>
  • Keep 3–6 months of expenses as liquid emergency fund <em>before</em> any investment.<br>
  • Review and rebalance your portfolio every 6 months using the sliders above.<br>
  • Increase your SIP by 10% every year — step-ups create massive long-term wealth.
</div>
<div class="disclaimer">
  ⚠ RITESH FUNDS ADVISOR is a personal finance education tool and does not constitute SEBI-registered financial advice.
  Past returns are indicative only and do not guarantee future performance.
  All investments are subject to market risk. Please consult a qualified investment advisor before making any decisions.
</div>
""", unsafe_allow_html=True)
