# Plan integral de Escanea y Entra

Documento independiente de las entregas anteriores. Versión 1.3: redacción orientada al lector final, fuentes descritas por su título, instrucciones sin rutas absolutas e índice y citas sin color azul. Conserva la eliminación de la sección de reproducción de cálculos y las referencias ampliadas de la versión 1.2. Los CSV y las imágenes incorporados en la versión 1.1 se conservan. Corte: 13 de noviembre de 2026.

- PDF para lectura: [plan-integral-escanea-y-entra.pdf](../output/pdf/plan-integral-escanea-y-entra.pdf).
- Fuente editable: `plan-integral.tex`, `fuentes.bib` y la base compartida `../citas.bib`.
- PERT original: [pestaña PERT Escanea y Entra, gid=1001](https://docs.google.com/spreadsheets/d/1OPwoyW0Szve5_up1tRR9yeShl-_CUFiBBaYvUr-OOFY/edit?gid=1001).
- Copia de valores consultados: `pert-hoja-fuente.json` (A1:J41). La hoja no se modificó.
- Cálculos: `calcular_pert.py` y `pert-resultados.json`. Las tablas `pert-estimaciones.tex`, `pert-calculos.tex` y `gantt.tex` se regeneran.
- Procedencia de archivos locales: `procedencia.json`, con hashes de los archivos técnicos principales consultados; no incluye vectores ni imágenes biométricas.

## Contenido

Alcance y objetivos, inventario de evidencias y código facial, arquitectura QR y facial, dependencias técnicas y de trabajo, resultados históricos, catálogo A-W, estimaciones PERT, precedencias, holguras, dos rutas críticas, Gantt relativo, calendario original y escenario restante, entregables por etapa, contratos de integración, modelo conceptual de datos, pruebas, equipo, presupuesto y riesgos.

## Resultados verificados

- 23 actividades de la pestaña enlazada, sin mezclar la pestaña alternativa «La actividad».
- Duración completa: 347/6 = 57,83 días hábiles.
- Ruta 1: A-B-C-H-J-K-O-Q-R-U-V-W.
- Ruta 2: A-B-C-H-J-K-L-P-Q-R-U-V-W.
- Suma de duraciones esperadas: 647/6 = 107,83 días-actividad.
- Suma de tiempos más probables: 102 días-actividad.
- La fila Total visible indica 98 y 103,5, respectivamente; ambas diferencias corresponden a W. La suma de varianzas de las 23 filas es 15,9167, que sí coincide con el total visible 15,9 al redondear. Se recomienda revisar los rangos y la fórmula de J25.
- Solo si A-F están realmente terminadas y G-W completamente pendientes, el escenario restante dura 43,50 días hábiles. No es una declaración de avance real ni una fecha comprometida.
- En la versión inicial el CSV externo estaba vacío. La actualización incorpora 24 intentos nuevos (11 correctos, 11 falsos rechazos y 2 falsas aceptaciones) y cuatro capturas de `Imagenes/`. La copia histórica local mantiene sus 45 intentos y 43 correctos, sin sumar el respaldo ni mezclar sesiones.
- Copias de los dos CSV y sus dos resúmenes: `evidencias-2026-11-13/`. La salida de `analizar.py` se conserva como texto. El programa original solo imprime el resumen; `incorporar_evidencias.py` exporta las mismas métricas a CSV.
- Las capturas de 16:02:21 y 16:02:28 muestran la misma última decisión, por lo que no se cuentan como dos intentos adicionales.

## Reproducir

Desde la raíz del repositorio:

```bash
python3 documentacion-integral/calcular_pert.py
```

Después, dentro de `documentacion-integral/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error plan-integral.tex
```

La compilación necesita los logos de `../img/`, LaTeX, biber y los paquetes indicados en el preámbulo. Tras compilar se copia el PDF al destino de lectura. Para actualizar desde Sheets, primero reemplazar la copia de origen por una lectura nueva de la misma pestaña y revisar las comprobaciones del script.

No se ejecutaron pruebas de cámara ni se instalaron dependencias en el prototipo externo. Se ejecutó el código original de análisis con la constante de ruta de `comun` aislada, para procesar exclusivamente los CSV sin importar los módulos de cámara. El informe diferencia código, evidencia histórica y propuestas pendientes.
