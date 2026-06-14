# Reflex Blossom Carousel — Component API Spec (v1)

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **PRD** | ../prd/reflex-blossom-carousel.md |

> Nota: este componente es de UI sin backend, por lo que el "API Spec" no describe endpoints HTTP sino el **contrato de la API Python del componente** (props, eventos, métodos y mapeo a la librería React subyacente). El **Data Model** del flujo SDD es **N/A** (no hay persistencia).

---

## 1. Resumen del Contrato

El paquete expone una única función-fábrica principal:

```python
from reflex_blossom_carousel import blossom_carousel
```

`blossom_carousel(*children, **props)` devuelve un `rx.Component` que compila al componente React `BlossomCarousel` de `@blossom-carousel/react`.

## 2. Mapeo a la librería React subyacente

Referencia: `packages/react/src/BlossomCarousel.tsx` de upstream.

| Concepto React (`@blossom-carousel/react`) | Tipo TS | Equivalente Reflex (Python) | Notas |
|---|---|---|---|
| `library` | — | `library = "@blossom-carousel/react@^1.1.1"` | Se ancla a un rango de versión. |
| `tag` | — | `tag = "BlossomCarousel"` | **Export nombrado** → `is_default = False`. |
| `@blossom-carousel/core` | dep | `lib_dependencies = ["@blossom-carousel/core@^1.1.7"]` | Aporta runtime + CSS. |
| `@blossom-carousel/core/style.css` | css | inyectado vía `add_custom_code()` / imports | Estilos base. |
| prop `as` (`ElementType`, def. `"div"`) | `as?` | `as_: rx.Var[str] = "div"` → renderiza prop `as` | `as` es reservada en Python: se usa `as_`. |
| prop `repeat` (def. `false`) | `repeat?: boolean` | `repeat: rx.Var[bool] = False` | Loop cíclico (experimental). |
| prop `load` (`"always"\|"conditional"`) | `load?` | `load: rx.Var[str] = "conditional"` | Estrategia de carga del runtime. |
| props HTML (`className`, etc.) | `HTMLAttributes` | props de estilo/atributos estándar de Reflex | `class_name`, `style`, etc. |
| `children` | `ReactNode[]` | `*children` de Reflex | Slides; admite `rx.foreach`. |
| ref handle `prev({align})` | método | método imperativo (ver §4) | `align ∈ {"start","center","end"}`. |
| ref handle `next({align})` | método | método imperativo (ver §4) | idem. |
| ref handle `element` | `HTMLElement` | no expuesto en v1 | Futuro. |

## 3. Props (contrato Python)

### `blossom_carousel(*children, **props)`

| Prop | Tipo Python | Default | Requerida | Descripción |
|---|---|---|---|---|
| `*children` | `rx.Component` | — | No | Slides del carrusel. Cada hijo debería tener su propia clase/estilo de slide (p. ej. `scroll-snap-align`). |
| `as_` | `rx.Var[str]` | `"div"` | No | Etiqueta HTML del contenedor (`"ul"`, `"div"`, ...). Se compila a la prop React `as`. |
| `repeat` | `rx.Var[bool]` | `False` | No | Activa el scroll cíclico/infinito (experimental en upstream). |
| `load` | `rx.Var[str]` | `"conditional"` | No | `"conditional"`: el runtime de drag solo se carga si se detecta puntero fino (0 KB en táctil). `"always"`: carga siempre. |
| `class_name` | `rx.Var[str]` | — | No | Clase CSS del contenedor (layout, snap, gap). |
| `style` / props de estilo Reflex | — | — | No | Estilos estándar de Reflex. |
| `id` | `rx.Var[str]` | — | Sólo si se usa control imperativo | Necesario para localizar el nodo en v1 (ver §4). |

#### Validación
- `as_`: cadena de etiqueta HTML válida. Valor inválido → el navegador puede fallar al crear el elemento; no se valida en Python (responsabilidad del usuario).
- `load`: debe ser `"always"` o `"conditional"`. Otros valores se pasan tal cual a React (comportamiento upstream: distinto de `"always"` se trata como condicional).

## 4. Métodos imperativos: `prev` / `next`

Blossom expone navegación mediante un *ref handle* de React (`prev`, `next`). En Reflex, los componentes se controlan por estado, no por refs de usuario, por lo que v1 ofrece **dos estrategias**; se elegirá una en el Tech Design tras un spike:

**Estrategia A (recomendada) — método de instancia que emite un script con `ref`:**
```python
carousel = blossom_carousel(*slides, id="my-carousel", as_="ul")
# En un event handler / on_click:
rx.button("Next", on_click=carousel.next(align="center"))
rx.button("Prev", on_click=carousel.prev(align="center"))
```
- `prev(align: str | None = None) -> rx.EventSpec`
- `next(align: str | None = None) -> rx.EventSpec`
- Semántica: hace scroll suave (`behavior: "smooth"`) a la slide anterior/siguiente respetando `align`.

**Estrategia B (fallback) — re-render por estado:** un `rx.Var` de control (`active_index`) que el componente observa mediante un hook `useEffect` y llama a `next/prev` del handle. Más "Reflex-idiomático" pero más código de hooks.

### Contrato de `align`
| Valor | Efecto |
|---|---|
| `"start"` | Alinea la slide destino al inicio del viewport del carrusel. |
| `"center"` | Centra la slide destino. |
| `"end"` | Alinea al final. |
| `None` | Usa el comportamiento por defecto de upstream. |

## 5. Eventos (futuro — no en v1)

Upstream despacha eventos DOM (`scrollend`, overscroll, snap change). Se expondrán como `EventHandler` en una versión posterior:

| Evento Reflex (propuesto) | Trigger DOM | Payload |
|---|---|---|
| `on_snap_change` | snap change | índice/elemento de la slide activa |
| `on_overscroll` | overscroll | dirección/cantidad |
| `on_scroll_end` | `scrollend` | posición de scroll |

## 6. Ejemplo de Integración (objetivo)

```python
import reflex as rx
from reflex_blossom_carousel import blossom_carousel

def index() -> rx.Component:
    carousel = blossom_carousel(
        *[
            rx.el.li(str(i + 1), class_name="slide")
            for i in range(12)
        ],
        id="demo-carousel",
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

CSS del usuario (en `assets/` o `add_custom_code`), equivalente al demo upstream:
```css
.carousel {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 300px;
  gap: 1rem;
  scroll-snap-type: x mandatory;
}
.slide { scroll-snap-align: center; aspect-ratio: 3/4; }
```

## 7. Errores y Casos Borde

| Caso | Comportamiento esperado |
|---|---|
| `prev/next` antes de que cargue el runtime (táctil + conditional) | No-op silencioso (upstream). |
| Sin `children` | Contenedor vacío; sin error. |
| `repeat=True` con pocos slides | Comportamiento experimental de upstream; documentar como tal. |
| SSR (primer render en servidor) | No debe ejecutar código de navegador; runtime solo en cliente. |
| `as_` no soportado por el navegador | Error de DOM en cliente (no validado en Python). |

## 8. Compatibilidad y Versionado

- **SemVer.** v1 del contrato = props `as_`, `repeat`, `load` + métodos `prev`/`next`.
- Anclaje npm: `@blossom-carousel/react@^1.1.1`, `@blossom-carousel/core@^1.1.7`.
- Reflex: `>=0.9.5.post2`.

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |
