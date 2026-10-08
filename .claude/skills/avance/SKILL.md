---
name: avance
description: Prepara una entrega (avance) del trabajo. Revisa datos de portada, compila, verifica citas y formato, y genera el PDF con nombre de entrega. Úsalo cuando el usuario diga que va a entregar o quiera preparar el siguiente avance.
argument-hint: <número de avance, p. ej. 2>
---

# Preparar la entrega del avance $ARGUMENTS

Sigue los pasos en orden y reporta el resultado de cada uno.

## 1. Requisitos de la entrega

Pregunta al usuario qué pide el profesor para este avance (secciones nuevas, extensión, formato), salvo que ya lo haya dicho o exista un PDF de indicaciones en el proyecto; en ese caso léelo. Compara lo pedido contra las secciones existentes y lista lo que falta.

## 2. Datos de portada (`trabajo.tex`)

Revisa y muestra para confirmar:
- Comentario del encabezado (`Avance N`).
- `\title`, `\authorsnames` (todos los integrantes), `\course`, `\professor`.
- `\duedate`: fecha de esta entrega.

## 3. Calidad

- Ejecuta la skill `compilar`. Debe terminar sin errores ni citas sin definir.
- Lanza en paralelo `verificador-citas` (todo el documento) y `revisor-apa`.
- Busca restos de trabajo pendiente: `TODO`, `XXX`, `??`, `[CITA]`, texto en inglés de plantilla.

No sigas al paso 4 si hay errores graves; muéstralos y pregunta si se corrigen primero.

## 4. PDF de entrega

Copia `trabajo.pdf` como `Avance $ARGUMENTS.pdf` en la raíz del proyecto. Reporta número de páginas y un resumen de lo verificado.
