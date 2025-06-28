from fastapi import APIRouter
from wildfire_1.app.services.wfs_queries import *
from wildfire_1.app.services.wcs_queries import *
from wildfire_1.app.services.additional_queries import *
#from wildfire_1.app.services.wfs_queries import get_raster_data
from typing import List
from fastapi import Query

router = APIRouter()


#Active fire API section..
@router.get("/active-fires")
def api_active_fires(min_date: str, max_date: str = None):
    return get_active_fires(max_date=max_date, min_date=min_date)

@router.get("/active-fires-by-name")
def api_active_fire_by_name(name: str):
    return get_active_fire_by_name(fire_name=name)

@router.get("/active-fire-names")
def api_active_fire_names():
    return get_active_fire_names()


#fire danger API section
@router.get("/fire-danger")
def api_fire_danger(date: str):
    return get_fire_danger_by_date(date=date)


@router.get("/fire-danger-dates")
def api_fire_danger_dates():
    return get_fire_danger_dates()


#Fire history API section
@router.get("/fire-history-by-date")
def api_fire_history_by_date(max_date: str, min_date: str = None):
    return get_fire_history_by_date(max_date=max_date, min_date=min_date)

@router.get("/fire-history-by-cause")
def api_fire_history_by_cause(cause: str):
    return get_fire_history_by_cause(cause=cause)

@router.get("/fire-history-by-response")
def api_fire_history_by_response(response: str):
    return get_fire_history_by_response(response=response)

@router.get("/fire-history-by-hectares")
def api_fire_history_by_hectares(max_hectares: float, min_hectares: float = None):
    return get_fire_history_by_hectares(max_hectares=max_hectares, min_hectares=min_hectares)

#fire perimeter API section
@router.get("/fire-perimeter-by-date")
def api_fire_perimeter_by_date(start_date: str, end_date: str):
    return get_perimeter_by_date(start_date=start_date, end_date=end_date)

@router.get("/fire-perimeter-by-hotspot-count")
def api_fire_perimeter_by_hcount(min_hcount: int, max_hcount: int):
    return get_perimeter_by_hcount(min_hcount=min_hcount, max_hcount=max_hcount)

@router.get("/fire-perimeter-by-area")
def api_fire_perimeter_by_area(min_area: float):
    return get_perimeter_by_area(min_area=min_area)

@router.get("/fire-perimeter-hotspots-max")
def api_fire_perimeter_hotspots_max():
    return fire_perimeter_hotspots_max()

#fire forecast stations API section
@router.get("/fire-forecast-stations-date-list")
def api_fire_forecast_stations_date_list():
    return get_forecast_stations_by_date_list()

@router.get("/fire-forecast-stations-date")
def api_fire_forecast_stations_date(date: str):
    return get_forecast_stations_by_date(date=date)

@router.get("/fire-forecast-stations-agency")
def api_fire_forecast_stations_agency(agency: List[str] = Query(...)):
    return get_forecast_stations_by_agency(agency_list=agency)

@router.get("/fire-forecast-station-agencies")
def api_fire_forecast_stations_agency_list():
    return get_forecast_station_agencies()

#fire reporting weather stations API section
@router.get("/fire-reporting-weather-stations")
def api_fire_reporting_stations_date(date: str):
    return get_reporting_stations_by_date(date=date)

@router.get("/fire-reporting-weather-stations-forecast")
def api_fire_reporting_stations_forecast(date: str):
    return get_reporting_stations_forecast_by_date(date=date)

@router.get("/fire-reporting-weather-stations-dates")
def api_fire_reporting_stations_date_list():
    return get_reporting_stations_date_list()

@router.get("/fire-reporting-weather-stations-forecast-dates")
def api_fire_reporting_stations_forecast_date_list():
    return get_reporting_stations_forecast_date_list()

#WCS and Additional layer section
@router.get("/wcs-layer")
def api_wcs_layers(date: str, table_name: str):
    return wcs_query(date=date, table=table_name)

@router.get("/add-layer")
def api_add_layers(date: str, table_name: str):
    return additional_table_query(date=date, table=table_name)

#M3 Hotspot API Section
@router.get("/fire-m3hotspot-by-date")
def api_hotspots_by_date(date: str):
    return get_hotspot_by_date(date=date)

@router.get("/fire-m3hotspot-date-list")
def api_hotspot_date_list():
    return get_hotspot_date_list()

@router.get("/fire-m3hotspot-ecozone-list")
def api_hotspot_ecozone_list():
    return get_ecozone_list()

@router.get("/fire-m3hotspot-by-ecozone")
def api_hotspot_by_ecozone(ecozone: str):
    return get_hotspot_by_ecozone(ecozone=ecozone)

@router.get("/fire-hotspot-temp-max")
def api_hotspot_temp_max():
    return get_hotspot_temp_max()

@router.get("/fire-hotspot-by-temp")
def api_fire_hotspot_by_temp(min_temp: float, max_temp: float):
    return get_hotspot_by_temp(min=min_temp, max=max_temp)
