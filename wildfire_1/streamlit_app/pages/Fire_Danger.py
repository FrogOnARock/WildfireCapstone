from datetime import datetime
import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_fire_danger, get_fire_danger_dates
import streamlit.components.v1 as components
import tempfile
import os
from PIL import Image

st.set_page_config(layout="wide")
st.title("Fire Danger")

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
page_data = 'fire_data_fd'

for fd in fire_data_list:
    if fd in st.session_state and fd != page_data:
        del st.session_state[fd]

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Fire Danger"
])

# Query form logic
params = {}
if query_type == "Get Fire Danger":
    st.markdown("### Parameters for Fire Danger")
    date = [datetime.fromisoformat(f["acquisition_date"]).strftime("%Y-%m-%d")
    for f in get_fire_danger_dates()
        if "acquisition_date" in f
    ]
    params["date"] = st.selectbox("Select Date", options=date, key="fd_dates")

    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Fire Danger":
        data = get_fire_danger(str(params["date"]))
    else:
        data = []

    st.session_state.fire_data_fd = data

if st.button("Clear Results"):
    st.session_state.fire_data_fd = None

# Show results
data = st.session_state.get("fire_data_fd", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for row in data:

    if row.get("geometry"):

        geometry = json.loads(row["geometry"])
        properties = {
            "Grid Code": row["GRIDCODE"],
            "Acquisition Date": row["acquisition_date"]
        }

        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": properties
        })

geojson = {
    "type": "FeatureCollection",
    "features": features
}



config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [{
                        "id": "fire_danger_layer",
                        "type": "geojson",
                        "config": {
                            "dataId": "Fire Danger",  # must match your KeplerGl data key
                            "label": "Fire Danger Polygons",
                            "color": [255, 140, 0],
                            "highlightColor": [252, 242, 26, 255],
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.5,
                                "thickness": 1,
                                "strokeColor": [255, 255, 255]
                            }
                        }
                    }],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "Fire Danger": [
                            {"name": "Grid Code", "format": None},
                            {"name": "Acquisition Date", "format": None}
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

kepler_map = KeplerGl(data={"Fire Danger": geojson})
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)

