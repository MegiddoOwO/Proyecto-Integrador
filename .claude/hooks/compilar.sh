#!/usr/bin/env bash
# Hook PostToolUse: compila el documento cada vez que Claude edita un .tex o .bib.
# Si hay errores o citas/referencias sin definir, los devuelve a Claude (exit 2)
# para que los corrija en ese momento.

entrada=$(cat)
archivo=$(printf '%s' "$entrada" | grep -o '"file_path" *: *"[^"]*"' | head -1 | sed 's/.*: *"\(.*\)"/\1/')

case "$archivo" in
  *.tex|*.bib) ;;
  *) exit 0 ;;
esac

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
command -v latexmk >/dev/null 2>&1 || exit 0

if ! latexmk -pdf -interaction=nonstopmode -halt-on-error -silent trabajo.tex >/dev/null 2>&1; then
  {
    echo "La compilación de trabajo.tex falló después de editar $archivo."
    echo "Errores de trabajo.log:"
    grep -A4 '^!' trabajo.log | head -40
    if [ -f trabajo.blg ]; then grep -i 'ERROR' trabajo.blg | head -10; fi
  } >&2
  exit 2
fi

avisos=$(grep -E "Citation .* undefined|Reference .* undefined|There were undefined" trabajo.log | sort -u | head -20)
if [ -n "$avisos" ]; then
  {
    echo "El documento compila, pero hay citas o referencias sin definir:"
    echo "$avisos"
  } >&2
  exit 2
fi

exit 0
