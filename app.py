import streamlit as st
import base64

# ================================================
# PAGE CONFIG
# ================================================

st.set_page_config(
    page_title="ThermoSim",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================================
# UTILITIES
# ================================================

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("assets/ThermoSim_background_image.png")

# ================================================
# CYCLE DATA
# ================================================

CYCLES = [
    {
        "name": "Carnot Cycle",
        "icon": "❄",
        "desc": "Ideal reversible thermodynamic cycle establishing maximum theoretical efficiency",
        "page": "pages/carnot_page.py",
    },
    {
        "name": "Otto Cycle",
        "icon": "🚗",
        "desc": "Spark-ignition petrol engine cycle with constant-volume heat addition",
        "page": "pages/otto_page.py",
    },
    {
        "name": "Diesel Cycle",
        "icon": "⚙",
        "desc": "Compression-ignition engine cycle with constant-pressure combustion",
        "page": "pages/diesel_page.py",
    },
    {
        "name": "Dual Cycle",
        "icon": "🔩",
        "desc": "Combined constant-volume and constant-pressure heat addition cycle",
        "page": "pages/dual_page.py",
    },
    {
        "name": "Brayton Cycle",
        "icon": "🔥",
        "desc": "Gas turbine power cycle used in jet engines and power generation",
        "page": "pages/brayton_page.py",
    },
    {
        "name": "Rankine Cycle",
        "icon": "♨",
        "desc": "Steam turbine cycle underpinning most thermal power plants",
        "page": "pages/rankine_page.py",
    },
    {
        "name": "Refrigeration Cycle",
        "icon": "❄",
        "desc": "Vapour-compression cycle for cooling and heat-pump applications",
        "page": "pages/refrigerator_page.py",
    },
]

# ================================================
# CSS
# ================================================

st.markdown(f"""
<style>

/* ── Fonts ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Permanent dark mode ────────────────────────── */
:root, html, body {{
    color-scheme: dark only !important;
    --background-color:           #07090F !important;
    --secondary-background-color: #0D1220 !important;
    --text-color:                 #D8E0EE !important;
    --font:                       'Inter', sans-serif !important;
}}

html, body,
.stApp,
.main,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
section[data-testid="stSidebar"] {{
    background-color: transparent !important;
    color: #D8E0EE !important;
    font-family: 'Inter', sans-serif !important;
}}

[data-baseweb="input"],
[data-baseweb="select"],
[data-baseweb="textarea"],
.stTextInput > div,
.stSelectbox > div,
.stSlider,
.stNumberInput,
[role="listbox"],
[role="option"] {{
    background-color: #0D1220 !important;
    color: #D8E0EE !important;
    border-color: rgba(255,255,255,0.10) !important;
}}

/* hide theme toggle and Streamlit chrome */
header, footer, #MainMenu                {{ visibility: hidden; }}
[data-testid="stDecoration"],
button[aria-label*="heme"],
[data-testid="baseButton-headerNoPadding"] {{ display: none !important; }}

/* ── Background ─────────────────────────────────── */
.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* layer 1 — primary dark wash (keeps renders atmospheric, not dominating) */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(5, 7, 14, 0.58);
    z-index: 0;
    pointer-events: none;
}}

/* layer 2 — radial vignette: edges darker, centre breathes */
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(
        ellipse 80% 70% at 50% 42%,
        rgba(5,7,14,0.0)  0%,
        rgba(5,7,14,0.42) 100%
    );
    z-index: 0;
    pointer-events: none;
}}

[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

/* ── Layout ─────────────────────────────────────── */
.block-container {{
    max-width: 1120px;
    padding-top:    2rem   !important;
    padding-bottom: 2.5rem !important;
    padding-left:   1.5rem !important;
    padding-right:  1.5rem !important;
}}

/* ── Hero header ────────────────────────────────── */
.ts-hero {{
    text-align: center;
    margin-bottom: 8px;
}}

.ts-wordmark {{
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: clamp(34px, 5vw, 52px);
    font-weight: 700;
    letter-spacing: 0.12em;
    line-height: 1;
    color: #F0F4FF;
    text-transform: uppercase;
}}

.ts-wordmark span {{
    color: #4A90D9;
}}

/* thin accent rule beneath title */
.ts-rule {{
    display: block;
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4A90D9, transparent);
    margin: 10px auto 0;
    border-radius: 2px;
    opacity: 0.7;
}}

.ts-subtitle {{
    text-align: center;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 0.20em;
    text-transform: uppercase;
    color: #7A92B0;
    margin-top: 14px;
    margin-bottom: 36px;
}}

/* ── Section label ──────────────────────────────── */
.ts-section-label {{
    font-size: 10.5px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3A4E68;
    margin-bottom: 14px;
    padding-left: 2px;
}}

/* ── Cycle card ─────────────────────────────────── */
.ts-card {{
    background: rgba(18, 26, 46, 0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 14px;
    padding: 16px 18px 14px;
    margin-bottom: 10px;
    transition: border-color 0.22s ease, box-shadow 0.22s ease, transform 0.22s ease;
    box-shadow: 0 4px 18px rgba(0,0,0,0.28);
    cursor: default;
}}

.ts-card:hover {{
    border-color: rgba(74,144,217,0.30);
    box-shadow:
        0 4px 18px rgba(0,0,0,0.32),
        0 0 0 1px rgba(74,144,217,0.12);
    transform: translateY(-2px);
}}

.ts-card-header {{
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 5px;
}}

.ts-card-icon {{
    font-size: 15px;
    line-height: 1;
    opacity: 0.88;
    flex-shrink: 0;
}}

.ts-card-title {{
    font-size: 14.5px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    letter-spacing: 0.01em;
    margin: 0 !important;
    line-height: 1.3;
}}

.ts-card-desc {{
    font-size: 12px !important;
    color: #9AAFC8 !important;
    line-height: 1.55;
    margin: 0 !important;
    padding-left: 24px;   /* aligns under title, past the icon */
}}

/* ── Launch button ──────────────────────────────── */
div.stButton {{
    margin-top: 0 !important;
    margin-bottom: 10px !important;
}}

div.stButton > button {{
    width: 100% !important;
    height: 40px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(74,144,217,0.20) !important;
    background: rgba(16, 24, 42, 0.82) !important;
    color: #8BAFD4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    white-space: nowrap !important;
    transition: all 0.20s ease !important;
    box-shadow: none !important;
}}

div.stButton > button:hover {{
    border-color: rgba(74,144,217,0.55) !important;
    background: rgba(26, 44, 74, 0.90) !important;
    color: #C5DAFA !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 12px rgba(74,144,217,0.15), 0 4px 14px rgba(0,0,0,0.22) !important;
}}

div.stButton > button:active {{
    transform: translateY(0px) !important;
    box-shadow: none !important;
}}

/* ── Responsive: single column on narrow viewports ── */
@media (max-width: 720px) {{
    .ts-wordmark {{
        font-size: 32px;
        letter-spacing: 0.08em;
    }}
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
}}

</style>
""", unsafe_allow_html=True)

# ================================================
# HERO
# ================================================

st.markdown("""
<div class="ts-hero">
    <div class="ts-wordmark">THERMO<span>SIM</span></div>
    <span class="ts-rule"></span>
</div>
<div class="ts-subtitle">Computational Thermodynamic Cycle Simulator</div>
""", unsafe_allow_html=True)

# ================================================
# SECTION LABEL
# ================================================

st.markdown('<div class="ts-section-label">Select a cycle to simulate</div>', unsafe_allow_html=True)

# ================================================
# GRID
# ================================================

col_left, col_right = st.columns(2, gap="medium")

for i, cycle in enumerate(CYCLES):
    col = col_left if i % 2 == 0 else col_right

    with col:
        # Card — info only, no button inside
        st.markdown(f"""
        <div class="ts-card">
            <div class="ts-card-header">
                <span class="ts-card-icon">{cycle['icon']}</span>
                <p class="ts-card-title">{cycle['name']}</p>
            </div>
            <p class="ts-card-desc">{cycle['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Launch button — outside card, directly below
        if st.button("Launch Simulation", key=cycle['name']):
            st.switch_page(cycle['page'])