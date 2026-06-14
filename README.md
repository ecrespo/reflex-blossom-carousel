# reflex-blossom-carousel

A [Reflex](https://reflex.dev) custom component that wraps [Blossom Carousel](https://github.com/jespervos/blossom-carousel) — a **native-scroll-first** carousel enhanced with physics-based drag for pointer devices (0 KB on touch).

> Status: **early development / scaffold**. The component wrapper is not implemented yet — this repo currently contains the project base (Reflex installed via `uv`) and the full Spec-Driven Design (SDD) plan under [`specs/`](specs/).

## Why

Reflex has no built-in carousel. Blossom Carousel builds on native browser scrolling (full performance + accessibility) and ships an official React package (`@blossom-carousel/react`, MIT). This project wraps it so you can use it from pure Python in Reflex.

## Planned usage

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

## Installation (once published)

```bash
pip install reflex-blossom-carousel
# or
uv add reflex-blossom-carousel
```

## Development

This project is managed with [`uv`](https://docs.astral.sh/uv/) and pinned to Python 3.13 (Reflex does not yet support 3.14).

```bash
uv sync                       # create the venv and install deps (editable local package)
uv run python -c "import reflex_blossom_carousel"   # smoke test

# run the demo app
cd blossom_carousel_demo
uv run reflex run
```

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
