# Reflex Blossom Carousel — Technical Design Document

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **PRD Relacionado** | ../prd/reflex-blossom-carousel.md |
| **API Spec Relacionado** | ../api/component-api-v1.md |
| **Reviewers** | — |

---

## 1. Contexto

Reflex permite envolver componentes React y exponerlos como componentes Python mediante subclases de `rx.Component`, declarando `library` (paquete npm), `tag` (nombre del componente) y `Var`s tipados para las props. Al compilar, Reflex genera el frontend (React + Vite) y traduce `snake_case` → `camelCase`.

Blossom Carousel publica un componente React oficial (`@blossom-carousel/react`, export **nombrado** `BlossomCarousel`) que internamente importa dinámicamente `@blossom-carousel/core` (la lógica vanilla + CSS) **solo en cliente** y solo cuando detecta un puntero fino. Expone un `forwardRef` con handle imperativo (`prev`, `next`, `element`). Por tanto, el wrapping en Reflex tiene tres retos técnicos: (1) cargar el CSS base, (2) evitar problemas de SSR/hidratación, y (3) traducir el control imperativo `prev/next` al modelo de eventos de Reflex.

La decisión central es **envolver el paquete React de upstream** (no el `core` vanilla), porque encaja directamente con el modelo de Reflex y minimiza el código a mantener.

## 2. Objetivos Técnicos

- **Correctitud:** El componente compila y renderiza sin errores de hidratación; props mapeadas fielmente a upstream.
- **Rendimiento:** No degradar el "0 KB en táctil"; no bloquear el render inicial.
- **Mantenibilidad:** Wrapper pequeño (<150 líneas), tipado, con tests de compilación; alineado a versiones npm ancladas.
- **Operabilidad:** Build y publish reproducibles con `uv` + `reflex component build`; CI con tests.

## 3. Arquitectura Propuesta

### 3.1 Diagrama de Alto Nivel

```
┌──────────────────────┐     compila      ┌───────────────────────────┐
│  App Reflex (Python)  │ ───────────────▶ │  Frontend React/Vite       │
│  blossom_carousel(...)│                  │  <BlossomCarousel as=...>  │
└──────────┬───────────┘                  └─────────────┬──────────────┘
           │ usa                                          │ importa (dyn, client-only)
           ▼                                              ▼
┌──────────────────────┐                  ┌───────────────────────────┐
│ reflex_blossom_       │  library/tag     │ @blossom-carousel/react    │
│ carousel (wrapper)    │ ───────────────▶ │  + @blossom-carousel/core  │
│  rx.Component         │  lib_dependencies│  (+ core/style.css)        │
└──────────────────────┘                  └───────────────────────────┘
```

### 3.2 Componentes

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| `reflex_blossom_carousel` (wrapper) | Python / Reflex `rx.Component` | Declarar library/tag/props, inyectar CSS, manejar SSR y prev/next |
| `@blossom-carousel/react` | npm / React | Componente React oficial (drag + scroll nativo) |
| `@blossom-carousel/core` | npm / TS + CSS | Lógica vanilla y estilos base |
| App demo `blossom_carousel_demo` | Reflex | Probar el componente en una app real |
| Empaquetado | `uv` + setuptools + `reflex component build` | Construir y publicar el paquete Python |

### 3.3 Flujo de Datos

**Flujo: render + drag**
```
1. Python: blossom_carousel(*slides, as_="ul", repeat=False, load="conditional")
2. Reflex compila a <BlossomCarousel as="ul" repeat={false} load="conditional"> con children
3. Reflex inyecta import de @blossom-carousel/core/style.css en la página
4. En cliente, BlossomCarousel detecta puntero fino; si aplica, importa core dinámicamente e init()
5. El contenedor obtiene el atributo blossom-carousel y habilita drag + scroll-snap
```

**Flujo: prev/next (Estrategia A — ver Tech Design §4 DD-003)**
```
1. on_click del botón emite un EventSpec que ejecuta JS en cliente
2. El JS obtiene el handle/elemento del carrusel (por id/ref) y llama prev/next({align})
3. core hace scrollTo({ behavior: "smooth" }) a la slide destino
```

**Flujo de error / compensación:**
```
1. Si el runtime aún no cargó → prev/next es no-op (sin excepción)
2. Si SSR intenta ejecutar código de navegador → se evita con NoSSRComponent/carga dinámica
3. Si falta el CSS → el carrusel funciona pero sin layout; se mitiga inyectando CSS por defecto
```

## 4. Decisiones de Diseño

### DD-001: Envolver `@blossom-carousel/react` en lugar de `@blossom-carousel/core`

- **Decisión:** Wrappear el paquete React oficial.
- **Contexto:** `core` es vanilla JS (no expone componente React); `react` ya provee `<BlossomCarousel>` con lifecycle, SSR-guard y ref handle.
- **Alternativas evaluadas:**

| Opción | Pros | Contras |
|---|---|---|
| **A. Envolver `@blossom-carousel/react` (elegida)** | Encaja con el modelo de Reflex; menos código; SSR/drag ya resueltos por upstream | Una capa npm extra; dependes de su API |
| B. Envolver `@blossom-carousel/core` (vanilla) | Sin capa React intermedia | Hay que reimplementar init/destroy/useEffect/ref en hooks de Reflex; más superficie a mantener |

- **Justificación:** Minimiza esfuerzo y riesgo; upstream ya mantiene el wrapper React.
- **Consecuencias:** El wrapper Reflex es una fina traducción de props; el versionado sigue a `@blossom-carousel/react`.

### DD-002: Manejo de SSR

- **Decisión:** Asegurar que el componente no ejecute código de navegador en SSR. Si el render server-side de `<BlossomCarousel>` causa problemas, subclasear `NoSSRComponent`; si no, basta con que upstream haga el trabajo en `useEffect` (solo cliente).
- **Contexto:** Reflex hace SSR; Blossom hace `import("@blossom-carousel/core")` dentro de `useEffect` (solo cliente) y guarda `window.matchMedia`. Eso ya es SSR-safe para la lógica, pero el componente debe poder renderizar su shell en servidor.
- **Alternativas evaluadas:**

| Opción | Pros | Contras |
|---|---|---|
| **A. `rx.Component` normal y validar (elegida si funciona)** | Permite SSR del shell (mejor SEO/markup) | Hay que verificar que no rompa hidratación |
| B. `NoSSRComponent` | Evita cualquier ejecución en server; simple y seguro | Pierde markup en SSR; flash de contenido |

- **Justificación:** Probar A en el spike; degradar a B si hay errores de hidratación.
- **Consecuencias:** Decisión final se cierra en F2 con `reflex run`.

### DD-003: Control imperativo `prev`/`next`

- **Decisión:** Exponer `prev(align)`/`next(align)` como métodos que devuelven un `EventSpec` que ejecuta JS en cliente sobre el elemento del carrusel (vía `id`/ref). Mantener Estrategia B (control por estado + hooks) como fallback documentado.
- **Contexto:** Reflex no usa refs de usuario como React; necesita un puente. El handle de upstream (`prev/next`) está en el ref del componente React, no directamente en el DOM, lo que complica A. El spike decidirá si se accede al handle (guardándolo en una variable global por id) o si se reimplementa prev/next llamando a `core` sobre el `element`.
- **Alternativas evaluadas:**

| Opción | Pros | Contras |
|---|---|---|
| **A. EventSpec + JS sobre el carrusel (elegida)** | API limpia (`carousel.next()`); idiomático en botones | Necesita puente JS para alcanzar el handle/ref |
| B. Var de control + `useEffect` (hooks) | 100% por estado de Reflex | Más código de hooks; re-render por cambios de índice |
| C. No exponer prev/next en v1 | Mínimo esfuerzo | Pierde un requisito SHOULD valioso |

- **Justificación:** A da la mejor DX; B queda como red de seguridad. Si A y B exceden el presupuesto de v0.1.0, se difiere a v0.2 (riesgo aceptado: RF-004 es `SHOULD`).
- **Consecuencias:** Posible necesidad de `add_hooks`/`add_custom_code` para registrar handles por `id`.

### DD-004: Inyección del CSS base

- **Decisión:** Importar `@blossom-carousel/core/style.css` vía `add_custom_code()` (o el sistema de imports/assets de Reflex) dentro del componente.
- **Justificación:** Garantiza estilos sin pasos manuales (RF-003).
- **Consecuencias:** El CSS se incluye una vez por página donde se use el componente.

### DD-005: Gestión con `uv` sobre el scaffold de `reflex component`

- **Decisión:** Usar el scaffold oficial `reflex component init` (estructura `custom_components/`, demo app) pero gestionar entorno/dependencias/lock con `uv` (`uv.lock`, `uv sync`), manteniendo el `pyproject.toml` setuptools generado.
- **Justificación:** Combina el layout estándar publicable con la velocidad/reproducibilidad de `uv`.
- **Consecuencias:** Build con `reflex component build`; publish con `uv publish`.

## 5. Patrones y Convenciones

### 5.1 Estructura del Código

```
reflex-blossom-carousel/
├── pyproject.toml                 # setuptools build backend; gestionado con uv
├── uv.lock                        # lockfile de uv
├── .python-version                # 3.13
├── README.md
├── specs/                         # Specs SDD (este conjunto de documentos)
│   ├── prd/
│   ├── api/
│   ├── technical/
│   └── plans/
├── custom_components/
│   └── reflex_blossom_carousel/
│       ├── __init__.py            # re-exporta blossom_carousel
│       └── blossom_carousel.py    # el wrapper rx.Component
├── blossom_carousel_demo/         # app demo Reflex
│   ├── rxconfig.py
│   ├── requirements.txt
│   └── blossom_carousel_demo/
└── tests/                         # tests del wrapper (compilación/render)
```

### 5.2 Patrones Aplicados

| Patrón | Dónde | Por qué |
|---|---|---|
| Wrapper/Adapter | `blossom_carousel.py` | Adaptar API React a API Reflex |
| Factory (`Component.create`) | `blossom_carousel = BlossomCarousel.create` | Convención de Reflex |
| Anclaje de versión | `library`/`lib_dependencies` | Estabilidad ante cambios upstream |

### 5.3 Esqueleto del Wrapper (objetivo, no final)

```python
import reflex as rx

class BlossomCarousel(rx.Component):
    """Wrapper de @blossom-carousel/react."""

    library = "@blossom-carousel/react@^1.1.1"
    tag = "BlossomCarousel"
    is_default = False
    lib_dependencies: list[str] = ["@blossom-carousel/core@^1.1.7"]

    # Props (as -> as_ por palabra reservada)
    as_: rx.Var[str] = "div"          # se renderiza como prop React `as`
    repeat: rx.Var[bool] = False
    load: rx.Var[str] = "conditional"

    def add_custom_code(self) -> list[str]:
        return ['import "@blossom-carousel/core/style.css";']

    # prev/next: ver DD-003 (spike). Posible add_hooks/add_custom_code.

blossom_carousel = BlossomCarousel.create
```

> El mapeo `as_` → `as` se hará con el mecanismo de alias de props de Reflex (p. ej. anotando el nombre real de la prop). Se valida en el spike de F2.

### 5.4 Manejo de Errores
No hay jerarquía de excepciones de dominio (componente de UI). Los fallos posibles son de compilación/hidratación y se detectan en tests/CI y `reflex run`.

## 6. Seguridad

### 6.1 Superficie de Ataque
| Vector | Mitigación |
|---|---|
| Dependencia npm comprometida (supply chain) | Anclar versiones; revisar CHANGELOG; lockfiles del frontend de Reflex |
| XSS por contenido de slides | Responsabilidad del usuario; Reflex escapa contenido por defecto |

### 6.2 Datos Sensibles
N/A — el componente no maneja ni almacena datos sensibles.

## 7. Observabilidad
Runtime: N/A (UI sin backend). Desarrollo/CI: tests de compilación y render como señal de salud; logs de `reflex run` durante el spike.

## 8. Testing Strategy

| Nivel | Cobertura Target | Herramientas | Qué cubre |
|---|---|---|---|
| Unit | > 80 % del wrapper | pytest | Que la clase declara library/tag/props correctos; render a dict/JS contiene `BlossomCarousel`, `as`, `repeat`, `load` |
| Compilación | Build del frontend | `reflex export`/compilación en CI | Que la app demo compila con el componente |
| Manual/E2E | Happy paths | `reflex run` + navegador | Drag en desktop, scroll en táctil, prev/next |
| Build/Publish | Artefactos | `reflex component build` (dry-run) | Que el paquete se construye |

## 9. Plan de Migración / Rollout

### 9.1 Estrategia de Deployment (publicación)
- [ ] Publicar `v0.1.0` en TestPyPI primero, validar instalación.
- [ ] Publicar en PyPI.
- [ ] `reflex component share` para la galería.

### 9.2 Backward Compatibility
- API v1 (`as_`, `repeat`, `load`, `prev`, `next`) estable bajo SemVer.
- Cambios de upstream se absorben subiendo el rango npm en `minor`/`patch`.

## 10. Preguntas Abiertas
- [ ] ¿`rx.Component` normal basta para SSR o se requiere `NoSSRComponent`? — Owner: Ernesto, F2.
- [ ] ¿Cómo alcanzar el ref handle de upstream para `prev/next` de forma robusta? — Owner: Ernesto, F2 (spike).
- [ ] ¿Mecanismo exacto de alias `as_`→`as` en la versión de Reflex usada? — Owner: Ernesto, F2.
- [ ] ¿Incluir CSS de demo por defecto o dejarlo 100% al usuario? — Owner: Ernesto, F3.

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |
