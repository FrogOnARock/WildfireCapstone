from datetime import datetime
import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_fire_history_by_date, get_fire_history_by_cause, get_fire_history_by_response, get_fire_history_by_hectares
import streamlit.components.v1 as components
import tempfile
import os
from PIL import Image

st.set_page_config(layout="wide")
st.title("Fire History")

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

# ---------- Sidebar Logo ----------
# Load logo
logo_path = os.path.join(os.getcwd(), "wildfire_1", "streamlit_app", "logo", "Maple_Leaf.svg.png")
logo = Image.open(logo_path)


with st.sidebar:
    st.image(logo, width=100)
    st.markdown("🇨🇦 **Canadian Wildfire Data**")

fire_data_list = ['fire_data_af', 'fire_data_fd', 'fire_data_h', 'fire_data_p', 'fire_data_fs', 'fire_data_rws', 'fire_data_rwsf', 'fire_data_wcs']
page_data = 'fire_data_h'

for fd in fire_data_list:
    if fd in st.session_state and fd != page_data:
        del st.session_state[fd]

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Fire History by Date",
    "Get Fire History by Cause",
    "Get Fire History by Response",
    "Get Fire History by Hectares"
])

# Query form logic
params = {}
if query_type == "Get Fire History by Date":
    st.markdown("### Parameters for Fire History by Date")
    params["min_date"] = st.date_input("Start Date", value=date(2024, 1, 1), key="fh_start")
    params["max_date"] = st.date_input("End Date", value=date.today(), key="fh_end")

elif query_type == "Get Fire History by Cause":
    st.markdown("### Parameters for Fire History by Cause")
    cause_list = ['Unknown', 'Human', 'Natural', 'Prescribed']
    params['fire_cause'] = st.selectbox("Select Cause", options=cause_list, key="fh_cause_id")


elif query_type == "Get Fire History by Response":
    st.markdown("### Parameters for Fire History by Response")
    response_list = ['None', 'NOR', 'MON', 'MOD', 'FUL']
    params['fire_response'] = st.selectbox("Select Response", options=response_list, key="fh_response_id")

elif query_type == "Get Fire History by Hectares":
    st.markdown("### Paramaters for Fire History by Hectares")
    params["min_hectares"] = float(st.text_input("Min Hectares", value=0, key="fh_minh"))
    params["max_hectares"] = float(st.text_input("Max Hectares", value=9999999, key="fh_maxh"))


    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Fire History by Date":
        data = get_fire_history_by_date(str(params["max_date"]), str(params["min_date"]))
    elif query_type == "Get Fire History by Cause":
        data = get_fire_history_by_cause(params["fire_cause"])
    elif query_type == "Get Fire History by Response":
        data = get_fire_history_by_response(params["fire_response"])
    elif query_type == "Get Fire History by Hectares":
        data = get_fire_history_by_hectares(params["max_hectares"], params["min_hectares"])
    else:
        data = []

    st.session_state.fire_data_h = data

if st.button("Clear Results"):
    st.session_state.fire_data_h = None

# Show results
data = st.session_state.get("fire_data_h", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for row in data:

    if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
        # Rename keys for tooltip display
        props = {
            "Fire Name": row.get("firename"),
            "Start Date": row.get("startdate"),
            "Hectares": row.get("hectares"),
            "Agency": row.get("agency"),
            "Stage of Control": row.get("stage_of_control"),
            "Response": row.get("response_type"),
            "Cause": row.get("cause"),
            "lat": row.get("lat"),
            "lon": row.get("lon")
        }

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["lon"], row["lat"]]
            },
            "properties": props
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "Fire History": [
                            {"name": "Fire Name", "format": None},
                            {"name": "Start Date", "format": None},
                            {"name": "Hectares", "format": None},
                            {"name": "Agency", "format": None},
                            {"name": "Stage of Control", "format": None},
                            {"name": "Response", "format": None},
                            {"name": "Cause", "format": None},
                            {"name": "lat", "format": None},
                            {"name": "lon", "format": None}
                        ]
                    },
                    "enabled": True
                },
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False}
            },
            "layerBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"currentTime": None, "speed": 1}
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 56.1304,
            "longitude": -106.3468,
            "pitch": 0,
            "zoom": 4,
            "isSplit": False
        },
        "mapStyle": {
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": False,
                "water": True,
                "land": True,
                "3d building": False
            },
            "threeDBuildingColor": [9.665468314072013, 17.18305478057247, 31.1442867897876],
            "mapStyles": {}
        }
    }
}

kepler_map = KeplerGl(data={"Fire History": geojson})
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)


st.markdown("---")
st.subheader("Fire Details")

if not df.empty:
    fire_options = df['firename'].dropna().unique().tolist()
    selected_fire = st.selectbox("Select a fire to view details", fire_options)

    fire_details = df[df['firename'] == selected_fire]

    if not fire_details.empty:
        st.write("### Fire Metadata")
        st.dataframe(fire_details.drop(columns=["id", "geometry", "lat", "lon"], errors="ignore").reset_index(drop=True))

st.markdown("---")
st.subheader("Complete Fire Details (Query Related)")

if not df.empty:

    fire_details_c = df.copy()

    st.dataframe(fire_details_c.drop(columns=["id", "geometry", "lat", "lon"], errors="ignore").reset_index(drop=True))
