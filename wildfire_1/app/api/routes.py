from fastapi import APIRouter
from wildfire_1.app.services.wcs_queries import get_active_fires
from wildfire_1.app.services.wcs_queries import get_raster_data

router = APIRouter()

@router.get("/active-fires")
def active_fires(date: str):
    return get_active_fires(date)

@router.get("/wcs/{layer_name}")
def raster_layer(layer_name: str, date: str):
    return get_raster_data(layer_name, date)