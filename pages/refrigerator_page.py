import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from cycles.refrigerator import refrigeration_cycle
from CoolProp.CoolProp import PropsSI

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="Refrigeration Cycle", layout="wide")

# ================================================================
# BACK BUTTON — paste this near the TOP of every cycle page,
# directly after st.set_page_config() and any CSS st.markdown().
# ================================================================

st.markdown("""
<style>
.back-btn-wrap {
    margin-bottom: 4px;
    margin-top: 2px;
}
.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 15px 7px 11px;
    background: rgba(18, 24, 38, 0.70);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 10px;
    color: #94A3B8 !important;
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    font-weight: 500;
    letter-spacing: 0.01em;
    text-decoration: none !important;
    cursor: pointer;
    transition: color 0.22s ease, border-color 0.22s ease,
                background 0.22s ease, transform 0.22s ease,
                box-shadow 0.22s ease;
}
.back-btn:hover {
    color: #E2E8F0 !important;
    border-color: rgba(99, 162, 255, 0.40);
    background: rgba(30, 42, 64, 0.88);
    transform: translateX(-3px);
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.12);
    text-decoration: none !important;
}
.back-btn .back-arrow {
    font-size: 15px;
    line-height: 1;
    transition: transform 0.22s ease;
}
.back-btn:hover .back-arrow {
    transform: translateX(-2px);
}
</style>
<div class="back-btn-wrap">
    <a class="back-btn" href="/" target="_self">
        <span class="back-arrow">←</span>
        Back to Home
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
  /* Modern Title & Heading Elements */
  .main-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 4px;
  }
  .section-title {
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: #f1f5f9;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
  }

  /* Process Flowsheet Translucent Panel */
  .flow-card {
    background: rgba(30, 30, 50, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 3px solid #4a9edd;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 16px;
    margin-bottom: 8px;
  }
  .flow-title {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8e9aab;
    margin-bottom: 8px;
    font-weight: 700;
  }
  .flow-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 16px 24px;
  }
  .flow-step {
    font-size: 0.825rem;
    color: #cbd5e1;
    font-family: monospace;
  }
  .flow-step span {
    color: #4a9edd;
    font-weight: bold;
  }

  /* Core Form Input Fields Override */
  div[data-baseweb="input"] {
    border-color: rgba(255,255,255,0.2) !important;
    box-shadow: none !important;
  }
  div[data-baseweb="input"]:focus-within {
    border-color: #4a9edd !important;
    box-shadow: 0 0 0 1px #4a9edd !important;
  }
  div[data-baseweb="input"] * {
    border-color: inherit !important;
  }
  div[data-baseweb="input"] button {
    background-color: #4a9edd !important;
    color: #fff !important;
    border-color: #4a9edd !important;
  }
  div[data-baseweb="input"] button:hover {
    background-color: #2e7cbf !important;
  }
  div[data-baseweb="input"] button:active {
    background-color: #1d5f99 !important;
  }
  [data-testid="stNumberInput"] div[data-baseweb="input"] {
    border-color: rgba(255,255,255,0.2) !important;
    box-shadow: none !important;
  }
  [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
    border-color: #4a9edd !important;
    box-shadow: 0 0 0 1px #4a9edd !important;
  }
  div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #4a9edd !important;
    border-color: #4a9edd !important;
    color: #fff !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #2e7cbf !important;
    border-color: #2e7cbf !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:active {
    background-color: #1d5f99 !important;
    border-color: #1d5f99 !important;
  }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# PAGE TITLE
# ------------------------------------------------

st.markdown('<div class="main-title">Vapor Compression Refrigeration Cycle</div>', unsafe_allow_html=True)
st.markdown("Simulate a real-property refrigeration cycle using the CoolProp fluid database.")
st.markdown("---")

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------

st.markdown('<div class="section-title">⚙️ Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    T_evap_C = st.number_input("Evaporator Temperature (°C)", min_value=-40.0, max_value=20.0, value=-10.0, step=1.0, format="%.1f")
    T_cond_C = st.number_input("Condenser Temperature (°C)", min_value=25.0, max_value=65.0, value=40.0, step=1.0, format="%.1f")

with col2:
    eta_comp = st.number_input("Compressor Isentropic Efficiency η_comp (0–1)", min_value=0.50, max_value=1.00, value=0.85, step=0.01, format="%.2f")

T_evap_K = T_evap_C + 273.15
T_cond_K = T_cond_C + 273.15
refrigerant = 'R134a'

# ------------------------------------------------
# VALIDATION
# ------------------------------------------------

errors = []
if T_evap_K >= T_cond_K:
    errors.append("Evaporator temperature must be strictly lower than condenser temperature.")
if T_cond_K >= 374.2:
    errors.append("Condenser temperature exceeds the critical point of R134a.")

for err in errors:
    st.error(err)
if errors:
    st.stop()

st.info("Assumptions: Fluid is R134a · State 1 is sat. vapor (Q=1) · State 3 is sat. liquid (Q=0) · Expansion is isenthalpic (h₃ = h₄)")

# ------------------------------------------------
# PROCESS FLOWSHEET
# ------------------------------------------------

st.markdown("""
<div class="flow-card">
  <div class="flow-title">🔀 Cycle Process Flow Steps</div>
  <div class="flow-grid">
    <div class="flow-step"><span>1 → 2</span> Isentropic Compression</div>
    <div class="flow-step"><span>2 → 3</span> Condensation</div>
    <div class="flow-step"><span>3 → 4</span> Expansion Valve Throttling</div>
    <div class="flow-step"><span>4 → 1</span> Evaporation</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# RUN BUTTON
# ------------------------------------------------

run = st.button("Run Refrigeration Simulation", type="primary")
st.markdown("---")

if run:
    try:
        results = refrigeration_cycle(T_evap=T_evap_K, T_cond=T_cond_K, eta_comp=eta_comp)
    except Exception as e:
        st.error(f"Simulation failed: {e}")
        st.stop()

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    st.markdown('<div class="section-title">📊 Simulation Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("COP", f"{results['COP']:.2f}")
    m2.metric("Cooling Capacity", f"{results['Q_in']/1000:.2f} kJ/kg")
    m3.metric("Compressor Work", f"{results['W_comp']/1000:.2f} kJ/kg")

    P_evap_kPa = PropsSI('P', 'T', T_evap_K, 'Q', 1, refrigerant) / 1000.0
    P_cond_kPa = PropsSI('P', 'T', T_cond_K, 'Q', 0, refrigerant) / 1000.0
    m4.metric("Pressure Ratio", f"{(P_cond_kPa / P_evap_kPa):.2f}")

    # ------------------------------------------------
    # STATE POINTS TABLE
    # ------------------------------------------------

    st.markdown("---")
    st.markdown('<div class="section-title">📋 State Points</div>', unsafe_allow_html=True)

    T = results["T"]
    S = results["S"]
    H = results["H"]

    T1, T2, T3, T4 = [float(t) for t in T]
    S1, S2, S3, S4 = [float(s) for s in S]
    H1, H2, H3, H4 = [float(h) for h in H]

    df = pd.DataFrame({
        "State": [
            "1 — Evaporator Outlet",
            "2 — Compressor Outlet",
            "3 — Condenser Outlet",
            "4 — Throttling Valve Outlet"
        ],
        "Temperature (°C)": [f"{t - 273.15:.2f}" for t in [T1, T2, T3, T4]],
        "Pressure (kPa)": [f"{P_evap_kPa:.2f}", f"{P_cond_kPa:.2f}", f"{P_cond_kPa:.2f}", f"{P_evap_kPa:.2f}"],
        "Enthalpy (kJ/kg)": [f"{h/1000:.2f}" for h in [H1, H2, H3, H4]],
        "Entropy (kJ/kg·K)": [f"{s/1000:.4f}" for s in [S1, S2, S3, S4]]
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    # ------------------------------------------------
    # GRAPH DATA PRE-COMPUTATION
    # ------------------------------------------------

    T_crit = 374.2
    T_range = np.linspace(220.0, T_crit - 0.05, 200)
    dome_liq_S, dome_liq_T, dome_vap_S, dome_vap_T = [], [], [], []

    for temp in T_range:
        try:
            dome_liq_S.append(float(PropsSI('S', 'T', temp, 'Q', 0, refrigerant)))
            dome_liq_T.append(float(temp))
            dome_vap_S.append(float(PropsSI('S', 'T', temp, 'Q', 1, refrigerant)))
            dome_vap_T.append(float(temp))
        except:
            pass

    S_crit = float(PropsSI('S', 'T', T_crit - 0.01, 'Q', 0, refrigerant))
    dome_liq_S.append(S_crit); dome_liq_T.append(T_crit)
    dome_vap_S.append(S_crit); dome_vap_T.append(T_crit)

    dome_S = dome_liq_S + dome_vap_S[::-1]
    dome_T = dome_liq_T + dome_vap_T[::-1]

    # Process 2→3: Condenser curve
    seg23_S, seg23_T = [], []
    H_sat_liq = float(PropsSI('H', 'T', T_cond_K, 'Q', 0, refrigerant))
    for h_node in np.linspace(H2, H_sat_liq, 150):
        try:
            seg23_S.append(float(PropsSI('S', 'P', P_cond_kPa * 1000.0, 'H', h_node, refrigerant)))
            seg23_T.append(float(PropsSI('T', 'P', P_cond_kPa * 1000.0, 'H', h_node, refrigerant)))
        except:
            pass

    # Process 4→1: Evaporator curve
    seg41_S, seg41_T = [], []
    for h_node in np.linspace(H4, H1, 100):
        try:
            seg41_S.append(float(PropsSI('S', 'P', P_evap_kPa * 1000.0, 'H', h_node, refrigerant)))
            seg41_T.append(float(PropsSI('T', 'P', P_evap_kPa * 1000.0, 'H', h_node, refrigerant)))
        except:
            pass

    chart_data = json.dumps({
        "dome": list(zip(dome_S, dome_T)),
        "seg12": [[S1, T1], [S2, T2]],
        "seg23": list(zip(seg23_S, seg23_T)),
        "seg34": [[S3, T3], [S4, T4]],
        "seg41": list(zip(seg41_S, seg41_T)),
        "pts": [[S1, T1], [S2, T2], [S3, T3], [S4, T4]]
    })

    # ------------------------------------------------
    # INTERACTIVE CHARTS
    # ------------------------------------------------

    st.markdown("---")
    st.markdown('<div class="section-title">📈 Cycle Diagrams</div>', unsafe_allow_html=True)

    html_code = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; font-family: 'Segoe UI', sans-serif; }
.chart-card {
  background: #1a1a2e;
  border: 1px solid #2a2a4a;
  border-radius: 12px;
  padding: 16px;
  display: inline-block;
  width: 55%;
  min-width: 420px;
}
.chart-title {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 12px;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  font-family: monospace;
}
.legend { display: flex; flex-wrap: wrap; gap: 8px 20px; margin-top: 10px; }
.legend-row { display: flex; align-items: center; gap: 8px; font-size: 11px; color: #aaa; }
.legend-line { width: 20px; height: 3px; border-radius: 2px; }
</style>

<div class="chart-card" id="db" data-layout='""" + chart_data + """'>
  <div class="chart-title">📊 T-S Diagram (R134a)</div>
  <canvas id="ts-canvas" width="660" height="280"></canvas>
  <div class="legend">
    <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>1→2 Compression</div>
    <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>2→3 Condensation</div>
    <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>3→4 Expansion</div>
    <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>4→1 Evaporation</div>
    <div class="legend-row"><div class="legend-line" style="background:#666; height:1.5px"></div>Dome</div>
  </div>
</div>

<script>
const data = JSON.parse(document.getElementById('db').getAttribute('data-layout'));
const canvas = document.getElementById('ts-canvas');
const ctx = canvas.getContext('2d');
const dpr = window.devicePixelRatio || 1;
const W = 660, H = 280;

canvas.width = W * dpr; canvas.height = H * dpr;
canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
ctx.scale(dpr, dpr);

const pad = { l: 62, r: 20, t: 20, b: 32 };
const allS = [...data.dome, ...data.seg12, ...data.seg23, ...data.seg34, ...data.seg41].map(p=>p[0]).filter(isFinite);
const allT = [...data.dome, ...data.seg12, ...data.seg23, ...data.seg34, ...data.seg41].map(p=>p[1]).filter(isFinite);

const Smin = Math.min(...allS) - 50, Smax = Math.max(...allS) + 50;
const Tmin = Math.min(...allT) - 15, Tmax = Math.max(...allT) + 20;

const toX = s => pad.l + (s - Smin) / (Smax - Smin) * (W - pad.l - pad.r);
const toY = t => H - pad.b - (t - Tmin) / (Tmax - Tmin) * (H - pad.t - pad.b);

// Grid
ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 0.5;
for(let i=1; i<5; i++){
  let x = Smin + i * (Smax - Smin) / 5;
  let y = Tmin + i * (Tmax - Tmin) / 5;
  ctx.beginPath(); ctx.moveTo(toX(x), pad.t); ctx.lineTo(toX(x), H - pad.b); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(pad.l, toY(y)); ctx.lineTo(W - pad.r, toY(y)); ctx.stroke();
}

// Axes
ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=1;
ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, H - pad.b); ctx.lineTo(W - pad.r, H - pad.b); ctx.stroke();

// Tick labels
ctx.fillStyle='#999'; ctx.font='10px sans-serif';
for(let i=0; i<=5; i++){
  let x = Smin + i * (Smax - Smin) / 5;
  let y = Tmin + i * (Tmax - Tmin) / 5;
  ctx.textAlign='center'; ctx.fillText((x/1000).toFixed(2), toX(x), H - pad.b + 14);
  ctx.textAlign='right';  ctx.fillText(Math.round(y), pad.l - 5, toY(y) + 4);
}

ctx.fillStyle='#bbb'; ctx.font='11px sans-serif';
ctx.textAlign='center'; ctx.fillText('Entropy (kJ/kg·K)', pad.l + (W - pad.l - pad.r) / 2, H - 2);
ctx.save(); ctx.translate(11, pad.t + (H - pad.t - pad.b) / 2); ctx.rotate(-Math.PI / 2);
ctx.fillText('Temperature (K)', 0, 0); ctx.restore();

function drawLine(pts, color, lw=2.5){
  if(!pts || pts.length < 2) return;
  ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=lw;
  pts.forEach((p, i) => i === 0 ? ctx.moveTo(toX(p[0]), toY(p[1])) : ctx.lineTo(toX(p[0]), toY(p[1])));
  ctx.stroke();
}

drawLine(data.dome, '#666', 1.5);
drawLine(data.seg12, '#4a9edd');
drawLine(data.seg23, '#e05c3a');
drawLine(data.seg34, '#4aad6e');
drawLine(data.seg41, '#c8941a');

const offsets = [{x: -12, y: -4}, {x: 12, y: -4}, {x: -12, y: -4}, {x: -12, y: 14}];
['1', '2', '3', '4'].forEach((lbl, i) => {
  const [s, t] = data.pts[i];
  const cx = toX(s), cy = toY(t);
  ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI * 2);
  ctx.fillStyle = '#1a1a2e'; ctx.fill();
  ctx.strokeStyle = '#e0e0e0'; ctx.lineWidth = 1.5; ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.font = 'bold 11px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(lbl, cx + offsets[i].x, cy + offsets[i].y);
});
</script>
"""
    components.html(html_code, height=420)