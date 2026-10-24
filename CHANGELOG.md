# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-10-24

### Added
- `Publish` workflow: pushing a `v*` tag publishes to PyPI via Trusted Publishing and creates the GitHub Release.

## [0.2.0] - 2026-10-24

### Changed
- Require **Reflex >= 0.10.0** (previously `>=0.9.5.post2`).
- Require **Python >= 3.11** (Reflex 0.10 dropped Python 3.10). Python 3.11–3.14 are supported.
- Build with `uv build`: Reflex 0.10 removed the `reflex component` CLI. Type stubs are regenerated with `python -m reflex_base.utils.pyi_generator`.
- Demo app: pinned to `reflex==0.10.0`, enables `rx.plugins.RadixThemesPlugin()` explicitly (implicit Radix enablement is deprecated) and refreshes the frontend lockfile.

### Fixed
- Demo `requirements.txt` had both requirements on a single line (`reflex==…reflex-blossom-carousel`), which made it uninstallable.

### Added
- GitHub Actions CI: tests on Python 3.11 / 3.13 / 3.14, wheel build with stub check, and demo app compilation.

The component API (`as_`, `repeat`, `load`, `prev()`, `next()`) is unchanged.
Users on Reflex 0.9.x should stay on `reflex-blossom-carousel==0.1.1`.

## [0.1.1]

### Added
- Type stubs (`.pyi`) for `BlossomCarousel`.

## [0.0.1]

- Initial release.
