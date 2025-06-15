import requests
from altair import param

API_URL = 'http://localhost:8000/api'

def get_active_fires(min_date: str, max_date: str = None):
    params = {
        'min_date': min_date,
    }
    if max_date:
        params['max_date'] = max_date

    response = requests.get(f'{API_URL}/active-fires', params=params)
    return response.json() if response.status_code == 200 else []


def get_active_fires_by_name(name: str):
    params = {
        'name': name
    }
    response = requests.get(f'{API_URL}/active-fires-by-name', params=params)
    return response.json() if response.status_code == 200 else []


def get_active_fire_firenames():
    response = requests.get(f'{API_URL}/active-fire-names')
    return response.json() if response.status_code == 200 else []


def get_fire_danger(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-danger', params=params)
    return response.json() if response.status_code == 200 else []

def get_fire_danger_dates():
    response = requests.get(f'{API_URL}/fire-danger-dates')
    return response.json() if response.status_code == 200 else []

def get_fire_history_by_date(max_date: str, min_date: str):
    params = {
        'min_date': min_date
    }
    if max_date:
        params['max_date'] = max_date
    response = requests.get(f'{API_URL}/fire-history-by-date', params=params)
    return response.json() if response.status_code == 200 else []

def get_fire_history_by_cause(cause: str):
    params = {
        'cause': cause
    }
    response = requests.get(f'{API_URL}/fire-history-by-cause', params=params)
    return response.json() if response.status_code == 200 else []

def get_fire_history_by_response(response: str):
    params = {
        'response': response
    }
    response = requests.get(f'{API_URL}/fire-history-by-response', params=params)
    return response.json() if response.status_code == 200 else []

def get_fire_history_by_hectares(max_hectares: float, min_hectares: float):
    params = {
        'max_hectares': max_hectares,
        'min_hectares': min_hectares
    }
    response = requests.get(f'{API_URL}/fire-history-by-hectares', params=params)
    return response.json() if response.status_code == 200 else []

def get_perimeter_by_date(start_date: str, end_date: str):
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-date', params=params)
    return response.json() if response.status_code == 200 else []

def get_perimeter_by_hcount(min_hcount: int, max_hcount: int):
    params = {
        'min_hcount': min_hcount,
        'max_hcount': max_hcount
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-hotspot-count', params=params)
    return response.json() if response.status_code == 200 else []

def get_perimeter_by_area(min_area: float):
    params = {
        'min_area': min_area
    }
    response = requests.get(f'{API_URL}/fire-perimeter-by-area', params=params)
    return response.json() if response.status_code == 200 else []

def get_perimeter_hcounts():
    response = requests.get(f'{API_URL}/fire-perimeter-hotspots-max')
    return response.json() if response.status_code == 200 else []

def get_forecast_station_dates():
    response = requests.get(f'{API_URL}/fire-forecast-stations-date-list')
    return response.json() if response.status_code == 200 else []

def get_forecast_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-forecast-stations-date', params=params)
    return response.json() if response.status_code == 200 else []

def get_forecast_stations_by_agency(agency: list):
    params = [('agency', a) for a in agency]
    response = requests.get(f'{API_URL}/fire-forecast-stations-agency', params=params)
    return response.json() if response.status_code == 200 else []

def get_forecast_station_agencies():
    response = requests.get(f'{API_URL}/fire-forecast-station-agencies')
    return response.json() if response.status_code == 200 else []

def get_reporting_weather_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations', params=params)
    return response.json() if response.status_code == 200 else []

def get_reporting_weather_forecast_stations_by_date(date: str):
    params = {
        'date': date
    }
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-forecast', params=params)
    return response.json() if response.status_code == 200 else []

def get_reporting_weather_stations_dates():
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-dates')
    return response.json() if response.status_code == 200 else []


def get_reporting_weather_forecast_stations_dates():
    response = requests.get(f'{API_URL}/fire-reporting-weather-stations-forecast-dates')
    return response.json() if response.status_code == 200 else []

def get_wcs_layer(date: str, table_name: str):
    params = {
        'date': date,
        'table_name': table_name
    }
    response = requests.get(f'{API_URL}/wcs-layer', params=params)
    return response.json() if response.status_code == 200 else []

