from datetime import datetime
import streamlit as st
import pandas as pd
import json
from datetime import date
from keplergl import KeplerGl
from wildfire_1.streamlit_app.api_client import get_perimeter_hcounts, get_perimeter_by_date, get_perimeter_by_hcount, get_perimeter_by_area
import streamlit.components.v1 as components
import tempfile


st.set_page_config(layout="wide")
st.title("Fire Perimeters")

# UI for choosing query
query_type = st.radio("Choose a query", [
    "Get Fire Perimeter by Date",
    "Get Fire Perimeter by Hotspot Count",
    "Get Fire Perimeter by Area"
])

# Query form logic
params = {}
if query_type == "Get Fire Perimeter by Date":
    st.markdown("### Parameters for Fire Perimeter by Date")
    params["start_date"] = st.date_input("Start Date", value=date(2024, 1, 1), key="fp_start")
    params["end_date"] = st.date_input("End Date", value=date.today(), key="fp_end")

elif query_type == "Get Fire Perimeter by Hotspot Count":
    st.markdown("### Parameters for Fire Perimeter by Hotspot Count")
    max_value = get_perimeter_hcounts()[0]['max']
    min_ha, max_ha = st.slider(
        "Select Hectare Range",
        min_value=0,
        max_value=max_value,
        value=(0, 50000),
        step=500
    )
    params['min_hotspot'] = min_ha
    params['max_hotspot'] = max_ha


elif query_type == "Get Fire Perimeter by Area":
    st.markdown("### Parameters for Fire Perimeter by Area")
    params['area'] = st.text_input("Minimum Area", value=0)


    # Buttons to run/clear
if st.button("Run Query"):
    if query_type == "Get Fire Perimeter by Date":
        data = get_perimeter_by_date(str(params["start_date"]), str(params["end_date"]))
    elif query_type == "Get Fire Perimeter by Hotspot Count":
        data = get_perimeter_by_hcount(params["min_hotspot"], params["max_hotspot"])
    elif query_type == "Get Fire Perimeter by Area":
        data = get_perimeter_by_area(params["area"])
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
for row in data:

    if row.get("geometry"):

        geometry = json.loads(row["geometry"])
        properties = {
            "Hotspot Count": row["hcount"],
            "Area": row["area"],
            "Start Date": row["firstdate"],
            "End Date": row["lastdate"],
            "Acquisition Date": row["acquisition_date"],
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
                    "id": "fire_perimeter_area_layer",
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
                        "Fire Perimeter": [
                            {"name": "Hotspot Count", "format": None},
                            {"name": "Area", "format": None},
                            {"name": "Start Date", "format": None},
                            {"name": "End Date", "format": None},
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

kepler_map = KeplerGl(data={"Fire Perimeter": geojson}, height=700)
kepler_map.config = config

with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmpfile:
    kepler_map.save_to_html(file_name=tmpfile.name)
    tmpfile.seek(0)
    html_content = tmpfile.read().decode("utf-8")


components.html(html_content, height=700, width=1800, scrolling=True)
