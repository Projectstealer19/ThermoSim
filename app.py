import streamlit as st
import base64
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="ThermoSim",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------
# LOAD BACKGROUND IMAGE
# ------------------------------------------------

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("assets/ThermoSim_background_image.png")

# ------------------------------------------------
# CUSTOM CSS  — dark-only, all 12 refinements
# ------------------------------------------------

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ------------------------------------------------ */
/* GLOBAL — always dark, no light-mode toggle       */
/* ------------------------------------------------ */

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    color-scheme: dark !important;
}}

/* ------------------------------------------------ */
/* BACKGROUND — reduced opacity renders (0.18)      */
/* ------------------------------------------------ */

.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* dark overlay — slightly heavier to suppress visual noise */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.62);
    z-index: -1;
}}

/* ------------------------------------------------ */
/* REMOVE STREAMLIT DEFAULTS & LIGHT-MODE ARTIFACTS */
/* ------------------------------------------------ */

header {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}

/* force dark on every Streamlit-injected element */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-baseweb="select"],
[data-baseweb="input"],
.stTextInput, .stSelectbox {{
    background-color: transparent !important;
    color: white !important;
}}

/* kill any theme toggle Streamlit injects */
[data-testid="stDecoration"],
[aria-label="Toggle theme"],
button[kind="icon"] {{ display: none !important; }}

/* ------------------------------------------------ */
/* MAIN CONTAINER — tighter, denser layout          */
/* ------------------------------------------------ */

.block-container {{
    max-width: 1100px;
    padding-top: 1.2rem !important;
    padding-bottom: 1.5rem !important;
}}

/* ------------------------------------------------ */
/* PAGE ENTRY ANIMATION — cards fade up with stagger */
/* ------------------------------------------------ */

@keyframes fadeUp {{
    from {{
        opacity: 0;
        transform: translateY(22px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.card-animate {{
    animation: fadeUp 0.55s ease both;
}}

/* ------------------------------------------------ */
/* TITLE — dominant visual hierarchy                */
/* ------------------------------------------------ */

.main-title {{
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 0.04em !important;
    margin-bottom: 4px;
    margin-top: 2px;
    line-height: 1.1;
}}

.white-text {{ color: white; }}
.blue-text  {{ color: #3B82F6; margin-left: 3px; }}

/* ------------------------------------------------ */
/* SUBTITLE — muted, smaller                        */
/* ------------------------------------------------ */

.subtitle {{
    text-align: center;
    font-size: 15px;
    color: #64748B !important;
    margin-bottom: 24px;
    font-weight: 500 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

/* ------------------------------------------------ */
/* CYCLE CARD — glassmorphism + hover interaction   */
/* ------------------------------------------------ */

.cycle-card {{
    background: rgba(12, 18, 30, 0.72);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 18px;
    padding: 20px 22px 18px 22px;
    margin-top: 10px;
    margin-bottom: 12px;
    box-shadow:
        0 2px 4px rgba(0,0,0,0.3),
        0 8px 20px rgba(0,0,0,0.22),
        inset 0 1px 0 rgba(255,255,255,0.04);
    transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
    cursor: default;
}}

.cycle-card:hover {{
    transform: translateY(-5px);
    border-color: rgba(59, 130, 246, 0.35);
    box-shadow:
        0 2px 4px rgba(0,0,0,0.3),
        0 14px 32px rgba(0,0,0,0.32),
        0 0 0 1px rgba(59, 130, 246, 0.15),
        inset 0 1px 0 rgba(255,255,255,0.06);
}}

.cycle-card-title {{
    color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    margin: 0 0 5px 0 !important;
    letter-spacing: -0.01em;
}}

.cycle-card-desc {{
    color: #94A3B8 !important;
    font-size: 13.5px !important;
    margin: 0 0 0 0 !important;
    opacity: 0.88;
    line-height: 1.45;
}}

/* ------------------------------------------------ */
/* LAUNCH BUTTON — inside each card                 */
/* ------------------------------------------------ */

div.stButton {{
    margin-top: 14px !important;
    margin-bottom: 0 !important;
}}

div.stButton > button {{
    width: 100% !important;
    height: 44px !important;
    border-radius: 11px !important;
    border: 1px solid rgba(59, 130, 246, 0.22) !important;
    background: linear-gradient(
        160deg,
        rgba(37, 52, 76, 0.95),
        rgba(18, 26, 42, 0.98)
    ) !important;
    color: #CBD5E1 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.25px !important;
    white-space: nowrap !important;
    transition: all 0.25s ease-in-out !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.04),
        0 4px 12px rgba(0,0,0,0.18) !important;
}}

div.stButton > button:hover {{
    border: 1px solid rgba(99, 162, 255, 0.55) !important;
    background: linear-gradient(
        160deg,
        rgba(55, 80, 120, 0.98),
        rgba(30, 48, 76, 0.99)
    ) !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.12),
        0 0 16px rgba(80, 160, 255, 0.18),
        0 6px 20px rgba(0,0,0,0.28) !important;
}}

/* ------------------------------------------------ */
/* LOADING OVERLAY — launch simulation animation    */
/* ------------------------------------------------ */

#thermo-loading-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(4, 8, 18, 0.93);
    backdrop-filter: blur(6px);
    z-index: 9999;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    animation: overlayFadeIn 0.2s ease forwards;
}}

#thermo-loading-overlay.active {{
    display: flex;
}}

@keyframes overlayFadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}

/* spinner ring */
.thermo-spinner {{
    width: 58px;
    height: 58px;
    border: 3px solid rgba(59, 130, 246, 0.15);
    border-top-color: #3B82F6;
    border-radius: 50%;
    animation: spinRing 0.85s linear infinite;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.30);
}}

@keyframes spinRing {{
    to {{ transform: rotate(360deg); }}
}}

/* inner pulse dot */
.thermo-spinner-inner {{
    position: absolute;
    width: 14px;
    height: 14px;
    background: #3B82F6;
    border-radius: 50%;
    animation: pulseDot 0.85s ease-in-out infinite alternate;
    box-shadow: 0 0 10px #3B82F6;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}}

@keyframes pulseDot {{
    from {{ opacity: 0.4; transform: translate(-50%,-50%) scale(0.8); }}
    to   {{ opacity: 1;   transform: translate(-50%,-50%) scale(1.15); }}
}}

.spinner-wrap {{
    position: relative;
    width: 58px;
    height: 58px;
}}

.thermo-loading-text {{
    color: #93C5FD;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    animation: textPulse 1.2s ease-in-out infinite alternate;
}}

@keyframes textPulse {{
    from {{ opacity: 0.5; }}
    to   {{ opacity: 1; }}
}}

.thermo-loading-sub {{
    color: #475569;
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    letter-spacing: 0.08em;
}}

/* ------------------------------------------------ */
/* BACK BUTTON (used on cycle pages via injection)  */
/* ------------------------------------------------ */

.back-btn-wrap {{
    margin-bottom: 10px;
}}

.back-btn {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 16px;
    background: rgba(20, 28, 44, 0.82);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 10px;
    color: #94A3B8 !important;
    font-size: 13.5px;
    font-weight: 500;
    letter-spacing: 0.02em;
    text-decoration: none !important;
    cursor: pointer;
    transition: all 0.22s ease;
    backdrop-filter: blur(6px);
}}

.back-btn:hover {{
    border-color: rgba(99, 162, 255, 0.4);
    color: #CBD5E1 !important;
    background: rgba(30, 44, 68, 0.92);
    transform: translateX(-2px);
    box-shadow: 0 0 12px rgba(59,130,246,0.14);
}}

</style>

<!-- Loading Overlay -->
<div id="thermo-loading-overlay">
    <div class="spinner-wrap">
        <div class="thermo-spinner"></div>
        <div class="thermo-spinner-inner"></div>
    </div>
    <div class="thermo-loading-text">Initializing Simulation…</div>
    <div class="thermo-loading-sub">Loading thermodynamic model</div>
</div>

<script>
// Show overlay on any Launch Simulation button click, hide after 1.4s
(function() {{
    function attachListeners() {{
        document.querySelectorAll('[data-testid="stButton"] > button, .stButton > button').forEach(function(btn) {{
            if (btn.dataset.thermoHooked) return;
            btn.dataset.thermoHooked = '1';
            btn.addEventListener('click', function() {{
                var overlay = document.getElementById('thermo-loading-overlay');
                if (overlay) {{
                    overlay.classList.add('active');
                    setTimeout(function() {{
                        overlay.classList.remove('active');
                    }}, 1500);
                }}
            }});
        }});
    }}
    // Re-attach after Streamlit re-renders
    var obs = new MutationObserver(attachListeners);
    obs.observe(document.body, {{ childList: true, subtree: true }});
    attachListeners();
}})();
</script>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER  — improved typography hierarchy
# ------------------------------------------------

st.markdown(
    """
    <h1 class="main-title">
        <span class="white-text">THERMO</span><span class="blue-text">SIM</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Select a Thermodynamic Cycle to Simulate</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------
# CYCLE DATA — with icons
# ------------------------------------------------

cycles = [
    {"name": "Carnot Cycle",        "desc": "Ideal reversible thermodynamic cycle",   "icon": "❄️",  "page": "pages/carnot_page.py"},
    {"name": "Otto Cycle",          "desc": "Petrol engine power cycle",               "icon": "🚗",  "page": "pages/otto_page.py"},
    {"name": "Diesel Cycle",        "desc": "Compression ignition engine cycle",       "icon": "⚙️",  "page": "pages/diesel_page.py"},
    {"name": "Dual Cycle",          "desc": "Mixed combustion engine cycle",           "icon": "🔩",  "page": "pages/dual_page.py"},
    {"name": "Brayton Cycle",       "desc": "Gas turbine power cycle",                 "icon": "🔥",  "page": "pages/brayton_page.py"},
    {"name": "Rankine Cycle",       "desc": "Steam turbine power plant cycle",         "icon": "♨️",  "page": "pages/rankine_page.py"},
    {"name": "Refrigeration Cycle", "desc": "Cooling and refrigeration cycle",         "icon": "🧊",  "page": "pages/refrigerator_page.py"},
]

# ------------------------------------------------
# GRID — 2-column, cards contain buttons
# ------------------------------------------------

col1, col2 = st.columns(2, gap="medium")

for i, cycle in enumerate(cycles):
    target_col = col1 if i % 2 == 0 else col2
    delay = f"{0.08 * i:.2f}s"

    with target_col:
        # Card wrapper with staggered fade-up entry animation
        st.markdown(f"""
            <div class="cycle-card card-animate" style="animation-delay: {delay};">
                <h3 class="cycle-card-title">{cycle['icon']}&nbsp; {cycle['name']}</h3>
                <p  class="cycle-card-desc">{cycle['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Launch button sits visually "inside" the card (immediately after, no gap)
        if st.button("Launch Simulation →", key=cycle['name']):
            st.switch_page(cycle['page'])