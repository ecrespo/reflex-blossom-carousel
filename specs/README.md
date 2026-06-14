# Specs — reflex-blossom-carousel

Spec-Driven Design (SDD) documents for this project. Specs are the primary artifact: written and reviewed **before** implementation, and kept in version control.

## Flow

```
PRD (qué) → Component API Spec (contrato) → Technical Design (cómo) → Implementation Plan (fases)
```

| Documento | Archivo | Propósito |
|---|---|---|
| PRD | [prd/reflex-blossom-carousel.md](prd/reflex-blossom-carousel.md) | Qué se construye, para quién, alcance, requisitos, riesgos |
| Component API Spec | [api/component-api-v1.md](api/component-api-v1.md) | Contrato de la API Python del componente y mapeo a la librería React |
| Technical Design | [technical/architecture.md](technical/architecture.md) | Arquitectura, decisiones de diseño (SSR, prev/next, CSS), estructura |
| Implementation Plan | [plans/implementation-plan.md](plans/implementation-plan.md) | Fases, tareas, dependencias, criterios de Done |
| Análisis upstream | [analysis/blossom-carousel-upstream.md](analysis/blossom-carousel-upstream.md) | Análisis del repo `jespervos/blossom-carousel` |

## Notas

- **Data Model:** N/A. Es un componente de UI sin persistencia, por lo que el documento de modelo de datos del flujo SDD no aplica.
- Detalle proporcional al riesgo: este es un wrapper de librería (feature media), por eso se incluyen PRD + API + Tech Design + Plan, pero no Data Model.
