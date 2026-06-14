# Reflex Blossom Carousel

## Product Requirements Document (PRD)

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **Reviewers** | — |
| **Última actualización** | 2026-06-14 |

---

## 1. Resumen Ejecutivo

`reflex-blossom-carousel` es una librería de componentes para [Reflex](https://reflex.dev) que envuelve [Blossom Carousel](https://github.com/jespervos/blossom-carousel), un carrusel "native-first" que se apoya en el scroll nativo del navegador en lugar de reemplazarlo, añadiendo arrastre (drag) con física para dispositivos con puntero fino (mouse/trackpad). El objetivo es permitir que desarrolladores que construyen apps full-stack en **Python con Reflex** usen este carrusel sin escribir JavaScript ni React, exponiendo una API idiomática de Reflex (`blossom_carousel(...)`).

Está dirigido a desarrolladores Python que usan Reflex y necesitan un carrusel accesible, performante y configurable por CSS. Resuelve el problema de que Reflex no incluye un carrusel nativo y los existentes en el ecosistema React suelen ser pesados o reemplazan el scroll nativo (perdiendo accesibilidad y rendimiento).

El entregable se publicará como paquete Python en PyPI bajo el nombre `reflex-blossom-carousel`, siguiendo el flujo oficial de *Custom Components* de Reflex.

## 2. Contexto y Problema

### 2.1 Situación Actual
Reflex ofrece componentes de layout y `rx.scroll_area`, pero no un carrusel con snap + drag listo para usar. Los desarrolladores que quieren un carrusel deben envolver manualmente una librería React (Embla, Swiper, Splide), lo cual exige conocer el modelo de *wrapping* de Reflex, manejar SSR, CSS e imports.

### 2.2 Problema
- No existe un carrusel oficial ni una librería de la comunidad madura para Reflex.
- Las librerías React populares (Swiper/Slick) reemplazan el scroll nativo, penalizando accesibilidad y rendimiento, y suelen pesar decenas de KB.
- Envolver React desde cero en Reflex tiene fricción: SSR (`NoSSRComponent`), imports de CSS, props `camelCase` vs `snake_case`, y métodos imperativos vía `ref`.

### 2.3 Oportunidad
Blossom Carousel ya publica un paquete React oficial (`@blossom-carousel/react`, MIT) con una API mínima y clara (`as`, `repeat`, `load`, métodos `prev`/`next` vía ref) y pesa 0 KB en dispositivos táctiles. Es un candidato ideal para envolver en Reflex: poca superficie de API, buena base de accesibilidad y configuración 100% por CSS. Publicarlo como custom component da visibilidad en la galería de Reflex y en PyPI.

## 3. Usuarios Objetivo

### Persona 1: Desarrollador Reflex full-stack
- **Descripción:** Desarrollador Python que construye dashboards, landings o apps de datos con Reflex y no quiere salir de Python.
- **Necesidad principal:** Insertar un carrusel de tarjetas/imágenes con snap y drag, controlable desde el estado de Reflex.
- **Frecuencia de uso:** Eventual por proyecto, recurrente en su día a día.
- **Nivel técnico:** Medio/Alto en Python, Bajo/Medio en JS/React.

### Persona 2: Mantenedor de la librería (open source)
- **Descripción:** Autor/contribuidor del paquete (Ernesto Crespo).
- **Necesidad principal:** Mantener el wrapper alineado con upstream, publicar en PyPI, documentar.
- **Frecuencia de uso:** Recurrente durante releases.
- **Nivel técnico:** Alto.

## 4. Objetivos y Métricas de Éxito

### 4.1 Objetivos del Negocio (proyecto OSS)

| Objetivo | Métrica | Target | Plazo |
|---|---|---|---|
| Publicar el paquete | Release en PyPI | v0.1.0 disponible | +2 semanas |
| Adopción inicial | Descargas / stars | 50 descargas/mes, 10 stars | +3 meses |
| Calidad | Cobertura de tests del wrapper | > 80 % | v0.1.0 |
| Alineación con upstream | Desfase de versión vs `@blossom-carousel/react` | <= 1 minor | Continuo |

### 4.2 Objetivos de Usuario

| Objetivo del Usuario | Indicador |
|---|---|
| Añadir un carrusel en < 5 min | `pip install` + 10 líneas y funciona |
| Controlar prev/next desde Python | Botones que llaman a métodos del carrusel |
| Sin tocar JS/CSS para empezar | Estilos por defecto importados automáticamente |

## 5. Alcance

### 5.1 In Scope (Incluido)
- [ ] Componente `blossom_carousel` que envuelve `@blossom-carousel/react` (export nombrado `BlossomCarousel`).
- [ ] Props soportadas: `as_` (etiqueta HTML del contenedor), `repeat` (loop cíclico), `load` (`"always"`/`"conditional"`), más props HTML estándar y estilos de Reflex.
- [ ] Renderizado de slides como `children` de Reflex (incluye `rx.foreach`).
- [ ] Importación automática del CSS base de Blossom (`@blossom-carousel/core/style.css`).
- [ ] Manejo correcto de SSR (carga del runtime solo en cliente).
- [ ] Control imperativo `prev()` / `next()` (con `align`) desde el estado de Reflex.
- [ ] App demo funcional + documentación (README con ejemplos).
- [ ] Tests del wrapper (compilación/render) y CI.
- [ ] Empaquetado y publicación en PyPI (`reflex component build` + `uv publish`).

### 5.2 Out of Scope (Excluido)
- Reescribir la física/lógica del carrusel — se reutiliza el paquete upstream tal cual.
- Mantener wrappers para Vue/Svelte/Web Components (upstream ya los provee).
- Theming visual propio: la configuración es por CSS del usuario, como en upstream.
- Soporte para versiones de Reflex < 0.9.5.

### 5.3 Futuras Consideraciones
- Exponer eventos de scroll/snap (`on_snap_change`, `overscroll`) como `EventHandler` de Reflex cuando upstream estabilice esos eventos.
- Helpers de alto nivel (p. ej. `blossom_carousel.item(...)`, indicadores/paginación).
- Modo "cyclical/infinite" documentado y testeado (hoy experimental en upstream).

## 6. Requisitos Funcionales

### RF-001: Renderizar un carrusel con slides
- **Descripción:** El sistema debe renderizar un contenedor de scroll Blossom con los hijos pasados como slides.
- **Actor:** Desarrollador Reflex.
- **Precondiciones:** Paquete instalado e importado.
- **Flujo principal:**
  1. El desarrollador llama `blossom_carousel(*slides, as_="ul")`.
  2. Reflex compila el componente React `BlossomCarousel` con sus hijos.
  3. En cliente, Blossom inicializa el contenedor (atributo `blossom-carousel`).
- **Flujo alternativo:** En dispositivos táctiles con `load="conditional"`, no se carga el runtime de drag (0 KB) pero el scroll nativo funciona.
- **Postcondiciones:** El carrusel es desplazable y, en puntero fino, arrastrable.
- **Prioridad:** `MUST`

### RF-002: Configurar comportamiento vía props
- **Descripción:** El sistema debe aceptar `repeat`, `load` y `as_` y mapearlas a las props React (`repeat`, `load`, `as`).
- **Actor:** Desarrollador Reflex.
- **Precondiciones:** RF-001.
- **Flujo principal:** Se pasan props en Python; Reflex las transforma a `camelCase`/alias correctos; `as_` se mapea a la prop reservada `as`.
- **Postcondiciones:** El componente refleja la configuración.
- **Prioridad:** `MUST`

### RF-003: Importar el CSS base automáticamente
- **Descripción:** El sistema debe inyectar `@blossom-carousel/core/style.css` para que el carrusel se vea correctamente sin pasos manuales.
- **Actor:** Sistema.
- **Flujo principal:** El componente añade el import del CSS vía `add_custom_code`/imports.
- **Postcondiciones:** Estilos base presentes en la página.
- **Prioridad:** `MUST`

### RF-004: Control imperativo prev/next desde el estado
- **Descripción:** El sistema debe permitir invocar `prev`/`next` (con `align` opcional) del carrusel desde un event handler de Reflex.
- **Actor:** Desarrollador Reflex.
- **Precondiciones:** RF-001; referencia al componente disponible.
- **Flujo principal:**
  1. El desarrollador obtiene una `ref` del carrusel.
  2. Un `on_click` de botón dispara una llamada al método `prev`/`next` del handle expuesto por `@blossom-carousel/react`.
  3. El carrusel hace scroll suave a la diapositiva destino.
- **Flujo alternativo:** Si el runtime aún no cargó (táctil + conditional), la llamada es no-op.
- **Postcondiciones:** El carrusel navega a la slide objetivo.
- **Prioridad:** `SHOULD`

### RF-005: App demo y documentación
- **Descripción:** El sistema debe incluir una app demo y un README con ejemplos copiables.
- **Prioridad:** `MUST`

## 7. Requisitos No Funcionales

### Rendimiento
- 0 KB de runtime de drag en dispositivos táctiles cuando `load="conditional"` (heredado de upstream).
- La inicialización no debe bloquear el render (carga dinámica del runtime en cliente).

### Accesibilidad
- Mantener el scroll nativo y la navegación por teclado del contenedor (heredado de upstream). No introducir regresiones de accesibilidad en el wrapper.

### Compatibilidad
- Python >= 3.10. Reflex >= 0.9.5.post2. React >= 18 (lo aporta Reflex en el frontend).
- Funcionar con SSR de Reflex sin errores de hidratación.

### Mantenibilidad
- Cobertura de tests del wrapper > 80 %. Código tipado. Versionado semántico.

### Observabilidad
- N/A en runtime (componente de UI sin backend). CI con tests verdes como gate.

## 8. Restricciones y Dependencias

### Restricciones Técnicas
- El wrapper depende de la API pública de `@blossom-carousel/react` (props `as`/`repeat`/`load`, ref handle `prev`/`next`/`element`).
- El CSS base vive en `@blossom-carousel/core`; debe importarse aparte.

### Restricciones de Negocio
- Licencias: upstream React es **MIT**; el paquete Reflex se publica como **Apache-2.0** (default de Reflex) reconociendo la atribución a upstream.

### Dependencias Externas

| Dependencia | Tipo | Owner | Estado | Riesgo |
|---|---|---|---|---|
| `@blossom-carousel/react` | npm (runtime frontend) | Jesper Vos | v1.1.1, MIT | Cambios de API en upstream |
| `@blossom-carousel/core` | npm (CSS + runtime) | Jesper Vos | v1.1.7, MIT | Idem |
| Reflex | Framework Python | Reflex Labs | 0.9.5.post2 | Cambios en API de wrapping |
| PyPI | Registro de paquetes | PSF | Activo | Bajo |
| GitHub + gh CLI | Hosting/repos | GitHub | Activo | Requiere auth del usuario |

## 9. User Stories

### Épica: Carrusel Blossom en Reflex

**US-001:** Como desarrollador Reflex, quiero `blossom_carousel(...)` con mis slides, para mostrar un carrusel sin escribir JS.
- Criterios de aceptación:
  - [ ] `blossom_carousel(*items, as_="ul")` compila y renderiza.
  - [ ] El CSS base se carga automáticamente.

**US-002:** Como desarrollador Reflex, quiero pasar `repeat` y `load`, para controlar loop y la estrategia de carga.
- Criterios de aceptación:
  - [ ] `repeat=True` activa el modo cíclico.
  - [ ] `load="always"` carga el runtime también en táctil.

**US-003:** Como desarrollador Reflex, quiero botones Prev/Next conectados al estado, para navegar el carrusel desde Python.
- Criterios de aceptación:
  - [ ] Un `on_click` puede invocar `prev`/`next` con `align`.

**US-004:** Como usuario del paquete, quiero instrucciones claras, para instalar y usar en minutos.
- Criterios de aceptación:
  - [ ] README con `pip install reflex-blossom-carousel` y ejemplo mínimo.

## 10. Wireframes / Mockups
Descripción textual: una fila horizontal de tarjetas con `scroll-snap`, padding lateral, y (en desktop) cursor de arrastre. Dos botones "Previous"/"Next" debajo. Equivalente visual al demo React de upstream (`packages/react/src/App.tsx`).

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Upstream cambia la API (props/ref) | Media | Alto | Fijar rango de versión npm; tests de compilación; seguir CHANGELOG |
| Errores de SSR/hidratación | Media | Alto | Usar `NoSSRComponent` o carga dinámica; probar en `reflex run` |
| Métodos imperativos (prev/next) difíciles vía Reflex | Media | Medio | Spike técnico con `ref` + hooks; degradar a `SHOULD` si bloquea v0.1.0 |
| `as` es palabra reservada en Python | Alta | Bajo | Exponer `as_` y mapear a la prop `as` |
| Versión de Reflex/React incompatible | Baja | Medio | Declarar `requires-python` y rango de Reflex; CI matricial |

## 12. Timeline Estimado

| Fase | Duración Estimada | Entregable |
|---|---|---|
| Spec & Design | 0.5 semana | Specs aprobados (este documento + tech design + plan) |
| Implementación MVP | 1 semana | Wrapper con props + CSS + demo |
| prev/next + tests | 0.5 semana | Control imperativo + tests/CI |
| Publicación | 0.5 semana | Release v0.1.0 en PyPI + docs |

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |

## Aprobaciones

| Rol | Nombre | Fecha | Estado |
|---|---|---|---|
| Product Owner | Ernesto Crespo | | ☐ Pendiente |
| Tech Lead | Ernesto Crespo | | ☐ Pendiente |
