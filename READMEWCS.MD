# PostGIS Table Documentation — WCS Layers

These tables support ingestion of raster-based geospatial data from the CWFIS WCS catalog. Each layer is processed into a point-based representation with an EPSG:4326 spatial reference system to support downstream frontend visualization and machine learning modeling.

All tables follow a standardized schema and are indexed for spatial and temporal queries.

---

## Shared Schema

All raster-derived tables follow the same column structure:

| Column             | Type                | Description                                         |
|--------------------|---------------------|-----------------------------------------------------|
| `id`               | `SERIAL`            | Unique row ID                                       |
| `acquisition_date` | `DATE`              | Date the raster was acquired or processed           |
| `lat`, `lon`       | `DOUBLE PRECISION`  | Latitude and longitude of the raster cell center    |
| `value`            | `FLOAT`             | Raster value at the point location                  |
| `geom`             | `GEOMETRY(POINT)`   | EPSG:4326 point geometry of the raster cell center  |

**Indexes**: `GIST(geom)`, `acquisition_date`

---

## Available Tables

| Table Name                  | Description                                      |
|----------------------------|--------------------------------------------------|
| `daily_severity_rating`    | Daily fire weather severity index                |
| `drought_code`             | Drought code measuring deep fuel dryness         |
| `wind_direction`           | Wind direction in degrees                        |
| `wind_speed`               | Wind speed in km/h                               |
| `fire_type`                | Categorical fire type code                       |
| `initial_spread_index`     | Potential fire spread index                      |
| `precipitation`            | Daily precipitation in mm                        |
| `temperature`              | Daily temperature in °C                          |

Each table contains georeferenced pixels extracted from GeoTIFFs, converted to point geometries for simplified querying and spatial joins. Raster data is cast to `float32` and filtered for NoData values prior to insertion.
