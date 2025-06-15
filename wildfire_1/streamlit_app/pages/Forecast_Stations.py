import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_forecast_station_agencies, get_forecast_stations_by_date, get_forecast_stations_by_agency
import streamlit.components.v1 as components
import tempfile


st.set_page_config(layout="wide")
st.title("Active Fires")

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Forecast Stations by Date",
    "Get Forecast Stations by Agency"
])

# Query form logic
params = {}
if query_type == "Get Forecast Stations by Date":
    st.markdown("### Parameters for Get Forecast Stations by Date")
    params["date"] = st.date_input("Date", value=date(2024, 1, 1), key="fs_date")

elif query_type == "Get Forecast Stations by Agency":
    st.markdown("### Parameters for Get Forecast Stations by Agency")

    agencies = [f["agency"] for f in get_forecast_station_agencies() if "agency" in f]
    selected = st.multiselect("Filter by Agency", agencies)
    params["agencies"] = selected


    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Forecast Stations by Date":
        data = get_forecast_stations_by_date(str(params["date"]))
    elif query_type == "Get Forecast Stations by Agency":
        data = get_forecast_stations_by_agency(params["agencies"])
    else:
        data = []

    st.session_state.fire_data = data

if st.button("Clear Results"):
    st.session_state.fire_data = None

# Show results
data = st.session_state.get("fire_data", None)
if not data:
    st.stop()


df = pd.DataFrame(data)

features = []
for _, row in df.iterrows():
    if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
        props = {
            "wmo": row.get("wmo"),
            "Name": row.get("name"),
            "Reporting Date": row.get("rep_date"),
            "Agency": row.get("agency"),
            "Upper Air Code": row.get("ua"),
            "Instrument": row.get("instr"),
            "Province": row.get("prov"),
            "Latitude": row.get("lat"),
            "Longitude": row.get("lon"),
            "Elevation": row.get("elev"),
            "Temperature": row.get("temp"),
            "Dew Point Temp.": row.get("td"),
            "Relative Humidity": row.get("rh"),
            "Wind Speed": row.get("ws"),
            "Wind Gust": row.get("wg"),
            "Wind Direction": row.get("wdir"),
            "Atmospheric Pressure": row.get("pres"),
            "Visibility": row.get("vis"),
            "Rainy Days": row.get("rndays"),
            "Precipitation": row.get("precip"),
            "Snow on Ground": row.get("sog"),
            "Fine Fuel Moisture Code": row.get("ffmc"),
            "Duff Moisture Code": row.get("dmc"),
            "Drought Code": row.get("dc"),
            "Buildup Index": row.get("bui"),
            "Initial Spread Index": row.get("isi"),
            "Fire Weather Index": row.get("fwi"),
            "Daily Severity Rating": row.get("dsr")
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
                        "Active Fires": [
                            {"name": "Name", "format": None},
                            {"name": "Reporting Date", "format": None},
                            {"name": "Agency", "format": None},
                            {"name": "Upper Air Code", "format": None},
                            {"name": "Instrument", "format": None},
                            {"name": "Province", "format": None},
                            {"name": "Latitude", "format": None},
                            {"name": "Longitude", "format": None},
                            {"name": "Elevation", "format": None},
                            {"name": "Temperature", "format": None},
                            {"name": "Dew Point Temp.", "format": None},
                            {"name": "Relative Humidity", "format": None},
                            {"name": "Wind Speed", "format": None},
                            {"name": "Wind Gust", "format": None},
                            {"name": "Wind Direction", "format": None},
                            {"name": "Atmospheric Pressure", "format": None},
                            {"name": "Visibility", "format": None},
                            {"name": "Rainy Days", "format": None},
                            {"name": "Precipitation", "format": None},
                            {"name": "Snow on Ground", "format": None},
                            {"name": "Fine Fuel Moisture Code", "format": None},
                            {"name": "Duff Moisture Code", "format": None},
                            {"name": "Drought Code", "format": None},
                            {"name": "Buildup Index", "format": None},
                            {"name": "Initial Spread Index", "format": None},
                            {"name": "Fire Weather Index", "format": None},
                            {"name": "Daily Severity Rating", "format": None}
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
kepler_map = KeplerGl(data={"Active Fires": geojson})
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)

st.markdown("---")
st.subheader("Station Observations")

# Group fields
station_metadata_cols = ["wmo", "Name", "Reporting Date", "Agency", "Upper Air Code", "Instrument", "Province", "Latitude", "Longitude", "Elevation"]
raw_weather_cols = ["wmo", "Name", "Reporting Date", "Agency", "Province", "Temperature", "Dew Point Temp.", "Relative Humidity", "Wind Speed", "Wind Gust", "Wind Direction", "Atmospheric Pressure", "Visibility", "Rainy Days", "Precipitation", "Snow on Ground"]
fire_index_cols = ["wmo", "Name", "Reporting Date", "Agency", "Province", "Fine Fuel Moisture Code", "Duff Moisture Code", "Drought Code", "Buildup Index", "Initial Spread Index", "Fire Weather Index", "Daily Severity Rating"]

# Clean and show each table
def display_table(title, columns):
    sub_df = df[columns].dropna(how="all")
    if not sub_df.empty:
        st.markdown(f"### {title}")
        st.dataframe(sub_df.reset_index(drop=True), use_container_width=True)

display_table("Station Metadata", station_metadata_cols)
display_table("Raw Weather Observations", raw_weather_cols)
display_table("Fire Weather Index Values", fire_index_cols)
