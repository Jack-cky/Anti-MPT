# Changelog

## [1.2.2] - 2026-08-19

Hardened the inference pipeline against transient yfinance failures and calendar-gap edge cases.

### Changed
- Cached yfinance fetches per process so benchmark data (`^IRX`, `XHB`) is downloaded once per run instead of once per agent.
- Copied cached benchmark frames before downstream cleansing so the shared cache remains pristine across agent evaluations.
- Hoisted benchmark computation into a dedicated `Fetch benchmark data` pipeline task, passing precomputed series into `consolidate_data` so the per-agent inference task performs no network calls.
- Updated `consolidate_data` to accept precomputed `risk_free` and `mkt_idx` DataFrames for reuse across agents.

### Fixed
- Raised a clear error when yfinance returns an empty DataFrame instead of failing later with a `KeyError` on the first trading date.
- Snapped benchmark lookups in `get_risk_free` and `get_market_index` forward to the first available date, guarding against calendar gaps in benchmark data.
- Stopped the welcome popup from closing on backdrop clicks; it is now dismissed only via the "Got it" button.
- Added explicit handling for missing benchmark data after the requested start date and corrected the market-index calculation to use the first available value on or after the start date instead of requiring an exact-day match.
- Added safe `funds=10_000` defaults for `get_risk_free` and `get_market_index` to avoid direct-call failures when arguments are omitted.

## [1.2.1] - 2026-08-15

Pipeline resilience and deployment workflow improvements.

### Added
- Added `make pull` target to fetch the latest pipeline container image from Docker Hub.
- Introduced retry logic with a delay-based retry policy to the `persist_snapshot` task for improved reliability during database writes.
- Committed the initial `dashboard` migration so a fresh database can be initialised with `manage.py migrate`.

### Changed
- Expanded `.gitignore` with comprehensive Python packaging patterns and environment management exclusions.
- Restructured GitHub Actions scheduled pipeline workflow to separate image pulling from pipeline execution with retry loop.
- Updated `docker compose run pipeline` to never pull images via `--pull never` flag.

### Fixed
- Guarded against empty inference output and only wrote the Parquet cache after the database transaction committed successfully.
- Configured MySQL session `wait_timeout` to 600 seconds so abandoned connections release their locks promptly instead of after the 8-hour server default.

## [1.1.1] - 2026-07-03

Repository restructuring, dependency management overhaul, and container orchestration integration.

### Added
- Added container orchestration via Docker Compose `apps/compose.yaml`.
- Configured `pyproject.toml` to manage project metadata and optional dependencies `dashboard`, `pipeline`.
- Introduced `notebooks/02_feature_engineering.ipynb` for feature engineering and pre-processing exploration.
- Configured GitHub Actions workflows under `.github/`.
- Added Prefect to the `pipeline` dependency group for inference workflow orchestration.

### Changed
- Refactored `antimpt` core structure into modular components: `environments`, `evaluation`, `market`, `transforms`, `models`, `cli`, and `experiments`.
- Migrated the Django project directory from `demo/` to `apps/`.
- Updated `makefile` commands for Docker Compose workflows, e.g. `make build` and `make dashboard`.
- Elevated the required Python version to `~=3.12.0`.
- Revised project documentation and branding in `README.md`.

### Fixed
- Replaced outdated legacy agent scripts and utilities with a consolidated structure.
- Repurposed legacy files including `requirements.txt`, `setup.py`, and `docker/` configuration.

## [1.0.2] - 2025-06-27

Enhanced security to prevent unauthorised third-party access.

### Added
- Implemented a `robots.txt` file to disallow web crawling.

### Changed
- Adjusted order-writing scripts for better readability.
- Modified error page styles to enhance user experience.
- Updated the trade history pipeline to utilise the new API with password protection.
- Improved the Dockerfile for better package management.

### Fixed
- Revised the `.dockerignore` file to prevent the exposure of sensitive credentials.

## [1.0.1] - 2025-06-17

Initial repository.
