from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

from app.config import Settings, settings
from app.engine import BackgroundRemovalEngine, BiRefNetEngine

app = FastAPI(title="Cutout", version="0.1.0", description="Self-hosted background removal API")
engine: BackgroundRemovalEngine = BiRefNetEngine(settings)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


def get_engine() -> BackgroundRemovalEngine:
    return engine


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "model_id": settings.model_id,
        "configured_device": settings.device,
        "model_loaded": engine.is_loaded,
    }


@app.post("/api/remove-background", response_class=Response)
async def remove_background(
    image: UploadFile = File(...),
    active_engine: BackgroundRemovalEngine = Depends(get_engine),
) -> Response:
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Upload a PNG, JPEG or WEBP image.")

    payload = await image.read(settings.max_upload_bytes + 1)
    if len(payload) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="The image exceeds the upload size limit.")

    try:
        source = Image.open(BytesIO(payload))
        source.load()
    except (UnidentifiedImageError, OSError) as error:
        raise HTTPException(status_code=422, detail="The uploaded file is not a valid image.") from error

    if source.width * source.height > settings.max_image_pixels:
        raise HTTPException(status_code=413, detail="The image exceeds the pixel limit.")

    output = active_engine.remove_background(source)
    return Response(
        content=output,
        media_type="image/png",
        headers={"Content-Disposition": 'attachment; filename="cutout.png"'},
    )
