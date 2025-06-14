from fastapi import APIRouter
from wildfire_1.app.services.wfs_queries import get_active_fires
#from wildfire_1.app.services.wfs_queries import get_raster_data

router = APIRouter()

@router.get("/active-fires")
def api_active_fires(min_date: str, max_date: str = None):
    return get_active_fires(max_date=max_date, min_date=min_date)

#@router.get("/wcs/{layer_name}")
#def raster_layer(layer_name: str, date: str):
#    return get_raster_data(layer_name, date)