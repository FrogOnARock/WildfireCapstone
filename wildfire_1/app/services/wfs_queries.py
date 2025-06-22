from wildfire_1.app.db.session import SessionLocal
from sqlalchemy.sql import text
from sqlalchemy import bindparam

##############
#WFS Queries:
##############

'''

Active Fire Queries:
- get_active_fires
    - Query to return active fires between two dates (max and minimum date)
- get_active_fire_by_id
    - Query to return active fire by fire id

'''

def get_active_fires(max_date: str, min_date:str):

    #Deal with no setting of max date (default to 9999 to include all values)
    if max_date is None:
        max_date = "9999-12-31"

    print(max_date)
    print(min_date)

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT ST_AsGeoJSON(geometry) AS geometry,
                    lat,
                    lon,
                    firename,
                    hectares,
                    agency,
                    stage_of_control,
                    response_type,
                    startdate
                FROM active_fires
                WHERE startdate > :min_date and startdate < :max_date
            """), {"max_date": max_date, "min_date": min_date}
        )

        return result.mappings().all()


def get_active_fire_by_name(fire_name: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM active_fires
                WHERE firename = :fire_name
            """), {"fire_name": fire_name}
        )
        return result.mappings().all()

def get_active_fire_names():
    with SessionLocal() as session:
        result = session.execute(
            text("""
            select distinct(firename)
            from active_fires""")
        )
        return result.mappings().all()

'''
Fire Danger Queries:

- get_fire_danger_by_date
    - Based on the acquisition date of the data, return the fire danger level at that time
    --> goal is to provide fire danger over time
'''

def get_fire_danger_by_date(date: str):


    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT "GRIDCODE", acquisition_date, ST_AsGeoJSON(geometry) as geometry
                FROM fire_danger
                WHERE acquisition_date = :date
            """), {"date": date}
        )
        return result.mappings().all()


def get_fire_danger_dates():

    with SessionLocal() as session:
        date = session.execute(
            text("""
                SELECT distinct(acquisition_date)
                FROM fire_danger
            """))

    return date.mappings().all()

'''
Fire History Queries:
- get_fire_history_by_date
    - Based on the max and min start date, return fire history
- get_fire_history_by_cause
    - Based on the cause of fire, return fire history
- get_fire_history_by_response
    - Based on the response to fire, return fire history
- get_fire_history_by_hectares
    - Based on the hectares of the fire (including min and max), return fire history
'''


def get_fire_history_by_date(max_date: str, min_date: str):

    #Deal with no setting of max date (default to 9999 to include all values)
    if max_date is None:
        max_date = "9999-12-31"

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT * FROM fire_history
                where startdate > :min_date and startdate < :max_date
            """), {"max_date": max_date, "min_date": min_date}
        )

    return result.mappings().all()

def get_fire_history_by_cause(cause: str):

    """
    There are various parameters that can be entered into this function, they will need to be mapped.

    unknown and under in: Unknown
    U: Unknown
    Under Investigation: Unknown
    N: Natural
    Lightning: Natural
    Undetermined: Unknown
    Prescribed Fire: Prescribed
    under investigation: Unknown
    H: Human
    Human caused: Human
    Rollout on steep ter: Prescribed

    I'll basically just have to take Unknown, Natural, Human, Prescribed and then pass a list to the database

    """

    cause_dict = {
        'Unknown': ['unknown and under in', 'U', 'Under Investigation', 'under investigation', 'Undetermined'],
        'Human': ['H', 'Human caused'],
        'Natural': ['N', 'Lightning'],
        'Prescribed': ['Prescribed Fire', 'Rollout on steep ter']
    }

    cause_list = cause_dict[cause]

    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM fire_history
                 WHERE cause IN :cause
                 """).bindparams(bindparam("cause", expanding=True)),
            {"cause": cause_list})
        return result.mappings().all()

def get_fire_history_by_response(response: str):

    #Possible values: None, NOR, MON, MOD, FUL

    if response == "None":
        response = None

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_history
                WHERE response_type = :response
            """), {"response": response}
        )

        return result.mappings().all()

def get_fire_history_by_hectares(max_hectares: float, min_hectares: float):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_history
                WHERE hectares > :min_hectares and hectares < :max_hectares
            """), {"max_hectares": max_hectares, "min_hectares": min_hectares}
        )

        return result.mappings().all()


'''
Fire Perimeter Estimate Queries:
- get_perimeter_by_date
    - Based on the start and end date of the data, return the perimeter estimates for that time frame
- get_perimeter_by_hcount
    - Return perimeters based on the minimum number of hotspots within the perimeter
- get_perimeter_by_area
    - Return perimeter based on the minimum area of the perimeter
'''

def get_perimeter_by_date(start_date: str, end_date: str):
    # Deal with no setting of max date (default to 9999 to include all values)
    if end_date is None:
        end_date = "9999-12-31"

    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT hcount, firstdate, lastdate, area, acquisition_date, ST_AsGeoJSON(geometry) as geometry
                 FROM fire_perimeter_estimates
                 where firstdate > :start_date
                   and lastdate < :end_date
                 """), {"start_date": start_date, "end_date": end_date}
        )

    return result.mappings().all()

def get_perimeter_by_hcount(min_hcount: int, max_hcount: int):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT hcount, firstdate, lastdate, area, acquisition_date, ST_AsGeoJSON(geometry) as geometry
                FROM fire_perimeter_estimates
                WHERE hcount >= :min_hcount and hcount <= :max_count
            """), {"min_hcount": min_hcount, "max_count": max_hcount}
        )

    return result.mappings().all()

def get_perimeter_by_area(min_area: float):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT hcount, firstdate, lastdate, area, acquisition_date, ST_AsGeoJSON(geometry) as geometry
                FROM fire_perimeter_estimates
                WHERE area >= :min_area
            """), {"min_area": min_area}
        )

    return result.mappings().all()

def fire_perimeter_hotspots_max():

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT max(hcount)
                FROM fire_perimeter_estimates
            """)
        )

    return result.mappings().all()


'''
Forecast Weather Stations Queries:
- get_forecast_stations_by_date
    - based on the reporting date, return data for a forecast station
- get_forecast_stations_by_agency
    - based on the reporting agency, return data for a forecast station
'''

def get_forecast_stations_by_date_list():
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(rep_date)
                FROM forecast_weather_stations
            """)
        )

        return result.mappings().all()

def get_forecast_stations_by_date(date: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM forecast_weather_stations
                WHERE rep_date = :date
            """), {"date": date}
        )

        return result.mappings().all()

def get_forecast_stations_by_agency(agency_list: list):

    #Possible values: MoFPB, AESRD, SERM, SOPFEU, NT, MBCONS, NWS, mSC, MoFPB


    if not isinstance(agency_list, list):
        raise ValueError("agency_list must be a list")

    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM forecast_weather_stations
                 WHERE agency in :agency_list
                 """).bindparams(bindparam("agency_list", expanding=True)),
            {"agency_list": agency_list}
        )

        return result.mappings().all()

def get_forecast_station_agencies():
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(agency)
                FROM forecast_weather_stations
            """)
        )

        return result.mappings().all()

'''
Reporting Weather Station Queries:
- get_reporting_stations_by_date
    - based on the reporting date, return data for a reporting station
'''

def get_reporting_stations_date_list():

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(rep_date)
                FROM reporting_weather_stations
            """)
        )

        return result.mappings().all()


def get_reporting_stations_by_date(date: str):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM reporting_weather_stations
                WHERE rep_date = :date
            """), {"date": date}
        )

        return result.mappings().all()


'''
Reporting Weather Stations Forecast queries:
- get_reporting_stations_forecast_by_date
    - based on the reporting date, return data for a reporting station 
'''

def get_reporting_stations_forecast_date_list():

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(rep_date)
                FROM reporting_weather_stations_forecast
            """)
        )

        return result.mappings().all()

def get_reporting_stations_forecast_by_date(date: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM reporting_weather_stations_forecast
                 WHERE rep_date = :date
                 """), {"date": date}
        )

        return result.mappings().all()


'''
M3 Hotspot queries:
- get_hotspot_by_date
    - Return hotspots by reported daate
- get_hotspot_by_ecozone
    - Get hotspots by ecological zone
- get_hotspot_by_temp
    - Get hotspots based on a temperature range
'''

def get_hotspot_date_list():

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(rep_date)
                FROM m3_hotspots
            """)
        )

        return result.mappings().all()

def get_hotspot_by_date(date: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM m3_hotspots
                 WHERE rep_date = :date
                 """), {"date": date}
        )

        return result.mappings().all()

def get_ecozone_list():
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT distinct(ecozone)
                FROM m3_hotspots
            """)
        )

        return result.mappings().all()


def get_hotspot_by_ecozone(ecozone: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM m3_hotspots
                 WHERE ecozone = :ecozone
                 """), {"ecozone": ecozone}
        )

        return result.mappings().all()

def get_hotspot_temp_max():
    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT max(temp)
                 FROM m3_hotspots
                 """)
        )

    return result.mappings().all()

def get_hotspot_by_temp(min: float, max: float):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM m3_hotspots
                WHERE temp >= :min and temp <= :max
            """), {"min": min, "max": max}
        )

    return result.mappings().all()