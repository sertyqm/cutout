from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    model_id: str = os.getenv("CUTOUT_MODEL_ID", "ZhengPeng7/BiRefNet_HR-matting")
    model_revision: str | None = os.getenv(
        "CUTOUT_MODEL_REVISION", "5d6b6f8adcb5b417c871b1d84ceaae9871355b7f"
    )
    device: str = os.getenv("CUTOUT_DEVICE", "auto")
    input_size: int = int(os.getenv("CUTOUT_INPUT_SIZE", "2048"))
    use_half_precision: bool = os.getenv("CUTOUT_USE_HALF_PRECISION", "true").lower() == "true"
    max_upload_bytes: int = int(os.getenv("CUTOUT_MAX_UPLOAD_BYTES", str(15 * 1024 * 1024)))
    max_image_pixels: int = int(os.getenv("CUTOUT_MAX_IMAGE_PIXELS", str(24_000_000)))


settings = Settings()
