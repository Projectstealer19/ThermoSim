import streamlit as st
import base64

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
# CUSTOM CSS
# ------------------------------------------------

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ============================================================ */
/* FORCE DARK MODE                                              */
/* ============================================================ */

:root, html, body {{
    color-scheme: dark only !important;
    --background-color:           #080C14 !important;
    --secondary-background-color: #0D1321 !important;
    --text-color:                 #E2E8F0 !important;
    --font:                       'Inter', sans-serif !important;
}}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
.stApp, .main, .block-container,
section[data-testid="stSidebar"] {{
    background-color: transparent !important;
    color: #E2E8F0 !important;
}}

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

[data-testid="stDecoration"],
button[aria-label*="theme"],
button[aria-label*="Theme"],
[data-testid="baseButton-headerNoPadding"] {{
    display: none !important;
}}

/* ============================================================ */
/* GLOBAL                                                       */
/* ============================================================ */

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ============================================================ */
/* BACKGROUND                                                   */
/* ============================================================ */

.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.50);
    z-index: 0;
    pointer-events: none;
}}

.stApp::after {{
    content: "";
    position: fixed;
    inset: 0;
    background: radial-gradient(
        ellipse 75% 65% at 50% 48%,
        rgba(0,0,0,0.0) 0%,
        rgba(0,0,0,0.30) 100%
    );
    z-index: 0;
    pointer-events: none;
}}

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
/* BUTTON — base style (idle state)                             */
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
    position: relative !important;
    overflow: hidden !important;
}}

div.stButton > button:hover {{
    border: 1px solid rgba(150,200,255,0.6) !important;
    background: linear-gradient(
        180deg,
        rgba(86,106,143,0.98),
        rgba(45,61,84,0.99)
    ) !important;
    color: white !important;
    transform: translateY(-1px) !important;
    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.15),
        0 0 14px rgba(140,195,255,0.22),
        0 8px 24px rgba(0,0,0,0.3) !important;
}}

/* ---- LAUNCHING state — applied by JS on click ---- */

div.stButton > button.btn-launching {{
    border: 1px solid rgba(99,162,255,0.70) !important;
    background: linear-gradient(
        180deg,
        rgba(55,80,124,0.98),
        rgba(24,38,64,0.99)
    ) !important;
    color: rgba(255,255,255,0.0) !important;   /* hide text — spinner takes over */
    box-shadow:
        0 0 0 3px rgba(59,130,246,0.15),
        0 0 18px rgba(59,130,246,0.30),
        0 6px 20px rgba(0,0,0,0.30) !important;
    transform: translateY(-1px) !important;
    pointer-events: none !important;
    cursor: default !important;
}}

/* tiny spinner rendered as ::after pseudo on the button */
div.stButton > button.btn-launching::after {{
    content: "";
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    width: 16px !important;
    height: 16px !important;
    margin-top: -8px !important;
    margin-left: -8px !important;
    border: 2px solid rgba(147,197,253,0.25) !important;
    border-top-color: #93C5FD !important;
    border-radius: 50% !important;
    animation: btn-spin 0.55s linear infinite !important;
    box-shadow: 0 0 6px rgba(147,197,253,0.4) !important;
}}

@keyframes btn-spin {{
    to {{ transform: rotate(360deg); }}
}}

/* page-level fade-out on navigate */
.page-fade-out {{
    animation: pageFade 0.35s ease forwards !important;
}}

@keyframes pageFade {{
    to {{ opacity: 0; }}
}}

</style>

<script>
(function() {{
    function hookButtons() {{
        var btns = document.querySelectorAll('div.stButton > button');
        btns.forEach(function(btn) {{
            if (btn.dataset.launchHooked) return;
            btn.dataset.launchHooked = '1';
            btn.addEventListener('click', function() {{
                // Apply launching style instantly
                btn.classList.add('btn-launching');
                // Fade the whole main content area out
                var main = document.querySelector('[data-testid="stAppViewContainer"] > .main');
                if (main) {{
                    main.style.transition = 'opacity 0.35s ease';
                    main.style.opacity = '0';
                }}
                // Streamlit will navigate server-side; the fade covers the brief delay
            }});
        }});
    }}
    // Re-hook after every Streamlit re-render
    var obs = new MutationObserver(hookButtons);
    obs.observe(document.body, {{ childList: true, subtree: true }});
    hookButtons();
}})();
</script>
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
    {"name": "Carnot Cycle",        "icon": "❄",  "desc": "Ideal reversible thermodynamic cycle",  "page": "pages/carnot_page.py"},
    {"name": "Otto Cycle",          "icon": "🚗", "desc": "Petrol engine power cycle",              "page": "pages/otto_page.py"},
    {"name": "Diesel Cycle",        "icon": "⚙",  "desc": "Compression ignition engine cycle",      "page": "pages/diesel_page.py"},
    {"name": "Dual Cycle",          "icon": "🔩", "desc": "Mixed combustion engine cycle",          "page": "pages/dual_page.py"},
    {"name": "Brayton Cycle",       "icon": "🔥", "desc": "Gas turbine power cycle",                "page": "pages/brayton_page.py"},
    {"name": "Rankine Cycle",       "icon": "♨",  "desc": "Steam turbine power plant cycle",        "page": "pages/rankine_page.py"},
    {"name": "Refrigeration Cycle", "icon": "❄",  "desc": "Cooling and refrigeration cycle",        "page": "pages/refrigerator_page.py"},
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
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 18px 22px;
                margin-top: 10px;
                margin-bottom: 12px;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.2);
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            ">
                <h3 style="color: white !important; font-size: 20px !important; font-weight: 600 !important; margin: 0 0 6px 0 !important;">
                    {cycle['icon']}&nbsp; {cycle['name']}
                </h3>
                <p style="color: #E2E8F0 !important; font-size: 14.5px !important; margin: 0 0 16px 0 !important; opacity: 0.85;">
                    {cycle['desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Direct navigation — no sleep, no session state detour
        if st.button("Launch Simulation →", key=cycle['name']):
            st.switch_page(cycle['page'])