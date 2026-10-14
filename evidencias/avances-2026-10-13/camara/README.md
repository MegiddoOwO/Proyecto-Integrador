# Capturas reales de una sesión adicional

Se obtuvieron el 13 de octubre de 2026 entre las 19:04:08 y las 19:04:21
(UTC-06:00), con la cámara local y la participación autorizada por el usuario
en la conversación.

- `01-deteccion.png`: vista de la aplicación al localizar el rostro.
- `02-parpadeo.png`: vista de la aplicación al detectar un parpadeo.
- Los archivos terminados en `-camara.png` conservan los cuadros de cámara
  de esos mismos instantes.
- `sesion-camara.json`: fecha, evento, puntuaciones, dimensiones y duración
  del procesamiento de cada cuadro.

La sesión usa `vida.Pose` del prototipo mediante
`scripts/capturar_pruebas_camara.py`. Documenta detección de rostro y
parpadeo, sin comparación de identidad. Se conserva separada del CSV de 45
intentos; las capturas no se suman a sus métricas de reconocimiento.
