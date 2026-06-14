# Análisis del repositorio upstream: `jespervos/blossom-carousel`

| Campo | Valor |
|---|---|
| **Fecha** | 2026-06-14 |
| **Repo** | https://github.com/jespervos/blossom-carousel |
| **Sitio/Docs** | https://blossom-carousel.com |
| **Licencia** | Apache-2.0 (repo) / MIT (paquetes npm publicados) |

## 1. Qué es

Blossom Carousel es, según su README, "el primer carrusel que se construye sobre el scroll nativo del navegador en lugar de reemplazarlo". Añade una pequeña mejora de arrastre (drag con física) para dispositivos con puntero, manteniendo el modelo de interacción, rendimiento y accesibilidad de un contenedor de scroll real.

Características clave:
- **Scroll nativo** (rendimiento y accesibilidad completos).
- **Drag** con física para punteros.
- **Sin abstracción**: usa las APIs web nativas (scroll-snap, position sticky, scroll-driven animations).
- **0 KB en táctil**: el runtime solo se carga si se detecta un puntero fino.
- **Framework ready**: componentes para React, Vue, Svelte y Web Components.
- **Scroll cíclico** experimental (loop infinito).

## 2. Estructura (monorepo pnpm + turbo)

```
packages/
├── core/     @blossom-carousel/core   (TS vanilla + CSS)   v1.1.7
├── react/    @blossom-carousel/react  (wrapper React)      v1.1.1
├── vue/      @blossom-carousel/vue
├── svelte/   @blossom-carousel/svelte
└── web/      @blossom-carousel/web    (web component)
```

Lenguajes: TypeScript 74 %, CSS 10 %, JS 6 %, Vue/Svelte/HTML el resto. Tooling: pnpm workspaces, turbo, vitest.

## 3. `@blossom-carousel/core` (la base)

- Export principal: `Blossom(scroller: HTMLElement, options: CarouselOptions)` → devuelve un objeto con (al menos) `init()`, `destroy()`, `prev(options)`, `next(options)`.
- `CarouselOptions`: `{ repeat?: boolean }`.
- `AlignOption = "start" | "center" | "end"`.
- `prev/next({ align })`: calculan la posición destino y hacen `scroller.scrollTo({ left, behavior: "smooth" })`.
- Usa `ResizeObserver`, `MutationObserver`, `StyleObserver`, intercepta `scrollIntoView`, y registra listeners de `pointerdown`/`wheel` solo cuando hay overflow.
- En `init()` marca el contenedor con el atributo `blossom-carousel="true"` y añade `has-overflow` cuando corresponde.
- Importa su propio `style.css` (estilos base del carrusel).

Conclusión: `core` **no expone un componente React** — es JS vanilla. Por eso, para Reflex conviene envolver el paquete React, no el core (ver Tech Design DD-001).

## 4. `@blossom-carousel/react` (lo que envolveremos)

Archivo: `packages/react/src/BlossomCarousel.tsx`.

- Es un `forwardRef` (export **nombrado** `BlossomCarousel`, vía `index.ts`).
- **Props** (`BlossomCarouselProps extends React.HTMLAttributes<HTMLElement>`):
  - `as?: ElementType` (default `"div"`) — etiqueta del contenedor.
  - `repeat?: boolean` (default `false`).
  - `load?: "always" | "conditional"` (default `"conditional"`).
  - `children?: ReactNode | ReactNode[]`.
  - más atributos HTML estándar (`className`, etc.).
- **Comportamiento** (`useEffect`):
  - Detecta puntero fino con `window.matchMedia("(hover: hover) and (pointer: fine)")`.
  - Si no hay mouse y `load !== "always"`, no carga nada (0 KB en táctil).
  - Importa dinámicamente `@blossom-carousel/core` (solo cliente), crea `Blossom(el, { repeat })` y llama `init()`.
  - En cleanup llama `destroy()`.
- **Handle imperativo** (`useImperativeHandle`): `{ prev(options?), next(options?), element }`.
- Depende de `@blossom-carousel/core` y de `@blossom-carousel/core/style.css` (el demo lo importa explícitamente).
- `peerDependencies`: `react >= 18`, `react-dom >= 18`.

### Ejemplo de uso (demo `App.tsx`)
```tsx
<BlossomCarousel ref={carouselRef} as="ul" className="carousel">
  {Array.from({ length: 12 }, (_, i) => (
    <li key={`slide${i+1}`} className="slide">{i + 1}</li>
  ))}
</BlossomCarousel>
// carouselRef.current?.next({ align: "center" })
```

## 5. Implicaciones para el wrapper Reflex

| Hallazgo | Implicación en Reflex |
|---|---|
| Export nombrado `BlossomCarousel` | `is_default = False`, `tag = "BlossomCarousel"` |
| Depende de `@blossom-carousel/core` | `lib_dependencies = ["@blossom-carousel/core@^1.1.7"]` |
| Necesita `core/style.css` | Inyectar vía `add_custom_code()` |
| Carga dinámica solo en cliente | Compatible con SSR; validar hidratación (posible `NoSSRComponent`) |
| Prop `as` | Exponer como `as_` y mapear a `as` (palabra reservada en Python) |
| Control vía ref handle (`prev/next`) | Necesita puente al modelo de eventos de Reflex (spike) |
| 0 KB en táctil | Mantener prop `load` para no perder esta ventaja |

## 6. Versiones de referencia (a anclar)

- `@blossom-carousel/react@^1.1.1`
- `@blossom-carousel/core@^1.1.7`
