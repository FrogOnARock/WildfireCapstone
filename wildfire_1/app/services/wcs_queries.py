from wildfire_1.app.db.session import SessionLocal
from sqlalchemy.sql import text

##############
#WCS Queries:
##############

'''

The WCS Tables are as follows:
- daily_severity_rating    
- drought_code
- wind_direction
- wind_speed               
- fire_type                
- initial_spread_index     
- precipitation
- temperature

The schema for each of these tables is as follows:
- value --> the value of the data (drought code, wind direction, etc.)
- geometry --> point geometry
- acquisition_date --> the date the data was acquired (to act as a time dimension as I continue data collection)
- lon --> longitude of point
- lat --> latitude of point

Because of the stable nature of the queries and the lack of diversity in data, each query will be the same, filtered
along the time dimension. Thus, one query will be used, with the table name as a parameter.
'''

# List of allowed WCS table names
ALLOWED_WCS_TABLES = {
    "daily_severity_rating",
    "drought_code",
    "wind_direction",
    "wind_speed",
    "fire_type",
    "initial_spread_index",
    "precipitation",
    "temperature"
}


def wcs_query(max_date: str, min_date:str, table: str):


    # Validate table name
    if table not in ALLOWED_WCS_TABLES:
        raise ValueError(f"Invalid table name: {table}")

    #Deal with no setting of max date (default to 9999 to include all values)
    if max_date is None:
        max_date = "9999-12-31"

    # Inject table name safely (after validation)
    query = f"""
        SELECT *
        FROM {table}
        WHERE acquisition_date > :min_date AND acquisition_date < :max_date
    """

    with SessionLocal() as session:
        result = session.execute(text(query), {
            "min_date": min_date,
            "max_date": max_date
        })
        return [dict(row) for row in result]
