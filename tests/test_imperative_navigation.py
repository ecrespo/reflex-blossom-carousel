"""Tests for RF-004: imperative prev()/next() navigation.

The carousel exposes `prev(align)` / `next(align)` methods that return an
`rx.EventSpec`. The spec runs JS on the client that reaches the upstream React
ref handle (`{prev, next, element}`) registered in the global `refs` map by id,
and calls its `prev`/`next` method with an optional `{ align }` option.

See specs/api/component-api-v1.md §4 and specs/technical/architecture.md DD-003.
"""

import pytest

from reflex.event import EventSpec

from reflex_blossom_carousel import blossom_carousel


def _script(spec: EventSpec) -> str:
    """Extract the raw (unescaped) JS payload from a call_script EventSpec."""
    return spec.args[0][1]._var_value


def test_next_returns_event_spec():
    carousel = blossom_carousel(id="demo")
    assert isinstance(carousel.next(), EventSpec)


def test_prev_returns_event_spec():
    carousel = blossom_carousel(id="demo")
    assert isinstance(carousel.prev(), EventSpec)


def test_next_reaches_handle_via_global_ref_by_id():
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.next())
    ref = carousel.get_ref()  # e.g. "ref_demo"
    assert ref is not None
    assert f'refs["{ref}"]' in js
    assert ".current" in js
    assert ".next(" in js


def test_prev_reaches_handle_prev_method():
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.prev())
    assert ".prev(" in js


def test_next_with_align_passes_align_option():
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.next(align="center"))
    assert ".next(" in js
    assert "align" in js
    assert "center" in js


def test_prev_with_align_passes_align_option():
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.prev(align="start"))
    assert ".prev(" in js
    assert "start" in js


def test_next_without_align_omits_options():
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.next())
    assert "align" not in js
    assert ".next()" in js


def test_optional_chaining_makes_call_a_noop_before_runtime_loads():
    # RF-004 flujo alternativo: if the handle isn't ready yet (touch +
    # conditional load), the call must be a silent no-op, not throw.
    carousel = blossom_carousel(id="demo")
    js = _script(carousel.next(align="center"))
    assert "?.current" in js


def test_missing_id_raises_clear_error():
    carousel = blossom_carousel()  # no id -> no ref to target
    with pytest.raises(ValueError, match="id"):
        carousel.next()


def test_invalid_align_raises():
    carousel = blossom_carousel(id="demo")
    with pytest.raises(ValueError, match="align"):
        carousel.next(align="middle")
