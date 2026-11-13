---
name: buscar-fuentes
description: Busca artículos y otras fuentes académicas en OpenAlex con scripts/buscar_openalex.py. Úsalo cuando el usuario quiera encontrar estudios, antecedentes o evidencia para una sección, o cuando el MCP paper-search no esté disponible.
argument-hint: <tema o palabras clave> [--desde AÑO]
---

# Buscar fuentes en OpenAlex

Entrada: `$ARGUMENTS`

El script `scripts/buscar_openalex.py` consulta la API de OpenAlex solo con la
biblioteca estándar de Python, así que no depende de `uvx` ni del MCP
`paper-search`.

## 1. Preparar la consulta

- Traduce el tema a palabras clave en inglés (OpenAlex indexa sobre todo en
  inglés) y haz una segunda búsqueda en español si el tema es local, por
  ejemplo, control de acceso en universidades mexicanas.
- Si la fuente es para los antecedentes, el profesor pidió que sean de este año
  o del anterior: usa `--desde` con el año anterior al actual.

## 2. Buscar

```
python3 scripts/buscar_openalex.py buscar "<palabras clave>" --desde 2025 -n 10 --resumen
python3 scripts/buscar_openalex.py buscar "<palabras clave>" --orden citas --tipo article
python3 scripts/buscar_openalex.py doi <DOI>
```

Opciones: `--hasta`, `--tipo` (article, review, book, dissertation),
`--abierto` (solo acceso abierto), `--orden relevancia|citas|fecha` y `-n`.
Si existe la variable de entorno `OPENALEX_API_KEY`, el script la usa; no
escribas la llave en el repositorio ni pidas el correo del usuario para
generarla.

Si la conexión falla con un error de certificado (por ejemplo, un certificado
de `securelogin.hpe.com`), la red pide iniciar sesión en un portal cautivo. En
ese caso pide al usuario que se conecte o que corra el comando con `!`. No
desactives la verificación de certificados.

## 3. Elegir

Presenta una lista corta con título, autores, año, revista, DOI y una línea
sobre lo que aporta a la sección. Descarta lo que no tenga DOI ni URL
verificable, las revistas sin revisión por pares cuando haya alternativas y
lo que solo se conozca por blogs de proveedores. Si el resumen no contiene el
dato que se quiere citar, dilo: no lo completes con suposiciones.

## 4. Agregar

Cada fuente elegida se agrega con `/nueva-cita <DOI>`. Este comando no
modifica `citas.bib`.
