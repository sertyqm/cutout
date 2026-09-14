# Portfolio notes

## Why this project exists

Cutout Lab is a compact demonstration of how I approach a computer-vision product request:

1. Define the real acceptance criterion instead of assuming a public benchmark equals user satisfaction.
2. Select a replaceable inference engine so it can be evaluated and swapped without rewriting the API.
3. Protect the service from malformed, oversized and unsupported uploads.
4. Package the application for repeatable local and container deployment.
5. Keep the limitations and evaluation work visible in the project documentation.

## What this project deliberately does not claim

- It does not claim to reproduce Remove.bg quality.
- It does not claim that a segmentation benchmark measures fine hair or transparent edges.
- It does not ship a model training pipeline or a manually annotated data set.
- It does not represent operating cost until the configured model is timed on the selected hosting setup.

## Good next experiments

- Add an engine adapter for a second model and a consistent benchmark harness.
- Add a small web client after selecting its product direction.
- Record p50 and p95 end-to-end latency across image sizes on a real GPU.
- Add object-selection guidance for cases with multiple foreground subjects.
- Add test fixtures that exercise EXIF rotation, large images and alpha preservation.

