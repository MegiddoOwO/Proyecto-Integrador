---
name: nueva-cita
description: Agrega una referencia verificada a citas.bib a partir de un DOI, una URL o un título. Úsalo cuando el usuario quiera agregar una fuente o citar un artículo nuevo.
argument-hint: <DOI, URL o título>
---

# Agregar una cita verificada

Entrada: `$ARGUMENTS`

## 1. Obtener los metadatos reales

- **DOI** (`10.xxxx/...` o `https://doi.org/...`): consulta Crossref con `mcp__paper-search__get_crossref_paper_by_doi` o con WebFetch a `https://api.crossref.org/works/<doi>`.
- **Título**: busca con `mcp__paper-search__search_crossref` o `search_openalex`. Si hay varios candidatos, muéstralos y pregunta cuál es antes de seguir.
- **URL sin DOI** (tesis, ley, página institucional): abre la página con WebFetch y toma autor, título, año, institución y URL de ahí.

Si no encuentras la fuente, **detente y dilo**. Nunca completes campos con datos supuestos.

## 2. Revisar que no exista ya

Busca en `citas.bib` el DOI y el título. Si ya está, informa la clave existente y no la dupliques.

## 3. Escribir la entrada

Sigue el formato que ya usa `citas.bib` (biblatex-apa):

- Clave: `apellidoaño palabraclave` en minúsculas y sin espacios ni acentos, p. ej. `kao2011physical`.
- Campos de biblatex: `journaltitle` (no `journal`), `date` (no `year`), `pages = {12--20}` con doble guion.
- Autores separados por `and`, con apellidos completos (`Cano Perfecto, Jesús Emmanuel`).
- Protege siglas en el título con llaves: `{QR}`, `{NFC}`, `{IoT}`.
- Título con las mayúsculas originales de la fuente (biblatex-apa aplica el formato).
- Incluye `doi` si existe; si no, `url`. Para `@online` agrega `urldate`.
- Alinea los `=` como en las entradas existentes.

Agrega la entrada al final de `citas.bib`.

## 4. Confirmar

Muestra la entrada agregada y cómo citarla: `\parencite{clave}` o `\textcite{clave}`.
