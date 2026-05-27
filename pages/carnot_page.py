import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from cycles.carnot import carnot_cycle

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Carnot Cycle",
    layout="wide"
)
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
# ------------------------------------------------
# CUSTOM STYLES (UI Polish & Custom Components)
# ------------------------------------------------
st.markdown("""
<style>
  /* Premium Heading Typography */
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
  
  /* Polished Info/Assumption Box */
  .engineering-info {
    background-color: rgba(30, 41, 59, 0.4);
    border-left: 3px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 6px;
    font-size: 0.875rem;
    color: #94a3b8;
    margin: 14px 0;
  }
  
  /* Process Flow Panel Style */
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

  /* Core Input Styling */
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
st.markdown('<div class="main-title">Carnot Cycle Simulation</div>', unsafe_allow_html=True)
st.markdown("Simulate an ideal reversible Carnot thermodynamic cycle.")
st.markdown("---")

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------
st.markdown('<div class="section-title">⚙️ Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    Th = st.number_input("Hot Reservoir Temperature Th (K)",
                          min_value=400, max_value=900, value=600, step=1)
    Tc = st.number_input("Cold Reservoir Temperature Tc (K)",
                          min_value=200, max_value=500, value=300, step=1)

with col2:
    Qh = st.number_input("Heat Supplied Qh (J)",
                          min_value=500, max_value=5000, value=2000, step=1)
    V1 = st.number_input("Initial Volume V1 (L)",
                          min_value=5, max_value=50, value=10, step=1)

V1_m3 = V1 / 1000.0   # convert L → m³

# Soft Translucent Info Panel
st.markdown('<div class="engineering-info">ℹ️ <b>Assumption:</b> Reference entropy $S_1 = 100$ J/K. Reversible cyclic processes evaluated using ideal gas assumptions.</div>', unsafe_allow_html=True)

# ------------------------------------------------
# VALIDATION WARNING
# ------------------------------------------------
if Tc >= Th:
    st.error("Tc must be less than Th for a valid Carnot cycle.")
    st.stop()

# ------------------------------------------------
# RUN BUTTON & PROCESS FLOW PANEL
# ------------------------------------------------
run = st.button("Run Carnot Simulation", type="primary")

st.markdown("""
<div class="flow-card">
  <div class="flow-title">🔀 Cycle Process Flow Steps</div>
  <div class="flow-grid">
    <div class="flow-step"><span>1 → 2</span> Isothermal Expansion (at Th)</div>
    <div class="flow-step"><span>2 → 3</span> Isentropic Expansion</div>
    <div class="flow-step"><span>3 → 4</span> Isothermal Compression (at Tc)</div>
    <div class="flow-step"><span>4 → 1</span> Isentropic Compression</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

if run:
    results = carnot_cycle(Th, Tc, Qh, V1=V1_m3)

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------
    st.markdown('<div class="section-title">📊 Simulation Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Efficiency",      f"{results['efficiency']:.1f}%")
    m2.metric("Work Done",       f"{results['work_done']/1000:.2f} kJ")
    m3.metric("Heat Rejected",   f"{results['heat_rejected']/1000:.2f} kJ")
    m4.metric("Entropy Change",  f"{results['delta_s']:.2f} J/K")

    # ------------------------------------------------
    # STATE POINTS TABLE
    # ------------------------------------------------
    st.markdown("---")
    st.markdown('<div class="section-title">📋 State Points</div>', unsafe_allow_html=True)

    V = results["V"]
    P = results["P"]
    T = results["T"]
    S = results["S"]

    df = pd.DataFrame({
        "State":     ["1 — Start", "2 — After isoth. exp.", "3 — After adiab. exp.", "4 — After isoth. comp."],
        "T (K)":     [f"{t:.0f}" for t in T],
        "P (kPa)":   [f"{p/1000:.2f}" for p in P],
        "V (L)":     [f"{v*1000:.3f}" for v in V],
        "S (J/K)":   [f"{s:.2f}" for s in S],
    })

    st.dataframe(df, hide_index=True, use_container_width=True)

    # ------------------------------------------------
    # INTERACTIVE CHARTS
    # ------------------------------------------------
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Cycle Diagrams</div>', unsafe_allow_html=True)

    P1, P2, P3, P4 = P
    V1c, V2, V3, V4 = V
    S1, S2, S3, S4  = S

    html_code = f"""
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      body {{ background: transparent; font-family: sans-serif; }}
      .charts-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        padding: 8px 0;
      }}
      
      /* Polish Chart Card Frame */
      .chart-card {{
        background: linear-gradient(135deg, #16162a 0%, #1a1a35 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
      }}
      .chart-title {{
        font-size: 13px;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 12px;
        letter-spacing: -0.01em;
        text-transform: uppercase;
        font-family: monospace;
      }}
      canvas {{ width: 100% !important; height: 220px !important; }}
      .legend {{
        display: flex;
        flex-direction: column;
        gap: 5px;
        margin-top: 10px;
      }}
      .legend-row {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        color: #94a3b8;
      }}
      .legend-line {{
        width: 20px;
        height: 3px;
        border-radius: 2px;
        flex-shrink: 0;
      }}
    </style>

    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-title">📊 P-V Diagram</div>
        <canvas id="pv-canvas"></canvas>
        <div class="legend">
          <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>1→2 Isothermal expansion (Th)</div>
          <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>2→3 Adiabatic expansion</div>
          <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>3→4 Isothermal compression (Tc)</div>
          <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>4→1 Adiabatic compression</div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-title">📊 T-S Diagram</div>
        <canvas id="ts-canvas"></canvas>
        <div class="legend">
          <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>1→2 Isothermal expansion (Th)</div>
          <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>2→3 Adiabatic expansion</div>
          <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>3→4 Isothermal compression (Tc)</div>
          <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>4→1 Adiabatic compression</div>
        </div>
      </div>
    </div>

    <script>
    const Th    = {Th};
    const Tc    = {Tc};
    const gamma = {results['gamma']};
    const nR    = {results['nR']};
    const P1={P1}, P2={P2}, P3={P3}, P4={P4};
    const V1={V1c}, V2={V2}, V3={V3}, V4={V4};
    const S1={S1}, S2={S2}, S3={S3}, S4={S4};

    function setupCanvas(id) {{
      const c   = document.getElementById(id);
      const dpr = window.devicePixelRatio || 1;
      const w   = c.parentElement.clientWidth - 32;
      const h   = 220;
      c.width   = w * dpr;
      c.height  = h * dpr;
      c.style.width  = w + 'px';
      c.style.height = h + 'px';
      const ctx = c.getContext('2d');
      ctx.scale(dpr, dpr);
      return {{ ctx, w, h }};
    }}

    function drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY) {{
      ctx.strokeStyle = 'rgba(255,255,255,0.04)';
      ctx.lineWidth   = 0.5;
      xTicks.forEach(x => {{ ctx.beginPath(); ctx.moveTo(toX(x), pad.t); ctx.lineTo(toX(x), h - pad.b); ctx.stroke(); }});
      yTicks.forEach(y => {{ ctx.beginPath(); ctx.moveTo(pad.l, toY(y)); ctx.lineTo(w - pad.r, toY(y)); ctx.stroke(); }});
    }}

    function drawAxes(ctx, w, h, pad, xLabel, yLabel, xTicks, yTicks, toX, toY, fmtX, fmtY) {{
      ctx.strokeStyle = 'rgba(255,255,255,0.15)';
      ctx.lineWidth   = 1;
      ctx.beginPath();
      ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, h - pad.b); ctx.lineTo(w - pad.r, h - pad.b);
      ctx.stroke();
      ctx.fillStyle  = '#888';
      ctx.font       = '10px sans-serif';
      ctx.textAlign  = 'center';
      xTicks.forEach(x => {{ ctx.fillText(fmtX(x), toX(x), h - pad.b + 14); }});
      ctx.textAlign = 'right';
      yTicks.forEach(y => {{ ctx.fillText(fmtY(y), pad.l - 5, toY(y) + 4); }});
      ctx.fillStyle  = '#aaa';
      ctx.font       = '11px sans-serif';
      ctx.textAlign  = 'center';
      ctx.fillText(xLabel, pad.l + (w - pad.l - pad.r) / 2, h - 2);
      ctx.save();
      ctx.translate(11, pad.t + (h - pad.t - pad.b) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(yLabel, 0, 0);
      ctx.restore();
    }}

    function curve(ctx, pts, color, toX, toY) {{
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth   = 2.5;
      pts.forEach((p, i) => i === 0 ? ctx.moveTo(toX(p[0]), toY(p[1])) : ctx.lineTo(toX(p[0]), toY(p[1])));
      ctx.stroke();
    }}

    function dot(ctx, x, y, label, toX, toY) {{
      const cx = toX(x), cy = toY(y);
      ctx.beginPath(); ctx.arc(cx, cy, 4.5, 0, Math.PI * 2);
      ctx.fillStyle   = '#16162a'; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.fillStyle   = '#fff';
      ctx.font        = 'bold 11px sans-serif';
      ctx.textAlign   = 'center';
      ctx.fillText(label, cx, cy - 10);
    }}

    // ---- P-V (With Proportional Aspect Ratio Scaling) ----
    (function() {{
      const {{ ctx, w, h }} = setupCanvas('pv-canvas');
      const pad = {{ l: 62, r: 16, t: 20, b: 32 }};
      const steps = 80;
      const seg12 = Array.from({{length: steps+1}}, (_, i) => {{ const v = V1 + i*(V2-V1)/steps; return [v, nR*Th/v]; }});
      const seg23 = Array.from({{length: steps+1}}, (_, i) => {{ const v = V2 + i*(V3-V2)/steps; return [v, P2*Math.pow(V2/v, gamma)]; }});
      const seg34 = Array.from({{length: steps+1}}, (_, i) => {{ const v = V3 + i*(V4-V3)/steps; return [v, nR*Tc/v]; }});
      const seg41 = Array.from({{length: steps+1}}, (_, i) => {{ const v = V4 + i*(V1-V4)/steps; return [v, P4*Math.pow(V4/v, gamma)]; }});

      // Fixed the deflation: adjust bounds padding proportionally to keep graph well proportioned
      const VrawMin = Math.min(V1,V4), VrawMax = Math.max(V2,V3);
      const PrawMin = Math.min(P3,P4), PrawMax = P1;
      
      const Vmin = VrawMin - (VrawMax - VrawMin) * 0.15;
      const Vmax = VrawMax + (VrawMax - VrawMin) * 0.15;
      const Pmin = PrawMin - (PrawMax - PrawMin) * 0.15;
      const Pmax = PrawMax + (PrawMax - PrawMin) * 0.15;

      const toX = v => pad.l + (v - Vmin)/(Vmax - Vmin)*(w - pad.l - pad.r);
      const toY = p => h - pad.b - (p - Pmin)/(Pmax - Pmin)*(h - pad.t - pad.b);

      const xTicks = Array.from({{length:5}}, (_,i) => Vmin + i*(Vmax-Vmin)/4);
      const yTicks = Array.from({{length:5}}, (_,i) => Pmin + i*(Pmax-Pmin)/4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      curve(ctx, seg12, '#e05c3a', toX, toY);
      curve(ctx, seg23, '#4a9edd', toX, toY);
      curve(ctx, seg34, '#c8941a', toX, toY);
      curve(ctx, seg41, '#4aad6e', toX, toY);
      [[V1,P1,'1'],[V2,P2,'2'],[V3,P3,'3'],[V4,P4,'4']].forEach(([v,p,l]) => dot(ctx,v,p,l,toX,toY));
      drawAxes(ctx, w, h, pad, 'Volume (m³)', 'Pressure (Pa)', xTicks, yTicks, toX, toY,
        x => x.toFixed(3), y => (y/1000).toFixed(0)+'k');
    }})();

    // ---- T-S (With Proportional Aspect Ratio Scaling) ----
    (function() {{
      const {{ ctx, w, h }} = setupCanvas('ts-canvas');
      const pad = {{ l: 56, r: 16, t: 20, b: 32 }};
      const steps = 80;
      const seg12 = Array.from({{length: steps+1}}, (_, i) => [S1 + i*(S2-S1)/steps, Th]);
      const seg23 = Array.from({{length: steps+1}}, (_, i) => [S2, Th + i*(Tc-Th)/steps]);
      const seg34 = Array.from({{length: steps+1}}, (_, i) => [S3 + i*(S4-S3)/steps, Tc]);
      const seg41 = Array.from({{length: steps+1}}, (_, i) => [S1, Tc + i*(Th-Tc)/steps]);

      // Fixed the deflation: expand limits safely to maximize dynamic space utilization
      const Smin = S1 - (S2 - S1) * 0.25;
      const Smax = S2 + (S2 - S1) * 0.25;
      const Tmin = Tc - (Th - Tc) * 0.20;
      const Tmax = Th + (Th - Tc) * 0.20;

      const toX = s => pad.l + (s - Smin)/(Smax - Smin)*(w - pad.l - pad.r);
      const toY = t => h - pad.b - (t - Tmin)/(Tmax - Tmin)*(h - pad.t - pad.b);

      const xTicks = Array.from({{length:5}}, (_,i) => Smin + i*(Smax-Smin)/4);
      const yTicks = Array.from({{length:5}}, (_,i) => Tmin + i*(Tmax-Tmin)/4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      curve(ctx, seg12, '#e05c3a', toX, toY);
      curve(ctx, seg23, '#4a9edd', toX, toY);
      curve(ctx, seg34, '#c8941a', toX, toY);
      curve(ctx, seg41, '#4aad6e', toX, toY);
      [[S1,Th,'1'],[S2,Th,'2'],[S3,Tc,'3'],[S4,Tc,'4']].forEach(([s,t,l]) => dot(ctx,s,t,l,toX,toY));
      drawAxes(ctx, w, h, pad, 'Entropy (J/K)', 'Temperature (K)', xTicks, yTicks, toX, toY,
        x => x.toFixed(1), y => Math.round(y));
    }})();
    </script>
    """

    components.html(html_code, height=420)