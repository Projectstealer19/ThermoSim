import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from cycles.rankine import rankine_cycle
from CoolProp.CoolProp import PropsSI

st.set_page_config(page_title="Rankine Cycle", layout="wide")

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

st.markdown('<div class="main-title">Rankine Cycle Simulation</div>', unsafe_allow_html=True)
st.markdown("Simulate a non-ideal Rankine cycle using real steam properties.")
st.markdown("---")

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------

st.markdown('<div class="section-title">⚙️ Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    P_boiler = st.number_input("Boiler Pressure P_boiler (MPa)", min_value=0.1, max_value=20.0, value=3.0, step=0.1, format="%.1f")
    P_cond   = st.number_input("Condenser Pressure P_cond (MPa)", min_value=0.001, max_value=0.2, value=0.01, step=0.001, format="%.3f")
    T3       = st.number_input("Turbine Inlet Temperature T3 (K)", min_value=400, max_value=900, value=600, step=1)

with col2:
    eta_turbine = st.number_input("Turbine Isentropic Efficiency η_turbine (0–1)", min_value=0.50, max_value=1.00, value=0.85, step=0.01, format="%.2f")
    eta_pump    = st.number_input("Pump Isentropic Efficiency η_pump (0–1)", min_value=0.50, max_value=1.00, value=0.80, step=0.01, format="%.2f")

P_boiler_pa = P_boiler * 1e6
P_cond_pa   = P_cond   * 1e6

# ------------------------------------------------
# VALIDATION
# ------------------------------------------------

errors = []
if P_cond_pa >= P_boiler_pa:
    errors.append("Condenser pressure must be less than boiler pressure.")
if P_boiler_pa > 22000000:
    errors.append("Boiler pressure exceeds water critical point (22 MPa).")
if P_cond_pa < 611:
    errors.append("Condenser pressure below triple point of water (611 Pa).")
if T3 <= 273.16:
    errors.append("Turbine inlet temperature must be above 273.16 K.")
if T3 > 1073:
    errors.append("Turbine inlet temperature exceeds CoolProp safe limit (~1073 K).")
try:
    T_sat_check = PropsSI('T', 'P', P_boiler_pa, 'Q', 1, 'Water')
    if T3 < T_sat_check:
        errors.append(f"T3 ({T3} K) is below saturation temperature at boiler pressure ({T_sat_check:.1f} K).")
except Exception:
    pass

for err in errors:
    st.error(err)
if errors:
    st.stop()

st.info("Assumptions: Working fluid is pure water (steam) · Real fluid properties via CoolProp · Isenthalpic pump and turbine losses applied")

# ------------------------------------------------
# PROCESS FLOWSHEET
# ------------------------------------------------

st.markdown("""
<div class="flow-card">
  <div class="flow-title">🔀 Cycle Process Flow Steps</div>
  <div class="flow-grid">
    <div class="flow-step"><span>1 → 2</span> Pump Compression</div>
    <div class="flow-step"><span>2 → 3</span> Boiler Heat Addition</div>
    <div class="flow-step"><span>3 → 4</span> Turbine Expansion</div>
    <div class="flow-step"><span>4 → 1</span> Condenser Heat Rejection</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# RUN BUTTON
# ------------------------------------------------

run = st.button("Run Rankine Simulation", type="primary")
st.markdown("---")

if run:

    try:
        results = rankine_cycle(P_boiler=P_boiler_pa, P_cond=P_cond_pa, T3=T3, eta_turbine=eta_turbine, eta_pump=eta_pump)
    except ValueError as e:
        st.error(f"CoolProp property lookup failed: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Simulation failed: {e}")
        st.stop()

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    st.markdown('<div class="section-title">📊 Simulation Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Efficiency",  f"{results['efficiency']:.1f}%")
    m2.metric("W Turbine",   f"{results['W_turbine']/1000:.2f} kJ/kg")
    m3.metric("W Pump",      f"{results['W_pump']/1000:.2f} kJ/kg")
    m4.metric("Heat Input",  f"{results['Q_in']/1000:.2f} kJ/kg")

    # ------------------------------------------------
    # STATE POINTS TABLE
    # ------------------------------------------------

    st.markdown("---")
    st.markdown('<div class="section-title">📋 State Points</div>', unsafe_allow_html=True)

    import pandas as pd
    T = results["T"]; S = results["S"]; H = results["H"]
    df = pd.DataFrame({
        "State":      ["1 — Condenser outlet (sat. liquid)", "2 — Pump outlet", "3 — Boiler outlet / Turbine inlet", "4 — Turbine outlet"],
        "T (K)":      [f"{t:.2f}" for t in T],
        "S (J/kg-K)": [f"{s:.2f}" for s in S],
        "H (kJ/kg)":  [f"{h/1000:.2f}" for h in H],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    # ------------------------------------------------
    # COMPUTE ALL CURVE DATA IN PYTHON
    # ------------------------------------------------
    T1, T2, T3r, T4 = T
    S1, S2, S3, S4  = S
    H1, H2, H3, H4  = H

    # Saturation dome
    T_range = np.linspace(273.16, 647.08, 300)
    dome_liq_S, dome_liq_T, dome_vap_S, dome_vap_T = [], [], [], []
    for temp in T_range:
        try:
            dome_liq_S.append(float(PropsSI('S', 'T', temp, 'Q', 0, 'Water')))
            dome_liq_T.append(float(temp))
            dome_vap_S.append(float(PropsSI('S', 'T', temp, 'Q', 1, 'Water')))
            dome_vap_T.append(float(temp))
        except Exception:
            pass

    T_crit = 647.09
    S_crit = float(PropsSI('S', 'T', T_crit, 'Q', 0, 'Water'))
    dome_liq_S.append(S_crit); dome_liq_T.append(T_crit)
    dome_vap_S.append(S_crit); dome_vap_T.append(T_crit)
    dome_S = dome_liq_S + dome_vap_S[::-1]
    dome_T = dome_liq_T + dome_vap_T[::-1]

    # Process 2→3: Boiler
    seg23_S, seg23_T = [], []
    h_sat_vap = float(PropsSI('H', 'P', P_boiler_pa, 'Q', 1, 'Water'))
    T_sat_b   = float(PropsSI('T', 'P', P_boiler_pa, 'Q', 1, 'Water'))
    for h in np.linspace(H2, h_sat_vap, 150):
        try:
            seg23_S.append(float(PropsSI('S', 'P', P_boiler_pa, 'H', h, 'Water')))
            seg23_T.append(float(PropsSI('T', 'P', P_boiler_pa, 'H', h, 'Water')))
        except Exception:
            pass
    for temp in np.linspace(T_sat_b, T3r, 100)[1:]:
        try:
            seg23_S.append(float(PropsSI('S', 'P', P_boiler_pa, 'T', temp, 'Water')))
            seg23_T.append(float(temp))
        except Exception:
            pass

    chart_data = json.dumps({
        "dome":  list(zip(dome_S, dome_T)),
        "seg12": [[S1, T1], [S2, T2]],
        "seg23": list(zip(seg23_S, seg23_T)),
        "seg34": [[S3, T3r], [S4, T4]],
        "seg41": [[S4, T1], [S1, T1]],
        "pts":   [[S1,T1],[S2,T2],[S3,T3r],[S4,T4]],
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
.legend-line { width: 20px; height: 3px; border-radius: 2px; flex-shrink: 0; }
</style>

<div class="chart-card">
  <div class="chart-title">📊 T-S Diagram</div>
  <canvas id="ts-canvas" width="660" height="280"></canvas>
  <div class="legend">
    <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>1→2 Pump</div>
    <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>2→3 Boiler</div>
    <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>3→4 Turbine</div>
    <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>4→1 Condenser</div>
    <div class="legend-row"><div class="legend-line" style="background:#666; height:1.5px"></div>Saturation dome</div>
  </div>
</div>

<script>
const data = """ + chart_data + """;

const canvas = document.getElementById('ts-canvas');
const ctx    = canvas.getContext('2d');
const dpr = window.devicePixelRatio || 1;
const W = 660, H = 280;
canvas.width  = W * dpr;
canvas.height = H * dpr;
canvas.style.width  = W + 'px';
canvas.style.height = H + 'px';
ctx.scale(dpr, dpr);
const pad = { l: 62, r: 20, t: 20, b: 32 };

const allS = [...data.dome,...data.seg12,...data.seg23,...data.seg34,...data.seg41].map(p=>p[0]).filter(isFinite);
const allT = [...data.dome,...data.seg12,...data.seg23,...data.seg34,...data.seg41].map(p=>p[1]).filter(isFinite);
const Smin = Math.min(...allS) - 100, Smax = Math.max(...allS) + 100;
const Tmin = Math.min(...allT) * 0.92, Tmax = Math.max(...allT) * 1.06;

const toX = s => pad.l + (s - Smin) / (Smax - Smin) * (W - pad.l - pad.r);
const toY = t => H - pad.b - (t - Tmin) / (Tmax - Tmin) * (H - pad.t - pad.b);

// Grid
ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 0.5;
for(let i=0;i<=5;i++){
  const x = Smin+i*(Smax-Smin)/5, y = Tmin+i*(Tmax-Tmin)/5;
  ctx.beginPath(); ctx.moveTo(toX(x),pad.t); ctx.lineTo(toX(x),H-pad.b); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(pad.l,toY(y)); ctx.lineTo(W-pad.r,toY(y)); ctx.stroke();
}

// Axes
ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=1;
ctx.beginPath(); ctx.moveTo(pad.l,pad.t); ctx.lineTo(pad.l,H-pad.b); ctx.lineTo(W-pad.r,H-pad.b); ctx.stroke();
ctx.fillStyle='#999'; ctx.font='10px sans-serif';
for(let i=0;i<=5;i++){
  const x=Smin+i*(Smax-Smin)/5, y=Tmin+i*(Tmax-Tmin)/5;
  ctx.textAlign='center'; ctx.fillText((x/1000).toFixed(1)+'k', toX(x), H-pad.b+14);
  ctx.textAlign='right';  ctx.fillText(Math.round(y), pad.l-5, toY(y)+4);
}
ctx.fillStyle='#bbb'; ctx.font='11px sans-serif';
ctx.textAlign='center'; ctx.fillText('Entropy (J/kg·K)', pad.l+(W-pad.l-pad.r)/2, H-2);
ctx.save(); ctx.translate(11,pad.t+(H-pad.t-pad.b)/2); ctx.rotate(-Math.PI/2);
ctx.fillText('Temperature (K)',0,0); ctx.restore();

// Draw curves
function curve(pts, color, lw=2.5){
  if(!pts||pts.length<2) return;
  ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=lw;
  pts.forEach((p,i)=>i===0?ctx.moveTo(toX(p[0]),toY(p[1])):ctx.lineTo(toX(p[0]),toY(p[1])));
  ctx.stroke();
}
curve(data.dome,'#666',1.5);
curve(data.seg12,'#4a9edd');
curve(data.seg23,'#e05c3a');
curve(data.seg34,'#4aad6e');
curve(data.seg41,'#c8941a');

// State point dots
const labelOffset = [{x:0,y:14},{x:0,y:-10},{x:0,y:-10},{x:0,y:-10}];
['1','2','3','4'].forEach((lbl,i)=>{
  const [s,t] = data.pts[i];
  const cx=toX(s), cy=toY(t);
  ctx.beginPath(); ctx.arc(cx,cy,5,0,Math.PI*2);
  ctx.fillStyle='#1a1a2e'; ctx.fill();
  ctx.strokeStyle='#e0e0e0'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.fillStyle='#fff'; ctx.font='bold 11px sans-serif';
  ctx.textAlign='center';
  ctx.fillText(lbl, cx+labelOffset[i].x, cy+labelOffset[i].y);
});
</script>
"""

    components.html(html_code, height=420)