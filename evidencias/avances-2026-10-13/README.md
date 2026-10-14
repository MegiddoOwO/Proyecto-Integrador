# Prueba de concepto: reconocimiento facial

Prueba de banco del proyecto _Escanea y Entra_ para comparar el reconocimiento
facial con el QR dinámico y el NFC. No forma parte del piloto en la entrada del
TESCHA: se corre en laboratorio, con voluntarios.

## Motores y pruebas de vida

| `--motor`             | Detección + reconocimiento                        | Umbral de similitud                                 | Licencia de los modelos         |
| --------------------- | ------------------------------------------------- | --------------------------------------------------- | ------------------------------- |
| `sface` (por defecto) | YuNet + SFace (OpenCV)                            | 0.363, el que recomienda la documentación de OpenCV | Apache 2.0                      |
| `buffalo_s`           | SCRFD-500MF + ArcFace MobileFaceNet (InsightFace) | 0.40, el valor base de InsightFace                  | Solo investigación no comercial |
| `buffalo_l`           | SCRFD-10GF + ArcFace ResNet50 (InsightFace)       | 0.40, el valor base de InsightFace                  | Solo investigación no comercial |

| `--vida`           | Qué hace                                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `no` (por defecto) | Solo reconoce                                                                                                                         |
| `pasiva`           | Modelo de InsightFace (`liveness.onnx`) sobre un cuadro: dice si es una cara real o una foto o pantalla. No le pide nada a la persona |
| `activa`           | Reto aleatorio con MediaPipe: girar a la izquierda, a la derecha y parpadear, en orden aleatorio, y volver al frente                  |
| `ambas`            | Pasiva y después activa                                                                                                               |

Los umbrales son valores iniciales y **hay que calibrarlos** con sus pruebas
(ver más abajo). Están en `comun.py` (similitud) y `vida.py` (vida).

## Instalación

Requiere [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Los modelos van en `modelos/` (unos 530 MB, fuera de git). Si faltan:

```bash
cd modelos
curl -LO https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
curl -LO https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx
mkdir -p insightface/models insightface/addons mediapipe
curl -L -o insightface/addons/liveness.onnx https://github.com/deepinsight/insightface-model-addons/releases/download/addons/liveness.onnx
for m in buffalo_s buffalo_l; do
  curl -L -o /tmp/$m.zip https://github.com/deepinsight/insightface/releases/download/model-zoo/$m.zip
  unzip -o /tmp/$m.zip -d insightface/models/$m && rm /tmp/$m.zip
done
curl -L -o mediapipe/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
```

## Uso

1. **Registrar** a cada voluntario (pide confirmar el consentimiento):

   ```bash
   uv run registrar.py --sujeto s01
   ```

   Captura 5 fotos con ESPACIO, **de frente y con la luz de las pruebas**, y
   calcula los vectores de los tres motores con las mismas capturas. Solo guarda
   los vectores (`datos/rostros/<motor>/s01.npy`), no las fotos. Los vectores de
   un motor no sirven para otro.

2. **Probar**, con una corrida de 20 intentos por combinación y condición
   (ESPACIO = un intento):

   ```bash
   # El titular debe pasar
   uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion luz_normal --esperado acepta
   uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion luz_baja   --esperado acepta
   # Suplantaciones: no deben pasar
   uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion foto_celular --esperado rechaza
   uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion foto_impresa --esperado rechaza
   uv run reconocer.py --motor buffalo_l --vida ambas --sujeto x01 --condicion no_registrado --esperado rechaza
   ```

   Repitan las mismas condiciones cambiando `--motor` y `--vida` para
   comparar. Cada intento se agrega a `resultados/pruebas.csv`, con
   `tecnologia = facial-<motor>+vida_<modo>`.

3. **Resumir**:

   ```bash
   uv run analizar.py
   ```

   Muestra por combinación y condición el % de aciertos, los falsos rechazos,
   las falsas aceptaciones y el tiempo (media, mediana, máximo).

4. **Borrar los datos biométricos** al terminar:

   ```bash
   uv run borrar_datos.py --todo
   ```

## Sesiones con voluntarios (`sesion.py`)

Para no etiquetar mal ninguna corrida, `sesion.py` guía la sesión completa:
registra al voluntario si hace falta y, condición por condición, dice qué
preparar y corre `reconocer.py` con cada combinación de la matriz
(`sface` sin vida, `buffalo_l` sin vida, `buffalo_l` con vida pasiva).

```bash
uv run sesion.py --sujeto s02             # voluntario: luz_normal, luz_baja, foto_celular
uv run sesion.py --sujeto x01 --impostor  # persona no registrada: no_registrado
```

En cada paso: Enter empieza, `s` lo salta, `q` termina. La matriz y las
condiciones están al inicio de `sesion.py`.

## Prueba de vida activa

Pide en orden aleatorio girar a la izquierda, girar a la derecha y parpadear
(5 s por paso), y luego volver al frente. Se rechaza (`rechaza_vida`) si:

- no cumple un paso a tiempo (`no_cumplio_izquierda`, `no_cumplio_parpadea`…);
- el rostro **no tiene volumen** (`rostro_plano`). Con los ojos y las comisuras
  se predice dónde quedaría la nariz si el rostro fuera plano (una foto o una
  pantalla). En una cara real la nariz sobresale y se aparta de esa predicción:
  esa diferencia es la _paralaje_. Sin esta comprobación, una foto inclinada
  podría «cumplir» los giros;
- al volver al frente ya no es la misma persona (`cambio_de_persona`).

El giro se mide en grados respecto a la pose del primer cuadro, así que la
cámara no tiene que estar exactamente enfrente.

Limitaciones: no detiene un **video** de la persona que haga el reto en el orden
pedido, ni una máscara 3D. El orden aleatorio lo dificulta, pero no lo impide.

## Calibrar los umbrales

Cada intento imprime los valores con los que se decidió, por ejemplo:

```
OK: acepta s01 sim=0.612 pasiva=0.97 paralaje=0.21/0.25 4210 ms
```

| Valor      | Dónde se cambia                      | Inicial      | Cómo calibrarlo                                                                    |
| ---------- | ------------------------------------ | ------------ | ---------------------------------------------------------------------------------- |
| `sim`      | `umbral` de cada motor en `comun.py` | 0.363 / 0.40 | Anoten `sim` del titular y de otras personas; el umbral va entre ambos grupos      |
| `pasiva`   | `UMBRAL_PASIVA` en `vida.py`         | 0.8          | Compárenlo entre caras reales y fotos o pantallas                                  |
| `paralaje` | `PARALAJE_MIN` en `vida.py`          | 0.12         | Caras reales contra fotos inclinadas. Con fotos planas de prueba salió hasta ~0.06 |
| giro       | `GIRO_GRADOS` en `vida.py`           | 20°          | Si a la gente le cuesta, bájenlo                                                   |

Si al girar a **tu** izquierda no avanza y al girar a la derecha sí, la
dirección está invertida: intercambien los signos de `delta` en `prueba_activa`.

## Usar el ESP32-CAM como cámara

Carguen al ESP32-CAM el ejemplo _CameraWebServer_ de Arduino y pasen la URL
del stream:

```bash
uv run reconocer.py --camara http://IP_DEL_ESP32:81/stream --sujeto s01 --condicion esp32cam --esperado acepta
```

El ESP32-CAM solo captura; la laptop hace el reconocimiento.

## Qué mide `tiempo_ms`

Va desde ESPACIO hasta la decisión. Sin vida activa es solo el procesamiento
en la laptop (detectar, obtener el vector, comparar y, si aplica, la vida
pasiva). Con vida activa incluye **el tiempo que la persona tarda en hacer el
reto**, que es lo que costaría en una fila.

No incluye el tiempo que tarda la persona en acomodarse frente a la cámara, ni
la transmisión del cuadro cuando se usa el ESP32-CAM. Para comparar con el QR y
el NFC, midan las tres tecnologías de la misma forma, o cronometren aparte el
tiempo total por persona.

## Formato del CSV

```
fecha_hora, tecnologia, sujeto, condicion, resultado_esperado,
resultado_obtenido, identidad_detectada, similitud, tiempo_ms, correcto
```

Es el formato común propuesto para las pruebas de QR y NFC (`tecnologia` =
`qr`, `nfc` o `facial-...`), así que `analizar.py` sirve para las tres.

## Ética y datos personales

- Solo integrantes del equipo o voluntarios con consentimiento por escrito.
- Usen códigos (`s01`, `s02`…) en lugar de nombres.
- `datos/`, `resultados/` y `modelos/` están en `.gitignore`: no se suben a git.
- Al terminar, `borrar_datos.py --todo`.
- Sin prueba de vida se espera que una foto engañe al sistema; medirlo, y
  compararlo con `--vida`, es parte de la prueba.
