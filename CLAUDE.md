# Escanea y Entra: Prototipo de Acceso QR para el TESCHA

Trabajo de investigación escolar escrito en LaTeX con formato APA 7, hecho en equipo.

## Archivos

- `trabajo.tex`: preámbulo, datos de portada y el orden de las secciones (`\input`). Usa la clase `apa7` en modo estudiante (`stu`) con `biblatex`. El texto **no** va aquí.
- `secciones/`: un archivo por sección del cuerpo (`00-introduccion.tex`, `01-tema.tex`, …). Para agregar una sección, crea el archivo y agrega su `\input` en `trabajo.tex`.
- `apendices/`: un archivo por apéndice (`a-encuesta.tex`, …). Cada uno inicia con `\section{}` y `\apendiceindice{letra}{título}`.
- `objetivos.tex`: envoltorio de dos líneas que compila `secciones/06-objetivos.tex` como PDF aparte (`latexmk -pdf objetivos.tex`), con el mismo preámbulo y datos de portada de `trabajo.tex`, solo las referencias que cita y sin apéndices. Las condicionales `\ifdefined\soloobjetivos` en `trabajo.tex` lo hacen posible. El hook solo compila `trabajo.tex`; este PDF se compila a mano.
- `REVISION-OBJETIVOS.md`: hallazgos de la revisión de la sección de Objetivos y pendientes que quedaron en otros archivos (secciones, apéndices, plan de acción). Léelo antes de editar `05-metodologia.tex` o los Apéndices A a D.
- `citas.bib`: referencias bibliográficas (biblatex-apa). Toda cita nueva se agrega aquí.
- `img/`: logos e imágenes.
- `APA-PURO.md`: qué partes de la plantilla pide la escuela y no son APA (logos, índice, texto justificado, etc.).
- `trabajo_original_backup.tex`: respaldo antiguo. No editarlo.

## Compilar

```
latexmk -pdf trabajo.tex
```

Usa pdfLaTeX y corre biber automáticamente. Un hook (`.claude/hooks/compilar.sh`) compila solo cada vez que Claude edita un `.tex` o `.bib` y le avisa de errores y citas sin definir: corrígelos antes de seguir.

## Reglas de escritura

- Todo el texto va en español.
- Citas y referencias en APA 7, siempre con `\parencite{}` o `\textcite{}` y una entrada en `citas.bib`. Nunca escribir referencias a mano.
- **No inventar fuentes.** Toda referencia nueva se obtiene con `/nueva-cita` (metadatos de Crossref, OpenAlex o la página oficial) y debe tener DOI o URL verificable. Si no se encuentra, se dice; no se completa con datos supuestos.
- Las indicaciones del profesor tienen prioridad sobre APA (ver `APA-PURO.md`).
- Tablas y figuras usan `\figurenote{}` / `\tablenote{}` para la nota.
- No descargar artículos de fuentes no autorizadas (Sci-Hub y similares).

## Comandos del proyecto

- `/compilar`: compila y resume errores y avisos.
- `/nueva-cita <DOI, URL o título>`: agrega una referencia verificada a `citas.bib`.
- `/revisar-seccion <archivo | todo>`: pasa una sección por los revisores en paralelo.
- `/avance <número>`: prepara una entrega (portada, compilación, citas, PDF final).

## Agentes

Del proyecto (`.claude/agents/`):

- `verificador-citas`: comprueba que cada cita exista en `citas.bib` y que el DOI coincida con los datos.
- `revisor-apa`: formato APA 7 respetando las excepciones de `APA-PURO.md`.
- `revisor-metodologia`: coherencia entre problema, pregunta, indicadores, instrumentos y plan.
- `corrector-estilo`: ortografía y redacción académica (solo reporta, salvo que se pida editar).

De plugins:

- `voltagent-research:scientific-literature-researcher`: buscar estudios y evidencia (usa el MCP `bgpt`).
- `voltagent-research:research-analyst` y `search-specialist`: búsqueda y síntesis de fuentes.
- `voltagent-qa-sec:ai-writing-auditor`: revisar que el texto no suene generado por IA.
- `documentation-generation:mermaid-expert`: borradores de diagramas (después se pasan a TikZ).

## MCP

- `paper-search`: búsqueda en Crossref, OpenAlex, Semantic Scholar, arXiv, DBLP, DOAJ y otras. Requiere `uv` instalado.
- `bgpt`: datos experimentales estructurados de artículos científicos.

## Trabajo en equipo

- Cada quien trabaja en una rama (`git switch -c <seccion>`) y se une a `main` con pull request.
- Editar solo los archivos de la sección propia para evitar conflictos; los cambios en `trabajo.tex` y `citas.bib` se avisan al equipo.
