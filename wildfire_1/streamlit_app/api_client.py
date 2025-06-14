import requests

API_URL = 'http://localhost:8000/api'

def get_active_fires(min_date: str, max_date: str = None):
    params = {
        'min_date': min_date,
    }
    if max_date:
        params['max_date'] = max_date
    response = requests.get(f'{API_URL}/active-fires', params=params)
    return response.json() if response.status_code == 200 else []


