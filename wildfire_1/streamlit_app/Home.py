import streamlit as st
from PIL import Image
import os

# Set page config early
st.set_page_config(page_title="Wildfire Dashboard", layout="wide")

# Load logo
logo_path = os.path.join(os.getcwd(), "wildfire_1", "streamlit_app", "logo", "Maple_Leaf.svg.png")
logo = Image.open(logo_path)

st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white;
    }

    .stButton > button {
        background-color: #b30000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }

    div[data-testid="stLinkButton"] {
        background-color: #b30000 !important;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 1rem;
        display: inline-block;
        margin-top: 0.5rem;
    }

    div[data-testid="stLinkButton"]:hover {
        background-color: #e60000 !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        color: white;
    }

    footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ---------- Header ----------
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    st.image(logo, width=100)

with col2:
    st.markdown("<h1 style='text-align: center;'>Wildfire Dashboard</h1>", unsafe_allow_html=True)

with col3:
    st.markdown("")

# ---------- Sidebar Logo ----------
with st.sidebar:
    st.image(logo, width=100)
    st.markdown("🇨🇦 **Canadian Wildfire Data**")

# ---------- Intro ----------
st.markdown("Welcome to the **Canadian Wildfire Data Visualization Tool**. Select a page below to explore detailed maps and tables.")

# ---------- Main Grid ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🔥 Active Fires")
    st.write("View current wildfire incidents with spatial and tabular data.")
    st.page_link("pages/Active_Fires.py", label="Go to Active Fires")

with col2:
    st.header("🌡️ Fire Danger")
    st.write("Visualize fire danger levels based on official risk indices.")
    st.page_link("pages/Fire_Danger.py", label="Go to Fire Danger")

with col3:
    st.header("🗺️ Fire Perimeter")
    st.write("Explore current and historical fire perimeters.")
    st.page_link("pages/Fire_Perimeter.py", label="Go to Fire Perimeter")

st.markdown("---")

col4, col5, col6 = st.columns(3)

with col4:
    st.header("📡 Forecast Stations")
    st.write("Inspect meteorological forecasts from WMO fire stations.")
    st.page_link("pages/Forecast_Stations.py", label="Go to Forecast Stations")

with col5:
    st.header("📈 Reporting Stations")
    st.write("Review recently reported weather observations.")
    st.page_link("pages/Reporting_Weather_Stations.py", label="Go to Reporting Stations")

with col6:
    st.header("🔄 Reporting (Forecast)")
    st.write("See reported values for forecasted weather conditions.")
    st.page_link("pages/Reporting_Weather_Stations_(Forecast).py", label="Go to Reporting Forecast")

st.markdown("---")

col7 = st.columns(1)[0]
with col7:
    st.header("🌀 WCS Layers")
    st.write("Query and visualize raster layers like DSR, ISI, wind, and precipitation.")
    st.page_link("pages/WCS_Layers.py", label="Go to WCS Layers")