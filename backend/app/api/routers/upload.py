from fastapi import (
    APIRouter,
    HTTPException,
    status,
    UploadFile,
    File,
)
from app.services.indexing import run_ingestion

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def upload_file(
    file: UploadFile = File(...),
):
    try:
        vectors = run_ingestion(file)
        return {"status": "success", "vectors_added": vectors}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e
