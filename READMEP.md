# PostGIS Table Documentation — WFS Layers

These tables support ingestion of vector geospatial data from the CWFIS WFS catalog. All layers are stored in a unified spatial reference system (EPSG:4326), support spatial indexing, and follow temporal modeling best practices.

---

## `active_fires`

Represents _current active wildfire events_ (point geometry) pulled from the WFS live feed.

| Column             | Type                | Description                                       |
|--------------------|---------------------|---------------------------------------------------|
| `id`               | `UUID`              | Unique identifier per fire (derived from WFS ID) |
| `acquisition_date`| `DATE`              | Date the data was pulled                         |
| `firename`         | `TEXT`              | Fire name or ID from agency                      |
| `startdate`        | `TIMESTAMPTZ`       | When the fire was first reported                 |
| `hectares`         | `REAL`              | Estimated burned area                            |
| `lat`, `lon`       | `DOUBLE PRECISION`  | Latitude and longitude                           |
| `agency`           | `TEXT`              | Reporting provincial agency                      |
| `stage_of_control` | `TEXT`              | Fire status (e.g., OUT, BEING HELD)              |
| `response_type`    | `TEXT`              | Level of suppression response                    |
| `geom`             | `GEOMETRY(POINT)`   | Fire location                                     |

**Indexes**: `GIST(geom)`, `acquisition_date`

---

## `fire_danger`

Represents _daily fire danger classification polygons_ based on a gridded surface.

| Column             | Type                   | Description                                  |
|--------------------|------------------------|----------------------------------------------|
| `id`               | `UUID`                 | Unique feature identifier                    |
| `acquisition_date`| `DATE`                 | The date the fire danger grid applies to     |
| `gridcode`         | `INTEGER`              | Danger level (1–5)                           |
| `geom`             | `GEOMETRY(MULTIPOLYGON)` | Polygonal extent                           |

**Indexes**: `GIST(geom)`, `acquisition_date`

---

## `fire_history`

Represents _historical wildfire records_ including year-to-date and previous years.

| Column             | Type                   | Description                                  |
|--------------------|------------------------|----------------------------------------------|
| `id`               | `UUID`                 | Unique fire identifier                       |
| `firename`         | `TEXT`                 | Agency-assigned fire ID                      |
| `agency`           | `TEXT`                 | Reporting provincial agency                  |
| `startdate`        | `TIMESTAMPTZ`          | Start date of the fire                       |
| `hectares`         | `REAL`                 | Final burned area estimate                   |
| `cause`            | `TEXT`                 | Fire cause (e.g., H = Human, L = Lightning)  |
| `lat`, `lon`       | `DOUBLE PRECISION`     | Coordinates                                  |
| `stage_of_control` | `TEXT`                 | Control status                               |
| `response_type`    | `TEXT`                 | Suppression response                         |
| `geom`             | `GEOMETRY(POINT)`      | Fire location                                |

**Indexes**: `GIST(geom)`, `startdate`

---

## `fire_perimeter_estimates`

Represents _estimated perimeters of ongoing wildfires_ with temporal snapshots.

| Column             | Type                   | Description                                  |
|--------------------|------------------------|----------------------------------------------|
| `id`               | `UUID`                 | Unique ID for a perimeter estimate           |
| `acquisition_date`| `DATE`                 | Pull date / perimeter estimate date          |
| `firstdate`        | `TIMESTAMPTZ`          | First hotspot within this perimeter          |
| `lastdate`         | `TIMESTAMPTZ`          | Most recent hotspot within this perimeter    |
| `hcount`           | `INTEGER`              | Number of hotspots detected in area          |
| `area`             | `REAL`                 | Area of the perimeter (hectares)             |
| `geom`             | `GEOMETRY(POLYGON)`    | Fire perimeter polygon                       |

**Indexes**: `GIST(geom)`, `acquisition_date`

---

## `forecast_weather_stations`

Represents _point-in-time meteorological reports_ from WMO fire weather stations.

| Column     | Type               | Description                              |
|------------|--------------------|------------------------------------------|
| `id`       | `TEXT`             | Unique per-station report ID (`wmo_rep_date`) |
| `rep_date` | `TIMESTAMPTZ`      | Timestamp of the forecast report         |
| `wmo`      | `INTEGER`          | World Meteorological Org station code    |
| `name`     | `TEXT`             | Station name                             |
| `agency`   | `TEXT`             | Reporting agency                         |
| `ua`       | `TEXT`             | Upper air code                           |
| `instr`    | `TEXT`             | Instrument type                          |
| `prov`     | `TEXT`             | Province                                 |
| `lat`, `lon` | `DOUBLE PRECISION` | Coordinates                             |
| `elev`     | `DOUBLE PRECISION` | Elevation (meters)                       |
| `temp`     | `REAL`             | Temperature (°C)                         |
| `td`       | `REAL`             | Dew point (°C)                           |
| `rh`       | `REAL`             | Relative humidity (%)                    |
| `ws`       | `REAL`             | Wind speed (km/h)                        |
| `wg`       | `REAL`             | Wind gust (km/h)                         |
| `wdir`     | `INTEGER`          | Wind direction (degrees)                 |
| `pres`     | `REAL`             | Atmospheric pressure                     |
| `vis`      | `REAL`             | Visibility                               |
| `rndays`   | `INTEGER`          | Recent rain days                         |
| `precip`   | `REAL`             | Precipitation (mm)                       |
| `sog`      | `REAL`             | Snow on ground (cm)                      |
| `ffmc`     | `REAL`             | Fine Fuel Moisture Code                  |
| `dmc`      | `REAL`             | Duff Moisture Code                       |
| `dc`       | `REAL`             | Drought Code                             |
| `bui`      | `REAL`             | Buildup Index                            |
| `isi`      | `REAL`             | Initial Spread Index                     |
| `fwi`      | `REAL`             | Fire Weather Index                       |
| `dsr`      | `REAL`             | Daily Severity Rating                    |
| `geom`     | `GEOMETRY(POINT)`  | Station location                         |

**Indexes**: `GIST(geom)`, `rep_date`

## `reporting_weather_stations`

Represents _forecast reports from physical meteorological stations (observed or interpolated by agency)_.

| Column       | Type               | Description                              |
|--------------|--------------------|------------------------------------------|
| `id`         | `TEXT`             | Unique report ID (e.g., `stationID_rep_date`) |
| `rep_date`   | `TIMESTAMPTZ`      | Timestamp of the forecast report         |
| `wmo`        | `INTEGER`          | WMO station ID                           |
| `name`       | `TEXT`             | Station name                             |
| `latitude`   | `DOUBLE PRECISION` | Latitude (decimal degrees)               |
| `longitude`  | `DOUBLE PRECISION` | Longitude (decimal degrees)              |
| `elevation`  | `REAL`             | Elevation in meters                      |
| `temp`       | `REAL`             | Temperature (°C)                         |
| `rh`         | `REAL`             | Relative humidity (%)                    |
| `ws`         | `REAL`             | Wind speed (km/h)                        |
| `wdir`       | `REAL`             | Wind direction (degrees)                 |
| `precip`     | `REAL`             | Precipitation (mm)                       |
| `sog`        | `REAL`             | Snow on ground (cm)                      |
| `ffmc`       | `REAL`             | Fine Fuel Moisture Code                  |
| `dmc`        | `REAL`             | Duff Moisture Code                       |
| `dc`         | `REAL`             | Drought Code                             |
| `isi`        | `REAL`             | Initial Spread Index                     |
| `bui`        | `REAL`             | Buildup Index                            |
| `fwi`        | `REAL`             | Fire Weather Index                       |
| `dsr`        | `REAL`             | Daily Severity Rating                    |
| `wx`         | `REAL`             | Wind X-component                         |
| `wy`         | `REAL`             | Wind Y-component                         |
| `timezone`   | `INTEGER`          | Local station timezone                   |
| `x`          | `DOUBLE PRECISION` | Projected X coordinate (meters)          |
| `y`          | `DOUBLE PRECISION` | Projected Y coordinate (meters)          |
| `geom`       | `GEOMETRY(POINT)`  | Station location geometry (EPSG:4326)    |

**Indexes**: `GIST(geom)`, `rep_date`

---

## `forecast_weather_stations_forecast`

Represents _interpolated fire weather forecasts from the SCRIBE model_, estimating values across the landscape and at virtual stations.

| Column       | Type               | Description                              |
|--------------|--------------------|------------------------------------------|
| `id`         | `TEXT`             | Unique ID (e.g., `firewx_scribe.stationID_rep_date`) |
| `rep_date`   | `TIMESTAMPTZ`      | Timestamp of the forecast report         |
| `wmo`        | `INTEGER`          | WMO station ID                           |
| `name`       | `TEXT`             | Station name                             |
| `latitude`   | `DOUBLE PRECISION` | Latitude (decimal degrees)               |
| `longitude`  | `DOUBLE PRECISION` | Longitude (decimal degrees)              |
| `elevation`  | `REAL`             | Elevation in meters                      |
| `temp`       | `REAL`             | Temperature (°C)                         |
| `rh`         | `REAL`             | Relative humidity (%)                    |
| `ws`         | `REAL`             | Wind speed (km/h)                        |
| `wdir`       | `REAL`             | Wind direction (degrees)                 |
| `precip`     | `REAL`             | Precipitation (mm)                       |
| `sog`        | `REAL`             | Snow on ground (cm)                      |
| `ffmc`       | `REAL`             | Fine Fuel Moisture Code                  |
| `dmc`        | `REAL`             | Duff Moisture Code                       |
| `dc`         | `REAL`             | Drought Code                             |
| `isi`        | `REAL`             | Initial Spread Index                     |
| `bui`        | `REAL`             | Buildup Index                            |
| `fwi`        | `REAL`             | Fire Weather Index                       |
| `dsr`        | `REAL`             | Daily Severity Rating                    |
| `wx`         | `REAL`             | Wind X-component                         |
| `wy`         | `REAL`             | Wind Y-component                         |
| `timezone`   | `INTEGER`          | Local station timezone                   |
| `x`          | `DOUBLE PRECISION` | Projected X coordinate (meters)          |
| `y`          | `DOUBLE PRECISION` | Projected Y coordinate (meters)          |
| `geom`       | `GEOMETRY(POINT)`  | Station location geometry (EPSG:4326)    |

**Indexes**: `GIST(geom)`, `rep_date`

---

## `m3_hotspots`

Represents _detected thermal anomalies (hotspots) from satellite observations_, enriched with environmental and fire behavior attributes. Derived from the M3 system.

| Column         | Type               | Description                              |
|----------------|--------------------|------------------------------------------|
| `id`           | `TEXT`             | Unique hotspot ID from WFS feature       |
| `rep_date`     | `TIMESTAMPTZ`      | Timestamp of detection                   |
| `lat`, `lon`   | `DOUBLE PRECISION` | Coordinates                              |
| `source`       | `TEXT`             | Source agency (e.g., NASA8)              |
| `sensor`       | `TEXT`             | Sensor type (e.g., VIIRS-I)              |
| `satellite`    | `TEXT`             | Satellite name (e.g., NOAA-21)           |
| `agency`       | `TEXT`             | Reporting provincial agency              |
| `temp`         | `REAL`             | Surface temperature                      |
| `rh`           | `REAL`             | Relative humidity (%)                    |
| `ws`           | `REAL`             | Wind speed (km/h)                        |
| `wd`           | `INTEGER`          | Wind direction (°)                       |
| `pcp`          | `REAL`             | Precipitation (mm)                       |
| `elev`         | `REAL`             | Elevation (m)                            |
| `ffmc`         | `REAL`             | Fine Fuel Moisture Code                  |
| `dmc`          | `REAL`             | Duff Moisture Code                       |
| `dc`           | `REAL`             | Drought Code                             |
| `isi`          | `REAL`             | Initial Spread Index                     |
| `bui`          | `REAL`             | Buildup Index                            |
| `fwi`          | `REAL`             | Fire Weather Index                       |
| `fuel`         | `TEXT`             | Fuel type (e.g., C2)                     |
| `ros`          | `REAL`             | Rate of spread                           |
| `sfc`          | `REAL`             | Surface fuel consumption                 |
| `tfc`          | `REAL`             | Total fuel consumption                   |
| `tfc0`         | `REAL`             | Reference total fuel consumption         |
| `sfc0`         | `REAL`             | Reference surface fuel consumption       |
| `bfc`          | `REAL`             | Burning fuel consumption                 |
| `hfi`          | `REAL`             | Head fire intensity                      |
| `cfb`          | `REAL`             | Crown fraction burned (%)                |
| `cbh`          | `REAL`             | Crown base height                        |
| `cfl`          | `REAL`             | Crown fire length                        |
| `pcuring`      | `REAL`             | Percent curing                           |
| `pconif`       | `REAL`             | Percent conifer                          |
| `cfactor`      | `REAL`             | Crown factor                             |
| `greenup`      | `INTEGER`          | Green-up stage (0 or 1)                  |
| `ecozone`      | `TEXT`             | Ecozone code                             |
| `ecozona2`     | `TEXT`             | Secondary ecozone code                   |
| `estarea`      | `REAL`             | Estimated burned area                    |
| `estarea2`     | `REAL`             | Alternate estimated area                 |
| `estarea3`     | `REAL`             | Alternate estimated area                 |
| `polyid`       | `TEXT`             | Associated polygon ID                    |
| `times_burned` | `INTEGER`          | Historical burn count                    |
| `age`          | `INTEGER`          | Age in hours since detection             |
| `geom`         | `GEOMETRY(POINT)`  | Location geometry                        |

**Indexes**: `GIST(geom)`, `rep_date`

---
