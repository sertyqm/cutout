from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_id: str = os.getenv("CUTOUT_MODEL_ID", "ZhengPeng7/BiRefNet_HR-matting")
    model_revision: str | None = os.getenv("CUTOUT_MODEL_REVISION")
    device: str = os.getenv("CUTOUT_DEVICE", "cuda")
    max_upload_bytes: int = int(os.getenv("CUTOUT_MAX_UPLOAD_BYTES", str(15 * 1024 * 1024)))
    max_image_pixels: int = int(os.getenv("CUTOUT_MAX_IMAGE_PIXELS", str(24_000_000)))


settings = Settings()

