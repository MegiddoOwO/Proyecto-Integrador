# Anexos de análisis e imágenes

Se incorporaron al plan integral, versión 1.1, el 13 de noviembre de 2026.

## CSV de origen

- `pruebas-2026-10-13.csv`: copia de 45 intentos históricos del repositorio Proyecto-Integrador. No se sumó el respaldo.
- `pruebas-2026-11-13.csv`: copia de 24 intentos nuevos de reconocimiento_facial/resultados/pruebas.csv.

## CSV de análisis

- `analisis-2026-10-13.csv`: seis grupos de la serie histórica.
- `analisis-2026-11-13.csv`: dos grupos de la serie nueva.

Cada grupo conserva tecnología, condición y resultado esperado. Los campos son intentos, aciertos, porcentaje correcto, falsos rechazos, falsas aceptaciones y tiempo medio, mediano y máximo en milisegundos. Los CSV de resumen usan UTF-8 con BOM y coma como separador; los decimales usan punto.

Las reglas reproducen analizar.py: una aceptación con identidad distinta de la esperada cuenta como falsa aceptación; un caso esperado de aceptación que no se acepta cuenta como falso rechazo. La columna correcto de cada registro se verificó contra resultado e identidad. El resumen nuevo tiene 11 aciertos, 11 falsos rechazos y dos falsas aceptaciones, en 24 intentos.

`analizar-salida-*.txt` conserva la salida del programa original. Se ejecutó el analizador original sustituyendo únicamente la constante de ruta de `comun`, sin importar cámara o modelos. No se realizaron nuevas pruebas con personas.

## Imágenes

Se copiaron completas y sin editar cuatro capturas de reconocimiento_facial/Imagenes/. `procedencia.json` relaciona las copias 01.png a 04.png con sus nombres originales y hashes SHA-256.

Las imágenes 03 y 04 muestran el mismo resultado persistente de las 16:02:00: no equivalen a dos intentos adicionales. La captura de registro y las otras imágenes no se suman al CSV como mediciones nuevas. Las series de octubre y noviembre se presentan por separado.
