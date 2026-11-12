# Niza: avance de Gestión de Proyectos de Software

Material de la materia Gestión de Proyectos de Software (docente Niza Lucero
Alpízar Martínez). Documenta el proyecto Escanea y Entra en lenguaje poco
técnico, con el mismo formato APA 7 de `trabajo.tex`.

## Contenido

| Ruta | Qué es |
|---|---|
| `avance-niza.tex` | Documento principal: preámbulo, portada y orden de las secciones. |
| `gestion/` | Una sección por archivo (`00-introduccion.tex` a `11-estado.tex`). |
| `Avance Niza.pdf` | PDF entregado (41 páginas). |
| `tareas-avance-niza.md` | Registro de tareas y decisiones tomadas al redactarlo. |
| `fuentes/` | Material de origen: Entregables 1 a 3, sus versiones nuevas y la presentación HTML. |

## Compilar

Desde esta carpeta:

```
latexmk -pdf avance-niza.tex
```

Usa `../citas.bib` y los logos de `../img/`, que están en la raíz del
repositorio. El resultado es `avance-niza.pdf`; para entregarlo se copia como
`Avance Niza.pdf`.

## Fuentes

- `Entregable_1.pdf`, `Entregable_2.pdf` y `Entregable_3.pdf`: ficha inicial,
  plan de calidad y tablero de metas.
- `entregable1_ficha_inicial.pdf` y `entregable2_plan_calidad.pdf`: versiones
  nuevas de los entregables 1 y 2. Mismo contenido; solo corrigen «Brayan» por
  «Bryan» y el formato.
- `Escanea y Entra — Avance.html`: presentación del avance.
