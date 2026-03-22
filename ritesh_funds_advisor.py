import streamlit as st
import plotly.graph_objects as go
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

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1400px; }

/* ── App Background ── */
.stApp {
  background: #080b14;
  background-image:
    radial-gradient(ellipse 80% 40% at 50% -10%, rgba(91,106,245,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 90% 80%, rgba(16,185,129,0.08) 0%, transparent 50%);
  color: #dde1f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #0c0f1d !important;
  border-right: 1px solid #1e2235 !important;
}
[data-testid="stSidebar"] .stMarkdown h3 {
  font-family: 'Syne', sans-serif;
  font-size: 11px !important;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #5b6af5 !important;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #1e2235;
}

/* ── Number inputs ── */
[data-testid="stNumberInput"] > div > div > input {
  background: #10142a !important;
  border: 1px solid #252840 !important;
  border-radius: 10px !important;
  color: #dde1f0 !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  padding: 10px 14px !important;
  transition: border-color 0.2s, box-shadow 0.2s;
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

/* ── Sliders ── */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] > div > p {
  color: #6b7194 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}
[data-testid="stSlider"] div[role="slider"] {
  background: #5b6af5 !important;
}
[data-testid="stSlider"] > div > div > div > div {
  background: linear-gradient(90deg, #5b6af5, #7c3aed) !important;
}

/* ── Buttons ── */
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
  transition: all 0.2s !important;
  text-transform: uppercase;
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(91,106,245,0.35) !important;
}
.stButton > button:active { transform: translateY(0); }

/* ── Metrics ── */
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

/* ── Select boxes ── */
[data-testid="stSelectbox"] > div > div {
  background: #10142a !important;
  border: 1px solid #252840 !important;
  border-radius: 10px !important;
  color: #dde1f0 !important;
}
[data-testid="stSelectbox"] label > div > p {
  color: #6b7194 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

/* ── Radio buttons ── */
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
  transition: all 0.15s;
}
.stRadio > div > label:hover { border-color: #5b6af5 !important; }
[data-checked="true"].stRadio > div > label,
.stRadio > div > label[data-checked="true"] {
  background: #5b6af5 !important;
  border-color: #5b6af5 !important;
  color: #fff !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #1e2235 !important; margin: 1.5rem 0 !important; }

/* ── Section header ── */
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

/* ── Cards ── */
.glass-card {
  background: linear-gradient(135deg, #10142a 0%, #0e1224 100%);
  border: 1px solid #1e2235;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 12px;
  transition: border-color 0.2s, transform 0.2s;
  position: relative;
  overflow: hidden;
}
.glass-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(91,106,245,0.03), transparent);
  pointer-events: none;
}
.glass-card:hover { border-color: #5b6af5; transform: translateY(-2px); }

/* ── Pick card ── */
.pick-card {
  background: #10142a;
  border: 1px solid #1e2235;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 10px;
  transition: border-color 0.2s, transform 0.15s;
}
.pick-card:hover { border-color: #5b6af5; transform: translateY(-1px); }
.pick-cat { font-size: 9px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 3px 10px; border-radius: 20px; display: inline-block; margin-bottom: 9px; }
.pick-name { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #dde1f0; margin-bottom: 2px; }
.pick-ticker { font-size: 11px; color: #6b7194; margin-bottom: 7px; font-weight: 500; }
.pick-why { font-size: 12px; color: #9095b0; line-height: 1.55; }
.pick-ret { font-size: 11px; font-weight: 700; color: #10b981; margin-top: 7px; }
.pick-alloc { font-size: 11px; font-weight: 700; color: #818cf8; margin-top: 3px; }

/* ── Alloc row ── */
.arow {
  display: flex; align-items: center;
  padding: 11px 0;
  border-bottom: 1px solid #131728;
  gap: 10px;
}
.arow-name { flex: 1.2; font-size: 13px; color: #b8bdd4; }
.arow-name small { font-size: 10px; color: #464c68; display: block; margin-top: 1px; }
.arow-bar { flex: 2; height: 5px; background: #191d30; border-radius: 3px; overflow: hidden; }
.arow-bar-fill { height: 5px; border-radius: 3px; transition: width 0.6s ease; }
.arow-pct { font-size: 11px; color: #6b7194; min-width: 30px; text-align: right; font-weight: 600; }
.arow-amt { font-family: 'Syne', sans-serif; font-size: 13px; color: #dde1f0; font-weight: 700; min-width: 72px; text-align: right; }

/* ── Info / disclaimer ── */
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

/* ── Live badge ── */
.live-dot {
  display: inline-block;
  width: 7px; height: 7px;
  background: #10b981;
  border-radius: 50%;
  margin-right: 5px;
  animation: pulse 1.8s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}

/* ── Progress ring container ── */
.ring-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 0;
}

/* ── Tip highlight ── */
.tip-highlight {
  background: linear-gradient(90deg, rgba(91,106,245,0.12), rgba(124,58,237,0.06));
  border: 1px solid rgba(91,106,245,0.25);
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 12px;
  color: #9095b0;
  margin-bottom: 10px;
}
.tip-highlight b { color: #818cf8; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0c0f1d; }
::-webkit-scrollbar-thumb { background: #252840; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATIC DATA
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_ALLOC = [
    {"key": "shares", "label": "Stocks",          "default": 22, "color": "#5b6af5", "desc": "Direct equity"},
    {"key": "mf",     "label": "Mutual Funds",    "default": 28, "color": "#10b981", "desc": "Equity SIP"},
    {"key": "etf",    "label": "ETFs",            "default": 20, "color": "#f59e0b", "desc": "Index passive"},
    {"key": "fd",     "label": "FD / Debt",       "default": 15, "color": "#06b6d4", "desc": "Stable return"},
    {"key": "ppf",    "label": "PPF / NPS",       "default": 10, "color": "#a78bfa", "desc": "Tax-free"},
    {"key": "gold",   "label": "Gold / SGB",      "default":  5, "color": "#fb923c", "desc": "Hedge"},
]

PICKS = [
    {"cat":"shares","name":"Reliance Industries","ticker":"NSE: RELIANCE","why":"Jio + retail vertical integration fuels multi-decade compounding.","ret":"~18% CAGR (5yr)","risk":"Medium"},
    {"cat":"shares","name":"HDFC Bank",          "ticker":"NSE: HDFCBANK","why":"India's most trusted private bank. Consistent asset quality.","ret":"~14% CAGR (5yr)","risk":"Low"},
    {"cat":"shares","name":"Infosys",            "ticker":"NSE: INFY",    "why":"IT leader with global enterprise clients and growing margins.","ret":"~16% CAGR (5yr)","risk":"Low"},
    {"cat":"shares","name":"Tata Motors",        "ticker":"NSE: TATAMOTORS","why":"EV pivot + JLR Europe recovery — high conviction growth.","ret":"~22% CAGR (3yr)","risk":"High"},
    {"cat":"shares","name":"Bajaj Finance",      "ticker":"NSE: BAJFINANCE","why":"NBFC king — massive consumer lending book, fintech moat.","ret":"~20% CAGR (5yr)","risk":"Medium"},
    {"cat":"etf",   "name":"Nifty 50 ETF",       "ticker":"NSE: NIFTYBEES","why":"Track 50 blue chips passively. Expense ratio just 0.04%.","ret":"~13% CAGR (5yr)","risk":"Low"},
    {"cat":"etf",   "name":"Nifty Next 50 ETF",  "ticker":"NSE: JUNIORBEES","why":"Mid-large blend — higher growth ceiling than Nifty 50.","ret":"~15% CAGR (5yr)","risk":"Low-Med"},
    {"cat":"etf",   "name":"Nasdaq 100 ETF",     "ticker":"NSE: MOM100",  "why":"US tech giants (Apple, Google, Nvidia) in INR — global diversification.","ret":"~20% CAGR (5yr)","risk":"Medium"},
    {"cat":"mf",    "name":"Mirae Asset Large Cap","ticker":"Direct Growth","why":"Consistently 5-star rated. Top quartile large-cap performer.","ret":"~15% CAGR (5yr)","risk":"Low"},
    {"cat":"mf",    "name":"Parag Parikh Flexi Cap","ticker":"Direct Growth","why":"Flexi-cap with international allocation and very low portfolio churn.","ret":"~19% CAGR (5yr)","risk":"Low-Med"},
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

# ─────────────────────────────────────────────────────────────────────────────
# LOGO / HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2rem 0 1.5rem; border-bottom: 1px solid #1e2235; margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between;">
  <div style="display: flex; align-items: center; gap: 18px;">
    <div style="
      width: 52px; height: 52px; border-radius: 14px;
      background: linear-gradient(135deg, #5b6af5, #7c3aed);
      display: flex; align-items: center; justify-content: center;
      font-size: 24px; box-shadow: 0 8px 24px rgba(91,106,245,0.4);
      flex-shrink: 0;
    ">💎</div>
    <div>
      <div style="
        font-family: 'Syne', sans-serif;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.06em;
        background: linear-gradient(90deg, #818cf8 0%, #c4b5fd 50%, #f0abfc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
      ">RITESH FUNDS ADVISOR</div>
      <div style="font-size: 12px; color: #6b7194; margin-top: 4px; font-weight: 400; letter-spacing: 0.03em;">
        <span class='live-dot'></span>
        AI-Powered Portfolio Planner &nbsp;·&nbsp; India Markets
      </div>
    </div>
  </div>
  <div style="text-align: right; display: none;">
    <div style="font-size: 10px; color: #464c68; text-transform: uppercase; letter-spacing: 0.1em;">Version</div>
    <div style="font-size: 14px; font-weight: 700; color: #5b6af5;">2.0 PRO</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR – Dynamic allocation sliders + settings
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Allocation controls")

    risk_profile = st.selectbox(
        "Risk Profile",
        ["Conservative", "Balanced", "Aggressive", "Custom"],
        index=1,
    )

    # Preset allocation by risk
    presets = {
        "Conservative": [10, 20, 15, 35, 15, 5],
        "Balanced":     [22, 28, 20, 15, 10, 5],
        "Aggressive":   [35, 35, 20,  5,  3, 2],
        "Custom":       None,
    }
    preset_vals = presets[risk_profile]

    st.markdown("---")
    st.markdown("### 📊 Adjust split (%)")

    alloc_pcts = {}
    total_pct = 0
    for i, a in enumerate(DEFAULT_ALLOC):
        default_v = preset_vals[i] if preset_vals else a["default"]
        v = st.slider(
            a["label"],
            min_value=0, max_value=60,
            value=default_v,
            step=1,
            key=f"slider_{a['key']}",
        )
        alloc_pcts[a["key"]] = v
        total_pct += v

    # Live total indicator
    color = "#10b981" if total_pct == 100 else "#f43f5e"
    st.markdown(f"""
    <div style="margin-top:14px; padding:12px 14px; border-radius:10px;
      background: {'#052817' if total_pct==100 else '#1c0812'};
      border: 1px solid {'#10b981' if total_pct==100 else '#f43f5e'};">
      <div style="font-size:10px;color:#6b7194;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Total allocation</div>
      <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:{color};">{total_pct}%</div>
      <div style="font-size:11px;color:{color};margin-top:2px;">{'✓ Perfect balance' if total_pct==100 else f'{"▲" if total_pct>100 else "▼"} {abs(100-total_pct)}% {"over" if total_pct>100 else "under"}'}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Projection settings")
    proj_years = st.slider("Projection horizon (years)", 1, 30, 10)
    show_rate  = st.slider("Expected return % p.a.", 8, 24, 13)
    inflation  = st.slider("Inflation rate % p.a.", 3, 10, 6)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA – Inputs
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio inputs</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])

with c1:
    salary = st.number_input("Monthly take-home salary (₹)", min_value=0, step=1000, value=80000, format="%d")
with c2:
    invest_raw = st.number_input("Amount you can invest (₹/mo)", min_value=0, step=500, value=25000, format="%d")
with c3:
    invest_pct_input = st.number_input("Or set invest % of salary", min_value=0, max_value=100, step=1, value=0, format="%d",
                                        help="Set a % and it overrides the amount above")
with c4:
    st.markdown("<br>", unsafe_allow_html=True)
    if salary > 0:
        invest = invest_raw if invest_pct_input == 0 else int(salary * invest_pct_input / 100)
        pct_of_sal = round(invest / salary * 100, 1) if salary else 0
        health = "🟢 Excellent" if pct_of_sal >= 30 else ("🟡 Good" if pct_of_sal >= 20 else "🔴 Low")
        st.markdown(f"""
        <div style="background:#10142a;border:1px solid #1e2235;border-radius:12px;padding:14px 16px;margin-top:4px;">
          <div style="font-size:9px;color:#6b7194;text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px;">Invest ratio</div>
          <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#818cf8;">{pct_of_sal}%</div>
          <div style="font-size:11px;color:#9095b0;margin-top:3px;">{health}</div>
        </div>""", unsafe_allow_html=True)
    else:
        invest = invest_raw

# Validation
if salary <= 0 or invest <= 0:
    st.markdown("""
    <div class="tip-highlight">
      <b>💡 Getting started:</b> Enter your monthly salary and the amount you can invest each month.
      Adjust the allocation sliders in the sidebar, then watch your personalised plan generate in real-time.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if invest > salary:
    st.error("⚠ Investment amount exceeds salary. Please adjust.")
    st.stop()

# Recalc alloc using sidebar sliders
# normalise to 100% if not exactly 100
if total_pct > 0:
    norm = {k: v / total_pct for k, v in alloc_pcts.items()}
else:
    norm = {a["key"]: a["default"] / 100 for a in DEFAULT_ALLOC}

ALLOC = [
    {**a, "pct": round(norm[a["key"]] * 100, 1), "amt": invest * norm[a["key"]]}
    for a in DEFAULT_ALLOC
]

expenses = salary - invest
inv_pct_display = round(invest / salary * 100, 1)

# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW METRICS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio overview</div>', unsafe_allow_html=True)

real_return = show_rate - inflation
future_val  = sip_future(invest, show_rate, proj_years)
real_val    = sip_future(invest, real_return if real_return > 0 else 1, proj_years)
total_invested = invest * 12 * proj_years
wealth_gain = future_val - total_invested

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Monthly salary",    fmt(salary))
m2.metric("You invest",        fmt(invest),         f"{inv_pct_display}% of salary")
m3.metric("Monthly expenses",  fmt(expenses),       f"{100 - inv_pct_display:.0f}% of salary")
m4.metric("Annual investment",  fmt(invest * 12),    "Per year")
m5.metric(f"Future value ({proj_years}yr)", fmt(future_val), f"At {show_rate}% p.a.")
m6.metric("Wealth gained",     fmt(wealth_gain),    f"Real: {fmt(real_val)}")

# ─────────────────────────────────────────────────────────────────────────────
# ALLOCATION BREAKDOWN + DONUT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Allocation breakdown</div>', unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for a in ALLOC:
        bar_w = min(int(a["pct"] * 3.5), 100)
        st.markdown(f"""
        <div class="arow">
          <div class="arow-name">{a['label']} <small>{a['desc']}</small></div>
          <div class="arow-bar"><div class="arow-bar-fill" style="width:{bar_w}%;background:{a['color']};"></div></div>
          <div class="arow-pct">{a['pct']:.0f}%</div>
          <div class="arow-amt">{fmt(a['amt'])}<span style="font-size:10px;color:#464c68;font-weight:400;">/mo</span></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    fig_pie = go.Figure(go.Pie(
        labels=[a["label"] for a in ALLOC],
        values=[a["pct"] for a in ALLOC],
        hole=0.65,
        marker=dict(
            colors=[a["color"] for a in ALLOC],
            line=dict(color="#080b14", width=3),
        ),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<br>" + fmt(invest) + " → %{customdata}<extra></extra>",
        customdata=[fmt(a["amt"]) for a in ALLOC],
    ))
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        height=310,
        showlegend=True,
        legend=dict(
            font=dict(family="DM Sans", color="#6b7194", size=11),
            bgcolor="rgba(0,0,0,0)",
            orientation="v",
            x=0.75, y=0.5,
        ),
        annotations=[dict(
            text=f"<b style='font-size:17px'>{fmt(invest)}</b><br><span style='font-size:11px;color:#6b7194'>per month</span>",
            x=0.37, y=0.5, showarrow=False,
            font=dict(family="Syne", size=16, color="#dde1f0"),
            align="center",
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────────────────────────────────────
# GROWTH PROJECTION CHART  (dynamic: years + rate from sidebar)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="sec-hdr">Growth projection — {proj_years}-year horizon</div>', unsafe_allow_html=True)

yr_range   = list(range(1, proj_years + 1))
inv_total  = [invest * 12 * y for y in yr_range]
val_base   = [sip_future(invest, 10, y) for y in yr_range]
val_sel    = [sip_future(invest, show_rate, y) for y in yr_range]
val_real   = [sip_future(invest, max(show_rate - inflation, 1), y) for y in yr_range]

fig_proj = go.Figure()
fig_proj.add_trace(go.Scatter(
    x=yr_range, y=inv_total, name="Capital invested",
    line=dict(color="#252840", width=2, dash="dot"),
    fill=None,
))
fig_proj.add_trace(go.Scatter(
    x=yr_range, y=val_base, name="At 10% p.a.",
    line=dict(color="#334155", width=1.5, dash="dash"),
))
fig_proj.add_trace(go.Scatter(
    x=yr_range, y=val_sel, name=f"At {show_rate}% p.a.",
    line=dict(color="#5b6af5", width=3),
    fill="tonexty", fillcolor="rgba(91,106,245,0.07)",
))
fig_proj.add_trace(go.Scatter(
    x=yr_range, y=val_real, name=f"Real (inflation-adj {inflation}%)",
    line=dict(color="#10b981", width=2, dash="longdash"),
))

fig_proj.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(16,20,42,0.7)",
    margin=dict(t=14, b=10, l=10, r=10),
    height=300,
    legend=dict(
        font=dict(family="DM Sans", color="#6b7194", size=11),
        bgcolor="rgba(0,0,0,0)",
        orientation="h", x=0, y=1.08,
    ),
    xaxis=dict(
        tickcolor="#252840", gridcolor="#13172a",
        color="#6b7194", tickvals=yr_range,
        ticktext=[f"Yr {y}" for y in yr_range],
        tickfont=dict(size=10),
    ),
    yaxis=dict(
        tickcolor="#252840", gridcolor="#13172a",
        color="#6b7194", tickformat="₹.2s",
        tickfont=dict(size=10),
    ),
    hovermode="x unified",
)
st.plotly_chart(fig_proj, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────────────────────────────────────
# MILESTONES  (dynamic)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Wealth milestones</div>', unsafe_allow_html=True)

milestones = [10_00_000, 25_00_000, 50_00_000, 1_00_00_000, 5_00_00_000, 10_00_00_000]
milestone_labels = ["₹10L","₹25L","₹50L","₹1Cr","₹5Cr","₹10Cr"]

cols_ms = st.columns(len(milestones))
for i, (ms, lbl) in enumerate(zip(milestones, milestone_labels)):
    # find year when portfolio crosses milestone
    yr_hit = None
    for y in range(1, 51):
        if sip_future(invest, show_rate, y) >= ms:
            yr_hit = y
            break
    with cols_ms[i]:
        if yr_hit:
            st.markdown(f"""
            <div style="background:#10142a;border:1px solid #1e2235;border-radius:12px;padding:14px 12px;text-align:center;">
              <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#818cf8;">{lbl}</div>
              <div style="font-size:22px;font-weight:700;color:#dde1f0;margin:6px 0;">{yr_hit}<span style="font-size:12px;color:#6b7194;">yr</span></div>
              <div style="font-size:10px;color:#6b7194;">to reach</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0d1020;border:1px solid #1a1d2a;border-radius:12px;padding:14px 12px;text-align:center;opacity:.45;">
              <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:800;color:#464c68;">{lbl}</div>
              <div style="font-size:14px;color:#464c68;margin:6px 0;">50yr+</div>
              <div style="font-size:10px;color:#3a3f55;">to reach</div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOP PICKS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Top investment picks</div>', unsafe_allow_html=True)

filter_opt = st.radio("Filter", ["All","Stocks","ETFs","Mutual Funds","FD / Debt"], horizontal=True, label_visibility="collapsed")
cat_map = {"All":None,"Stocks":"shares","ETFs":"etf","Mutual Funds":"mf","FD / Debt":"fd"}
filtered_picks = PICKS if not cat_map[filter_opt] else [p for p in PICKS if p["cat"] == cat_map[filter_opt]]

cat_count = {}
for p in PICKS: cat_count[p["cat"]] = cat_count.get(p["cat"], 0) + 1

alloc_by_key = {a["key"]: a for a in ALLOC}
pick_cols = st.columns(3)
for i, p in enumerate(filtered_picks):
    alloc_obj = alloc_by_key.get(p["cat"])
    suggested = fmt(round(alloc_obj["amt"] / cat_count.get(p["cat"], 1))) if alloc_obj else ""
    m = CAT_META.get(p["cat"], CAT_META["shares"])
    risk_col = RISK_COLOR.get(p.get("risk","Medium"), "#fb923c")
    with pick_cols[i % 3]:
        st.markdown(f"""
        <div class="pick-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:2px;">
            <span class="pick-cat" style="background:{m['bg']};color:{m['color']}">{m['label']}</span>
            <span style="font-size:9px;font-weight:700;color:{risk_col};background:rgba(0,0,0,.25);padding:2px 7px;border-radius:20px;border:1px solid {risk_col}44;">
              {p.get('risk','—')} RISK
            </span>
          </div>
          <div class="pick-name">{p['name']}</div>
          <div class="pick-ticker">{p['ticker']}</div>
          <div class="pick-why">{p['why']}</div>
          <div class="pick-ret">↑ {p['ret']}</div>
          {f'<div class="pick-alloc">→ Suggested {suggested}/mo</div>' if suggested else ''}
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY BREAKDOWN BAR CHART
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Monthly allocation by category</div>', unsafe_allow_html=True)

fig_bar = go.Figure(go.Bar(
    x=[a["label"] for a in ALLOC],
    y=[a["amt"] for a in ALLOC],
    marker=dict(
        color=[a["color"] for a in ALLOC],
        line=dict(color="rgba(0,0,0,0)", width=0),
    ),
    text=[fmt(a["amt"]) for a in ALLOC],
    textposition="outside",
    textfont=dict(family="Syne", size=11, color="#9095b0"),
    hovertemplate="<b>%{x}</b><br>%{y:,.0f} ₹<extra></extra>",
))
fig_bar.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(16,20,42,0.6)",
    margin=dict(t=20, b=10, l=10, r=10),
    height=240,
    bargap=0.3,
    xaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
    yaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="#13172a", tickformat="₹,.0f", tickfont=dict(size=10)),
    showlegend=False,
)
st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────────────────────────────────────
# TIPS + DISCLAIMER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="infobox">
  💡 <b>Pro tips from RITESH FUNDS ADVISOR:</b><br>
  • Start SIPs on the 1st of every month — consistent entry beats timing the market.<br>
  • For stocks, invest in 2–3 tranches per month. Never deploy all funds in a single day.<br>
  • Keep 3–6 months of expenses as liquid emergency fund <em>before</em> any investment.<br>
  • Review and rebalance your portfolio every 6 months. Use the sliders above to adjust as life changes.<br>
  • Increase your SIP by 10% every year — a small step-up creates massive long-term wealth.
</div>
<div class="disclaimer">
  ⚠ RITESH FUNDS ADVISOR is a personal finance education tool and does not constitute SEBI-registered financial advice.
  Past returns are indicative only and do not guarantee future performance.
  All investments are subject to market risk. Please read all scheme-related documents carefully and consult a qualified
  investment advisor before making any financial decisions.
</div>
""", unsafe_allow_html=True)
