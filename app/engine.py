from __future__ import annotations

from io import BytesIO
from threading import Lock
from typing import Protocol

import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

from app.config import Settings


class BackgroundRemovalEngine(Protocol):
    @property
    def is_loaded(self) -> bool: ...

    def remove_background(self, image: Image.Image) -> bytes: ...


class BiRefNetEngine:
    """Lazy wrapper around a BiRefNet-compatible Hugging Face segmentation model."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: torch.nn.Module | None = None
        self._device: torch.device | None = None
        self._lock = Lock()

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def _load(self) -> None:
        if self._model is not None:
            return

        with self._lock:
            if self._model is not None:
                return

            configured_device = self._settings.device
            if configured_device == "cuda" and not torch.cuda.is_available():
                configured_device = "cpu"

            self._device = torch.device(configured_device)
            self._model = AutoModelForImageSegmentation.from_pretrained(
                self._settings.model_id,
                revision=self._settings.model_revision,
                trust_remote_code=True,
            )
            self._model.to(self._device)
            self._model.eval()

    def remove_background(self, image: Image.Image) -> bytes:
        self._load()
        assert self._model is not None
        assert self._device is not None

        source = image.convert("RGB")
        transform = transforms.Compose(
            [
                transforms.Resize((2048, 2048)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        tensor = transform(source).unsqueeze(0).to(self._device)

        with torch.inference_mode():
            prediction = self._model(tensor)[-1].sigmoid().cpu()[0].squeeze()

        alpha = transforms.ToPILImage()(prediction).resize(source.size, Image.Resampling.LANCZOS)
        output = source.copy()
        output.putalpha(alpha)

        buffer = BytesIO()
        output.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()

