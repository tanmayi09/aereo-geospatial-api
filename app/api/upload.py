from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import json

from app.database import SessionLocal
from app.models.file import FileRecord
from app.services.geospatial_service import (
    read_geospatial_file,
    extract_features,
    calculate_measurement
)

router = APIRouter(
    prefix="/api/files",
    tags=["Files"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in [".kml", ".zip"]:
        raise HTTPException(
            status_code=400,
            detail="Only .kml or .zip files are supported"
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Read geospatial file
        gdf = read_geospatial_file(str(file_path))

        # Extract features
        features = extract_features(gdf)

        # Calculate measurements
        measurements = calculate_measurement(gdf)

        # Save record to database
        db = SessionLocal()

        record = FileRecord(
            filename=file.filename,
            crs=str(gdf.crs),
            feature_count=len(gdf),
            features=json.dumps(features),
            measurements=json.dumps(measurements)
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        db.close()

        return {
            "id": record.id,
            "message": "File uploaded and processed successfully",
            "filename": file.filename,
            "feature_count": len(gdf),
            "crs": str(gdf.crs),
            "features": features,
            "measurements": measurements
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to process geospatial file: {str(e)}"
        )


@router.get("/{file_id}")
def get_file(file_id: int):

    db = SessionLocal()

    record = db.query(FileRecord).filter(
        FileRecord.id == file_id
    ).first()

    db.close()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "id": record.id,
        "filename": record.filename,
        "feature_count": record.feature_count,
        "crs": record.crs
    }
@router.get("/{file_id}/measurements/")
def get_measurements(file_id: int):

    db = SessionLocal()

    record = db.query(FileRecord).filter(
        FileRecord.id == file_id
    ).first()

    db.close()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    measurements = json.loads(record.measurements)

    return {
        "file_id": record.id,
        "filename": record.filename,
        "measurements": measurements
    }