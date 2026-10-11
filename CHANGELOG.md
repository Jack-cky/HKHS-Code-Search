# Changelog

## [1.0.3] - 2026-10-11

Updated the API container build and project version.

### Changed

- Mounted `uv` during the API image build and configured system-wide, cache-free dependency installation.
- Bumped the package version to 1.0.3.

## [1.0.2] - 2026-09-24

Improved search inference performance and container optimisation.

### Changed

- Improved dense search inference by using ONNX Runtime and the Hugging Face tokeniser directly, making cold startup faster.
- Reused shared metadata when loading hybrid search indexes and added typed search-engine dependency interfaces for the search API.
- Removed unused data-processing dependencies from the production package configuration.

### Fixed
- Prepared a writable `checkpoints` directory for the non-root API container.
- Corrected WordNet detection for the packaged `wordnet.zip` corpus to avoid unnecessary downloads.

## [1.0.1] - 2026-09-16

Initial repository.
