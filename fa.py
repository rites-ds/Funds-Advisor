import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import math
import json
from datetime import date

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SMARTFUNDS ADVISOR",
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
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1500px; }

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

[data-testid="stSlider"] [data-testid="stWidgetLabel"] > div > p {
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
  transition: all 0.2s !important;
  text-transform: uppercase;
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(91,106,245,0.35) !important;
}
.stButton > button:active { transform: translateY(0); }

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
  font-size: 22px !important;
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
[data-testid="stSelectbox"] label > div > p {
  color: #6b7194 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
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
  transition: all 0.15s;
}
.stRadio > div > label:hover { border-color: #5b6af5 !important; }

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
  animation: pulse 1.8s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}

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

.score-ring {
  background: #10142a;
  border: 1px solid #1e2235;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}

.goal-card {
  background: linear-gradient(135deg, #10142a 0%, #0e1224 100%);
  border: 1px solid #1e2235;
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 10px;
  position: relative;
  overflow: hidden;
}
.goal-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}

.tax-card {
  background: #10142a;
  border: 1px solid #1e2235;
  border-radius: 14px;
  padding: 18px;
}

.tab-badge {
  background: #5b6af5;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: 6px;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0c0f1d; }
::-webkit-scrollbar-thumb { background: #252840; border-radius: 3px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: #0c0f1d !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 4px !important;
  border: 1px solid #1e2235 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 8px !important;
  color: #6b7194 !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #5b6af5, #7c3aed) !important;
  color: #fff !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

/* Expander */
.streamlit-expanderHeader {
  background: #10142a !important;
  border: 1px solid #1e2235 !important;
  border-radius: 10px !important;
  color: #9095b0 !important;
  font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATIC DATA - REMOVED PPF/NPS
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_ALLOC = [
    {"key": "shares", "label": "Stocks",        "default": 0, "color": "#5b6af5", "desc": "Direct equity"},
    {"key": "mf",     "label": "Mutual Funds",  "default": 0, "color": "#10b981", "desc": "Equity SIP"},
    {"key": "etf",    "label": "ETFs",          "default": 0, "color": "#f59e0b", "desc": "Index passive"},
    {"key": "fd",     "label": "FD / Debt",     "default": 0, "color": "#06b6d4", "desc": "Stable return"},
    {"key": "gold",   "label": "Gold / SGB",    "default": 0, "color": "#fb923c", "desc": "Hedge"},
]

PICKS = [
    {"cat":"shares","name":"Reliance Industries","ticker":"NSE: RELIANCE","why":"Jio + retail vertical integration fuels multi-decade compounding.","ret":"~18% CAGR (5yr)","risk":"Medium","sector":"Conglomerate"},
    {"cat":"shares","name":"HDFC Bank","ticker":"NSE: HDFCBANK","why":"India's most trusted private bank. Consistent asset quality.","ret":"~14% CAGR (5yr)","risk":"Low","sector":"Banking"},
    {"cat":"shares","name":"Infosys","ticker":"NSE: INFY","why":"IT leader with global enterprise clients and growing margins.","ret":"~16% CAGR (5yr)","risk":"Low","sector":"IT"},
    {"cat":"shares","name":"Tata Motors","ticker":"NSE: TATAMOTORS","why":"EV pivot + JLR Europe recovery — high conviction growth.","ret":"~22% CAGR (3yr)","risk":"High","sector":"Auto"},
    {"cat":"shares","name":"Bajaj Finance","ticker":"NSE: BAJFINANCE","why":"NBFC king — massive consumer lending book, fintech moat.","ret":"~20% CAGR (5yr)","risk":"Medium","sector":"NBFC"},
    {"cat":"shares","name":"Adani Ports","ticker":"NSE: ADANIPORTS","why":"Dominant ports + logistics ecosystem; infra supercycle beneficiary.","ret":"~17% CAGR (5yr)","risk":"Medium","sector":"Infrastructure"},
    {"cat":"shares","name":"Asian Paints","ticker":"NSE: ASIANPAINT","why":"Consistent compounder with 60% market share and pricing power.","ret":"~15% CAGR (5yr)","risk":"Low","sector":"Paints"},
    {"cat":"shares","name":"Zomato","ticker":"NSE: ZOMATO","why":"Profitable food-tech leader. Hyperpure B2B + Blinkit dark stores.","ret":"~30% CAGR (2yr)","risk":"High","sector":"Tech/Food"},
    {"cat":"etf","name":"Nifty 50 ETF","ticker":"NSE: NIFTYBEES","why":"Track 50 blue chips passively. Expense ratio just 0.04%.","ret":"~13% CAGR (5yr)","risk":"Low","sector":"Index"},
    {"cat":"etf","name":"Nifty Next 50 ETF","ticker":"NSE: JUNIORBEES","why":"Mid-large blend — higher growth ceiling than Nifty 50.","ret":"~15% CAGR (5yr)","risk":"Low-Med","sector":"Index"},
    {"cat":"etf","name":"Nasdaq 100 ETF","ticker":"NSE: MOM100","why":"US tech giants (Apple, Google, Nvidia) in INR — global diversification.","ret":"~20% CAGR (5yr)","risk":"Medium","sector":"Global"},
    {"cat":"etf","name":"Nifty Midcap 150 ETF","ticker":"NSE: NM150BEES","why":"Midcap exposure at low cost. Long runway for growth.","ret":"~18% CAGR (5yr)","risk":"Medium","sector":"Midcap"},
    {"cat":"etf","name":"Gold ETF","ticker":"NSE: GOLDBEES","why":"Digital gold without storage hassle. Inflation hedge.","ret":"~12% CAGR (5yr)","risk":"Low","sector":"Commodity"},
    {"cat":"mf","name":"Mirae Asset Large Cap","ticker":"Direct Growth","why":"Consistently 5-star rated. Top quartile large-cap performer.","ret":"~15% CAGR (5yr)","risk":"Low","sector":"Large Cap"},
    {"cat":"mf","name":"Parag Parikh Flexi Cap","ticker":"Direct Growth","why":"Flexi-cap with international allocation and very low portfolio churn.","ret":"~19% CAGR (5yr)","risk":"Low-Med","sector":"Flexi Cap"},
    {"cat":"mf","name":"Axis Small Cap","ticker":"Direct Growth","why":"Best-in-class small cap with disciplined stock selection.","ret":"~21% CAGR (5yr)","risk":"High","sector":"Small Cap"},
    {"cat":"mf","name":"SBI Nifty Index Fund","ticker":"Direct Growth","why":"Ultra low-cost index tracking — perfect anchor for any SIP.","ret":"~13% CAGR (5yr)","risk":"Low","sector":"Index"},
    {"cat":"mf","name":"Canara Robeco Emerging Equities","ticker":"Direct Growth","why":"Strong mid-small cap blended fund. Consistent alpha generation.","ret":"~22% CAGR (5yr)","risk":"High","sector":"Mid-Small Cap"},
    {"cat":"mf","name":"ICICI Pru Balanced Advantage","ticker":"Direct Growth","why":"Dynamic asset allocation — adapts to market conditions automatically.","ret":"~14% CAGR (5yr)","risk":"Low-Med","sector":"Hybrid"},
    {"cat":"fd","name":"SBI FD (2yr)","ticker":"Fixed Deposit","why":"Capital safety with ~7.25% p.a. Guaranteed and predictable.","ret":"7.25% p.a.","risk":"None","sector":"Debt"},
    {"cat":"fd","name":"RBI Floating Rate Bonds","ticker":"RBI Bond","why":"7.35% floating, sovereign guarantee — safest debt option.","ret":"7.35% p.a.","risk":"None","sector":"Govt Debt"},
    {"cat":"gold","name":"Sovereign Gold Bond","ticker":"RBI SGB","why":"8% capital gain exemption on maturity + 2.5% interest p.a.","ret":"~12% (w/ interest)","risk":"Low","sector":"Commodity"},
]

RISK_COLOR = {"None":"#10b981","Low":"#34d399","Low-Med":"#f59e0b","Medium":"#fb923c","High":"#f43f5e"}
CAT_META = {
    "shares": {"label":"Stock",       "bg":"#1a2550","color":"#818cf8"},
    "etf":    {"label":"ETF",         "bg":"#2d1f07","color":"#f59e0b"},
    "mf":     {"label":"Mutual Fund", "bg":"#052817","color":"#34d399"},
    "fd":     {"label":"FD / Debt",   "bg":"#062025","color":"#22d3ee"},
    "gold":   {"label":"Gold",        "bg":"#2a1505","color":"#fb923c"},
}

GOAL_ICONS = {"🏠 House": "🏠", "🚗 Car": "🚗", "🎓 Education": "🎓", "✈️ Vacation": "✈️", "💍 Wedding": "💍", "🏦 Retirement": "🏦", "🏥 Medical Fund": "🏥"}
GOAL_COLORS = {"🏠 House": "#5b6af5", "🚗 Car": "#10b981", "🎓 Education": "#f59e0b", "✈️ Vacation": "#06b6d4", "💍 Wedding": "#f472b6", "🏦 Retirement": "#a78bfa", "🏥 Medical Fund": "#fb923c"}

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

def step_up_sip(monthly, rate_annual, years, step_up_pct):
    """SIP with annual step-up"""
    r = rate_annual / 12 / 100
    total = 0
    current_sip = monthly
    for y in range(years):
        months_left = (years - y) * 12
        for m in range(12):
            n = months_left - m
            total += current_sip * ((1 + r) ** n)
        current_sip *= (1 + step_up_pct / 100)
    return total

def lumpsum_future(amount, rate_annual, years):
    return amount * ((1 + rate_annual / 100) ** years)

def months_to_goal(monthly_sip, rate_annual, target):
    r = rate_annual / 12 / 100
    if r == 0:
        return math.ceil(target / monthly_sip)
    lo, hi = 1, 600
    while lo < hi:
        mid = (lo + hi) // 2
        val = monthly_sip * (((1 + r) ** mid - 1) / r) * (1 + r)
        if val >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo

def compute_health_score(pct_invested, has_emergency, total_pct, risk_profile, proj_years):
    score = 0
    if pct_invested >= 30: score += 30
    elif pct_invested >= 20: score += 20
    elif pct_invested >= 10: score += 10
    else: score += 5
    if 95 <= total_pct <= 105: score += 25
    elif 90 <= total_pct <= 110: score += 15
    else: score += 5
    if has_emergency: score += 20
    if proj_years >= 15: score += 15
    elif proj_years >= 7: score += 10
    else: score += 5
    if risk_profile in ["Balanced", "Aggressive"]: score += 10
    else: score += 7
    return min(score, 100)

def tax_old_regime(income):
    slabs = [(250000, 0), (500000, 0.05), (1000000, 0.20), (float('inf'), 0.30)]
    deductions = 150000
    taxable = max(0, income - deductions - 50000)
    tax = 0
    prev = 0
    for limit, rate in slabs:
        if taxable <= prev: break
        band = min(taxable, limit) - prev
        tax += band * rate
        prev = limit
    if taxable <= 500000: tax = 0
    tax = tax * 1.04
    return tax

def tax_new_regime(income):
    slabs = [(300000, 0), (600000, 0.05), (900000, 0.10), (1200000, 0.15), (1500000, 0.20), (float('inf'), 0.30)]
    taxable = max(0, income - 75000)
    tax = 0
    prev = 0
    for limit, rate in slabs:
        if taxable <= prev: break
        band = min(taxable, limit) - prev
        tax += band * rate
        prev = limit
    if taxable <= 700000: tax = 0
    tax = tax * 1.04
    return tax

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 2rem 0 1.5rem; border-bottom: 1px solid #1e2235; margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between;">
  <div style="display: flex; align-items: center; gap: 18px;">
    <div style="
      width: 52px; height: 52px; border-radius: 14px;
      background: linear-gradient(135deg, #5b6af5, #7c3aed);
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; box-shadow: 0 8px 24px rgba(91,106,245,0.4);
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
      ">SMARTFUNDS ADVISOR</div>
      <div style="font-size: 12px; color: #6b7194; margin-top: 4px; font-weight: 400; letter-spacing: 0.03em;">
        <span class='live-dot'></span>
        XAI-Powered Portfolio Planner &nbsp;·&nbsp; India Markets &nbsp;·&nbsp; v3.0 PRO
      </div>
    </div>
  </div>
  <div style="display:flex;gap:12px;align-items:center;">
    <div style="text-align:right;">
      <div style="font-size:10px;color:#464c68;text-transform:uppercase;letter-spacing:0.1em;">Today</div>
      <div style="font-size:13px;font-weight:700;color:#5b6af5;">{date.today().strftime('%A, %d %B %Y')}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Allocation controls")

    # Risk profile - default to "Custom" (index 3)
    risk_profile = st.selectbox(
        "Risk Profile",
        ["Conservative", "Balanced", "Aggressive", "Custom"],
        index=3,
    )

    presets = {
        "Conservative": [10, 20, 15, 5],  # Stocks, MF, ETF, FD, Gold (no PPF)
        "Balanced":     [22, 28, 20, 5],  # Stocks, MF, ETF, FD, Gold
        "Aggressive":   [35, 35, 20, 2],  # Stocks, MF, ETF, FD, Gold
        "Custom":       None,
    }
    preset_vals = presets[risk_profile]

    st.markdown("---")
    st.markdown("### 📊 Adjust split (%) — must total 100%")
    st.markdown("""
    <div style="font-size:11px;color:#6b7194;margin-bottom:12px;line-height:1.5;">
      Drag sliders to set your allocation. The remaining % is shown live.
      All sliders start at 0 by default.
    </div>
    """, unsafe_allow_html=True)

    alloc_pcts = {}
    used_so_far = 0
    raw_vals = {}
    last_idx = len(DEFAULT_ALLOC) - 1
    
    for i, a in enumerate(DEFAULT_ALLOC):
        if i == last_idx:
            break
        if preset_vals is not None and i < len(preset_vals):
            default_v = preset_vals[i]
        else:
            default_v = 0
            
        remaining_for_this = max(1, 100 - used_so_far)
        default_v = min(default_v, remaining_for_this)
        v = st.slider(
            a["label"],
            min_value=0,
            max_value=remaining_for_this,
            value=default_v,
            step=1,
            key=f"slider_{a['key']}",
        )
        raw_vals[a["key"]] = v
        used_so_far += v

    last_key = DEFAULT_ALLOC[-1]["key"]
    raw_vals[last_key] = max(0, 100 - used_so_far)
    st.markdown(
        f"<div style='font-size:11px;color:#6b7194;padding:4px 0;'>"
        f"{DEFAULT_ALLOC[-1]['label']}: auto-set to <b style='color:#dde1f0'>{raw_vals[last_key]}%</b>"
        f"</div>",
        unsafe_allow_html=True,
    )

    alloc_pcts = raw_vals
    total_pct = sum(alloc_pcts.values())

    st.markdown(f"""
    <div style="margin-top:14px; padding:12px 14px; border-radius:10px;
      background: #052817;
      border: 1px solid #10b981;">
      <div style="font-size:10px;color:#6b7194;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">Total allocation</div>
      <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#10b981;">{total_pct}%</div>
      <div style="font-size:11px;color:#10b981;margin-top:2px;">{'✓ Perfectly balanced' if total_pct == 100 else '⚠ Adjust to reach 100%'}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="margin-top:8px;font-size:11px;color:#6b7194;">
      {" &nbsp;·&nbsp; ".join([f"<b style='color:#dde1f0'>{a['label']}</b> {alloc_pcts.get(a['key'], 0)}%" for a in DEFAULT_ALLOC])}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Projection settings")
    proj_years = st.slider("Projection horizon (years)", 1, 40, 10)
    show_rate  = st.slider("Expected return % p.a.", 8, 24, 13)
    inflation  = st.slider("Inflation rate % p.a.", 3, 10, 6)
    step_up    = st.slider("Annual SIP step-up %", 0, 25, 10, help="Increase SIP by this % every year")

    st.markdown("---")
    st.markdown("### 🛡 Safety net")
    has_emergency = st.checkbox("I have an emergency fund (3–6 mo)", value=False)
    emergency_months = st.slider("Emergency fund target (months)", 3, 12, 6) if not has_emergency else 6

# ─────────────────────────────────────────────────────────────────────────────
# MAIN INPUTS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio inputs</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])

with c1:
    salary = st.number_input("Monthly take-home salary (₹)", min_value=0, step=1000, value=0, format="%d")
with c2:
    invest_raw = st.number_input("Amount you can invest (₹/mo)", min_value=0, step=500, value=0, format="%d")
with c3:
    invest_pct_input = st.number_input("Or set invest % of salary", min_value=0, max_value=100, step=1, value=0, format="%d")
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

if total_pct != 100:
    st.warning(f"⚠ Your allocation total is {total_pct}%. Please adjust sliders to reach exactly 100%.")
    st.stop()

# Normalize allocation
norm = {k: v / 100 for k, v in alloc_pcts.items()}

ALLOC = [
    {**a, "pct": round(norm[a["key"]] * 100, 1), "amt": invest * norm[a["key"]]}
    for a in DEFAULT_ALLOC
]

expenses = salary - invest
inv_pct_display = round(invest / salary * 100, 1)

# Core calculations
real_return    = show_rate - inflation
future_val     = sip_future(invest, show_rate, proj_years)
real_val       = sip_future(invest, real_return if real_return > 0 else 1, proj_years)
total_invested = invest * 12 * proj_years
wealth_gain    = future_val - total_invested
stepup_val     = step_up_sip(invest, show_rate, proj_years, step_up)
stepup_gain    = stepup_val - total_invested
health_score   = compute_health_score(inv_pct_display, has_emergency, total_pct, risk_profile, proj_years)

# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW METRICS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio overview</div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
m1.metric("Monthly salary",           fmt(salary))
m2.metric("You invest",               fmt(invest),         f"{inv_pct_display}% of salary")
m3.metric("Monthly expenses",         fmt(expenses),       f"{100 - inv_pct_display:.0f}% of salary")
m4.metric("Annual investment",        fmt(invest * 12),    "Per year")
m5.metric(f"Future value ({proj_years}yr)",  fmt(future_val),     f"At {show_rate}% p.a.")
m6.metric("Wealth gained",            fmt(wealth_gain),    f"Real: {fmt(real_val)}")
m7.metric("With 10% step-up",         fmt(stepup_val),     f"+{fmt(stepup_val - future_val)} extra")

# ─────────────────────────────────────────────────────────────────────────────
# PORTFOLIO HEALTH SCORE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Portfolio health score</div>', unsafe_allow_html=True)

hs_col1, hs_col2 = st.columns([1, 2])
with hs_col1:
    score_color = "#10b981" if health_score >= 75 else ("#f59e0b" if health_score >= 50 else "#f43f5e")
    score_label = "Excellent" if health_score >= 80 else ("Good" if health_score >= 65 else ("Fair" if health_score >= 45 else "Needs Work"))
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#252840", 'tickfont': {'color': '#6b7194', 'size': 10}},
            'bar': {'color': score_color, 'thickness': 0.3},
            'bgcolor': "#0c0f1d",
            'steps': [
                {'range': [0, 45], 'color': '#1c0812'},
                {'range': [45, 65], 'color': '#1a1500'},
                {'range': [65, 80], 'color': '#0a2010'},
                {'range': [80, 100], 'color': '#062817'},
            ],
            'threshold': {'line': {'color': score_color, 'width': 3}, 'thickness': 0.8, 'value': health_score}
        },
        number={'suffix': "/100", 'font': {'family': 'Syne', 'size': 28, 'color': score_color}},
        title={'text': f"<span style='font-size:13px;color:#6b7194'>{score_label}</span>"}
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=200,
        margin=dict(t=30, b=10, l=20, r=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

with hs_col2:
    checks = [
        ("Savings rate ≥ 20%", inv_pct_display >= 20, f"Currently {inv_pct_display:.1f}%"),
        ("Allocation sums to 100%", total_pct == 100, f"Currently {total_pct}%"),
        ("Emergency fund in place", has_emergency, "Set in sidebar"),
        ("Long-term horizon (7+ yrs)", proj_years >= 7, f"Currently {proj_years} yrs"),
        ("Diversified across asset classes", len([v for v in alloc_pcts.values() if v > 0]) >= 3, f"{len([v for v in alloc_pcts.values() if v > 0])} active classes"),
        ("SIP step-up planned", step_up >= 5, f"Currently {step_up}% step-up"),
    ]
    cols_chk = st.columns(2)
    for idx, (label, ok, hint) in enumerate(checks):
        with cols_chk[idx % 2]:
            icon = "✅" if ok else "❌"
            color = "#10b981" if ok else "#f43f5e"
            st.markdown(f"""
            <div style="background:#10142a;border:1px solid #1e2235;border-radius:10px;padding:12px 14px;margin-bottom:8px;">
              <div style="font-size:12px;font-weight:600;color:{color};">{icon} {label}</div>
              <div style="font-size:10px;color:#464c68;margin-top:3px;">{hint}</div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Allocation & Growth",
    "🎯 Goal Planner",
    "💰 Tax Calculator",
    "📈 SIP vs Lumpsum",
    "🏆 Top Picks",
])

# ──────────────────────────────────────────────────────────
# TAB 1 — Allocation & Growth
# ──────────────────────────────────────────────────────────
with tab1:
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
            marker=dict(colors=[a["color"] for a in ALLOC], line=dict(color="#080b14", width=3)),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value:.1f}%<br>" + fmt(invest) + " → %{customdata}<extra></extra>",
            customdata=[fmt(a["amt"]) for a in ALLOC],
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=10), height=310, showlegend=True,
            legend=dict(font=dict(family="DM Sans", color="#6b7194", size=11), bgcolor="rgba(0,0,0,0)", orientation="v", x=0.75, y=0.5),
            annotations=[dict(
                text=f"<b style='font-size:17px'>{fmt(invest)}</b><br><span style='font-size:11px;color:#6b7194'>per month</span>",
                x=0.37, y=0.5, showarrow=False,
                font=dict(family="Syne", size=16, color="#dde1f0"), align="center",
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    # Growth projection
    st.markdown(f'<div class="sec-hdr">Growth projection — {proj_years}-year horizon</div>', unsafe_allow_html=True)

    yr_range  = list(range(1, proj_years + 1))
    inv_total = [invest * 12 * y for y in yr_range]
    val_base  = [sip_future(invest, 10, y) for y in yr_range]
    val_sel   = [sip_future(invest, show_rate, y) for y in yr_range]
    val_real  = [sip_future(invest, max(real_return, 1), y) for y in yr_range]
    val_step  = [step_up_sip(invest, show_rate, y, step_up) for y in yr_range]

    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(x=yr_range, y=inv_total, name="Capital invested",
        line=dict(color="#252840", width=2, dash="dot")))
    fig_proj.add_trace(go.Scatter(x=yr_range, y=val_base, name="At 10% p.a.",
        line=dict(color="#334155", width=1.5, dash="dash")))
    fig_proj.add_trace(go.Scatter(x=yr_range, y=val_sel, name=f"At {show_rate}% p.a.",
        line=dict(color="#5b6af5", width=3), fill="tonexty", fillcolor="rgba(91,106,245,0.07)"))
    fig_proj.add_trace(go.Scatter(x=yr_range, y=val_real, name=f"Real (adj {inflation}%)",
        line=dict(color="#10b981", width=2, dash="longdash")))
    fig_proj.add_trace(go.Scatter(x=yr_range, y=val_step, name=f"With {step_up}% step-up",
        line=dict(color="#f59e0b", width=2.5, dash="solid")))

    fig_proj.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(16,20,42,0.7)",
        margin=dict(t=14, b=10, l=10, r=10), height=320,
        legend=dict(font=dict(family="DM Sans", color="#6b7194", size=11), bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.08),
        xaxis=dict(tickcolor="#252840", gridcolor="#13172a", color="#6b7194", tickvals=yr_range, ticktext=[f"Yr {y}" for y in yr_range], tickfont=dict(size=10)),
        yaxis=dict(tickcolor="#252840", gridcolor="#13172a", color="#6b7194", tickformat="₹.2s", tickfont=dict(size=10)),
        hovermode="x unified",
    )
    st.plotly_chart(fig_proj, use_container_width=True, config={"displayModeBar": False})

    # Milestones
    st.markdown('<div class="sec-hdr">Wealth milestones</div>', unsafe_allow_html=True)
    milestones = [10_00_000, 25_00_000, 50_00_000, 1_00_00_000, 5_00_00_000, 10_00_00_000]
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
                <div style="background:#10142a;border:1px solid #1e2235;border-radius:12px;padding:14px 12px;text-align:center;">
                  <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:#818cf8;">{lbl}</div>
                  <div style="font-size:22px;font-weight:700;color:#dde1f0;margin:6px 0;">{yr_hit}<span style="font-size:11px;color:#6b7194;">yr</span></div>
                  <div style="font-size:10px;color:#6b7194;">to reach</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#0d1020;border:1px solid #1a1d2a;border-radius:12px;padding:14px 12px;text-align:center;opacity:.45;">
                  <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:#464c68;">{lbl}</div>
                  <div style="font-size:14px;color:#464c68;margin:6px 0;">50yr+</div>
                  <div style="font-size:10px;color:#3a3f55;">to reach</div>
                </div>""", unsafe_allow_html=True)

    # Bar chart
    st.markdown('<div class="sec-hdr">Monthly allocation by category</div>', unsafe_allow_html=True)
    fig_bar = go.Figure(go.Bar(
        x=[a["label"] for a in ALLOC], y=[a["amt"] for a in ALLOC],
        marker=dict(color=[a["color"] for a in ALLOC], line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[fmt(a["amt"]) for a in ALLOC], textposition="outside",
        textfont=dict(family="Syne", size=11, color="#9095b0"),
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} ₹<extra></extra>",
    ))
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(16,20,42,0.6)",
        margin=dict(t=20, b=10, l=10, r=10), height=240, bargap=0.3,
        xaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
        yaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="#13172a", tickformat="₹,.0f", tickfont=dict(size=10)),
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ──────────────────────────────────────────────────────────
# TAB 2 — Goal Planner
# ──────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-hdr">Goal-based investment planner</div>', unsafe_allow_html=True)

    goal_col1, goal_col2 = st.columns([1, 1])
    with goal_col1:
        goal_type    = st.selectbox("Goal type", list(GOAL_ICONS.keys()))
        goal_amount  = st.number_input("Target amount (₹)", min_value=10000, step=50000, value=5000000, format="%d")
        goal_years   = st.slider("Time horizon (years)", 1, 30, 5, key="goal_yrs")
    with goal_col2:
        goal_rate    = st.slider("Expected return %", 6, 20, 12, key="goal_rate")
        existing_amt = st.number_input("Existing savings towards this goal (₹)", min_value=0, step=10000, value=0, format="%d")
        goal_inflation_toggle = st.checkbox("Adjust goal for inflation", value=True)

    goal_inflated = goal_amount * ((1 + inflation / 100) ** goal_years) if goal_inflation_toggle else goal_amount
    future_existing = lumpsum_future(existing_amt, goal_rate, goal_years)
    shortfall = max(0, goal_inflated - future_existing)

    r_m = goal_rate / 12 / 100
    n   = goal_years * 12
    if r_m > 0 and shortfall > 0:
        required_sip = shortfall * r_m / (((1 + r_m) ** n - 1) * (1 + r_m))
    else:
        required_sip = shortfall / n if n > 0 else 0

    achievable = sip_future(invest, goal_rate, goal_years) + future_existing
    surplus_deficit = achievable - goal_inflated
    pct_achieved = min(100, achievable / goal_inflated * 100) if goal_inflated > 0 else 100

    g_color = GOAL_COLORS.get(goal_type, "#5b6af5")
    icon = GOAL_ICONS.get(goal_type, "🎯")

    gc1, gc2, gc3, gc4 = st.columns(4)
    gc1.metric(f"{icon} Target", fmt(goal_amount))
    gc2.metric("Inflation-adjusted", fmt(goal_inflated), f"+{fmt(goal_inflated - goal_amount)}" if goal_inflation_toggle else "No adj.")
    gc3.metric("Required SIP", fmt(required_sip), f"from ₹0 savings")
    gc4.metric("Current SIP achieves", f"{pct_achieved:.1f}%", fmt(surplus_deficit) if surplus_deficit >= 0 else f"-{fmt(abs(surplus_deficit))}")

    st.markdown(f"""
    <div style="background:#10142a;border:1px solid #1e2235;border-radius:14px;padding:20px;margin:12px 0;">
      <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
        <span style="font-size:12px;color:#9095b0;">Goal progress with current SIP</span>
        <span style="font-family:'Syne',sans-serif;font-weight:700;color:{g_color};">{pct_achieved:.1f}%</span>
      </div>
      <div style="height:10px;background:#1e2235;border-radius:5px;overflow:hidden;">
        <div style="height:100%;width:{min(pct_achieved, 100):.1f}%;background:linear-gradient(90deg,{g_color},{g_color}99);border-radius:5px;transition:width 0.5s;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:8px;">
        <span style="font-size:10px;color:#464c68;">₹0</span>
        <span style="font-size:10px;color:#464c68;">{fmt(goal_inflated)}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">Quick multi-goal overview</div>', unsafe_allow_html=True)

    quick_goals = [
        ("🏠 House", 7500000, 10, 12),
        ("🚗 Car", 1500000, 4, 10),
        ("🎓 Education", 3000000, 8, 12),
        ("🏦 Retirement", 50000000, 25, 13),
    ]

    g_cols = st.columns(4)
    for i, (g_name, g_amt, g_yrs, g_rt) in enumerate(quick_goals):
        g_adj = g_amt * ((1 + inflation / 100) ** g_yrs)
        r_m2 = g_rt / 12 / 100
        n2 = g_yrs * 12
        req_sip = g_adj * r_m2 / (((1 + r_m2) ** n2 - 1) * (1 + r_m2)) if r_m2 > 0 else g_adj / n2
        g_c = GOAL_COLORS.get(g_name, "#5b6af5")
        can_do = invest >= req_sip
        with g_cols[i]:
            st.markdown(f"""
            <div style="background:#10142a;border:1px solid {'#10b981' if can_do else '#f43f5e'}22;border-radius:14px;padding:16px;text-align:center;">
              <div style="font-size:24px;margin-bottom:6px;">{g_name.split()[0]}</div>
              <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#dde1f0;">{g_name.split(' ',1)[1]}</div>
              <div style="font-size:11px;color:#6b7194;margin:4px 0;">{g_yrs} yrs · {fmt(g_adj)}</div>
              <div style="font-size:13px;font-weight:700;color:{g_c};margin-top:8px;">{fmt(req_sip)}/mo</div>
              <div style="font-size:10px;margin-top:4px;color:{'#10b981' if can_do else '#f43f5e'}">{'✓ Achievable' if can_do else '✗ Increase SIP'}</div>
            </div>""", unsafe_allow_html=True)

    if not has_emergency:
        st.markdown('<div class="sec-hdr">🚨 Emergency fund gap</div>', unsafe_allow_html=True)
        ef_target = expenses * emergency_months
        ef_sip_needed = ef_target / 12
        st.markdown(f"""
        <div style="background:#130c14;border:1px solid #f43f5e44;border-radius:14px;padding:20px;display:flex;gap:24px;align-items:center;">
          <div style="font-size:36px;">🚨</div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#f43f5e;">Emergency Fund Missing</div>
            <div style="font-size:12px;color:#9095b0;margin-top:4px;line-height:1.6;">
              You need <b style="color:#fb923c">{fmt(ef_target)}</b> ({emergency_months} months of expenses) as liquid backup before investing.<br>
              Set aside <b style="color:#fb923c">{fmt(ef_sip_needed)}/mo</b> for 12 months in a high-yield savings account or liquid MF.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# TAB 3 — Tax Calculator
# ──────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-hdr">Income tax comparison — FY 2025-26</div>', unsafe_allow_html=True)

    tx1, tx2 = st.columns(2)
    with tx1:
        annual_income = st.number_input("Annual gross income (₹)", min_value=0, step=50000, value=int(salary * 12), format="%d")
    with tx2:
        extra_deductions = st.number_input("Additional deductions — 80D, HRA, NPS etc. (₹)", min_value=0, step=5000, value=0, format="%d")

    tax_old = tax_old_regime(annual_income - extra_deductions)
    tax_new = tax_new_regime(annual_income)
    better  = "New Regime" if tax_new <= tax_old else "Old Regime"
    savings = abs(tax_old - tax_new)

    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Old Regime Tax", fmt(tax_old), f"₹{tax_old/12:,.0f}/mo")
    tc2.metric("New Regime Tax", fmt(tax_new), f"₹{tax_new/12:,.0f}/mo")
    tc3.metric("Better Option", better, "saves " + fmt(savings))
    tc4.metric("Effective tax rate", f"{tax_new/annual_income*100:.1f}%" if annual_income else "0%", "New regime")

    incomes = [300000, 500000, 700000, 1000000, 1200000, 1500000, 2000000, 3000000]
    old_taxes = [tax_old_regime(i) for i in incomes]
    new_taxes = [tax_new_regime(i) for i in incomes]
    income_labels = [f"₹{i//100000}L" for i in incomes]

    fig_tax = go.Figure()
    fig_tax.add_trace(go.Bar(x=income_labels, y=old_taxes, name="Old Regime",
        marker_color="#f43f5e", text=[f"₹{t/1000:.0f}K" for t in old_taxes], textposition="outside",
        textfont=dict(size=9, color="#9095b0")))
    fig_tax.add_trace(go.Bar(x=income_labels, y=new_taxes, name="New Regime (2024)",
        marker_color="#5b6af5", text=[f"₹{t/1000:.0f}K" for t in new_taxes], textposition="outside",
        textfont=dict(size=9, color="#9095b0")))

    closest_idx = min(range(len(incomes)), key=lambda i: abs(incomes[i] - annual_income))
    fig_tax.add_vline(x=closest_idx, line_color="#f59e0b", line_dash="dot", line_width=1.5)

    fig_tax.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(16,20,42,0.6)",
        barmode="group", bargap=0.2, bargroupgap=0.05,
        margin=dict(t=20, b=10, l=10, r=10), height=280,
        legend=dict(font=dict(family="DM Sans", color="#6b7194", size=11), bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.1),
        xaxis=dict(color="#6b7194", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
        yaxis=dict(color="#6b7194", gridcolor="#13172a", tickformat="₹,.0f", tickfont=dict(size=10)),
    )
    st.plotly_chart(fig_tax, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="sec-hdr">Tax-saving investment opportunities</div>', unsafe_allow_html=True)
    tax_opts = [
        ("80C: ELSS / PPF / NPS", 150000, "15–22% returns from ELSS. EEE in PPF.", "#5b6af5"),
        ("80CCD(1B): NPS Tier-1", 50000, "Extra NPS deduction over 80C limit.", "#a78bfa"),
        ("80D: Health Insurance", 50000, "Self + parents. Up to ₹50K deduction.", "#10b981"),
        ("HRA Exemption", "Varies", "Claim if paying rent in metro cities.", "#f59e0b"),
        ("80EE: Home Loan Interest", 50000, "First-time home buyers under section 80EE.", "#06b6d4"),
        ("SGB Interest", "2.5%", "Sovereign Gold Bond: interest tax-free at maturity.", "#fb923c"),
    ]
    t_cols = st.columns(3)
    for i, (name, limit, desc, color) in enumerate(tax_opts):
        with t_cols[i % 3]:
            st.markdown(f"""
            <div style="background:#10142a;border:1px solid #1e2235;border-left:3px solid {color};border-radius:10px;padding:14px;margin-bottom:10px;">
              <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#dde1f0;">{name}</div>
              <div style="font-size:18px;font-weight:800;color:{color};margin:5px 0;">{'₹'+f'{limit:,}' if isinstance(limit,int) else limit}</div>
              <div style="font-size:11px;color:#6b7194;line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# TAB 4 — SIP vs Lumpsum
# ──────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-hdr">SIP vs lumpsum comparison</div>', unsafe_allow_html=True)

    ls1, ls2 = st.columns(2)
    with ls1:
        lumpsum_amt  = st.number_input("Lumpsum amount (₹)", min_value=10000, step=10000, value=300000, format="%d")
        ls_rate      = st.slider("Expected return % p.a.", 6, 24, 13, key="ls_rate")
    with ls2:
        sip_amt      = st.number_input("Monthly SIP amount (₹)", min_value=500, step=500, value=invest, format="%d")
        ls_years     = st.slider("Comparison period (years)", 1, 30, proj_years, key="ls_yrs")
        step_up_ls   = st.slider("SIP step-up % p.a.", 0, 20, step_up, key="ls_stepup")

    ls_future  = lumpsum_future(lumpsum_amt, ls_rate, ls_years)
    sip_future_val = sip_future(sip_amt, ls_rate, ls_years)
    sip_stepup_val = step_up_sip(sip_amt, ls_rate, ls_years, step_up_ls)
    sip_invested   = sip_amt * 12 * ls_years

    lc1, lc2, lc3, lc4 = st.columns(4)
    lc1.metric("Lumpsum grows to", fmt(ls_future), f"Invested {fmt(lumpsum_amt)}")
    lc2.metric("SIP grows to", fmt(sip_future_val), f"Invested {fmt(sip_invested)}")
    lc3.metric("SIP with step-up", fmt(sip_stepup_val), f"+{fmt(sip_stepup_val - sip_future_val)} vs flat SIP")
    lc4.metric("Winner", "Lumpsum" if ls_future > sip_stepup_val else "Step-up SIP",
               fmt(max(ls_future, sip_stepup_val) - min(ls_future, sip_stepup_val)) + " ahead")

    yr_range2 = list(range(1, ls_years + 1))
    ls_vals   = [lumpsum_future(lumpsum_amt, ls_rate, y) for y in yr_range2]
    sip_vals  = [sip_future(sip_amt, ls_rate, y) for y in yr_range2]
    sip_su_v  = [step_up_sip(sip_amt, ls_rate, y, step_up_ls) for y in yr_range2]

    fig_ls = go.Figure()
    fig_ls.add_trace(go.Scatter(x=yr_range2, y=ls_vals, name=f"Lumpsum {fmt(lumpsum_amt)}",
        line=dict(color="#f43f5e", width=2.5)))
    fig_ls.add_trace(go.Scatter(x=yr_range2, y=sip_vals, name=f"SIP {fmt(sip_amt)}/mo",
        line=dict(color="#5b6af5", width=2.5)))
    fig_ls.add_trace(go.Scatter(x=yr_range2, y=sip_su_v, name=f"SIP + {step_up_ls}% step-up",
        line=dict(color="#10b981", width=2.5), fill="tonexty", fillcolor="rgba(16,185,129,0.05)"))

    fig_ls.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(16,20,42,0.7)",
        margin=dict(t=14, b=10, l=10, r=10), height=300,
        legend=dict(font=dict(family="DM Sans", color="#6b7194", size=11), bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.08),
        xaxis=dict(tickcolor="#252840", gridcolor="#13172a", color="#6b7194", tickfont=dict(size=10)),
        yaxis=dict(tickcolor="#252840", gridcolor="#13172a", color="#6b7194", tickformat="₹.2s", tickfont=dict(size=10)),
        hovermode="x unified",
    )
    st.plotly_chart(fig_ls, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="sec-hdr">Step-up SIP monthly contributions over time</div>', unsafe_allow_html=True)
    su_months = list(range(0, ls_years * 12 + 1, 12))
    su_amts   = [sip_amt * ((1 + step_up_ls / 100) ** y) for y in range(ls_years + 1)]

    fig_su = go.Figure(go.Bar(
        x=[f"Yr {y}" for y in range(ls_years + 1)], y=su_amts,
        marker=dict(color=su_amts, colorscale=[[0, "#1a2550"], [1, "#5b6af5"]], showscale=False),
        text=[fmt(a) for a in su_amts], textposition="outside",
        textfont=dict(family="Syne", size=9, color="#9095b0"),
    ))
    fig_su.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(16,20,42,0.6)",
        margin=dict(t=20, b=10, l=10, r=10), height=220,
        xaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
        yaxis=dict(color="#6b7194", tickcolor="#252840", gridcolor="#13172a", tickformat="₹,.0f", tickfont=dict(size=10)),
        showlegend=False,
    )
    st.plotly_chart(fig_su, use_container_width=True, config={"displayModeBar": False})

# ──────────────────────────────────────────────────────────
# TAB 5 — Top Picks
# ──────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="sec-hdr">Top investment picks — curated for Indian markets</div>', unsafe_allow_html=True)

    pf1, pf2, pf3 = st.columns([1.5, 1.5, 1])
    with pf1:
        filter_opt = st.radio("Asset class", ["All","Stocks","ETFs","Mutual Funds","FD / Debt","Gold"], horizontal=True, label_visibility="collapsed")
    with pf2:
        risk_filter = st.radio("Risk level", ["All","None","Low","Low-Med","Medium","High"], horizontal=True, label_visibility="collapsed", key="risk_filter")
    with pf3:
        search_q = st.text_input("Search picks", placeholder="e.g. Nifty, HDFC", label_visibility="collapsed")

    cat_map  = {"All":None,"Stocks":"shares","ETFs":"etf","Mutual Funds":"mf","FD / Debt":"fd","Gold":"gold"}
    cat_filter = cat_map[filter_opt]

    filtered_picks = PICKS
    if cat_filter:
        filtered_picks = [p for p in filtered_picks if p["cat"] == cat_filter]
    if risk_filter != "All":
        filtered_picks = [p for p in filtered_picks if p.get("risk") == risk_filter]
    if search_q:
        q = search_q.lower()
        filtered_picks = [p for p in filtered_picks if q in p["name"].lower() or q in p["ticker"].lower() or q in p.get("sector","").lower()]

    st.markdown(f"<div style='font-size:11px;color:#464c68;margin-bottom:12px;'>Showing {len(filtered_picks)} picks</div>", unsafe_allow_html=True)

    cat_count = {}
    for p in PICKS: cat_count[p["cat"]] = cat_count.get(p["cat"], 0) + 1
    alloc_by_key = {a["key"]: a for a in ALLOC}

    pick_cols = st.columns(3)
    for i, p in enumerate(filtered_picks):
        alloc_obj  = alloc_by_key.get(p["cat"])
        suggested  = fmt(round(alloc_obj["amt"] / cat_count.get(p["cat"], 1))) if alloc_obj else ""
        m          = CAT_META.get(p["cat"], CAT_META["shares"])
        risk_col   = RISK_COLOR.get(p.get("risk","Medium"), "#fb923c")
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
              <div class="pick-ticker">{p['ticker']} &nbsp;·&nbsp; <span style="color:#5b6af5;font-size:10px;">{p.get('sector','')}</span></div>
              <div class="pick-why">{p['why']}</div>
              <div class="pick-ret">↑ {p['ret']}</div>
              {f'<div class="pick-alloc">→ Suggested {suggested}/mo</div>' if suggested else ''}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TIPS + DISCLAIMER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="infobox">
  💡 <b>Pro tips from SMARTFUNDS ADVISOR:</b><br>
  • Start SIPs on the 1st of every month — consistent entry beats timing the market.<br>
  • Step up your SIP by 10% every year — this small habit creates massive long-term wealth (see SIP vs Lumpsum tab).<br>
  • Keep 3–6 months of expenses as liquid emergency fund <em>before</em> any investment.<br>
  • Use the Tax Calculator tab to decide between Old vs New regime and save up to ₹50K+ extra annually.<br>
  • Review and rebalance your portfolio every 6 months. Use the sliders above to adjust as life changes.<br>
  • For stocks, invest in 2–3 tranches per month. Never deploy all funds in a single day.
</div>
<div class="disclaimer">
  ⚠ SMARTFUNDS ADVISOR is an XAI-powered personal finance education tool and does not constitute SEBI-registered financial advice.
  Tax calculations are indicative only — consult a CA for exact liability. Past returns are not guaranteed.
  All investments are subject to market risk. Please read all scheme-related documents carefully and consult a qualified
  investment advisor before making any financial decisions. FY 2025-26 tax slabs used.
</div>
""", unsafe_allow_html=True)