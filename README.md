# Cutout

A self-hosted background-removal web tool built as a learning and portfolio project. It uploads an image, creates a transparent PNG cutout and lets the visitor compare and download the result.

The first engine is designed for the official `ZhengPeng7/BiRefNet_HR-matting` model. This is an **experimental portfolio project**, not a claim of Remove.bg-equivalent quality. The right way to judge it is on a representative, held-out image set that includes hair, fabric, products, reflections and semi-transparent materials.

## What is included

- Responsive browser interface with upload, before/after slider, dark mode and PNG download
- FastAPI API with image validation and transparent PNG output
- A model-engine boundary that makes experiments reproducible and testable
- Lazy model loading, GPU FP16 inference, serial inference and health reporting
- A test suite that exercises request validation and output handling without downloading model weights
- An evaluation plan for comparing candidate models against a defined acceptance set

## Quick start

Python 3.11 and an NVIDIA CUDA environment are recommended for actual inference. The default is a pinned snapshot of the official [`ZhengPeng7/BiRefNet_HR-matting`](https://huggingface.co/ZhengPeng7/BiRefNet_HR-matting) model. Its remote model code depends on `timm`; the pinned runtime dependencies include it and follow the upstream requirement that NumPy remain below v2.

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

The first real request downloads the model weights from Hugging Face unless they are already cached. Copy `.env.example` to `.env` and adjust the variables if needed. `CUTOUT_DEVICE=auto` selects CUDA when it is available, otherwise CPU. CPU inference is expected to be slow. The model loads lazily so starting the web server does not download it.

For a different model, do not change only `CUTOUT_MODEL_ID`. Confirm that its preprocessing, prediction output and licensing are compatible with `BiRefNetEngine`, then record the model ID and immutable revision in `.env`.

## API

`POST /api/remove-background`

- Form field: `image`
- Supported input: PNG, JPEG, WEBP
- Result: a PNG with an alpha channel

`GET /health` reports the configured model, immutable revision, requested device, active device and whether it has been loaded.

## Run tests

```bash
pytest
```

## Docker

```bash
docker build -t cutout-lab .
docker run --rm -p 8000:8000 --gpus all cutout-lab
```

The base image is intentionally CPU-compatible. For a CUDA deployment, use an NVIDIA CUDA base image that matches the installed PyTorch build and validate it on the target GPU.

## Evaluation plan

Before describing the service as production ready:

1. Assemble a 50–100 image acceptance set: portraits with loose hair, garments, catalog products, reflective objects, transparent objects and multiple subjects.
2. Keep 20% of it unseen until the selected approach is configured.
3. Compare output at matching resolution on white, black and coloured backgrounds. Record missing detail, halos, background colour spill and processing time.
4. Benchmark at least the selected BiRefNet matting model and one alternative. Include the exact model revision, settings, GPU and request timing.
5. Publish the results and failure cases. Do not claim parity with a commercial service without evidence from that test.

## License and model responsibility

The repository code is MIT licensed. Model weights and datasets have their own terms. Check the exact model card and deployment terms before commercial use. The default model choice should be pinned to a reviewed revision before any real deployment.
