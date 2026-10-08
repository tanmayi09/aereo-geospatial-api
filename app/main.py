from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.database import Base, engine
from app.models.file import FileRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aereo Geospatial File Measurement API",
    description="API for processing KML and Shapefile geospatial files.",
    version="1.0.0"
)

app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "Aereo Geospatial File Measurement API is running"
    }