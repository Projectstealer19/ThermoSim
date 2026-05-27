import importlib

# -----------------------------------------------------------------------
# CACHE BUSTING — force Streamlit to reload the backend module on every
# execution so edits to cycles/diesel.py take effect immediately.
# -----------------------------------------------------------------------
import cycles.diesel
importlib.reload(cycles.diesel)
from cycles.diesel import diesel_cycle

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# -----------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(page_title="Diesel Cycle", layout="wide")
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
# -----------------------------------------------------------------------
# CUSTOM STYLES
# -----------------------------------------------------------------------
st.markdown("""
<style>
  .main-title {
    font-size: 2.2rem; font-weight: 700; letter-spacing: -0.02em;
    color: #ffffff; margin-bottom: 4px;
  }
  .section-title {
    font-size: 1.3rem; font-weight: 600; letter-spacing: -0.01em;
    color: #f1f5f9; margin-top: 1rem; margin-bottom: 0.8rem;
  }
  .flow-card {
    background: rgba(30,30,50,0.35);
    border: 1px solid rgba(255,255,255,0.05);
    border-left: 3px solid #4a9edd;
    border-radius: 8px; padding: 14px 18px;
    margin-top: 16px; margin-bottom: 8px;
  }
  .flow-title {
    font-size: 0.75rem; text-transform: uppercase;
    letter-spacing: 0.08em; color: #8e9aab;
    margin-bottom: 8px; font-weight: 700;
  }
  .flow-grid  { display: flex; flex-wrap: wrap; gap: 16px 24px; }
  .flow-step  { font-size: 0.825rem; color: #cbd5e1; font-family: monospace; }
  .flow-step span { color: #4a9edd; font-weight: bold; }

  div[data-baseweb="input"] {
    border-color: rgba(255,255,255,0.2) !important; box-shadow: none !important;
  }
  div[data-baseweb="input"]:focus-within {
    border-color: #4a9edd !important;
    box-shadow: 0 0 0 1px #4a9edd !important;
  }
  div[data-baseweb="input"] * { border-color: inherit !important; }
  div[data-baseweb="input"] button {
    background-color: #4a9edd !important; color: #fff !important;
    border-color: #4a9edd !important;
  }
  div[data-baseweb="input"] button:hover { background-color: #2e7cbf !important; }
  [data-testid="stNumberInput"] div[data-baseweb="input"] {
    border-color: rgba(255,255,255,0.2) !important;
  }
  div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #4a9edd !important;
    border-color: #4a9edd !important; color: #fff !important;
  }
  div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #2e7cbf !important;
  }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Diesel Cycle Simulation</div>', unsafe_allow_html=True)
st.markdown("Simulate an ideal air-standard Diesel thermodynamic cycle.")
st.markdown("---")

# -----------------------------------------------------------------------
# INPUT PARAMETERS
# -----------------------------------------------------------------------
st.markdown('<div class="section-title">⚙️ Input Parameters</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    T1 = st.number_input("Initial Temperature T1 (K)",
                         min_value=200, max_value=600, value=300, step=1)
    r  = st.number_input("Compression Ratio r",
                         min_value=2.0, max_value=25.0, value=16.0,
                         step=0.1, format="%.1f")
with col2:
    rc = st.number_input("Cutoff Ratio rc",
                         min_value=1.0, max_value=4.0, value=2.0,
                         step=0.1, format="%.1f")
    V1_L = st.number_input("Initial Volume V1 (L)",
                            min_value=1, max_value=100, value=10, step=1)

# -----------------------------------------------------------------------
# UNIT CONVERSION  — litres → cubic metres BEFORE calling the backend.
# The backend works entirely in SI (m³, Pa, J/kg·K).
# All litre ↔ m³ conversions back to the display layer happen below.
# -----------------------------------------------------------------------
V1_m3: float = V1_L / 1000.0   # e.g. 10 L  →  0.010 m³

st.info("Assumptions: Air-standard cycle (γ = 1.4, R = 287 J/kg·K) · S₁ = 100 J/kg·K")

if rc >= r:
    st.error("Cutoff ratio rc must be strictly less than compression ratio r.")
    st.stop()

run = st.button("Run Diesel Simulation", type="primary")

st.markdown("""
<div class="flow-card">
  <div class="flow-title">🔀 Cycle Process Flow</div>
  <div class="flow-grid">
    <div class="flow-step"><span>1 → 2</span> Isentropic Compression</div>
    <div class="flow-step"><span>2 → 3</span> Constant-Pressure Heat Addition</div>
    <div class="flow-step"><span>3 → 4</span> Isentropic Expansion</div>
    <div class="flow-step"><span>4 → 1</span> Constant-Volume Heat Rejection</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------
# RUN SIMULATION
# -----------------------------------------------------------------------
if run:
    # Pass V1 in m³ — the backend expects SI units throughout.
    results = diesel_cycle(T1=T1, r=r, rc=rc, V1=V1_m3)

    # -------------------------------------------------------------------
    # METRICS  — all values come directly from the results dict.
    # W_net / Q_in / Q_out are in J/kg; display as kJ/kg.
    # -------------------------------------------------------------------
    st.markdown('<div class="section-title">📊 Simulation Results</div>',
                unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Efficiency",    f"{results['efficiency']:.2f} %")
    m2.metric("Net Work",      f"{results['W_net']  / 1000.0:.2f} kJ/kg")
    m3.metric("Heat Added",    f"{results['Q_in']   / 1000.0:.2f} kJ/kg")
    m4.metric("Heat Rejected", f"{results['Q_out']  / 1000.0:.2f} kJ/kg")

    st.markdown("---")

    # -------------------------------------------------------------------
    # STATE POINTS TABLE
    # V from backend is in m³ → multiply by 1000 to display as litres.
    # P from backend is in Pa  → divide by 1000 to display as kPa.
    # -------------------------------------------------------------------
    st.markdown('<div class="section-title">📋 State Points</div>',
                unsafe_allow_html=True)

    T_pts = results["T"]   # [T1, T2, T3, T4]  (K)
    P_pts = results["P"]   # [P1, P2, P3, P4]  (Pa)
    V_pts = results["V"]   # [V1, V2, V3, V4]  (m³)
    S_pts = results["S"]   # [S1, S2, S3, S4]  (J/kg·K)

    df = pd.DataFrame({
        "State": [
            "1 — Start of compression",
            "2 — After isentropic compression",
            "3 — After constant-pressure heat addition",
            "4 — After isentropic expansion",
        ],
        "T (K)":      [f"{t:.1f}"                 for t in T_pts],
        "P (kPa)":    [f"{p / 1000.0:.2f}"        for p in P_pts],
        # m³ → litres: multiply by 1000
        "V (L)":      [f"{v * 1000.0:.4f}"        for v in V_pts],
        "S (J/kg·K)": [f"{s:.2f}"                 for s in S_pts],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📈 Cycle Diagrams</div>',
                unsafe_allow_html=True)

    # -------------------------------------------------------------------
    # Unpack state points for the JavaScript canvas renderer.
    # -------------------------------------------------------------------
    P1c, P2, P3, P4  = results["P"]   # Pa
    V1c, V2, V3, V4  = results["V"]   # m³
    T1c, T2, T3c, T4 = results["T"]   # K
    S1c, S2, S3, S4  = results["S"]   # J/kg·K
    gamma_val         = results["gamma"]
    cv_val            = results["cv"]
    cp_val            = results["cp"]

    # -------------------------------------------------------------------
    # JAVASCRIPT UNIT CONVENTIONS
    #
    # Volumes : injected as m³ floats, then converted to LITRES in JS
    #           by multiplying by 1000.  Example:
    #               const jsV1 = {V1c} * 1000;   // 0.010 m³ → 10 L
    #
    # Pressures: injected as Pa floats, then converted to kPa in JS
    #            by dividing by 1000.  Example:
    #               const jsP1 = {P1c} / 1000;   // 860000 Pa → 860 kPa
    #
    # The isentropic curves use the relation  P·Vᵞ = const,
    # which holds regardless of units as long as P and V are internally
    # consistent — both are in kPa and L inside the JS scope.
    # -------------------------------------------------------------------

    html_code = f"""
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      body {{ background: transparent; font-family: sans-serif; }}
      .charts-grid {{
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 16px; padding: 8px 0;
      }}
      .chart-card {{
        background: #1a1a2e; border: 1px solid #2a2a4a;
        border-radius: 12px; padding: 16px;
      }}
      .chart-title {{
        font-size: 13px; font-weight: 600; color: #e2e8f0;
        margin-bottom: 12px; letter-spacing: -0.01em;
        text-transform: uppercase; font-family: monospace;
      }}
      canvas {{ display: block; }}
      .legend {{
        display: flex; flex-direction: column; gap: 5px; margin-top: 10px;
      }}
      .legend-row {{
        display: flex; align-items: center; gap: 8px;
        font-size: 11px; color: #aaa;
      }}
      .legend-line {{
        width: 20px; height: 3px; border-radius: 2px; flex-shrink: 0;
      }}
    </style>

    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-title">P-V Diagram</div>
        <canvas id="pv-canvas"></canvas>
        <div class="legend">
          <div class="legend-row">
            <div class="legend-line" style="background:#4a9edd"></div>
            1→2 Isentropic compression
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#e05c3a"></div>
            2→3 Constant-pressure heat addition
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#4aad6e"></div>
            3→4 Isentropic expansion
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#c8941a"></div>
            4→1 Constant-volume heat rejection
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-title">T-S Diagram</div>
        <canvas id="ts-canvas"></canvas>
        <div class="legend">
          <div class="legend-row">
            <div class="legend-line" style="background:#4a9edd"></div>
            1→2 Isentropic compression
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#e05c3a"></div>
            2→3 Constant-pressure heat addition
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#4aad6e"></div>
            3→4 Isentropic expansion
          </div>
          <div class="legend-row">
            <div class="legend-line" style="background:#c8941a"></div>
            4→1 Constant-volume heat rejection
          </div>
        </div>
      </div>
    </div>

    <script>
    // ----------------------------------------------------------------
    // Gas constants — injected from Python
    // ----------------------------------------------------------------
    const gamma = {gamma_val};
    const cv    = {cv_val};
    const cp    = {cp_val};

    // ----------------------------------------------------------------
    // State-point values — injected from Python results dict.
    //
    // PRESSURES: backend returns Pa → convert to kPa for display.
    //   jsP = pythonP_Pa / 1000
    //
    // VOLUMES: backend returns m³ → convert to Litres for display.
    //   jsV = pythonV_m3 * 1000
    //
    // The isentropic relation  P * V^gamma = constant  is dimensionally
    // homogeneous, so it holds correctly in (kPa, L) just as in (Pa, m³).
    // ----------------------------------------------------------------
    const P1 = {P1c} / 1000.0;   // Pa  → kPa
    const P2 = {P2}  / 1000.0;
    const P3 = {P3}  / 1000.0;
    const P4 = {P4}  / 1000.0;

    const V1 = {V1c} * 1000.0;   // m³ → L
    const V2 = {V2}  * 1000.0;
    const V3 = {V3}  * 1000.0;
    const V4 = {V4}  * 1000.0;

    const T1 = {T1c};             // K  (no conversion needed)
    const T2 = {T2};
    const T3 = {T3c};
    const T4 = {T4};

    const S1 = {S1c};             // J/kg·K (no conversion needed)
    const S2 = {S2};
    const S3 = {S3};
    const S4 = {S4};

    // ----------------------------------------------------------------
    // Canvas helpers
    // ----------------------------------------------------------------
    function setupCanvas(id) {{
      const canvas = document.getElementById(id);
      const dpr    = window.devicePixelRatio || 1;
      const w      = canvas.parentElement.clientWidth - 32;
      const h      = 220;
      canvas.width        = w * dpr;
      canvas.height       = h * dpr;
      canvas.style.width  = w + 'px';
      canvas.style.height = h + 'px';
      const ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);
      return {{ ctx, w, h }};
    }}

    function drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY) {{
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth   = 0.5;
      xTicks.forEach(x => {{
        ctx.beginPath();
        ctx.moveTo(toX(x), pad.t);
        ctx.lineTo(toX(x), h - pad.b);
        ctx.stroke();
      }});
      yTicks.forEach(y => {{
        ctx.beginPath();
        ctx.moveTo(pad.l,       toY(y));
        ctx.lineTo(w - pad.r,   toY(y));
        ctx.stroke();
      }});
    }}

    function drawAxes(ctx, w, h, pad, xLabel, yLabel,
                      xTicks, yTicks, toX, toY, fmtX, fmtY) {{
      ctx.strokeStyle = 'rgba(255,255,255,0.25)';
      ctx.lineWidth   = 1;
      ctx.beginPath();
      ctx.moveTo(pad.l,     pad.t);
      ctx.lineTo(pad.l,     h - pad.b);
      ctx.lineTo(w - pad.r, h - pad.b);
      ctx.stroke();

      ctx.fillStyle = '#999';
      ctx.font      = '10px sans-serif';
      ctx.textAlign = 'center';
      xTicks.forEach(x => {{
        ctx.fillText(fmtX(x), toX(x), h - pad.b + 14);
      }});
      ctx.textAlign = 'right';
      yTicks.forEach(y => {{
        ctx.fillText(fmtY(y), pad.l - 5, toY(y) + 4);
      }});

      ctx.fillStyle = '#bbb';
      ctx.font      = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(xLabel, pad.l + (w - pad.l - pad.r) / 2, h - 2);

      ctx.save();
      ctx.translate(11, pad.t + (h - pad.t - pad.b) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(yLabel, 0, 0);
      ctx.restore();
    }}

    function drawCurve(ctx, pts, color, toX, toY) {{
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth   = 2.5;
      pts.forEach((p, i) => {{
        if (i === 0) ctx.moveTo(toX(p[0]), toY(p[1]));
        else         ctx.lineTo(toX(p[0]), toY(p[1]));
      }});
      ctx.stroke();
    }}

    function drawDot(ctx, x, y, label, toX, toY) {{
      const cx = toX(x);
      const cy = toY(y);
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fillStyle   = '#1a1a2e';
      ctx.fill();
      ctx.strokeStyle = '#e0e0e0';
      ctx.lineWidth   = 1.5;
      ctx.stroke();
      ctx.fillStyle   = '#ffffff';
      ctx.font        = 'bold 11px sans-serif';
      ctx.textAlign   = 'center';
      ctx.fillText(label, cx, cy - 10);
    }}

    // ----------------------------------------------------------------
    // P-V Diagram
    // All values in kPa and L — consistent with the unit conversions above.
    // ----------------------------------------------------------------
    (function () {{
      const {{ ctx, w, h }} = setupCanvas('pv-canvas');
      const pad   = {{ l: 68, r: 16, t: 20, b: 32 }};
      const steps = 200;

      // 1→2  Isentropic compression:  P * V^gamma = P1 * V1^gamma
      const seg12 = Array.from({{ length: steps + 1 }}, (_, i) => {{
        const v = V1 + i * (V2 - V1) / steps;
        return [v, P1 * Math.pow(V1 / v, gamma)];
      }});

      // 2→3  Isobaric heat addition:  P = P2 = const
      const seg23 = Array.from({{ length: steps + 1 }}, (_, i) => [
        V2 + i * (V3 - V2) / steps,
        P2
      ]);

      // 3→4  Isentropic expansion:  P * V^gamma = P3 * V3^gamma
      const seg34 = Array.from({{ length: steps + 1 }}, (_, i) => {{
        const v = V3 + i * (V4 - V3) / steps;
        return [v, P3 * Math.pow(V3 / v, gamma)];
      }});

      // 4→1  Isochoric (constant-volume) heat rejection:  V = V4 = V1
      const seg41 = Array.from({{ length: steps + 1 }}, (_, i) => [
        V4,
        P4 + i * (P1 - P4) / steps
      ]);

      // Axis bounds — add a small margin so state points aren't clipped
      const Vmin = V2 * 0.85;
      const Vmax = V1 * 1.05;
      const Pmin = P1 * 0.80;
      const Pmax = P3 * 1.05;

      const toX = v => pad.l + (v - Vmin) / (Vmax - Vmin) * (w - pad.l - pad.r);
      const toY = p => h - pad.b - (p - Pmin) / (Pmax - Pmin) * (h - pad.t - pad.b);

      const xTicks = Array.from({{ length: 5 }}, (_, i) => Vmin + i * (Vmax - Vmin) / 4);
      const yTicks = Array.from({{ length: 5 }}, (_, i) => Pmin + i * (Pmax - Pmin) / 4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      drawCurve(ctx, seg12, '#4a9edd', toX, toY);
      drawCurve(ctx, seg23, '#e05c3a', toX, toY);
      drawCurve(ctx, seg34, '#4aad6e', toX, toY);
      drawCurve(ctx, seg41, '#c8941a', toX, toY);

      [[V1,P1,'1'],[V2,P2,'2'],[V3,P3,'3'],[V4,P4,'4']].forEach(
        ([v, p, lbl]) => drawDot(ctx, v, p, lbl, toX, toY)
      );

      drawAxes(ctx, w, h, pad,
        'Volume (L)', 'Pressure (kPa)',
        xTicks, yTicks, toX, toY,
        x => x.toFixed(2) + ' L',
        y => y.toFixed(0)
      );
    }})();

    // ----------------------------------------------------------------
    // T-S Diagram
    // ----------------------------------------------------------------
    (function () {{
      const {{ ctx, w, h }} = setupCanvas('ts-canvas');
      const pad   = {{ l: 60, r: 16, t: 20, b: 32 }};
      const steps = 200;

      // 1→2  Isentropic compression:  S = const = S1
      const seg12 = Array.from({{ length: steps + 1 }}, (_, i) => [
        S1,
        T1 + i * (T2 - T1) / steps
      ]);

      // 2→3  Isobaric heat addition:  dS = cp * dT / T
      //   → S(T) = S2 + cp * ln(T / T2)
      const seg23 = Array.from({{ length: steps + 1 }}, (_, i) => {{
        const t = T2 + i * (T3 - T2) / steps;
        return [S2 + cp * Math.log(t / T2), t];
      }});

      // 3→4  Isentropic expansion:  S = const = S3
      const seg34 = Array.from({{ length: steps + 1 }}, (_, i) => [
        S3,
        T3 + i * (T4 - T3) / steps
      ]);

      // 4→1  Isochoric heat rejection:  dS = cv * dT / T
      //   → S(T) = S4 + cv * ln(T / T4)
      const seg41 = Array.from({{ length: steps + 1 }}, (_, i) => {{
        const t = T4 + i * (T1 - T4) / steps;
        return [S4 + cv * Math.log(t / T4), t];
      }});

      const allS = [S1, S2, S3, S4];
      const allT = [T1, T2, T3, T4];
      const Smin = Math.min(...allS) - 5;
      const Smax = Math.max(...allS) + 5;
      const Tmin = Math.min(...allT) * 0.88;
      const Tmax = Math.max(...allT) * 1.06;

      const toX = s => pad.l + (s - Smin) / (Smax - Smin) * (w - pad.l - pad.r);
      const toY = t => h - pad.b - (t - Tmin) / (Tmax - Tmin) * (h - pad.t - pad.b);

      const xTicks = Array.from({{ length: 5 }}, (_, i) => Smin + i * (Smax - Smin) / 4);
      const yTicks = Array.from({{ length: 5 }}, (_, i) => Tmin + i * (Tmax - Tmin) / 4);

      drawGrid(ctx, w, h, pad, xTicks, yTicks, toX, toY);
      drawCurve(ctx, seg12, '#4a9edd', toX, toY);
      drawCurve(ctx, seg23, '#e05c3a', toX, toY);
      drawCurve(ctx, seg34, '#4aad6e', toX, toY);
      drawCurve(ctx, seg41, '#c8941a', toX, toY);

      [[S1,T1,'1'],[S2,T2,'2'],[S3,T3,'3'],[S4,T4,'4']].forEach(
        ([s, t, lbl]) => drawDot(ctx, s, t, lbl, toX, toY)
      );

      drawAxes(ctx, w, h, pad,
        'Entropy (J/kg·K)', 'Temperature (K)',
        xTicks, yTicks, toX, toY,
        x => x.toFixed(1),
        y => Math.round(y)
      );
    }})();
    </script>
    """

    components.html(html_code, height=460)