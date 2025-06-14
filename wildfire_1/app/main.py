from fastapi import FastAPI
from wildfire_1.app.api.routes import router

app = FastAPI(title="Wildfire API")
app.include_router(router, prefix="/api")

