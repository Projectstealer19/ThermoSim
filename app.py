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
# SESSION STATE — controls loading animation flow
# ------------------------------------------------

if "launch_target" not in st.session_state:
    st.session_state.launch_target = None
if "launching" not in st.session_state:
    st.session_state.launching = False

# ------------------------------------------------
# NAVIGATION STEP 2:
# If we are in "launching" state, show spinner,
# wait briefly, then navigate.
# ------------------------------------------------

if st.session_state.launching and st.session_state.launch_target:
    target = st.session_state.launch_target
    st.session_state.launching = False
    st.session_state.launch_target = None

    # ---- FULL-SCREEN LOADING OVERLAY ----
    st.markdown("""
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: #080C14 !important;
    }
    .loading-screen {
        position: fixed;
        inset: 0;
        background: #080C14;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 22px;
        z-index: 99999;
    }
    .spinner-ring {
        width: 64px;
        height: 64px;
        border: 3px solid rgba(59, 130, 246, 0.12);
        border-top-color: #3B82F6;
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
        box-shadow: 0 0 22px rgba(59,130,246,0.25), 0 0 6px rgba(59,130,246,0.15);
        position: relative;
    }
    .spinner-dot {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #60A5FA;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        animation: dotpulse 0.9s ease-in-out infinite alternate;
        box-shadow: 0 0 10px #3B82F6;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    @keyframes dotpulse {
        from { opacity: 0.3; transform: translate(-50%,-50%) scale(0.7); }
        to   { opacity: 1;   transform: translate(-50%,-50%) scale(1.2); }
    }
    .loading-label {
        color: #93C5FD;
        font-family: 'Inter', sans-serif;
        font-size: 13.5px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        animation: textblink 1.1s ease-in-out infinite alternate;
    }
    .loading-sub {
        color: #334155;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        letter-spacing: 0.10em;
        margin-top: -10px;
    }
    @keyframes textblink {
        from { opacity: 0.45; }
        to   { opacity: 1; }
    }
    </style>
    <div class="loading-screen">
        <div class="spinner-ring"><div class="spinner-dot"></div></div>
        <div class="loading-label">Initializing Simulation…</div>
        <div class="loading-sub">Loading thermodynamic model</div>
    </div>
    """, unsafe_allow_html=True)

    # Hold for 1.4 seconds so the user sees the animation
    time.sleep(1.4)

    # Now navigate
    st.switch_page(target)
    st.stop()

# ------------------------------------------------
# LOAD BACKGROUND IMAGE
# ------------------------------------------------

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("assets/ThermoSim_background_image.png")

# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ============================================================ */
/* FORCE DARK MODE — override every Streamlit light-theme var   */
/* ============================================================ */

:root, html, body {{
    color-scheme: dark only !important;
    --background-color:           #080C14 !important;
    --secondary-background-color: #0D1321 !important;
    --text-color:                 #E2E8F0 !important;
    --font:                       'Inter', sans-serif !important;
}}

/* Kill any white/light surfaces Streamlit renders */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
.stApp,
.main, .block-container,
section[data-testid="stSidebar"] {{
    background-color: transparent !important;
    color: #E2E8F0 !important;
}}

/* Prevent white flash on any widget */
[data-baseweb], [data-baseweb="select"],
[data-baseweb="input"], [data-baseweb="textarea"],
.stTextInput > div, .stSelectbox > div,
.stSlider, .stNumberInput,
[role="listbox"], [role="option"],
.css-1d391kg, .css-12oz5g7 {{
    background-color: #0D1321 !important;
    color: #E2E8F0 !important;
    border-color: rgba(255,255,255,0.10) !important;
}}

/* Hide any theme-toggle Streamlit injects */
[data-testid="stDecoration"],
button[aria-label*="theme"],
button[aria-label*="Theme"],
[data-testid="baseButton-headerNoPadding"] {{
    display: none !important;
}}

/* ============================================================ */
/* GLOBAL                                                        */
/* ============================================================ */

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ============================================================ */
/* BACKGROUND — heavy overlay to suppress image noise           */
/*                                                              */
/* The bg image itself cannot be dimmed in CSS (it's data-URI). */
/* We stack TWO overlays:                                       */
/*   ::before  — very dark base  rgba(0,0,0,0.72)               */
/*   ::after   — centre vignette so cards pop                   */
/* Together this brings the bg renders into ~0.18-0.25 range.   */
/* ============================================================ */

.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    /* Also desaturate/dim the image itself via filter */
    isolation: isolate;
}}

/* Primary dark suppression layer */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(4, 8, 18, 0.78);
    z-index: 0;
    pointer-events: none;
}}

/* Vignette — edges darker, centre slightly lighter for focus */
.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(
        ellipse 70% 60% at 50% 45%,
        rgba(4, 8, 18, 0.0) 0%,
        rgba(4, 8, 18, 0.55) 100%
    );
    z-index: 0;
    pointer-events: none;
}}

/* Ensure main content renders above the overlay layers */
[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

/* ============================================================ */
/* REMOVE STREAMLIT CHROME                                      */
/* ============================================================ */

header    {{ visibility: hidden; }}
footer    {{ visibility: hidden; }}
#MainMenu {{ visibility: hidden; }}

/* ============================================================ */
/* MAIN CONTAINER                                               */
/* ============================================================ */

.block-container {{
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* ============================================================ */
/* TITLE                                                        */
/* ============================================================ */

.main-title {{
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.01em !important;
    margin-bottom: 6px;
    margin-top: 4px;
}}

.white-text {{ color: white; }}
.blue-text  {{ color: #3B82F6; margin-left: 3px; }}

/* ============================================================ */
/* SUBTITLE                                                     */
/* ============================================================ */

.subtitle {{
    text-align: center;
    font-size: 19px;
    color: #93C5FD !important;
    margin-bottom: 32px;
    font-weight: 600 !important;
}}

/* ============================================================ */
/* BUTTON                                                       */
/* ============================================================ */

div.stButton {{
    margin-top: 0px !important;
}}

div.stButton > button {{
    width: 230px !important;
    height: 50px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(160,180,210,0.18) !important;
    background: linear-gradient(
        180deg,
        rgba(52,64,86,0.94),
        rgba(24,32,46,0.98)
    ) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    letter-spacing: 0.2px !important;
    white-space: nowrap !important;
    transition: all 0.25s ease-in-out !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.03),
        0 6px 16px rgba(0,0,0,0.18) !important;
}}

div.stButton > button:hover {{
    border: 1px solid rgba(150, 200, 255, 0.6) !important;
    background: linear-gradient(
        180deg,
        rgba(86, 106, 143, 0.98),
        rgba(45, 61, 84, 0.99)
    ) !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.15),
        0 0 14px rgba(140, 195, 255, 0.22),
        0 8px 24px rgba(0, 0, 0, 0.3) !important;
}}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
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
# CYCLE DATA
# ------------------------------------------------

cycles = [
    {"name": "Carnot Cycle",        "desc": "Ideal reversible thermodynamic cycle",  "page": "pages/carnot_page.py"},
    {"name": "Otto Cycle",          "desc": "Petrol engine power cycle",              "page": "pages/otto_page.py"},
    {"name": "Diesel Cycle",        "desc": "Compression ignition engine cycle",      "page": "pages/diesel_page.py"},
    {"name": "Dual Cycle",          "desc": "Mixed combustion engine cycle",          "page": "pages/dual_page.py"},
    {"name": "Brayton Cycle",       "desc": "Gas turbine power cycle",                "page": "pages/brayton_page.py"},
    {"name": "Rankine Cycle",       "desc": "Steam turbine power plant cycle",        "page": "pages/rankine_page.py"},
    {"name": "Refrigeration Cycle", "desc": "Cooling and refrigeration cycle",        "page": "pages/refrigerator_page.py"},
]

# ------------------------------------------------
# GRID
# ------------------------------------------------

col1, col2 = st.columns(2, gap="medium")

for i, cycle in enumerate(cycles):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:

        st.markdown(f"""
            <div style="
                background: rgba(18, 24, 38, 0.65);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 18px 22px;
                margin-top: 10px;
                margin-bottom: 12px;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.2);
            ">
                <h3 style="color: white !important; font-size: 20px !important; font-weight: 600 !important; margin: 0 0 6px 0 !important;">{cycle['name']}</h3>
                <p style="color: #E2E8F0 !important; font-size: 14.5px !important; margin: 0 0 16px 0 !important; opacity: 0.85;">{cycle['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Button sets session state → triggers animation on next re-run
        if st.button("Launch Simulation →", key=cycle['name']):
            st.session_state.launch_target = cycle['page']
            st.session_state.launching = True
            st.rerun()