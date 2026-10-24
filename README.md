# reflex-blossom-carousel

A [Reflex](https://reflex.dev) custom component that wraps [Blossom Carousel](https://github.com/jespervos/blossom-carousel) — a **native-scroll-first** carousel enhanced with physics-based drag for pointer devices (0 KB on touch).

> Status: **beta**. The component wrapper is implemented and tested. Design and API are documented under [`specs/`](specs/) following Spec-Driven Design (SDD).

## Why

Reflex has no built-in carousel. Blossom Carousel builds on native browser scrolling (full performance + accessibility) and ships an official React package (`@blossom-carousel/react`, MIT). This project wraps it so you can use it from pure Python in Reflex.

## Usage

```python
import reflex as rx
from reflex_blossom_carousel import blossom_carousel

def index() -> rx.Component:
    carousel = blossom_carousel(
        *[rx.el.li(str(i + 1), class_name="slide") for i in range(12)],
        as_="ul",
        class_name="carousel",
        repeat=False,
        load="conditional",
    )
    return rx.vstack(
        carousel,
        rx.hstack(
            rx.button("Previous", on_click=carousel.prev(align="center")),
            rx.button("Next", on_click=carousel.next(align="center")),
        ),
    )
```

See the full API in [`specs/api/component-api-v1.md`](specs/api/component-api-v1.md).

## Installation

```bash
pip install reflex-blossom-carousel
# or
uv add reflex-blossom-carousel
```

Requires Python ≥ 3.11 and Reflex ≥ 0.10.0. For Reflex 0.9.x, pin `reflex-blossom-carousel==0.1.1`.

## Development

Requires **Python ≥ 3.11** and **Reflex ≥ 0.10.0**. This project is managed with [`uv`](https://docs.astral.sh/uv/); local development uses Python 3.13 (`.python-version`), and CI also checks 3.11 and 3.14.

```bash
uv sync --all-extras          # create the venv and install deps (editable local package)
uv run pytest                 # unit tests
uv run python -c "import reflex_blossom_carousel"   # smoke test

# run the demo app
cd blossom_carousel_demo
uv run reflex run
```

### Building and releasing

Reflex 0.10 removed the `reflex component` CLI (`init` / `build` / `publish` / `share`). The package is now built with standard tooling:

```bash
# Regenerate the .pyi type stubs (only needed when the component's props change)
uv run python -m reflex_base.utils.pyi_generator custom_components/reflex_blossom_carousel

uv build                      # sdist + wheel in dist/ (the wheel ships the .pyi stub)
uv publish                    # upload to PyPI (token via UV_PUBLISH_TOKEN or ~/.pypirc + twine)
```

Bump `version` in `pyproject.toml` for every release. See [`CHANGELOG.md`](CHANGELOG.md).

Project layout:

```
custom_components/reflex_blossom_carousel/   # the wrapper (rx.Component)
blossom_carousel_demo/                       # demo Reflex app
specs/                                        # SDD documents (PRD, API, tech design, plan)
```

## Specs (Spec-Driven Design)

See [`specs/README.md`](specs/README.md) for the index: PRD, Component API Spec, Technical Design, and Implementation Plan.

## Credits & License

- Wraps [`@blossom-carousel/react`](https://www.npmjs.com/package/@blossom-carousel/react) and [`@blossom-carousel/core`](https://www.npmjs.com/package/@blossom-carousel/core) by Jesper Vos (MIT).
- This wrapper is licensed under **Apache-2.0** (Reflex custom component default).
