import requests
from altair import param

API_URL = 'https://wildfire-api-848755338708.us-east1.run.app/api'

#these are the functions to call the relevant APIs

"""
Get active fires function
Params: min_date, max_date
Returns: list of active fires
"""
def get_active_fires(min_date: str, max_date: str = None):
    params = {
        'min_date': min_date,
    }
    if max_date:
        params['max_date'] = max_date

    response = requests.get(f'{API_URL}/active-fires', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get active fire by name function
Params: Name
Returns: Active fire data by name
"""

def get_active_fires_by_name(name: str):
    params = {
        'name': name
    }
    response = requests.get(f'{API_URL}/active-fires-by-name', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get active fire names function
Returns: List of active fire names
"""
def get_active_fire_firenames():
    response = requests.get(f'{API_URL}/active-fire-names')
    return response.json() if response.status_code == 200 else []

"""
Get fire danger function
Params: date
Returns: Fire danger data for given date
"""
def get_fire_danger(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-danger', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire danger dates function
Returns: List of dates with fire danger data
"""
def get_fire_danger_dates():
    response = requests.get(f'{API_URL}/fire-danger-dates')
    return response.json() if response.status_code == 200 else []

"""
Get fire history by date function
Params: min_date, max_date
Returns: List of fire history records within date range
"""
def get_fire_history_by_date(max_date: str, min_date: str):
    params = {
        'min_date': min_date
    }
    if max_date:
        params['max_date'] = max_date
    response = requests.get(f'{API_URL}/fire-history-by-date', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire history by cause function
Params: cause
Returns: List of fire history records by cause
"""
def get_fire_history_by_cause(cause: str):
    params = {
        'cause': cause
    }
    response = requests.get(f'{API_URL}/fire-history-by-cause', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire history by response function
Params: response
Returns: List of fire history records by response category
"""
def get_fire_history_by_response(response: str):
    params = {
        'response': response
    }
    response = requests.get(f'{API_URL}/fire-history-by-response', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire history by hectares function
Params: max_hectares, min_hectares
Returns: List of fires by size in hectares
"""
def get_fire_history_by_hectares(max_hectares: float, min_hectares: float):
    params = {
        'max_hectares': max_hectares,
        'min_hectares': min_hectares
    }
    response = requests.get(f'{API_URL}/fire-history-by-hectares', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire perimeter by date function
Params: start_date, end_date
Returns: Fire perimeter records within date range
"""
def get_perimeter_by_date(start_date: str, end_date: str):
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-date', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire perimeter by hotspot count function
Params: min_hcount, max_hcount
Returns: Perimeters with hotspot counts in range
"""
def get_perimeter_by_hcount(min_hcount: int, max_hcount: int):
    params = {
        'min_hcount': min_hcount,
        'max_hcount': max_hcount
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-hotspot-count', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get fire perimeter by area function
Params: min_area
Returns: Perimeter records with area greater than min_area
"""
def get_perimeter_by_area(min_area: float):
    params = {
        'min_area': min_area
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-area', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get perimeter hotspot max counts function
Returns: List of maximum hotspot counts per fire perimeter
"""
def get_perimeter_hcounts():
    response = requests.get(f'{API_URL}/fire-perimeter-hotspots-max')
    return response.json() if response.status_code == 200 else []

"""
Get forecast station dates function
Returns: List of available forecast station dates
"""
def get_forecast_station_dates():
    response = requests.get(f'{API_URL}/fire-forecast-stations-date-list')
    return response.json() if response.status_code == 200 else []

"""
Get forecast stations by date function
Params: date
Returns: Forecast stations and related data reporting on that date
"""
def get_forecast_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-forecast-stations-date', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get forecast stations by agency function
Params: agency (list)
Returns: Forecast stations and related data by agency name
"""
def get_forecast_stations_by_agency(agency: list):
    params = [('agency', a) for a in agency]
    response = requests.get(f'{API_URL}/fire-forecast-stations-agency', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get forecast station agencies function
Returns: List of forecast station agencies
"""
def get_forecast_station_agencies():
    response = requests.get(f'{API_URL}/fire-forecast-station-agencies')
    return response.json() if response.status_code == 200 else []

"""
Get reporting weather stations by date function
Params: date
Returns: Reporting stations and related data for given date
"""
def get_reporting_weather_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get forecast reporting stations by date function
Params: date
Returns: Forecast reporting stations and related data for given date
"""
def get_reporting_weather_forecast_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-forecast', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get reporting weather station dates function
Returns: List of dates for which reporting stations exist
"""
def get_reporting_weather_stations_dates():
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-dates')
    return response.json() if response.status_code == 200 else []


"""
Get forecast reporting station dates function
Returns: List of dates with forecast station reporting
"""
def get_reporting_weather_forecast_stations_dates():
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-forecast-dates')
    return response.json() if response.status_code == 200 else []

"""
Get WCS layer function
Params: date, table_name
Returns: Raster layer data from WCS
"""
def get_wcs_layer(date: str, table_name: str):
    params = {
        'date': date,
        'table_name': table_name
    }
    response = requests.get(f'{API_URL}/wcs-layer', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get additional layer function
Params: date, table_name
Returns: Raster layer data
"""
def get_add_layer(date: str, table_name: str):
    params = {
        'date': date,
        'table_name': table_name
    }
    response = requests.get(f'{API_URL}/add-layer', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get hotspot date list function
Returns: List of available dates for hotspot data
"""
def get_hotspot_date_list():
    response = requests.get(f'{API_URL}/fire-m3hotspot-date-list')
    return response.json() if response.status_code == 200 else []

"""
Get hotspots by date function
Params: date
Returns: Wildfire data hotspots for a specific date
"""
def get_hotspot_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-m3hotspot-by-date', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get hotspot ecozone list function
Returns: List of available ecozones
"""
def get_hotspot_ecozone_list():
    response = requests.get(f'{API_URL}/fire-m3hotspot-ecozone-list')
    return response.json() if response.status_code == 200 else []

"""
Get hotspots by ecozone function
Params: ecozone
Returns: Records of hotspots for given ecozone
"""
def get_hotspot_by_ecozone(ecozone: str):
    params = {
        'ecozone': ecozone
    }
    response = requests.get(f'{API_URL}/fire-m3hotspot-by-ecozone', params=params)
    return response.json() if response.status_code == 200 else []

"""
Get hotspot temperature max function
Returns: Maximum recorded hotspot temperatures
"""
def get_hotspot_temp_max():
    response = requests.get(f'{API_URL}/fire-hotspot-temp-max')
    return response.json() if response.status_code == 200 else []

"""
Get hotspots by temperature range function
Params: min_temp, max_temp
Returns: Records of hotspots within temperature range
"""
def get_hotspot_by_temp(min_temp: float, max_temp: float):
    params = {
        'min_temp': min_temp,
        'max_temp': max_temp
    }
    response = requests.get(f'{API_URL}/fire-hotspot-by-temp', params=params)
    return response.json() if response.status_code == 200 else []

