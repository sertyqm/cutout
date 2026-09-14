from __future__ import annotations

from io import BytesIO
from threading import Lock
from typing import Protocol

import torch
from PIL import Image, ImageOps
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

from app.config import Settings


class BackgroundRemovalEngine(Protocol):
    @property
    def is_loaded(self) -> bool: ...

    @property
    def active_device(self) -> str | None: ...

    def remove_background(self, image: Image.Image) -> bytes: ...


class InferenceUnavailableError(RuntimeError):
    """Raised when model weights cannot be loaded or inference cannot begin."""


class BiRefNetEngine:
    """Lazy wrapper around a BiRefNet-compatible Hugging Face segmentation model."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: torch.nn.Module | None = None
        self._device: torch.device | None = None
        self._lock = Lock()
        self._inference_lock = Lock()
        self._use_half_precision = False
        self._transform = transforms.Compose(
            [
                transforms.Resize((settings.input_size, settings.input_size)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def active_device(self) -> str | None:
        return str(self._device) if self._device is not None else None

    def _resolve_device(self) -> torch.device:
        requested = self._settings.device.lower()
        if requested == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if requested.startswith("cuda") and not torch.cuda.is_available():
            return torch.device("cpu")
        return torch.device(requested)

    def _load(self) -> None:
        if self._model is not None:
            return

        with self._lock:
            if self._model is not None:
                return

            try:
                self._device = self._resolve_device()
                self._model = AutoModelForImageSegmentation.from_pretrained(
                    self._settings.model_id,
                    revision=self._settings.model_revision,
                    trust_remote_code=True,
                )
                self._model.to(self._device)
                self._use_half_precision = (
                    self._settings.use_half_precision and self._device.type == "cuda"
                )
                if self._use_half_precision:
                    self._model.half()
                self._model.eval()
            except Exception as error:
                self._model = None
                self._device = None
                raise InferenceUnavailableError(
                    "The background-removal model could not be loaded. Check the model settings, "
                    "network access and available memory."
                ) from error

    def remove_background(self, image: Image.Image) -> bytes:
        self._load()
        assert self._model is not None
        assert self._device is not None

        source = ImageOps.exif_transpose(image).convert("RGB")
        tensor = self._transform(source).unsqueeze(0).to(self._device)
        if self._use_half_precision:
            tensor = tensor.half()

        with self._inference_lock, torch.inference_mode():
            prediction = self._model(tensor)[-1].sigmoid().float().cpu()[0].squeeze()

        alpha = transforms.ToPILImage()(prediction).resize(source.size, Image.Resampling.LANCZOS)
        output = source.copy()
        output.putalpha(alpha)

        buffer = BytesIO()
        output.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()
