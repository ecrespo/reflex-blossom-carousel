#!/usr/bin/env bash
# Crea el repositorio público en GitHub y sube el commit inicial.
# Requisito: estar autenticado en gh  ->  gh auth login   (o exportar GH_TOKEN)
set -euo pipefail

REPO_NAME="reflex-blossom-carousel"
DESC="Reflex wrapper for Blossom Carousel — native-scroll-first carousel with pointer drag support"

cd "$(dirname "$0")/.."

# Verifica autenticación
if ! gh auth status >/dev/null 2>&1; then
  echo "No estás autenticado en gh. Ejecuta primero:  gh auth login" >&2
  exit 1
fi

# Crea el repo público bajo tu cuenta, añade el remote 'origin' y hace push
gh repo create "$REPO_NAME" \
  --public \
  --source=. \
  --remote=origin \
  --description "$DESC" \
  --push

echo "Listo: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
