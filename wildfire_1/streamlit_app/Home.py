import streamlit as st
from streamlit_option_menu import option_menu

# Page selector sidebar
st.set_page_config(page_title='Wildfire Dashboard', layout='wide')

page = option_menu(
    "Wildfire Dashboard",
    ["Active Fires", "Fire Danger", "Fire History", "Fire Perimeter", "Forecast Weather Stations", "Reporting Weather Stations", "Reporting Forecast Weather Stations"],
    icons=["fire", "thermometer-half", "book", "map", "cloud", "cloud-download", "cloud-upload"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# Page routing logic
if page == "Active Fires":
    import pages.Active_Fires as af
    af.run()

elif page == "Fire Danger":
    import pages.fire_danger as fd
    fd.run()

elif page == "Fire History":
    import pages.fire_history as fh
    fh.run()

elif page == "Fire Perimeter":
    import pages.fire_perimeter as fp
    fp.run()

elif page == "Forecast Weather Stations":
    import pages.forecast_weather as fws
    fws.run()

elif page == "Reporting Weather Stations":
    import pages.reporting_weather as rws
    rws.run()

elif page == "Reporting Forecast Weather Stations":
    import pages.reporting_forecast_weather as rfws
    rfws.run()
