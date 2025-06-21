from fastapi import FastAPI
from wildfire_1.app.api.routes import router
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Wildfire API")
app.include_router(router, prefix="/api")

