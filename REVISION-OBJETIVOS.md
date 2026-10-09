# Revisión de `secciones/06-objetivos.tex`: hallazgos y pendientes

Registro de la revisión de coherencia metodológica (agente `revisor-metodologia`)
y de la verificación de citas (agente `verificador-citas`) hecha el 8 de octubre
de 2026 sobre la sección de Objetivos, contra `03-problema`, `04-pregunta`,
`05-metodologia` y los Apéndices A a D.

Sirve para que otra sesión, o cualquier integrante, retome lo que quedó fuera de
`06-objetivos.tex`. Las secciones y apéndices ajenos **no se editaron**
(`CLAUDE.md`: cada quien edita solo su sección). Las referencias `archivo:línea`
son de esos archivos tal como estaban ese día y pueden haberse movido.

Estados: **Aplicado** (ya corregido en `06-objetivos.tex`), **Pendiente** (hay
que decidir o editar otro archivo), **Equipo** (decisión del equipo, no de código).

## 1. Cambios ya aplicados en `06-objetivos.tex`

| # | Hallazgo | Estado |
|---|---|---|
| 1 | La prueba «para muestras relacionadas» no tenía unidad de emparejamiento. Los estudiantes cronometrados antes y durante el piloto son distintos; solo se puede emparejar por intervalo. | Aplicado en OI4: unidad de análisis = intervalo de 5 min, emparejado por posición y día (40 pares). Falta reflejarlo en `05-metodologia` (Diseño) y Apéndice C (Análisis). |
| 2 | «Incidencias de identidad» sin definición operativa; un sistema mejor detecta más, así que subir no es empeorar. | Aplicado como **propuesta** en la nota de la Tabla 3: tasa = (sin credencial + rechazos) / ingresos, leída como capacidad de detección; «sin revisión» se reporta aparte. **El equipo debe confirmarla** y llevarla al Apéndice C y a `04-pregunta`. |
| 3 | «Registros del propio sistema» en el *cómo* del objetivo general: solo existen durante el piloto, no en la línea base. | Aplicado: la comparación es solo con la hoja del Apéndice C; los registros complementan. |
| 6 | OT4 comparaba latencia (ms) con tiempo de revisión (s) y adelantaba la respuesta a la pregunta («más rápido que la revisión manual»). | Aplicado: el *para qué* es «descartar que el lector sea cuello de botella»; el indicador es el tiempo de una lectura completa en banco. Falta el instrumento (ver 2.3). |
| 7 | El 100 % de OT2 se aplica a casos de prueba sin lista cerrada; el desfase de reloj (eje «Validez del código» de `03-problema`) no tenía objetivo. | Aplicado: OT2 incluye desfases de reloj dentro y fuera de la tolerancia; la nota aclara que el 100 % es criterio de aceptación, no resultado de investigación. Falta la lista de casos (ver 2.3). |
| 8 | Verbos de Bloom: OI4 con dos verbos («contrastar» es Comprender, «valorar» es Evaluar); «Determinar» no es verbo de la taxonomía. | Aplicado: OI4 = Evaluar; OI2 = «Estimar» (Aplicar); OI1 agrega identificar intervalos con utilización ≥ 1. |
| 10 | El *para qué* hablaba de «extender el sistema», contra el alcance declarado en `05-metodologia` (no generalizable, evidencia orientativa). | Aplicado: «evidencia orientativa para decidir si conviene ampliar el piloto». Amenazas de OI4 ampliadas a historia, maduración e instrumentación. |
| 11 | OT3: los reportes «definidos con vigilancia y Control Escolar» ya venían fijados; «estudiantes sin ingresos consecutivos» no tiene sentido con un solo acceso controlado. | Aplicado: reportes «propuestos en el planteamiento del problema», el de ausencias como demostración funcional, validados en la entrevista a Control Escolar. |
| 12 | Sin aviso de privacidad ni consentimiento para el piloto. | Aplicado en OI3 (definidos antes del piloto). Falta incluirlo en el Apéndice D (ver 2.2). |
| 14 | «Específico» exigía nombrar acceso y turno, que OT1 a OT3 y OI3 no cumplen. | Aplicado: nombra el producto o indicador y, cuando aplica, acceso y turno. |
| 16 | «Tiempo de validación» y «tiempo de revisión» usados como sinónimos. | Aplicado: se define el tiempo de validación (desde que llega al punto de revisión hasta que lo cruza, con revisión visual o QR) y se usa solo ese término. El Apéndice C aún dice «revisión». |
| 5 | OI4 usaba entrevistas posteriores al piloto, que no existen como instrumento. | Aplicado: se quitaron de OI4. La contradicción en `05-metodologia` sigue (ver 2.1). |

Actualización posterior: a pedido del equipo se quitó la subsección «Criterios de
Redacción» y la columna «Nivel» de la Tabla 3. Los criterios (qué/cómo/para qué,
taxonomía de Bloom revisada y SMART) siguen aplicándose, pero de forma implícita:
cada objetivo es una oración con verbo, medio y finalidad, y la tabla de
indicadores aporta lo medible y el plazo. Por eso `anderson2001taxonomy` y
`doran1981smart` quedan en `citas.bib` **sin citarse** en el texto (no salen en
la bibliografía). Si la profesora pide mencionar explícitamente Bloom o SMART,
se pueden citar de nuevo; los niveles que se usaron fueron: OT1 y OT3 Crear,
OT2 Aplicar, OT4 Evaluar, OI1 Analizar, OI2 Aplicar (estimar), OI3 Comprender
(interpretar), OI4 Evaluar.

Citas (`verificador-citas`):

- Se corrigió la atribución de SMART: Doran propuso *Specific, Measurable,
  Assignable, Realistic, Time-related*; «alcanzable» y «relevante» son variantes
  posteriores. El texto ya lo dice así.
- La regla de evitar «conocer» y «entender» se marcó como criterio del equipo, no
  de Anderson y Krathwohl.
- `doran1981smart` no tiene DOI. Título, autor, año y páginas 35--36 coinciden con
  un escaneo de las páginas originales; volumen 70 y número 11 solo en fuentes
  secundarias. Confirmar en ProQuest o EBSCO si hay acceso.
- `anderson2001taxonomy`: ISBN 978-0-321-08405-7 confirmado en Open Library; sin
  DOI ni URL (libro). La edición sale impresa como «(Complete ed.)».

## 2. Pendientes fuera de `06-objetivos.tex`

### 2.1 Contradicciones entre secciones

1. **`05-metodologia.tex:76-77`** dice que la observación es «el único instrumento
   que se aplica dos veces»; **`05-metodologia.tex:133-135`** dice que «los tres
   instrumentos se aplican antes ... y de nuevo durante». El Apéndice B no tiene
   guía posterior al piloto. Opciones: (a) agregar al Apéndice B una sección
   «Después del piloto» (experiencia con el sistema, rechazos, carga de
   vigilancia) y corregir 05:76-77; o (b) dejar que solo la hoja de observación
   se aplique dos veces y corregir 05:133-135.
2. **Tratamiento del piloto.** `04-pregunta.tex:10-11` dice que el sistema
   «sustituye la revisión visual»; `d-plan-de-accion.tex:13-14` dice «sin retirar
   la revisión manual». Si coexisten, se evalúa QR más revisión manual. Propuesta:
   fase 4 = «el QR sustituye la revisión visual; la revisión manual queda solo
   para quien no pueda mostrar su código» (ya dicho en Delimitación), y agregar
   al Apéndice C una columna «Ingresos por QR / por revisión manual». Definir
   cuántos estudiantes se darán de alta para el piloto.
3. **`05-metodologia.tex:41-42`** dice que el prototipo «explica la reducción
   observada», lo que da por hecha una reducción. Propuesta: «establecer si el
   cambio de mecanismo se asocia con un cambio en los indicadores».
4. **`05-metodologia.tex` (Diseño):** agregar a las amenazas a la validez la
   instrumentación (los registros del sistema solo existen en el piloto), la
   novedad o efecto Hawthorne (los estudiantes saben que se les observa) y el
   número de puntos de revisión *c*.

### 2.2 Apéndice D (`d-plan-de-accion.tex`)

- La segunda serie de observación está en la fase 5 («repetir la observación»),
  pero `04-pregunta`, `05-metodologia` y `06-objetivos` la ubican **durante el
  piloto** (fase 4). Propuesta: fase 4 = cinco días hábiles de observación tras un
  periodo de adaptación de N días; fase 5 = solo análisis.
- La fase 2 no incluye la arquitectura ni el modelo entidad-relación (OT1).
  Propuesta: «Diseño del sistema (arquitectura y modelo entidad-relación),
  hardware y firmware».
- El piloto es de «periodo acotado» sin duración, y ninguna fase tiene semanas;
  la «T» de SMART solo se cumple por fase. Agregar duraciones.
- Faltan fases para las pruebas técnicas (OT4) y para el alta de estudiantes y el
  aviso de privacidad del piloto.

### 2.3 Instrumentos que no existen

- **Protocolo de pruebas técnicas** (propuesta: Apéndice E). Debe fijar niveles de
  iluminación, brillo y distancia; número de lecturas por condición (por ejemplo,
  n ≥ 30, para poder comprobar el 95 % provisional); hoja de registro; y la lista
  cerrada de casos de OT2: token vencido, repetido, alterado, firma inválida,
  estudiante dado de baja y desfase de reloj dentro y fuera de tolerancia.
- **Definición de indicadores en el Apéndice C:** qué columnas forman las
  incidencias (ver hallazgo 2 de la sección 1) y cómo se resume la «fila máxima»
  de una serie (¿promedio de los máximos por intervalo o máximo absoluto?).
- **Entrevista a vigilancia:** agregar un reactivo sobre qué información del
  registro le serviría durante su turno (valida los reportes de OT3).

### 2.4 Encuesta (Apéndice A)

- A9 es pregunta doble (credencial ajena / persona que no es estudiante):
  separarla.
- Escalas inconsistentes: A16 (Sí / Casi siempre / No), A17 (3 niveles), A18 (4
  niveles). Unificar, por ejemplo, Siempre / Casi siempre / A veces / Nunca, y
  definir cómo se codifica «viable».
- Reactivos que no alimentan ningún objetivo ni indicador: A4, A6, A7, A8, A10,
  A11, A12, A14, A15, A19 y B-Vig 1, 3 y 5. Vincularlos (por ejemplo, A5 para
  triangular el tiempo de espera, A14 para OI3) o eliminarlos.
- Muestra de OI2: «196 a 384» es un rango. Fijar el margen de error (0.05 o 0.07)
  y el procedimiento de selección (estratificado por turno) o declarar la muestra
  no probabilística y quitar el margen de error.

### 2.5 Ejes del problema sin objetivo

`03-problema.tex` (Lo que desconocemos) plantea durabilidad mecánica del
torniquete, ergonomía del lector (altura y ángulo de la cámara) y duración del
token. La duración del token y el desfase de reloj ya entran en OT2. Falta decidir
si la durabilidad y la ergonomía se incorporan a OT4 o se declaran fuera de
alcance en Delimitación.

### 2.6 Decisiones del equipo

- Confirmar la definición de incidencias de identidad (sección 1, hallazgo 2).
- Fijar la meta de lecturas exitosas (hoy 95 %, provisional) con el protocolo de
  pruebas.
- Fechas de calendario para cada fase (hoy los plazos van por fase).
- Fecha de la portada del PDF aparte (`\duedate` en `trabajo.tex`, hoy 30 de
  septiembre de 2026).

## 3. Trazabilidad pregunta → objetivo → instrumento

| Indicador / objetivo | Instrumento | Reactivo | Estado |
|---|---|---|---|
| Tiempo promedio de validación (OG, OI4) | Apéndice C | «Tiempos de revisión (s)», 5 estudiantes por intervalo | Cubierto |
| Longitud máxima de la fila (OG, OI4) | Apéndice C | «Fila máx.» | Cubierto; falta regla de resumen |
| Incidencias de identidad (OG, OI4) | Apéndice C | «Sin cred.», «Sin revisión», «Rechaz.» | Definida como propuesta; confirmar |
| Tasa de llegada, utilización (OI1) | Apéndice C | «Ingresos», *c* | Cubierto |
| Viabilidad del estudiante (OI2) | Apéndice A | A16, A17, A18 | Cubierto; falta regla de codificación |
| Aceptación (OI2) | Apéndice A | A13 (y A14, A15) | Cubierto en la tabla; falta indicador numérico |
| Requisitos legales (OI3) | Documental + Apéndice B | B-CE 4 | Cubierto |
| Reportes del panel (OT3) | Apéndice B | B-CE 3 | Parcial; falta reactivo a vigilancia |
| Pruebas de OT2 y OT4 | — | — | **Sin instrumento** (ver 2.3) |
| OT1 (diagramas) | Producto | — | Sin fase explícita en D (ver 2.2) |

## 4. Indicadores retirados de la sección (para recuperarlos)

Por pedido del equipo se quitó, por el momento, la subsección «Indicadores y
Plazos» y su tabla (Tabla 3). Además, los objetivos específicos pasaron de tabla
a lista con viñetas, cada uno con su «porque». El contenido de la tabla, listo
para volver a pegar al final de `secciones/06-objetivos.tex`, antes de
«Relación con la Pregunta de Investigación» (usa la columna `P` definida en
`trabajo.tex`):

```latex
\subsection{Indicadores y Plazos}
La Tabla~\ref{tab:obj-smart} indica el indicador o la meta con que se comprueba
cada objetivo y la fase del Plan de Acción Preliminar (Apéndice~D) en la que
debe cumplirse. Las fechas de calendario las fijará el equipo con la profesora.

\begin{table}[tbp]
	\caption{Indicador, Evidencia y Plazo de los Objetivos}
	\label{tab:obj-smart}
	\small\linespread{1}\selectfont
	\begin{tabular}{@{}lP{7.6cm}P{3.9cm}P{2.2cm}@{}}
		\toprule
		Clave & Indicador o meta & Evidencia & Plazo (fase) \\
		\midrule
		OT1 & Diagrama de componentes y modelo entidad-relación que cubren todos los elementos de \figarq. & Diagramas & 2 \\[0.6em]
		OT2 & 100\,\% de los casos de prueba con token vencido, repetido o alterado son rechazados. & Bitácora de pruebas & 3 \\[0.6em]
		OT3 & Un ingreso validado y registrado de extremo a extremo, y tres reportes disponibles en el panel. & Demostración y registros & 2 y 3 \\[0.6em]
		OT4 & Tiempo de una lectura completa en banco (captura, decodificación y consulta) menor que el tiempo medio de validación de la línea base (Apéndice~C); 95\,\% o más de lecturas exitosas (meta provisional). & Hoja de registro de pruebas técnicas (por elaborar) & 3 (antes del piloto) \\[0.6em]
		OI1 & Tasa de llegada, tiempo medio de validación, utilización, fila máxima e incidencias calculados en los 40 intervalos de cinco días, e identificación de los intervalos con utilización igual o mayor que 1. & Hojas de observación & 1 \\[0.6em]
		OI2 & Proporción de estudiantes con celular propio, conexión y batería, y proporción que declara disposición a usar el QR, con la muestra mínima del Apéndice~A (196 a 384 estudiantes según el margen de error). & Encuestas & 1 \\[0.6em]
		OI3 & Lista de requisitos legales, cada uno con la ley de la que proviene, incorporados al diseño, con el aviso de privacidad y el periodo de conservación definidos antes del piloto. & Documento de requisitos & 1 y 2 \\[0.6em]
		OI4 & Diferencia entre línea base y piloto en tiempo medio de validación, fila máxima e incidencias, con su valor de contraste en los 40 pares de intervalos. & Hojas de observación & 4 y 5 \\
		\bottomrule
	\end{tabular}
	\tablenote{Elaboración propia. Fases del Apéndice~D: 1 diagnóstico, 2 diseño
		de hardware y firmware, 3 desarrollo del servidor, 4 piloto controlado,
		5 evaluación. Los 40 intervalos son 8 de cinco minutos por día durante
		cinco días. La meta de lecturas exitosas es una propuesta del equipo que se
		ajustará con las pruebas, y el 100\,\% de OT2 es un criterio de aceptación
		de las pruebas, no un resultado de investigación. Las incidencias de
		identidad se expresan como tasa por ingresos: (sin credencial + rechazos) /
		ingresos; un sistema que detecta mejor puede registrar más incidencias, por
		lo que se interpretan como capacidad de detección. Los casos «sin revisión»
		se reportan aparte.}
\end{table}
```

Mientras la tabla esté fuera, los hallazgos 2 (definición de incidencias), 6 y 7
de la sección 1 quedan sin reflejo en el texto: la definición de incidencias
(sin credencial + rechazos, sobre ingresos, leída como capacidad de detección)
y la meta provisional de 95 % de lecturas siguen siendo decisiones pendientes.
