"""Reflex custom component BlossomCarousel.

Thin wrapper around ``@blossom-carousel/react`` — a native-scroll-first carousel
that adds physics-based drag for pointer devices (0 KB on touch).

Upstream: https://github.com/jespervos/blossom-carousel
See the API contract in ``specs/api/component-api-v1.md`` and the design
decisions (DD-001 wrap the React package, DD-004 inject base CSS) in
``specs/technical/architecture.md``.
"""

import json

import reflex as rx
from reflex.event import EventSpec
from reflex.vars import Var

# Pinned npm versions (see specs §8 Compatibilidad y Versionado).
_REACT_PKG = "@blossom-carousel/react@^1.1.1"
_CORE_PKG = "@blossom-carousel/core@^1.1.7"
_CORE_STYLE = "@blossom-carousel/core/style.css"

# Valid `align` values for prev()/next() (specs/api/component-api-v1.md §4).
_ALIGN_VALUES = ("start", "center", "end")


class BlossomCarousel(rx.Component):
    """Wrapper of ``@blossom-carousel/react``'s ``BlossomCarousel``."""

    # The React library to wrap (named export -> is_default = False).
    library = _REACT_PKG
    tag = "BlossomCarousel"
    is_default = False

    # The React runtime + base CSS live in @blossom-carousel/core.
    lib_dependencies: list[str] = [_CORE_PKG]

    # Props mapped to the upstream React component.
    # `as` is a reserved word in Python, so we expose `as_` and rename it
    # back to `as` at compile time via `_rename_props`.
    as_: Var[str] = Var.create("div")  # container HTML tag, e.g. "ul"

    # Cyclic/infinite scroll (experimental upstream).
    repeat: Var[bool] = Var.create(False)

    # Runtime load strategy: "conditional" (0 KB on touch) or "always".
    load: Var[str] = Var.create("conditional")

    # Rename `as_` -> `as` so the compiled prop matches the React API.
    _rename_props: dict[str, str] = {"as_": "as"}

    def add_imports(self) -> dict:
        """Inject the carousel's base stylesheet (DD-004).

        The empty library key produces a side-effect CSS import:
        ``import "@blossom-carousel/core/style.css";``.
        """
        return {"": _CORE_STYLE}

    # ------------------------------------------------------------------ #
    # RF-004: imperative navigation (Strategy A, DD-003).
    #
    # Upstream exposes `prev`/`next` on the React ref handle via
    # `useImperativeHandle`. Reflex attaches that handle to a `useRef` when the
    # component has an `id`, and registers it in the global `refs` map as
    # `refs["ref_<id>"]`. From an event handler we reach the handle there and
    # call its method. Optional chaining (`?.current?.`) makes the call a silent
    # no-op if the runtime has not loaded yet (touch + conditional load).
    # ------------------------------------------------------------------ #

    def prev(self, align: str | None = None) -> EventSpec:
        """Scroll to the previous slide.

        Args:
            align: How to align the target slide ("start", "center", "end").
                ``None`` uses upstream's default alignment.

        Returns:
            An ``EventSpec`` usable as an ``on_click`` handler.
        """
        return self._navigate("prev", align)

    def next(self, align: str | None = None) -> EventSpec:
        """Scroll to the next slide.

        Args:
            align: How to align the target slide ("start", "center", "end").
                ``None`` uses upstream's default alignment.

        Returns:
            An ``EventSpec`` usable as an ``on_click`` handler.
        """
        return self._navigate("next", align)

    def _navigate(self, method: str, align: str | None) -> EventSpec:
        """Build the EventSpec that calls the carousel's ref handle method."""
        ref = self.get_ref()
        if ref is None:
            raise ValueError(
                "blossom_carousel requires an `id` to use prev()/next() "
                "(it is needed to locate the carousel's ref handle)."
            )
        if align is not None and align not in _ALIGN_VALUES:
            raise ValueError(
                f"align must be one of {_ALIGN_VALUES} or None, got {align!r}."
            )
        options = "" if align is None else f"{{ align: {json.dumps(align)} }}"
        return rx.call_script(f'refs["{ref}"]?.current?.{method}({options})')


blossom_carousel = BlossomCarousel.create
