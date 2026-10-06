# Cómo dejar la plantilla en APA 7 puro

La plantilla `trabajo.tex` usa la clase `apa7` en modo estudiante (`stu`) y trae
algunas modificaciones que pide la escuela pero que **no son parte de APA**.
Este archivo explica cuáles son y cómo quitarlas.

Referencia: *Student Paper Setup Guide*, APA, actualizada el 8 de octubre de 2025
(<https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf>).
La propia guía aclara: *"Instructors' guidelines supersede APA Style"*, es decir,
lo que pida tu profesor tiene prioridad sobre APA.

Compilar: `latexmk -pdf trabajo.tex`

---

## Modificaciones que NO son APA

Para APA puro, aplica los 5 cambios.

### 1. Logos en la portada

**APA:** la portada no lleva logos.

**Dónde:** preámbulo, bloque `% Logos arriba de la portada`.

**Cómo quitarlo:** comenta (con `%`) las líneas de la opción activa:

```latex
% \newcommand{\hrm}{\noindent
%   \includegraphics[height=1.6cm]{img/tescha_logo.png}\hfill
%   \includegraphics[height=1.6cm]{img/logo_sitemas.png}\par}
```

### 2. Índice

**APA:** los trabajos de estudiante no llevan índice. El orden es portada
(página 1), texto (desde la página 2) y referencias (en página nueva).

**Dónde:** son dos lugares.

1. En el preámbulo, borra todo el bloque `% Índice después de la portada`
   (desde `\setcounter{tocdepth}{2}` hasta `\newcommand{\apendiceindice}...`).
2. En el cuerpo, borra la línea `\apendiceindice{...}` debajo de cada apéndice.
   Si no la borras, la compilación falla con `Undefined control sequence`.

### 3. Portada sin número de página

**APA:** todas las páginas llevan número arriba a la derecha, incluida la
portada, que es la página 1.

**Dónde:** preámbulo.

**Cómo quitarlo:** borra esta línea:

```latex
\fancypagestyle{titlepage}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}}
```

### 4. Tablas y figuras centradas

**APA:** la tabla y la imagen van alineadas a la izquierda, igual que su
número, título y nota.

**Dónde:** en cada `table` y `figure` del cuerpo.

**Cómo quitarlo:** quita las llaves, `\centering` y el `\par` final:

```latex
% Centrado (plantilla)
{\centering
\includegraphics[width=0.6\textwidth]{img/figura}\par}

% APA puro
\includegraphics[width=0.6\textwidth]{img/figura}
```

En las tablas es lo mismo: deja solo `\begin{tabular}...\end{tabular}`.

### 5. Tablas y figuras a la mitad de la página

**APA:** recomienda evitar la mitad de la página. Deben ir al final o al inicio
de una página, o solas en su propia página, siempre después de mencionarlas en
el texto.

**Dónde:** en cada `table` y `figure` del cuerpo.

**Cómo quitarlo:** quita la `h`:

```latex
\begin{table}[tbp]    % en lugar de [htbp]
\begin{figure}[tbp]
```

---

## Ajustes que SÍ son APA (no los quites)

Estos cambios corrigen detalles de `apa7` o `biblatex-apa` para que el resultado
cumpla la norma en español:

| Ajuste | Por qué |
|---|---|
| `\usepackage{tgheros}` + `\sfdefault`, 11 pt | Sans serif tipo Arial a 11 pt, aceptada por APA. Para Times New Roman usa `\usepackage{newtxtext,newtxmath}` y cambia a `12pt`. |
| `babel` con `spanish,es-tabla` | Textos en español y "Tabla" en lugar de "Cuadro". |
| `\renewcommand{\figurenote}` y `\tablenote` | APA pide las notas con la misma letra que el texto y a doble espacio; `apa7` las ponía pequeñas. |
| `\DeclareDelimFormat{finalnamedelim}` | "y" en lugar de "&", como en la edición en español del manual APA 7. Si tu profesor pide "&", bórralo. |
| `\DefineBibliographyExtras{spanish}` | Rangos de páginas con guion medio (45–67); `biblatex` en español ponía guion corto. |
| `\AtBeginDocument{... Palabras clave, Nota ...}` | Corrige traducciones de `apa7` ("Palabras Claves", "Note"). |
| `\hypersetup{hidelinks}` | Enlaces sin recuadros de color. |
| `\setlength{\headheight}{15.4pt}` | Solo evita una advertencia al compilar. |
| Bloque `\@ifundefined{def@stu}` | En modo `stu` ignora el título corto y la nota del autor, que APA no usa en trabajos de estudiante. |

---

## Recordatorios de APA para trabajos de estudiante

- **Resumen:** no va, salvo que el profesor lo pida. Para usarlo, descomenta
  `\abstract{...}` y `\keywords{...}`.
- **Introducción:** no se titula "Introducción"; el título del trabajo se
  repite al inicio del texto (la clase lo hace sola).
- **Títulos:** cada sección principal empieza con nivel 1 (`\section`). No
  dejes una sola subsección dentro de una sección: usa dos o más, o ninguna.
- **Tablas y figuras:** menciónalas en el texto antes de que aparezcan.
- **Referencias:** usa DOI cuando exista. Pon fecha de consulta (`urldate`)
  solo si el contenido cambia con el tiempo y no está archivado.
- **Modo profesional:** para enviar a una revista, cambia `stu` por `man`,
  llena `\shorttitle` y `\authornote`, y descomenta el resumen (ahí es
  obligatorio).
