import streamlit as st
import streamlit.components.v1 as components

from cycles.dual import dual_cycle

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Dual Cycle",
    layout="wide"
)

# ------------------------------------------------
# CUSTOM STYLES (UI Polish & Modern Typography)
# ------------------------------------------------

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

st.markdown('<div class="main-title">Dual Cycle Simulation</div>', unsafe_allow_html=True)
st.markdown("Simulate an ideal air-standard Dual (mixed) thermodynamic cycle.")
st.markdown("---")

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------

st.markdown('<div class="section-title">⚙️ Input Parameters</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    T1    = st.number_input("Initial Temperature T1 (K)",
                             min_value=200, max_value=600, value=300, step=1)
    r     = st.number_input("Compression Ratio r",
                             min_value=2.0, max_value=25.0, value=16.0, step=0.1,
                             format="%.1f")

with col2:
    alpha = st.number_input("Pressure Ratio α (const-vol. heat addition)",
                             min_value=1.0, max_value=5.0, value=1.5, step=0.1,
                             format="%.1f")
    rc    = st.number_input("Cutoff Ratio rc (const-pressure heat addition)",
                             min_value=1.0, max_value=4.0, value=2.0, step=0.1,
                             format="%.1f")
    V1    = st.number_input("Initial Volume V1 (L)",
                             min_value=1, max_value=100, value=10, step=1)

V1_m3 = V1 / 1000.0    # L → m³

st.info("Assumptions: Air-standard cycle (γ = 1.4, R = 287 J/kg·K) · S1 = 100 J/kg·K (reference entropy)")

# ------------------------------------------------
# VALIDATION
# ------------------------------------------------

if rc * alpha > r:
    st.error("α × rc must not exceed compression ratio r (expansion would exceed initial volume).")
    st.stop()

# ------------------------------------------------
# PROCESS FLOWSHEET
# ------------------------------------------------

st.markdown("""
<div class="flow-card">
  <div class="flow-title">🔀 Cycle Process Flow Steps</div>
  <div class="flow-grid">
    <div class="flow-step"><span>1 → 2</span> Isentropic Compression</div>
    <div class="flow-step"><span>2 → 3</span> Constant-Volume Heat Addition</div>
    <div class="flow-step"><span>3 → 4</span> Constant-Pressure Heat Addition</div>
    <div class="flow-step"><span>4 → 5</span> Isentropic Expansion</div>
    <div class="flow-step"><span>5 → 1</span> Constant-Volume Heat Rejection</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# RUN BUTTON
# ------------------------------------------------

run = st.button("Run Dual Simulation", type="primary")

st.markdown("---")

if run:

    results = dual_cycle(T1, r, alpha, rc, V1=V1_m3)

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    st.markdown('<div class="section-title">📊 Simulation Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Efficiency",    f"{results['efficiency']:.1f}%")
    m2.metric("Net Work",      f"{results['W_net']/1000:.2f} kJ/kg")
    m3.metric("Heat Added",    f"{results['Q_in']/1000:.2f} kJ/kg")
    m4.metric("Heat Rejected", f"{results['Q_out']/1000:.2f} kJ/kg")

    # ------------------------------------------------
    # STATE POINTS TABLE
    # ------------------------------------------------

    st.markdown("---")
    st.markdown('<div class="section-title">📋 State Points</div>', unsafe_allow_html=True)

    import pandas as pd

    V = results["V"]
    P = results["P"]
    T = results["T"]
    S = results["S"]

    df = pd.DataFrame({
        "State":      ["1 — Start of compression",
                       "2 — After isentropic compression",
                       "3 — After const-volume heat addition",
                       "4 — After const-pressure heat addition",
                       "5 — After isentropic expansion"],
        "T (K)":      [f"{t:.1f}" for t in T],
        "P (kPa)":    [f"{p/1000:.2f}" for p in P],
        "V (L)":      [f"{v*1000:.4f}" for v in V],
        "S (J/kg·K)": [f"{s:.2f}" for s in S],
    })

    st.dataframe(df, hide_index=True, use_container_width=True)

    # ------------------------------------------------
    # INTERACTIVE CHARTS
    # ------------------------------------------------

    st.markdown("---")
    st.markdown('<div class="section-title">📈 Cycle Diagrams</div>', unsafe_allow_html=True)

    P1c, P2, P3, P4, P5   = results["P"]
    V1c, V2, V3, V4, V5   = results["V"]
    T1c, T2, T3c, T4, T5  = results["T"]
    S1c, S2, S3, S4, S5   = results["S"]
    gamma_val              = results["gamma"]
    cv_val                 = results["cv"]
    cp_val                 = results["cp"]

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
      .chart-card {{
        background: #1a1a2e;
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 16px;
        transition: all 0.25s ease;
      }}
      .chart-card:hover {{
        border-color: rgba(74,158,221,0.22);
        box-shadow:
          0 0 18px rgba(74,158,221,0.08),
          0 0 30px rgba(74,158,221,0.03);
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
        color: #aaa;
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
          <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>1→2 Isentropic compression</div>
          <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>2→3 Constant-volume heat addition</div>
          <div class="legend-row"><div class="legend-line" style="background:#b06fd8"></div>3→4 Constant-pressure heat addition</div>
          <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>4→5 Isentropic expansion</div>
          <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>5→1 Constant-volume heat rejection</div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-title">📊 T-S Diagram</div>
        <canvas id="ts-canvas"></canvas>
        <div class="legend">
          <div class="legend-row"><div class="legend-line" style="background:#4a9edd"></div>1→2 Isentropic compression</div>
          <div class="legend-row"><div class="legend-line" style="background:#e05c3a"></div>2→3 Constant-volume heat addition</div>
          <div class="legend-row"><div class="legend-line" style="background:#b06fd8"></div>3→4 Constant-pressure heat addition</div>
          <div class="legend-row"><div class="legend-line" style="background:#4aad6e"></div>4→5 Isentropic expansion</div>
          <div class="legend-row"><div class="legend-line" style="background:#c8941a"></div>5→1 Constant-volume heat rejection</div>
        </div>
      </div>
    </div>

    <script>
    const gamma = {gamma_val};
    const cv    = {cv_val};
    const cp    = {cp_val};
    const P1={P1c}, P2={P2}, P3={P3}, P4={P4}, P5={P5};
    const V1={V1c}, V2={V2}, V3={V3}, V4={V4}, V5={V5};
    const T1={T1c}, T2={T2}, T3={T3c}, T4={T4}, T5={T5};
    const S1={S1c}, S2={S2}, S3={S3}, S4={S4}, S5={S5};

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
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth   = 0.5;
      xTicks.forEach(x => {{ ctx.beginPath(); ctx.moveTo(toX(x), pad.t); ctx.lineTo(toX(x), h - pad.b); ctx.stroke(); }});
      yTicks.forEach(y => {{ ctx.beginPath(); ctx.moveTo(pad.l, toY(y)); ctx.lineTo(w - pad.r, toY(y)); ctx.stroke(); }});
    }}

    function drawAxes(ctx, w, h, pad, xLabel, yLabel, xTicks, yTicks, toX, toY, fmtX, fmtY) {{
      ctx.strokeStyle = 'rgba(255,255,255,0.25)';
      ctx.lineWidth   = 1;
      ctx.beginPath();
      ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, h - pad.b); ctx.lineTo(w - pad.r, h - pad.b);
      ctx.stroke();
      ctx.fillStyle = '#999'; ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      xTicks.forEach(x => {{ ctx.fillText(fmtX(x), toX(x), h - pad.b + 14); }});
      ctx.textAlign = 'right';
      yTicks.forEach(y => {{ ctx.fillText(fmtY(y), pad.l - 5, toY(y) + 4); }});
      ctx.fillStyle = '#bbb'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(xLabel, pad.l + (w - pad.l - pad.r) / 2, h - 2);
      ctx.save();
      ctx.translate(11, pad.t + (h - pad.t - pad.b) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(yLabel, 0, 0);
      ctx.restore();
    }}

    function curve(ctx, pts, color, toX, toY) {{
      ctx.beginPath(); ctx.strokeStyle = color; ctx.lineWidth = 2.5;
      pts.forEach((p, i) => i === 0 ? ctx.moveTo(toX(p[0]), toY(p[1])) : ctx.lineTo(toX(p[0]), toY(p[1])));
      ctx.stroke();
    }}

    function dot(ctx, x, y, label, toX, toY) {{
      const cx = toX(x), cy = toY(y);
      ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#1a1a2e'; ctx.fill();
      ctx.strokeStyle = '#e0e0e0'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.fillStyle = '#fff'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(label, cx, cy - 10);
    }}

    // ---- P-V Diagram ----
    (function() {{
      const {{ ctx, w, h }} = setupCanvas('pv-canvas');
      const pad = {{ l: 68, r: 16, t: 20, b: 32 }};
      const steps = 200;

      // 1→2 isentropic compression
      const seg12 = Array.from({{length: steps+1}}, (_, i) => {{
        const v = V1 + i*(V2-V1)/steps;
        return [v, P1 * Math.pow(V1/v, gamma)];
      }});
      // 2→3 constant volume (vertical)
      const seg23 = Array.from({{length: steps+1}}, (_, i) => [V2, P2 + i*(P3-P2)/steps]);
      // 3→4 constant pressure (horizontal)
      const seg34 = Array.from({{length: steps+1}}, (_, i) => [V3 + i*(V4-V3)/steps, P3]);
      // 4→5 isentropic expansion
      const seg45 = Array.from({{length: steps+1}}, (_, i) => {{
        const v = V4 + i*(V5-V4)/steps;
        return [v, P4 * Math.pow(V4/v, gamma)];
      }});
      // 5→1 constant volume (vertical)
      const seg51 = Array.from({{length: steps+1}}, (_, i) => [V5, P5 + i*(P1-P5)/steps]);

      const Vmin = V2 * 0.88, Vmax = V1 * 1.06;
      const Pmin = P1 * 0.82, Pmax = P3 * 1.08;
      const toX = v => pad.l + (v - Vmin)/(Vmax - Vmin)*(w - pad.l - pad.r);
      const toY = p => h - pad.b - (p - Pmin)/(Pmax - Pmin)*(h - pad.t - pad.b);

      const xTicks = Array.from({{length:5}}, (_,i) => Vmin + i*(Vmax-Vmin)/4);
      const yTicks = Array.from({{length:5}}, (_,i) => Pmin + i*(Pmax-Pmin)/4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      curve(ctx, seg12, '#4a9edd', toX, toY);
      curve(ctx, seg23, '#e05c3a', toX, toY);
      curve(ctx, seg34, '#b06fd8', toX, toY);
      curve(ctx, seg45, '#4aad6e', toX, toY);
      curve(ctx, seg51, '#c8941a', toX, toY);
      [[V1,P1,'1'],[V2,P2,'2'],[V3,P3,'3'],[V4,P4,'4'],[V5,P5,'5']].forEach(([v,p,l]) => dot(ctx,v,p,l,toX,toY));
      drawAxes(ctx, w, h, pad, 'Volume (m³)', 'Pressure (Pa)', xTicks, yTicks, toX, toY,
        x => (x*1000).toFixed(2)+'L', y => (y/1000).toFixed(0)+'k');
    }})();

    // ---- T-S Diagram ----
    (function() {{
      const {{ ctx, w, h }} = setupCanvas('ts-canvas');
      const pad = {{ l: 56, r: 16, t: 20, b: 32 }};
      const steps = 200;

      // 1→2 isentropic: vertical at S1
      const seg12 = Array.from({{length: steps+1}}, (_, i) => [S1, T1 + i*(T2-T1)/steps]);
      // 2→3 const volume: S = S2 + cv*ln(T/T2)
      const seg23 = Array.from({{length: steps+1}}, (_, i) => {{
        const t = T2 + i*(T3-T2)/steps;
        return [S2 + cv * Math.log(t/T2), t];
      }});
      // 3→4 const pressure: S = S3 + cp*ln(T/T3)
      const seg34 = Array.from({{length: steps+1}}, (_, i) => {{
        const t = T3 + i*(T4-T3)/steps;
        return [S3 + cp * Math.log(t/T3), t];
      }});
      // 4→5 isentropic: vertical at S4
      const seg45 = Array.from({{length: steps+1}}, (_, i) => [S4, T4 + i*(T5-T4)/steps]);
      // 5→1 const volume: S = S5 + cv*ln(T/T5)
      const seg51 = Array.from({{length: steps+1}}, (_, i) => {{
        const t = T5 + i*(T1-T5)/steps;
        return [S5 + cv * Math.log(t/T5), t];
      }});

      const allS = [S1,S2,S3,S4,S5], allT = [T1,T2,T3,T4,T5];
      const Smin = Math.min(...allS) - 5, Smax = Math.max(...allS) + 5;
      const Tmin = Math.min(...allT)*0.88, Tmax = Math.max(...allT)*1.06;
      const toX = s => pad.l + (s - Smin)/(Smax - Smin)*(w - pad.l - pad.r);
      const toY = t => h - pad.b - (t - Tmin)/(Tmax - Tmin)*(h - pad.t - pad.b);

      const xTicks = Array.from({{length:5}}, (_,i) => Smin + i*(Smax-Smin)/4);
      const yTicks = Array.from({{length:5}}, (_,i) => Tmin + i*(Tmax-Tmin)/4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      curve(ctx, seg12, '#4a9edd', toX, toY);
      curve(ctx, seg23, '#e05c3a', toX, toY);
      curve(ctx, seg34, '#b06fd8', toX, toY);
      curve(ctx, seg45, '#4aad6e', toX, toY);
      curve(ctx, seg51, '#c8941a', toX, toY);
      [[S1,T1,'1'],[S2,T2,'2'],[S3,T3,'3'],[S4,T4,'4'],[S5,T5,'5']].forEach(([s,t,l]) => dot(ctx,s,t,l,toX,toY));
      drawAxes(ctx, w, h, pad, 'Entropy (J/kg·K)', 'Temperature (K)', xTicks, yTicks, toX, toY,
        x => x.toFixed(1), y => Math.round(y));
    }})();
    </script>
    """

    components.html(html_code, height=450)