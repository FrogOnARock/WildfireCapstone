import streamlit as st
import pandas as pd
import json
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from api_client import get_active_fires
from datetime import date

st.set_page_config(page_title='Wildfire Dashboard', layout='wide')
st.markdown("""
<style>
.keplergl-component {
    width: 100vw !important;
    margin-left: -3.5em;  /* adjust if needed to align */
}
</style>
""", unsafe_allow_html=True)

st.title('Active Fires Map (Kepler.gl Edition)')

# Date inputs
min_date = st.date_input("Select start date", value=date(2024, 1, 1))
max_date = st.date_input("Select end date", value=date.today())

# Load and clear buttons
if 'fire_data' not in st.session_state:
    st.session_state.fire_data = None

if st.button("Load Fires"):
    st.session_state.fire_data = get_active_fires(str(min_date), str(max_date))

if st.button("Clear Map"):
    st.session_state.fire_data = None

# Process and show map
fire_data = st.session_state.fire_data
if not fire_data:
    st.warning("No fires found for this date range or no date range picked.")
else:
    st.success(f"{len(fire_data)} fires loaded.")

    df = pd.DataFrame(fire_data)

    # Create a GeoJSON FeatureCollection
    features = []
    for _, row in df.iterrows():
        if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["lon"], row["lat"]]
                },
                "properties": row.to_dict()
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    kepler_map = KeplerGl(height=600, data={"Active Fires": geojson})
    # Force full-width rendering using a single column layout
    full_width_col = st.columns([1])[0]
    with full_width_col:
        keplergl_static(kepler_map, center_map=True)
























'''


st.set_page_config(page_title='Wildfire Dashboard', layout='wide')

st.title('Active Fires Map')

# Date input
min_date = st.date_input("Select start date", value=date(2024, 1, 1))
max_date = st.date_input("Select end date (optional)", value=date.today())

if 'fire_data' not in st.session_state:
    st.session_state.fire_data = None


if st.button("Load Fires"):
    st.session_state.fire_data = get_active_fires(str(min_date), str(max_date))

if st.button("Clear Map"):
    st.session_state.fire_data = None


def style_function(feature):
    return {
        "fillColor": "#ff0000",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.7,
        "radius": 6  # this is relevant only for points when using custom renderers
    }




# Only render map if fire data exists
data = st.session_state.fire_data
if not data:
    st.warning("No fires found for this date range or no date range picked.")
else:
    st.success(f"{len(data)} fires loaded.")



    m = folium.Map(location=[56, -106], zoom_start=4)

    for fire in data:
        geometry = fire.get("geometry")

        if geometry:
            try:
                geojson_geom = json.loads(geometry) if isinstance(geometry, str) else geometry

                coords = geojson_geom.get("coordinates", None)
                if not coords:
                    continue  # skip if no coordinates

                # Add CircleMarker for styled point
                folium.CircleMarker(
                    location=[coords[1], coords[0]],
                    radius=6,
                    color="blue",
                    fill=True,
                    fill_opacity=0.1
                ).add_to(m)

                # Add GeoJson for click interactivity
                feature = {
                    "type": "Feature",
                    "geometry": geojson_geom,
                    "properties": fire
                }

                folium.GeoJson(
                    data=feature,
                    name="interactive-point"
                ).add_to(m)

            except Exception as e:
                st.error(f"Invalid geometry: {e}")
                continue  # skip invalid record

    map_data = st_folium(m, width=1750, height=600)

    if "last_active_drawing" in map_data and map_data["last_active_drawing"]:
        props = map_data["last_active_drawing"]["properties"] #properties of the last active drawing assigned to props
        st.subheader("Fire Info")
        st.table(props) #create a table of those properties

  clicked_coords = map_data.get("last_clicked")
    if clicked_coords:
        st.subheader("Fire info at clicked location:")
        lat_clicked = clicked_coords["lat"]
        lon_clicked = clicked_coords["lng"]

        # Find the closest fire (you could use a distance threshold here too)
        closest_fire = min(
            data,
            key=lambda fire: (fire["lat"] - lat_clicked) ** 2 + (fire["lon"] - lon_clicked) ** 2
        )

        # Display as table
        st.table(closest_fire)



   # Optional: visualize full geometry if present and valid GeoJSON
        geom = fire.get("geometry")
        if geom:
            try:
                geojson_geom = json.loads(geom)
                folium.GeoJson(
                    geojson_geom,
                    name="Fire Shape"
                ).add_to(m)
            except Exception as e:
                st.error(f"Failed to parse geometry: {e}")

    folium.LayerControl().add_to(m)
    '''