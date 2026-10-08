---
name: compilar
description: Compila trabajo.tex con latexmk y resume errores y avisos importantes. Úsalo cuando el usuario pida compilar, generar el PDF o revisar si el documento tiene errores.
allowed-tools: Bash(latexmk:*), Bash(pdfinfo:*), Read, Grep
---

# Compilar el documento

1. Compila desde la raíz del proyecto:

   ```
   latexmk -pdf -interaction=nonstopmode -halt-on-error trabajo.tex
   ```

2. Si falla, lee `trabajo.log` y busca las líneas que empiezan con `!`. Para cada error indica el archivo y la línea (`l.<n>` en el log; el archivo es el último `(./secciones/...tex` abierto antes del error) y propón la corrección.

3. Si compila, revisa en `trabajo.log` y `trabajo.blg`:
   - `Citation ... undefined` y `Reference ... undefined` → errores a corregir.
   - `biber` con `WARN` o `ERROR` → problemas en `citas.bib`.
   - `Overfull \hbox` mayores a 10pt → texto que se sale del margen; menciona la línea.
   - Ignora los avisos menores de `Underfull` y de fuentes.

4. Termina con un resumen corto: si compiló, número de páginas (`pdfinfo trabajo.pdf`) y la lista de problemas pendientes. Si `$ARGUMENTS` dice «corrige», arregla los problemas en vez de solo listarlos.
