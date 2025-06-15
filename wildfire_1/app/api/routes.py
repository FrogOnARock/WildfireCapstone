from fastapi import APIRouter
from wildfire_1.app.services.wfs_queries import *
from wildfire_1.app.services.wcs_queries import *
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

@router.get("/fire-danger")
def api_fire_danger(date: str):
    return get_fire_danger_by_date(date=date)


@router.get("/fire-danger-dates")
def api_fire_danger_dates():
    return get_fire_danger_dates()

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

@router.get("/wcs-layer")
def api_wcs_layers(date: str, table_name: str):
    return wcs_query(date=date, table=table_name)
