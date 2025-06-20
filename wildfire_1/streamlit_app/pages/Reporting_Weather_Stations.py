import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_reporting_weather_stations_dates, get_reporting_weather_stations_by_date
import streamlit.components.v1 as components
import tempfile
from datetime import datetime
import os
from PIL import Image


st.set_page_config(layout="wide")
st.title("Reporting Weather Stations")

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

fire_data_list = ['fire_data_af', 'fire_data_fd', 'fire_data_h', 'fire_data_p', 'fire_data_fs', \
                  'fire_data_rws', 'fire_data_rwsf', 'fire_data_wcs', 'fire_data_add']
page_data = 'fire_data_rws'

for fd in fire_data_list:
    if fd in st.session_state and fd != page_data:
        del st.session_state[fd]

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Reporting Weather Stations by Date"
])

# Query form logic
params = {}
if query_type == "Get Reporting Weather Stations by Date":
    st.markdown("### Parameters for Get Reporting Weather Stations by Date")
    rep_dates = [f["rep_date"] for f in get_reporting_weather_stations_dates() if "rep_date" in f]
    # Create a mapping from date (YYYY-MM-DD) to full timestamp
    date_map = {
        d[:10]: d for d in rep_dates  # assumes format is always ISO
    }

    # Sorted list of just the date parts for the UI
    date_display_list = sorted(date_map.keys())

    # User selects just a clean date
    selected_date = st.selectbox("Select Reporting Date", options=date_display_list)

    # Convert back to full ISO timestamp
    params["date"] = date_map[selected_date]

    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Reporting Weather Stations by Date":
        data = get_reporting_weather_stations_by_date(str(params["date"]))
    else:
        data = []

    st.session_state.fire_data_rws = data

if st.button("Clear Results"):
    st.session_state.fire_data_rws = None

# Show results
data = st.session_state.get("fire_data_rws", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for _, row in df.iterrows():
    if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude")):
        props = {
            "wmo": row.get("wmo"),
            "Name": row.get("name"),
            "Reporting Date": row.get("rep_date"),
            "Latitude": row.get("latitude"),
            "Longitude": row.get("longitude"),
            "Elevation": row.get("elevation"),
            "Temperature": row.get("temp"),
            "Relative Humidity": row.get("rh"),
            "Wind Speed": row.get("ws"),
            "Wind Direction": row.get("wdir"),
            "Precipitation": row.get("precip"),
            "Snow on Ground": row.get("sog"),
            "Fine Fuel Moisture Code": row.get("ffmc"),
            "Duff Moisture Code": row.get("dmc"),
            "Drought Code": row.get("dc"),
            "Initial Spread Index": row.get("isi"),
            "Buildup Index": row.get("bui"),
            "Fire Weather Index": row.get("fwi"),
            "Daily Severity Rating": row.get("dsr"),
            "X": row.get("x"),
            "Y": row.get("y"),
            "WX": row.get("wx"),
            "WY": row.get("wy"),
            "Timezone": row.get("timezone")
        }

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]]
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
                        "Reporting Weather Stations": [
                            {"name": "wmo", "format": None},
                            {"name": "Name", "format": None},
                            {"name": "Reporting Date", "format": None},
                            {"name": "Latitude", "format": None},
                            {"name": "Longitude", "format": None},
                            {"name": "Elevation", "format": None},
                            {"name": "Temperature", "format": None},
                            {"name": "Relative Humidity", "format": None},
                            {"name": "Wind Speed", "format": None},
                            {"name": "Wind Direction", "format": None},
                            {"name": "Precipitation", "format": None},
                            {"name": "Snow on Ground", "format": None},
                            {"name": "Fine Fuel Moisture Code", "format": None},
                            {"name": "Duff Moisture Code", "format": None},
                            {"name": "Drought Code", "format": None},
                            {"name": "Initial Spread Index", "format": None},
                            {"name": "Buildup Index", "format": None},
                            {"name": "Fire Weather Index", "format": None},
                            {"name": "Daily Severity Rating", "format": None},
                            {"name": "X", "format": None},
                            {"name": "Y", "format": None},
                            {"name": "WX", "format": None},
                            {"name": "WY", "format": None},
                            {"name": "Timezone", "format": None}
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
kepler_map = KeplerGl(data={"Reporting Weather Stations": geojson})
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)

st.markdown("---")
st.subheader("Reporting Weather Station Observations")

rename_dict = {
    "wmo": "WMO",
    "name": "Name",
    "rep_date": "Reporting Date",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "elevation": "Elevation",
    "temp": "Temperature",
    "rh": "Relative Humidity",
    "ws": "Wind Speed",
    "wdir": "Wind Direction",
    "precip": "Precipitation",
    "sog": "Snow on Ground",
    "ffmc": "Fine Fuel Moisture Code",
    "dmc": "Duff Moisture Code",
    "dc": "Drought Code",
    "isi": "Initial Spread Index",
    "bui": "Buildup Index",
    "fwi": "Fire Weather Index",
    "dsr": "Daily Severity Rating",
    "x": "X",
    "y": "Y",
    "wx": "WX",
    "wy": "WY",
    "timezone": "Timezone"
}

df.rename(columns=rename_dict, inplace=True)

# Define categories
station_metadata_cols = ["WMO", "Name", "Reporting Date", "Latitude", "Longitude", "Elevation", "X", "Y", "WX", "WY", "Timezone"]
raw_weather_cols = ["WMO", "Name", "Reporting Date", "Temperature", "Relative Humidity", "Wind Speed", "Wind Direction", "Precipitation", "Snow on Ground"]
fire_index_cols = ["WMO", "Name", "Reporting Date", "Fine Fuel Moisture Code", "Duff Moisture Code", "Drought Code", "Initial Spread Index", "Buildup Index", "Fire Weather Index", "Daily Severity Rating"]

# Render grouped tables
def display_table(title, columns):
    sub_df = df[columns].dropna(how="all")
    if not sub_df.empty:
        st.markdown(f"### {title}")
        st.dataframe(sub_df.reset_index(drop=True), use_container_width=True)

display_table("Station Metadata", station_metadata_cols)
display_table("Raw Weather Observations", raw_weather_cols)
display_table("Fire Weather Index Values", fire_index_cols)
