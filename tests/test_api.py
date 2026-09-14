from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app, get_engine


class FakeEngine:
    is_loaded = True

    def remove_background(self, image: Image.Image) -> bytes:
        output = image.convert("RGBA")
        output.putalpha(128)
        buffer = BytesIO()
        output.save(buffer, format="PNG")
        return buffer.getvalue()


def image_bytes(format: str = "PNG") -> bytes:
    image = Image.new("RGB", (8, 8), "red")
    buffer = BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()


def client() -> TestClient:
    app.dependency_overrides[get_engine] = lambda: FakeEngine()
    return TestClient(app)


def test_health_reports_configuration() -> None:
    response = client().get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_remove_background_returns_transparent_png() -> None:
    response = client().post(
        "/api/remove-background",
        files={"image": ("source.png", image_bytes(), "image/png")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert Image.open(BytesIO(response.content)).mode == "RGBA"


def test_remove_background_rejects_unsupported_content_type() -> None:
    response = client().post(
        "/api/remove-background",
        files={"image": ("notes.txt", b"not an image", "text/plain")},
    )

    assert response.status_code == 415


def test_remove_background_rejects_malformed_image() -> None:
    response = client().post(
        "/api/remove-background",
        files={"image": ("broken.png", b"not a png", "image/png")},
    )

    assert response.status_code == 422

