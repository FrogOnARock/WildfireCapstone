import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from api_client import get_wcs_layer
import streamlit.components.v1 as components
import tempfile
from datetime import datetime
from session import SessionLocal
from sqlalchemy.sql import text
import os
from PIL import Image


WCS_LAYERS = {
    "Daily Severity Rating": "daily_severity_rating",
    "Drought Code": "drought_code",
    "Wind Speed": "wind_speed",
    "Wind Direction": "wind_direction",
    "Fire Type": "fire_type",
    "Initial Spread Index": "initial_spread_index",
    "Precipitation": "precipitation"
}

def wcs_query_dates(table:str):

    table = WCS_LAYERS[table]

    # Validate table name
    if table not in WCS_LAYERS.values():
        raise ValueError(f"Invalid table name: {table}")


    query = f"""
        SELECT DISTINCT(acquisition_date)
        FROM {table}
        ORDER BY acquisition_date DESC
    """

    with SessionLocal() as session:
        result = session.execute(text(query))
        return result.mappings().all()

st.set_page_config(layout="wide")
st.title("WCS Layers")

st.markdown("""
    <style>
    /* Default (Light mode) */
    .stApp {
        color: black;
    }

    h1, h2, h3, h4, h5, h6 {
        color: black;
    }

    .stButton > button, div[data-testid="stLinkButton"] {
        background-color: #b30000 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        text-align: center;
        font-size: 1rem;
        display: inline-block;
        margin-top: 0.5rem;
    }

    div[data-testid="stLinkButton"]:hover {
        background-color: #e60000 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #f5f5f5;
        color: black;
    }

    footer, header {visibility: hidden;}

    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #121212;
            color: white;
        }

        h1, h2, h3, h4, h5, h6 {
            color: white;
        }

        .stButton > button, div[data-testid="stLinkButton"] {
            background-color: #b30000 !important;
            color: white !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #1e1e1e;
            color: white;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar Logo ----------
# Load logo
logo_path = os.path.join(os.getcwd(), "wildfire_1", "streamlit_app", "logo", "Maple_Leaf.svg.png")
logo = Image.open(logo_path)


with st.sidebar:
    st.image(logo, width=100)
    st.markdown("**Canadian Wildfire Data**")

#section to clear session data if moving between layer types
fire_data_list = ['fire_data_af', 'fire_data_fd', 'fire_data_h', 'fire_data_p', 'fire_data_fs', \
                  'fire_data_rws', 'fire_data_rwsf', 'fire_data_wcs', 'fire_data_add', 'fire_data_m3']
page_data = 'fire_data_wcs'

for fd in fire_data_list:
    if fd in st.session_state and fd != page_data:
        del st.session_state[fd]


# UI for choosing query
layer_choice = st.selectbox("Choose a WCS Layer", list(WCS_LAYERS.keys()))

# Query form logic
params = {}
params["wcs_layer"] = WCS_LAYERS[layer_choice]


acquisition_dates = [
    f["acquisition_date"] for f in wcs_query_dates(layer_choice)
    if f.get("acquisition_date")
]

if acquisition_dates == []:
    acquisition_dates = [wcs_query_dates(layer_choice)]

acquisition_dates = [
    f.isoformat()
    for f in acquisition_dates
]

# Create a mapping from date (YYYY-MM-DD) to full timestamp
date_map = {
    d[:10]: d for d in acquisition_dates  # assumes format is always ISO
}

# Sorted list of just the date parts for the UI
date_display_list = sorted(date_map.keys())

# User selects just a clean date
selected_date = st.selectbox("Select Acquisition Date", options=date_display_list)

# Convert back to full ISO timestamp
params["date"] = date_map[selected_date]

    # Buttons to run/clear
if st.button("Run Query"):
    data = get_wcs_layer(str(params["date"]), str(params["wcs_layer"]))
    st.session_state.fire_data_wcs = data

if st.button("Clear Results"):
    st.session_state.fire_data_wcs = None

# Show results
data = st.session_state.get("fire_data_wcs", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for row in data:

    if row.get("geometry"):

        if layer_choice == "Daily Severity Rating":
            value = round(row["value"], 1)
        else:
            value = row["value"]


        geometry = json.loads(row["geometry"])
        properties = {
            "Value": value,
            "Longitude": row["lon"],
            "Latitude": row["lat"],
            "Acquisition Date": row["acquisition_date"]
        }

        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": properties
        })

#collect the data in the format of geojson
geojson = {
    "type": "FeatureCollection",
    "features": features
}


#set the config for this map
config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [{
                    "id": "WCS Layer",
                    "type": "geojson",
                    "config": {
                        "dataId": "Area",  # This must match your KeplerGl data key
                        "label": "Fire Perimeter Area Polygon",
                        "color": [140, 255, 0],
                        "highlightColor": [252, 242, 26, 255],
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.5,
                            "thickness": 1,
                            "strokeColor": [255, 255, 255]
                        }
                    }
                }
            ],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "WCS Layer": [
                            {"name": "Value", "format": None},
                            {"name": "Latitude", "format": None},
                            {"name": "Longitude", "format": None},
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
#create the kepler map
kepler_map = KeplerGl(data={"WCS Layer": geojson})
kepler_map.config = config

#render the map
with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)
