import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_active_fires, get_active_fires_by_name, get_active_fire_firenames
import streamlit.components.v1 as components
import tempfile


st.set_page_config(layout="wide")
st.title("Active Fires")

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Active Fires",
    "Get Active Fire by Name"
])

# Query form logic
params = {}
if query_type == "Get Active Fires":
    st.markdown("### Parameters for Get Active Fires")
    params["min_date"] = st.date_input("Start Date", value=date(2024, 1, 1), key="af_start")
    params["max_date"] = st.date_input("End Date", value=date.today(), key="af_end")


elif query_type == "Get Active Fire by Name":

    st.markdown("### Parameters for Get Active Fire by Name")
    fire_id_list = [f["firename"] for f in get_active_fire_firenames() if "firename" in f]
    params["fire_id"] = st.selectbox("Select Fire ID", options=fire_id_list, key="af_id")

    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Active Fires":
        data = get_active_fires(str(params["min_date"]), str(params["max_date"]))
    elif query_type == "Get Active Fire by Name":
        data = get_active_fires_by_name(params["fire_id"])
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
        # Rename keys for tooltip display
        props = {
            "Fire Name": row.get("firename"),
            "Start Date": row.get("startdate"),
            "Hectares": row.get("hectares"),
            "Agency": row.get("agency"),
            "Stage of Control": row.get("stage_of_control"),
            "Response": row.get("response_type"),
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
                        "Active Fires": [
                            {"name": "Fire Name", "format": None},
                            {"name": "Start Date", "format": None},
                            {"name": "Hectares", "format": None},
                            {"name": "Agency", "format": None},
                            {"name": "Stage of Control", "format": None},
                            {"name": "Response", "format": None},
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
kepler_map = KeplerGl(data={"Active Fires": geojson})
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
        st.dataframe(fire_details.drop(columns=["geometry", "lat", "lon"], errors="ignore").reset_index(drop=True))


