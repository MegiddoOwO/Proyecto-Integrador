---
name: revisar-seccion
description: Revisa una sección o apéndice del trabajo con los agentes revisores (APA, citas, estilo y, si aplica, metodología) en paralelo y junta sus observaciones. Úsalo cuando el usuario pida revisar una sección, un apéndice o todo el documento.
argument-hint: <archivo o nombre de sección, o "todo">
---

# Revisar una sección

Objetivo: `$ARGUMENTS`

1. **Ubica el archivo.** Busca en `secciones/` y `apendices/` el que corresponda (por nombre de archivo o por el `\section{}` que contiene). Si es «todo», revisa todos. Si es ambiguo, pregunta.

2. **Lanza los revisores en paralelo** (en un solo mensaje, con la herramienta Agent), indicando a cada uno el archivo:
   - `revisor-apa`
   - `verificador-citas`, solo para las claves citadas en ese archivo.
   - `corrector-estilo`, en modo reporte (sin editar).
   - `revisor-metodologia`, solo si el archivo es `03-problema`, `04-pregunta`, `05-metodologia` o un apéndice con instrumentos.

3. **Junta los resultados** en un solo reporte, sin repetir observaciones que coincidan:
   - **Errores** (citas inexistentes, incoherencias metodológicas, errores de APA).
   - **Sugerencias** (estilo, claridad).
   Cada punto con `archivo:línea`.

4. Pregunta al usuario qué correcciones aplicar. No edites nada antes de que responda.
