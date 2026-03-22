import { useState, useEffect, useRef } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Legend, AreaChart, Area } from "recharts";

const COLORS = {
  stocks: "#6C63FF",
  mutualFunds: "#00D4AA",
  etfs: "#F5A623",
  fdDebt: "#00B4D8",
  ppfNps: "#A855F7",
  goldSgb: "#F97316",
};

const COLOR_LIST = Object.values(COLORS);

const LABELS = ["Stocks", "Mutual Funds", "ETFs", "FD / Debt", "PPF / NPS", "Gold / SGB"];
const SUBTITLES = ["Direct equity", "Equity SIP", "Index passive", "Stable return", "Tax-free", "Hedge"];
const COLOR_KEYS = Object.keys(COLORS);

const RISK_PROFILES = {
  Conservative: [20, 25, 15, 25, 10, 5],
  Balanced: [37, 23, 16, 12, 8, 4],
  Aggressive: [55, 20, 15, 5, 3, 2],
};

function generateProjection(totalMonthly, years = 15) {
  const data = [];
  const rate = 0.12 / 12;
  for (let y = 0; y <= years; y++) {
    const months = y * 12;
    const conservative = totalMonthly * ((Math.pow(1.08 / 12 + 1, months) - 1) / (0.08 / 12));
    const moderate = totalMonthly * ((Math.pow(rate + 1, months) - 1) / rate);
    const aggressive = totalMonthly * ((Math.pow(1.15 / 12 + 1, months) - 1) / (0.15 / 12));
    data.push({
      year: `Y${y}`,
      Conservative: Math.round(conservative / 100000) / 10,
      Moderate: Math.round(moderate / 100000) / 10,
      Aggressive: Math.round(aggressive / 100000) / 10,
    });
  }
  return data;
}

function formatINR(val) {
  if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)}Cr`;
  if (val >= 100000) return `₹${(val / 100000).toFixed(2)}L`;
  if (val >= 1000) return `₹${(val / 1000).toFixed(1)}K`;
  return `₹${val}`;
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 10, padding: "10px 16px" }}>
        <p style={{ color: "#94a3b8", marginBottom: 6, fontSize: 12 }}>{label}</p>
        {payload.map((p) => (
          <p key={p.name} style={{ color: p.color, margin: "2px 0", fontSize: 13 }}>
            {p.name}: <b>₹{p.value}L</b>
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function FundsAdvisor() {
  const [riskProfile, setRiskProfile] = useState("Balanced");
  const [monthly, setMonthly] = useState(30000);
  const [splits, setSplits] = useState(RISK_PROFILES["Balanced"]);
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    setAnimated(false);
    const t = setTimeout(() => setAnimated(true), 100);
    return () => clearTimeout(t);
  }, [splits]);

  useEffect(() => {
    setSplits(RISK_PROFILES[riskProfile]);
  }, [riskProfile]);

  const allocations = splits.map((pct, i) => ({
    name: LABELS[i],
    subtitle: SUBTITLES[i],
    pct,
    amount: Math.round((monthly * pct) / 100),
    color: COLOR_LIST[i],
    key: COLOR_KEYS[i],
  }));

  const pieData = allocations.map((a) => ({ name: a.name, value: a.pct, color: a.color }));
  const projData = generateProjection(monthly);

  const updateSplit = (idx, val) => {
    const newSplits = [...splits];
    const oldVal = newSplits[idx];
    const delta = val - oldVal;
    newSplits[idx] = val;
    // distribute delta from last item
    const otherIdxs = newSplits.map((_, i) => i).filter((i) => i !== idx);
    const lastOther = otherIdxs[otherIdxs.length - 1];
    newSplits[lastOther] = Math.max(1, newSplits[lastOther] - delta);
    const total = newSplits.reduce((a, b) => a + b, 0);
    if (total !== 100) newSplits[lastOther] += 100 - total;
    setSplits(newSplits.map((v) => Math.max(1, v)));
  };

  return (
    <div style={{ minHeight: "100vh", background: "#060d1a", color: "#e2e8f0", fontFamily: "'DM Sans', sans-serif", display: "flex" }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet" />

      {/* Sidebar */}
      <aside style={{ width: 280, background: "#0a1628", borderRight: "1px solid #1a2740", padding: "28px 20px", display: "flex", flexDirection: "column", gap: 28, flexShrink: 0 }}>
        <div>
          <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a6080", textTransform: "uppercase", marginBottom: 8 }}>Ritesh Funds</div>
          <div style={{ fontSize: 22, fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, color: "#e2e8f0" }}>Advisor</div>
        </div>

        {/* Risk Profile */}
        <div>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: "#4a6080", textTransform: "uppercase", marginBottom: 12 }}>⊙ Allocation Controls</div>
          <div style={{ fontSize: 12, color: "#64748b", marginBottom: 8 }}>Risk Profile</div>
          <select
            value={riskProfile}
            onChange={(e) => setRiskProfile(e.target.value)}
            style={{ width: "100%", background: "#0f1f35", border: "1px solid #1e3a5f", color: "#e2e8f0", borderRadius: 8, padding: "10px 14px", fontSize: 14, cursor: "pointer", outline: "none" }}
          >
            {Object.keys(RISK_PROFILES).map((r) => <option key={r}>{r}</option>)}
          </select>
        </div>

        {/* Monthly input */}
        <div>
          <div style={{ fontSize: 12, color: "#64748b", marginBottom: 8 }}>Monthly Investment (₹)</div>
          <input
            type="number"
            value={monthly}
            onChange={(e) => setMonthly(Number(e.target.value))}
            style={{ width: "100%", background: "#0f1f35", border: "1px solid #1e3a5f", color: "#e2e8f0", borderRadius: 8, padding: "10px 14px", fontSize: 14, outline: "none", boxSizing: "border-box" }}
          />
        </div>

        {/* Sliders */}
        <div>
          <div style={{ fontSize: 11, letterSpacing: 1.5, color: "#4a6080", textTransform: "uppercase", marginBottom: 14 }}>📊 Adjust Split (%)</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {allocations.map((a, i) => (
              <div key={a.key}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                  <span style={{ fontSize: 12, color: "#94a3b8" }}>{a.name}</span>
                  <span style={{ fontSize: 13, fontWeight: 600, color: a.color }}>{a.pct}</span>
                </div>
                <input
                  type="range" min={1} max={80} value={a.pct}
                  onChange={(e) => updateSplit(i, Number(e.target.value))}
                  style={{ width: "100%", accentColor: a.color, cursor: "pointer" }}
                />
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, padding: "32px 36px", overflowY: "auto" }}>
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }}>
          <div>
            <div style={{ fontSize: 11, letterSpacing: 2, color: "#4a6080", textTransform: "uppercase" }}>Portfolio Overview</div>
            <div style={{ fontSize: 28, fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, marginTop: 4 }}>Investment Breakdown</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 12, color: "#64748b" }}>Total Monthly SIP</div>
            <div style={{ fontSize: 32, fontWeight: 700, color: "#6C63FF", fontFamily: "'Space Grotesk', sans-serif" }}>₹{(monthly / 1000).toFixed(1)}K</div>
          </div>
        </div>

        {/* Top Row: Allocation bars + Pie */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 380px", gap: 24, marginBottom: 24 }}>
          {/* Allocation bars */}
          <div style={{ background: "#0a1628", borderRadius: 16, border: "1px solid #1a2740", padding: 28 }}>
            <div style={{ fontSize: 12, letterSpacing: 1.5, color: "#4a6080", textTransform: "uppercase", marginBottom: 20 }}>Allocation Breakdown</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
              {allocations.map((a) => (
                <div key={a.key}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
                    <div>
                      <span style={{ fontSize: 14, fontWeight: 500 }}>{a.name}</span>
                      <span style={{ fontSize: 11, color: "#4a6080", marginLeft: 8 }}>{a.subtitle}</span>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ fontSize: 12, color: "#64748b" }}>{a.pct}%</span>
                      <span style={{ fontSize: 14, fontWeight: 600, color: a.color }}>₹{(a.amount / 1000).toFixed(1)}K<span style={{ fontSize: 10, color: "#4a6080" }}>/mo</span></span>
                    </div>
                  </div>
                  <div style={{ height: 8, background: "#0f1f35", borderRadius: 8, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: animated ? `${a.pct}%` : "0%", background: `linear-gradient(90deg, ${a.color}cc, ${a.color})`, borderRadius: 8, transition: "width 0.7s cubic-bezier(0.4,0,0.2,1)" }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pie Chart */}
          <div style={{ background: "#0a1628", borderRadius: 16, border: "1px solid #1a2740", padding: 28, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ fontSize: 12, letterSpacing: 1.5, color: "#4a6080", textTransform: "uppercase", marginBottom: 8, alignSelf: "flex-start" }}>Portfolio Mix</div>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%" cy="50%"
                  innerRadius={65} outerRadius={95}
                  paddingAngle={3} dataKey="value"
                  animationBegin={0} animationDuration={900}
                >
                  {pieData.map((entry, i) => (
                    <Cell key={i} fill={entry.color} stroke="transparent" />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val, name) => [`${val}%`, name]}
                  contentStyle={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 8, fontSize: 12 }}
                />
              </PieChart>
            </ResponsiveContainer>
            {/* Center label overlay */}
            <div style={{ marginTop: -16, textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 700, fontFamily: "'Space Grotesk', sans-serif", color: "#e2e8f0" }}>₹{(monthly / 1000).toFixed(1)}K</div>
              <div style={{ fontSize: 11, color: "#4a6080" }}>per month</div>
            </div>
            {/* Legend */}
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 14px", marginTop: 14, justifyContent: "center" }}>
              {allocations.map((a) => (
                <div key={a.key} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11, color: "#94a3b8" }}>
                  <div style={{ width: 8, height: 8, borderRadius: 2, background: a.color, flexShrink: 0 }} />
                  {a.name}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Growth Projection */}
        <div style={{ background: "#0a1628", borderRadius: 16, border: "1px solid #1a2740", padding: 28 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
            <div>
              <div style={{ fontSize: 12, letterSpacing: 1.5, color: "#4a6080", textTransform: "uppercase" }}>Growth Projection</div>
              <div style={{ fontSize: 18, fontWeight: 600, marginTop: 2 }}>15-Year Horizon</div>
            </div>
            <div style={{ display: "flex", gap: 16 }}>
              {[["Conservative", "#00B4D8"], ["Moderate", "#00D4AA"], ["Aggressive", "#6C63FF"]].map(([label, color]) => (
                <div key={label} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "#94a3b8" }}>
                  <div style={{ width: 20, height: 3, borderRadius: 2, background: color }} />
                  {label}
                </div>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <AreaChart data={projData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                {[["Conservative", "#00B4D8"], ["Moderate", "#00D4AA"], ["Aggressive", "#6C63FF"]].map(([name, color]) => (
                  <linearGradient key={name} id={`grad${name}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={color} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={color} stopOpacity={0.02} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1a2740" />
              <XAxis dataKey="year" tick={{ fill: "#4a6080", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#4a6080", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `₹${v}L`} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="Conservative" stroke="#00B4D8" strokeWidth={2} fill="url(#gradConservative)" dot={false} />
              <Area type="monotone" dataKey="Moderate" stroke="#00D4AA" strokeWidth={2} fill="url(#gradModerate)" dot={false} />
              <Area type="monotone" dataKey="Aggressive" stroke="#6C63FF" strokeWidth={2} fill="url(#gradAggressive)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>

          {/* Projection cards */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginTop: 20 }}>
            {[
              { label: "Conservative (8%)", color: "#00B4D8", key: "Conservative" },
              { label: "Moderate (12%)", color: "#00D4AA", key: "Moderate" },
              { label: "Aggressive (15%)", color: "#6C63FF", key: "Aggressive" },
            ].map(({ label, color, key }) => {
              const final = projData[projData.length - 1][key];
              return (
                <div key={key} style={{ background: "#0f1f35", borderRadius: 12, padding: "16px 20px", borderLeft: `3px solid ${color}` }}>
                  <div style={{ fontSize: 11, color: "#4a6080", marginBottom: 6 }}>{label}</div>
                  <div style={{ fontSize: 22, fontWeight: 700, color, fontFamily: "'Space Grotesk', sans-serif" }}>₹{final}L</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>at 15 years</div>
                </div>
              );
            })}
          </div>
        </div>
      </main>
    </div>
  );
}
