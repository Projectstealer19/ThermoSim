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

/* ------------------------------------------------ */
/* GLOBAL */
/* ------------------------------------------------ */

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ------------------------------------------------ */
/* BACKGROUND */
/* ------------------------------------------------ */

.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.42);
    z-index: -1;
}}

/* ------------------------------------------------ */
/* REMOVE STREAMLIT DEFAULTS */
/* ------------------------------------------------ */

header {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

#MainMenu {{
    visibility: hidden;
}}

/* ------------------------------------------------ */
/* MAIN CONTAINER */
/* ------------------------------------------------ */

.block-container {{
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* ------------------------------------------------ */
/* TITLE */
/* ------------------------------------------------ */

.main-title {{
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -0.01em !important;
    margin-bottom: 6px;
    margin-top: 4px;
}}

.white-text {{
    color: white;
}}

.blue-text {{
    color: #3B82F6;
    margin-left: 3px;
}}

/* ------------------------------------------------ */
/* SUBTITLE */
/* ------------------------------------------------ */

.subtitle {{
    text-align: center;
    font-size: 19px;
    color: #93C5FD !important;
    margin-bottom: 32px;
    font-weight: 600 !important;
}}

/* ------------------------------------------------ */
/* BUTTON (ORIGINAL SIZES PRESERVED PERFECTLY) */
/* ------------------------------------------------ */

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

/* ------------------------------------------------ */
/* BUTTON HOVER (HIGH SHINE METALLIC EFFECT) */
/* ------------------------------------------------ */

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
    {
        "name": "Carnot Cycle",
        "desc": "Ideal reversible thermodynamic cycle"
    },
    {
        "name": "Otto Cycle",
        "desc": "Petrol engine power cycle"
    },
    {
        "name": "Diesel Cycle",
        "desc": "Compression ignition engine cycle"
    },
    {
        "name": "Dual Cycle",
        "desc": "Mixed combustion engine cycle"
    },
    {
        "name": "Brayton Cycle",
        "desc": "Gas turbine power cycle"
    },
    {
        "name": "Rankine Cycle",
        "desc": "Steam turbine power plant cycle"
    },
    {
        "name": "Refrigeration Cycle",
        "desc": "Cooling and refrigeration cycle"
    }
]

# ------------------------------------------------
# GRID (CUSTOM TARGETS FOR CLEAN SHRUNK CARD HEIGHTS)
# ------------------------------------------------

col1, col2 = st.columns(2, gap="medium")

for i, cycle in enumerate(cycles):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        
        # Pure HTML block completely strips Streamlit's forced vertical stretching layout
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
        
        # Placed perfectly right under the compact text container box
        if st.button(
            "Launch Simulation →",
            key=cycle['name']
        ):
            if cycle['name'] == "Carnot Cycle":
                st.switch_page("pages/carnot_page.py")
            elif cycle['name'] == "Otto Cycle":
                st.switch_page("pages/otto_page.py")
            elif cycle['name'] == "Diesel Cycle":
                st.switch_page("pages/diesel_page.py")
            elif cycle['name'] == "Dual Cycle":
                st.switch_page("pages/dual_page.py")
            elif cycle['name'] == "Brayton Cycle":
                st.switch_page("pages/brayton_page.py")
            elif cycle['name'] == "Rankine Cycle":
                st.switch_page("pages/rankine_page.py")
            elif cycle['name'] == "Refrigeration Cycle":
                st.switch_page("pages/refrigerator_page.py")