# Avance Niza: documento de Gestión de Proyectos

- **Rama:** `documentacion-niza`
- **Objetivo:** documento LaTeX (APA 7, mismo formato que `trabajo.tex`) para la materia Gestión de Proyectos de Software (docente Niza Lucero Alpízar Martínez) que documente el proyecto Escanea y Entra en lenguaje natural, poco técnico.
- **Fuentes:** `trabajo.tex` y sus secciones/apéndices (rama `main`, equivalente a `Trabajo 2.pdf`), Entregable 1 (ficha inicial), Entregable 2 (plan de calidad), Entregable 3 (tablero de metas) y la presentación HTML "Escanea y Entra — Avance".
- **Restricciones:** no inventar fuentes ni datos; no tocar `trabajo.tex`, `secciones/`, `apendices/` ni `trabajo_original_backup.tex`; turno vespertino (el HTML dice matutino en una diapositiva, se toma el de `main` y Entregable 1).
- **TDD:** no aplica (documento LaTeX). Fuente: naturaleza del entregable. Verificación: `latexmk -pdf avance-niza.tex` sin errores ni citas indefinidas.
- **Entrega:** PDF `Avance Niza.pdf`.

## Tareas

- [x] T1 — Redactar `avance-niza.tex` + `gestion/*.tex` concatenando las fuentes (ruta: delegada, disparador: 5 fuentes y 2+ archivos no triviales).
- [x] T2 — Compilar, revisar y generar `Avance Niza.pdf` (ruta: inline).
- [x] T3 — Commit en `documentacion-niza` (push lo decide el usuario).

## Progreso

- Rama creada desde `main` (89a6942).
- T1: `avance-niza.tex` + `gestion/00..10` (11 secciones). Conflictos resueltos: turno vespertino, fin del piloto 18 dic, "Bryan", M5 según Plan de Calidad, contingencia 380 MXN tal cual la presentación.
- T2: `latexmk -pdf avance-niza.tex` exit 0, sin citas indefinidas, un Overfull de 7.6pt (entrada de `citas.bib`). `Avance Niza.pdf`, 36 páginas.
- T3: commit en `documentacion-niza`. Push pendiente (lo decide el usuario).
- Fuentes nuevas `entregable1_ficha_inicial.pdf` y `entregable2_plan_calidad.pdf` comparadas palabra por palabra con Entregable_1/2: mismo contenido, solo corrigen "Brayan" → "Bryan" y el formato. El documento ya las cubre; no hubo cambios de texto.
- T4: diagrama de Gantt (Figura 2) en `gestion/06-equipo.tex`, replicado de la diapositiva 11 del HTML, junto a la matriz RACI; `\FloatBarrier` lo mantiene en su sección. latexmk exit 0, 38 páginas.
