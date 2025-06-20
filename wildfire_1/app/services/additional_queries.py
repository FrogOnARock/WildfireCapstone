from wildfire_1.app.db.session import SessionLocal
from sqlalchemy.sql import text

##############
#Additional Table Queries:
##############

'''

The additional tables are as follows:
- bulk_density_5cm    
- clay_5cm
- landcover
- ph_5cm   
- sand_5cm                
- silt_5cm     
- soc_5cm

The schema for each of these tables is as follows:
- value --> the value of the data
- geometry --> point geometry
- acquisition_date --> the date the data was acquired (to act as a time dimension as I continue data collection)
- lon --> longitude of point
- lat --> latitude of point

Because of the stable nature of the queries and the lack of diversity in data, each query will be the same, filtered
along the time dimension. Thus, one query will be used, with the table name as a parameter.
'''

# List of allowed additional table names
ALLOWED_ADD_TABLES = {
    "bulk_density_5cm",
    "clay_5cm",
    "landcover",
    "ph_5cm",
    "sand_5cm",
    "silt_5cm",
    "soc_5cm"
}


def additional_table_query(date:str, table: str):


    # Validate table name
    if table not in ALLOWED_ADD_TABLES:
        raise ValueError(f"Invalid table name: {table}")

    #Deal with no setting of max date (default to 9999 to include all values)
    if date is None:
        with SessionLocal() as session:
            date = session.execute(
                text("""
                     SELECT max(acquisition_date)
                     FROM :table
                     """), {"table": table}
            )

    # Inject table name safely (after validation)
    query = f"""
        SELECT value, acquisition_date, lon, lat, ST_AsGeoJSON(geometry) as geometry
        FROM {table}
        WHERE acquisition_date = :date
    """

    with SessionLocal() as session:
        result = session.execute(text(query), {
            "date": date
        })
        return result.mappings().all()


