Release v0.1.22

- Fix Dockerfile: switch to `python:3.14-slim-bookworm`, remove Rust toolchain install, and rely on prebuilt wheels where possible.
- Install necessary build deps for wheel compilation (`build-essential`, `libpq-dev`, `libffi-dev`, `python3-dev`).
- Prepare image build improvements to avoid heavy Rust installs during CI/local builds.

See CHANGELOG.md for past releases.