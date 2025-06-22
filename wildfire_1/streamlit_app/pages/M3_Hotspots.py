from datetime import datetime
import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from api_client import get_hotspot_date_list, get_hotspot_by_date, get_hotspot_ecozone_list, get_hotspot_by_ecozone, get_hotspot_temp_max, get_hotspot_by_temp
import streamlit.components.v1 as components
import tempfile
import os
from PIL import Image

st.set_page_config(layout="wide")
st.title("Fire Perimeters")

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

fire_data_list = ['fire_data_af', 'fire_data_fd', 'fire_data_h', 'fire_data_p', 'fire_data_fs', \
                  'fire_data_rws', 'fire_data_rwsf', 'fire_data_wcs', 'fire_data_add', 'fire_data_m3']
page_data = 'fire_data_m3'

for fd in fire_data_list:
    if fd in st.session_state and fd != page_data:
        del st.session_state[fd]

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Hotspots by Date",
    "Get Hotspots by Ecozone",
    "Get Hotspots by Temperature",
])

# Query form logic
params = {}
if query_type == "Get Hotspots by Date":
    st.markdown("### Parameters for Hotspots by Date")

    rep_dates = [f["rep_date"] for f in get_hotspot_date_list() if "rep_date" in f]
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

elif query_type == "Get Hotspots by Temperature":
    st.markdown("### Parameters for Hotspot by Temperature")
    max_value = get_hotspot_temp_max()[0]['max']
    min_temp, max_temp = st.slider(
        "Select Hectare Range",
        min_value=0.0,
        max_value=max_value,
        value=(0, 25),
        step=0.1
    )
    params['min_temp'] = min_temp
    params['max_temp'] = max_temp


elif query_type == "Get Hotspots by Ecozone":
    st.markdown("### Parameters for Hotspots by Ecozone")
    ecozone_list = [f["ecozone"] for f in get_hotspot_ecozone_list() if "ecozone" in f]
    selected = st.multiselect("Filter by Ecozone", ecozone_list)
    params["ecozone"] = selected


    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Hotspots by Date":
        data = get_hotspot_by_date(str(params["date"]))
    elif query_type == "Get Hotspots by Temperature":
        data = get_hotspot_by_temp(params["min_temp"], params["max_temp"])
    elif query_type == "Get Hotspots by Ecozone":
        data = get_hotspot_by_ecozone(params["ecozone"])
    else:
        data = []

    st.session_state.fire_data_p = data

if st.button("Clear Results"):
    st.session_state.fire_data_p = None

# Show results
data = st.session_state.get("fire_data_p", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for _, row in df.iterrows():
    if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
        props = {col: row.get(col) for col in df.columns if col != "geometry"}
        props["Latitude"] = row["lat"]
        props["Longitude"] = row["lon"]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["lon"], row["lat"]],
            },
            "properties": props,
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

tooltip_fields = [{"name": col, "format": None} for col in df.columns if col != "geometry"]

config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "M3 Hotspots": [
                            {"name": "id", "format": None},
                            {"name": "rep_date", "format": None},
                            {"name": "source", "format": None},
                            {"name": "sensor", "format": None},
                            {"name": "satellite", "format": None},
                            {"name": "agency", "format": None},
                            {"name": "lat", "format": None},
                            {"name": "lon", "format": None},
                            {"name": "elev", "format": None},
                            {"name": "temp", "format": None},
                            {"name": "rh", "format": None},
                            {"name": "ws", "format": None},
                            {"name": "wd", "format": None},
                            {"name": "pcp", "format": None},
                            {"name": "ffmc", "format": None},
                            {"name": "dmc", "format": None},
                            {"name": "dc", "format": None},
                            {"name": "isi", "format": None},
                            {"name": "bui", "format": None},
                            {"name": "fwi", "format": None},
                            {"name": "fuel", "format": None},
                            {"name": "ros", "format": None},
                            {"name": "sfc", "format": None},
                            {"name": "tfc", "format": None},
                            {"name": "bfc", "format": None},
                            {"name": "hfi", "format": None},
                            {"name": "cfb", "format": None},
                            {"name": "age", "format": None},
                            {"name": "estarea", "format": None},
                            {"name": "polyid", "format": None},
                            {"name": "pcuring", "format": None},
                            {"name": "cfactor", "format": None},
                            {"name": "greenup", "format": None},
                            {"name": "tfc0", "format": None},
                            {"name": "sfc0", "format": None},
                            {"name": "ecozone", "format": None},
                            {"name": "sfl", "format": None},
                            {"name": "cfl", "format": None},
                            {"name": "estarea2", "format": None},
                            {"name": "frp", "format": None},
                            {"name": "times_burned", "format": None},
                            {"name": "estarea3", "format": None},
                            {"name": "pconif", "format": None},
                            {"name": "ecozona2", "format": None},
                            {"name": "cbh", "format": None}
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
kepler_map = KeplerGl(data={"M3 Hotspots": geojson})
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)

st.markdown("---")
st.subheader("Hotspot Observations")

rename_dict = {
    "lat": "Latitude",
    "lon": "Longitude",
    "rep_date": "Reporting Date",
    "temp": "Temperature",
    "rh": "Relative Humidity",
    "ws": "Wind Speed",
    "wd": "Wind Direction",
    "pcp": "Precipitation",
    "ffmc": "FFMC",
    "dmc": "DMC",
    "dc": "DC",
    "isi": "ISI",
    "bui": "BUI",
    "fwi": "FWI",
    "fuel": "Fuel",
    "ros": "ROS",
    "sfc": "SFC",
    "tfc": "TFC",
    "bfc": "BFC",
    "hfi": "HFI",
    "cfb": "CFB",
    "age": "Age",
    "estarea": "Est. Area",
    "polyid": "Polygon ID",
    "pcuring": "Percent Curing",
    "cfactor": "C Factor",
    "greenup": "Greenup",
    "elev": "Elevation",
    "tfc0": "TFC (0)",
    "sfc0": "SFC (0)",
    "ecozone": "Ecozone",
    "sfl": "SFL",
    "cfl": "CFL",
    "estarea2": "Est. Area 2",
    "frp": "FRP",
    "times_burned": "Times Burned",
    "estarea3": "Est. Area 3",
    "pconif": "P. Conif",
    "ecozona2": "Ecozone 2",
    "cbh": "CBH"
}


df.rename(columns=rename_dict, inplace=True)

meta_cols = ["Latitude", "Longitude", "Elevation", "Ecozone", "Ecozone 2", "Fuel", "FRP", "Times Burned"]
weather_cols = ["Temperature", "Relative Humidity", "Wind Speed", "Wind Direction", "Precipitation"]
fire_indices = ["FFMC", "DMC", "DC", "ISI", "BUI", "FWI", "CFB", "HFI"]
spread_metrics = ["SFC", "TFC", "BFC", "ROS", "TFC (0)", "SFC (0)"]
estimates = ["Est. Area", "Est. Area 2", "Est. Area 3", "Age", "C Factor", "Percent Curing", "Greenup"]
misc = ["P. Conif", "SFL", "CFL", "Polygon ID", "CBH", "Reporting Date"]

# Clean and show each table
def display_table(title, columns):
    sub_df = df[columns].dropna(how="all")
    if not sub_df.empty:
        st.markdown(f"### {title}")
        st.dataframe(sub_df.reset_index(drop=True), use_container_width=True)

display_table("Metadata", meta_cols)
display_table("Weather Conditions", weather_cols)
display_table("Fire Indices", fire_indices)
display_table("Spread & Intensity", spread_metrics)
display_table("Area Estimates & Age", estimates)
display_table("Other Attributes", misc)