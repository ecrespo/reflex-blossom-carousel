# Reflex Blossom Carousel — Implementation Plan

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **PRD** | ../prd/reflex-blossom-carousel.md |
| **Tech Design** | ../technical/architecture.md |
| **Data Model** | N/A (componente de UI sin persistencia) |
| **API Spec** | ../api/component-api-v1.md |

---

## 1. Resumen de Implementación

Cinco fases incrementales para llevar `reflex-blossom-carousel` de un scaffold a un paquete publicado en PyPI. La estrategia es envolver `@blossom-carousel/react` (ver Tech Design DD-001), resolver primero los riesgos técnicos (SSR y control imperativo `prev/next`) mediante un spike temprano, y dejar la publicación para el final con validación en TestPyPI.

**Duración total estimada:** ~2.5 semanas (1 persona).
**Equipo requerido:** 1 desarrollador (Python + nociones de React/Reflex).
**Fecha objetivo de release:** v0.1.0 en ~2.5 semanas.

## 2. Pre-requisitos

| Pre-requisito | Owner | Estado | Fecha Límite |
|---|---|---|---|
| Specs SDD escritos (PRD, API, Tech Design, Plan) | Ernesto | ☑ Hecho | 2026-06-14 |
| Proyecto scaffolded + Reflex instalado con uv | Ernesto | ☑ Hecho | 2026-06-14 |
| Repo en GitHub | Ernesto | ☐ Pendiente (requiere `gh auth login`) | — |
| Cuenta PyPI + TestPyPI + API tokens | Ernesto | ☐ Pendiente | Antes de F5 |
| Node/Bun disponible para `reflex run` local | Ernesto | ☐ Pendiente | Antes de F2 |

## 3. Fases de Implementación

---

### Fase 0: Foundation (✅ completada en esta sesión)

**Objetivo:** Base técnica lista.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F0-01 | `uv init` + `uv add reflex` (Python 3.13) | Ernesto | 0.2d | — | ☑ |
| F0-02 | `reflex component init --library-name blossom-carousel` | Ernesto | 0.2d | F0-01 | ☑ |
| F0-03 | `uv lock` + `uv sync` (editable install del paquete local) | Ernesto | 0.1d | F0-02 | ☑ |
| F0-04 | Metadata de `pyproject.toml` (autor, URLs, descripción) | Ernesto | 0.1d | F0-02 | ☑ |
| F0-05 | Specs SDD en `specs/` | Ernesto | 0.5d | — | ☑ |

**Criterios de "Done":** `uv run python -c "import reflex_blossom_carousel"` OK; specs versionados. ✅

---

### Fase 1: Spike técnico (de-risking)

**Duración:** 2-3 días
**Objetivo:** Resolver las incógnitas de SSR, mapeo `as_`→`as`, CSS y `prev/next` antes de comprometer la API.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F1-01 | Wrapper mínimo (`library`/`tag`/`is_default=False`/`lib_dependencies`) que solo renderice slides | Ernesto | 0.5d | F0 | ☐ |
| F1-02 | Verificar SSR: ¿`rx.Component` basta o se necesita `NoSSRComponent`? (cierra DD-002) | Ernesto | 0.5d | F1-01 | ☐ |
| F1-03 | Inyectar `@blossom-carousel/core/style.css` y confirmar layout (cierra DD-004) | Ernesto | 0.5d | F1-01 | ☐ |
| F1-04 | Resolver alias `as_`→`as` en la versión de Reflex usada | Ernesto | 0.5d | F1-01 | ☐ |
| F1-05 | Spike `prev/next`: probar Estrategia A (EventSpec+JS) y B (hooks) (cierra DD-003) | Ernesto | 1d | F1-01 | ☐ |

**Criterios de "Done":**
- Carrusel visible y arrastrable en `reflex run` (desktop).
- Preguntas abiertas del Tech Design (§10) respondidas y documentadas.

---

### Fase 2: Implementación del componente (MVP)

**Duración:** 3-4 días
**Objetivo:** Componente completo según el API Spec v1.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F2-01 | Props `as_`, `repeat`, `load` con defaults y tipos | Ernesto | 1d | F1 | ☐ |
| F2-02 | Inyección de CSS definitiva (`add_custom_code`/assets) | Ernesto | 0.5d | F1-03 | ☐ |
| F2-03 | Estrategia SSR definitiva implementada | Ernesto | 0.5d | F1-02 | ☐ |
| F2-04 | `prev(align)`/`next(align)` (o diferir a v0.2 si excede presupuesto) | Ernesto | 1.5d | F1-05 | ☐ |
| F2-05 | `__init__.py` re-exporta `blossom_carousel` y tipos públicos | Ernesto | 0.2d | F2-01 | ☐ |

**Criterios de "Done":** Todos los RF `MUST` cubiertos; API coincide con el API Spec v1.

---

### Fase 3: Demo, estilos y documentación

**Duración:** 2 días
**Objetivo:** App demo equivalente al ejemplo de upstream + docs.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F3-01 | Demo: 12 slides + botones Prev/Next, CSS de carrusel | Ernesto | 0.5d | F2 | ☐ |
| F3-02 | README: instalación, ejemplo mínimo, props, prev/next, atribución a upstream (MIT) | Ernesto | 1d | F2 | ☐ |
| F3-03 | Capturas/GIF del demo en README | Ernesto | 0.5d | F3-01 | ☐ |

**Criterios de "Done":** `cd blossom_carousel_demo && reflex run` muestra el carrusel funcional; README copiable.

---

### Fase 4: Tests y CI

**Duración:** 2 días
**Objetivo:** Red de seguridad automatizada.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F4-01 | Tests unитarios del wrapper (render contiene tag/props correctos) | Ernesto | 1d | F2 | ☐ |
| F4-02 | Test de compilación del demo (`reflex export`/build en CI) | Ernesto | 0.5d | F3-01 | ☐ |
| F4-03 | GitHub Actions: `uv sync` + `pytest` + build en push/PR | Ernesto | 0.5d | F4-01 | ☐ |

**Criterios de "Done":** CI verde; cobertura del wrapper > 80 %.

---

### Fase 5: Empaquetado y publicación

**Duración:** 1-2 días
**Objetivo:** Release v0.1.0 en PyPI.

| ID | Tarea | Responsable | Estimación | Dependencia | Estado |
|---|---|---|---|---|---|
| F5-01 | `reflex component build` (genera `dist/`) | Ernesto | 0.3d | F4 | ☐ |
| F5-02 | Publicar en **TestPyPI** (`uv publish --index testpypi`) y validar `pip install` | Ernesto | 0.5d | F5-01 | ☐ |
| F5-03 | Publicar en **PyPI** (`uv publish`) | Ernesto | 0.3d | F5-02 | ☐ |
| F5-04 | Tag `v0.1.0` + GitHub Release + `reflex component share` (galería) | Ernesto | 0.4d | F5-03 | ☐ |

**Criterios de "Done":** `pip install reflex-blossom-carousel` funciona desde PyPI; release tag publicado.

---

## 4. Mapa de Dependencias

```
Fase 0: Foundation (hecha)
  │
  ▼
Fase 1: Spike (SSR, as_, CSS, prev/next)
  │
  ▼
Fase 2: Componente MVP ──▶ Fase 3: Demo + Docs ──▶ Fase 4: Tests + CI ──▶ Fase 5: Publish
```

## 5. Riesgos de Implementación

| Riesgo | Probabilidad | Impacto | Mitigación | Owner |
|---|---|---|---|---|
| `prev/next` imperativo más complejo de lo previsto | Media | Medio | Spike F1-05; diferir a v0.2 (es `SHOULD`) | Ernesto |
| Errores de SSR/hidratación | Media | Alto | F1-02; fallback `NoSSRComponent` | Ernesto |
| Cambios de API en upstream npm | Media | Alto | Anclar `^1.1.x`; seguir CHANGELOG; tests | Ernesto |
| `gh`/PyPI sin credenciales | Alta | Bajo | Configurar auth antes de F5; repo/publish son pasos manuales con token | Ernesto |
| Reflex en Python 3.14 no soportado | Media | Medio | Proyecto pinneado a 3.13 vía `.python-version` | Ernesto |

## 6. Comunicación y Seguimiento

Proyecto OSS individual: seguimiento vía Issues/Projects de GitHub. Checklist de fases como milestones. Cambios de spec entran como PRs a `specs/`.

## 7. Definición de Done (Global)

- [ ] Código implementado y mergeado a `main`.
- [ ] Tests pasando (unit + compilación) en CI.
- [ ] Code review (auto-review documentado si es individual).
- [ ] README y specs actualizados.
- [ ] Demo verificado con `reflex run`.
- [ ] Paquete publicado en PyPI y tag de versión creado.
- [ ] Specs actualizados si hubo cambios durante la implementación.

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Versión inicial |
