# PostGIS Table Documentation — Additional Layers

These tables support ingestion of raster-based geospatial data from Additional Sources. Each layer is processed into a point-based representation with an EPSG:4326 spatial reference system to support downstream frontend visualization and machine learning modeling.

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
| `geometry`         | `GEOMETRY(POINT)`   | EPSG:4326 point geometry of the raster cell center  |

**Indexes**: `GIST(geom)`, `acquisition_date`

---

## Available Tables

| Table Name                  | Description                                      |
|-----------------------------|--------------------------------------------------|
| `bulk_density_5cm`          | Soil bulk density (g/cm³) at 0–5 cm depth        |
| `clay_5cm`                  | Percentage of clay in soil at 0–5 cm depth       |
| `landcover`                 | Land cover classification                        |
| `ph_5cm`                    | Soil pH at 0–5 cm depth                          |
| `sand_5cm`                  | Percentage of sand in soil at 0–5 cm depth       |
| `silt_5cm`                  | Percentage of silt in soil at 0–5 cm depth       |
| `soc_5cm`                   | Soil organic carbon at 0–5 cm depth (g/kg)       |


Each table contains georeferenced pixels extracted from GeoTIFFs, converted to point geometries for simplified querying and spatial joins. Raster data is cast to `float32` and filtered for NoData values prior to insertion.
