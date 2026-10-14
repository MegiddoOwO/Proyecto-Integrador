# Escanea y Entra: Prototipo de Acceso QR para el TESCHA

Trabajo de investigación escolar escrito en LaTeX con formato APA 7, hecho en equipo.

## Archivos

- `trabajo.tex`: preámbulo, datos de portada y el orden de las secciones (`\input`). Usa la clase `apa7` en modo estudiante (`stu`) con `biblatex`. El texto **no** va aquí.
- `secciones/`: un archivo por sección del cuerpo (`00-introduccion.tex`, `01-tema.tex`, …). Para agregar una sección, crea el archivo y agrega su `\input` en `trabajo.tex`.
- `secciones/08-justificacion.tex`: reúne la importancia del proyecto y la viabilidad, cargada desde `secciones/07-viabilidad.tex`. La justificación se excluye de `problema-objetivos.tex`.
- `secciones/03-problema.tex`: planteamiento en texto corrido, de lo general a lo particular, sin subtítulos, listas ni procedimientos metodológicos. Cierra con el enunciado de la pregunta de investigación de `secciones/04-pregunta.tex`, sin encabezado propio. No volver a cargar la pregunta desde `trabajo.tex`.
- `secciones/06-objetivos.tex`: objetivos específicos en una sola lista con viñetas, en orden cronológico, sin negritas en los ítems ni citas.
- `apendices/`: un archivo por apéndice (`a-encuesta.tex`, …). Cada uno inicia con `\section{}` y `\apendiceindice{letra}{título}`.
- `objetivos.tex`: compila `secciones/06-objetivos.tex` como PDF aparte (`latexmk -pdf objetivos.tex`), con el mismo preámbulo y datos de portada de `trabajo.tex`, sin citas, bibliografía ni apéndices. Las condicionales `\ifdefined\soloobjetivos` en `trabajo.tex` lo hacen posible. El hook solo compila `trabajo.tex`; este PDF se compila a mano.
- `problema-objetivos.tex`: genera una versión con carátula, índice, planteamiento del problema con el enunciado de la pregunta de investigación, objetivos y las referencias citadas en el planteamiento (`latexmk -pdf problema-objetivos.tex`). Comparte el formato y los datos de portada de `trabajo.tex`, con la condicional `\ifdefined\soloproblemaobjetivos`. Excluye la justificación y la viabilidad.
- `avances.tex`: informe independiente para presentar avances documentales y las pruebas de banco del reconocimiento facial (`latexmk -pdf avances.tex`). Mantiene los autores del equipo; el docente es OMAR HETZAEL LOPEZ ALMONTE. Usa la condicional `\ifdefined\soloavances` y el contenido de `secciones/09-avances.tex`.
- `evidencias/avances-2026-10-13/`: copia identificable del CSV y el código de reconocimiento facial, con procedencia y resúmenes. Las tablas y la gráfica se generan con `python3 scripts/resumir_avances_facial.py`. No sumar el respaldo al archivo vigente: contiene intentos coincidentes.
- `evidencias/avances-2026-10-13/camara/`: dos capturas reales de detección de rostro y parpadeo tomadas con autorización del usuario. La sesión adicional tiene su propio registro JSON y se presenta separada de los 45 intentos históricos. La captura usa `scripts/capturar_pruebas_camara.py` con el entorno del prototipo.
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
