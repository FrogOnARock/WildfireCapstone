from wildfire_1.app.db.session import SessionLocal
from sqlalchemy.sql import text

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

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM active_fires
                WHERE startdate > :min_date and startdate < :max_date
            """), {"max_date": max_date, "min_date": min_date}
        )
        return [dict(row) for row in result]


def get_active_fire_by_id(fire_id: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM active_fires
                WHERE id = :fire_id
            """), {"fire_id": fire_id}
        )
        return [dict(row) for row in result]



'''
Fire Danger Queries:

- get_fire_danger_by_date
    - Based on the acquisition date of the data, return the fire danger level at that time
    --> goal is to provide fire danger over time
'''

def get_fire_danger_by_date(date: str):

    #set up a conditional to return data for the latest date if no date is provided
    if date is None:
        with SessionLocal() as session:
            date = session.execute(
                text("""
                    SELECT max(acquisition_date)
                    FROM fire_danger
                """))

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_danger
                WHERE acq_date = :date
            """), {"date": date}
        )
        return [dict(row) for row in result]


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

    return [dict(row) for row in result]

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
                WHERE cause in :cause
            """), {"cause": cause_list}
        )
        return [dict(row) for row in result]

def get_fire_history_by_response(response: str):

    #Possible values: None, NOR, MON, MOD, FUL

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_history
                WHERE response_type = :response_type
            """), {"response": response}
        )

        return [dict(row) for row in result]

def get_fire_history_by_hectares(max_hectares: float, min_hectares: float):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_history
                WHERE hectares > :min_hectares and hectares < :max_hectares
            """)
        ), {"max_hectares": max_hectares, "min_hectares": min_hectares}

        return [dict(row) for row in result]


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
                 SELECT *
                 FROM fire_perimeter_estimate
                 where firstdate > :start_date
                   and lastdate < :end_date
                 """), {"max_date": start_date, "min_date": end_date}
        )

    return [dict(row) for row in result]

def get_perimeter_by_hcount(min_hcount: int):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_perimeter_estimate
                WHERE hcount >= :min_hcount
            """), {"min_hcount": min_hcount}
        )

    return [dict(row) for row in result]

def get_perimeter_by_area(min_area: float):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM fire_perimeter_estimate
                WHERE area >= :min_area
            """), {"min_area": min_area}
        )

    return [dict(row) for row in result]


'''
Forecast Weather Stations Queries:
- get_forecast_stations_by_date
    - based on the reporting date, return data for a forecast station
- get_forecast_stations_by_agency
    - based on the reporting agency, return data for a forecast station
'''

def get_forecast_stations_by_date(date: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM forecast_weather_stations
                WHERE rep_date = :date
            """), {"date": date}
        )

        return [dict(row) for row in result]

def get_forecast_stations_by_agency(agency_list: list):

    #Possible values: MoFPB, AESRD, SERM, SOPFEU, NT, MBCONS, NWS, mSC, MoFPB

    assert agency_list is object, "Agency list must be a list"

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM forecast_weather_stations
                WHERE reporting_agency in :agency_list
            """), {"agency": agency_list}
        )

        return [dict(row) for row in result]


'''
Reporting Weather Station Queries:
- get_reporting_stations_by_date
    - based on the reporting date, return data for a reporting station
'''

def get_reporting_stations_by_date(date: str):

    with SessionLocal() as session:
        result = session.execute(
            text("""
                SELECT *
                FROM reporting_weather_stations
                WHERE rep_date = :date
            """), {"date": date}
        )

        return [dict(row) for row in result]


'''
Reporting Weather Stations Forecast queries:
- get_reporting_stations_forecast_by_date
    - based on the reporting date, return data for a reporting station 
'''


def get_reporting_stations_forecast_by_date(date: str):
    with SessionLocal() as session:
        result = session.execute(
            text("""
                 SELECT *
                 FROM reporting_weather_stations_forecast
                 WHERE rep_date = :date
                 """), {"date": date}
        )

        return [dict(row) for row in result]