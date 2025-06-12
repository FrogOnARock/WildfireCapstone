from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Wildfire API")
app.include_router(router, prefix="/api")

