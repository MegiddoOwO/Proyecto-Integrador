"""Pruebas de vida: ¿hay una persona real frente a la cámara o una foto/pantalla?

- Pasiva: modelo de InsightFace (liveness.onnx) sobre un solo cuadro. No le
  pide nada a la persona. Solo investigación no comercial.
- Activa: reto aleatorio con MediaPipe Face Landmarker (Apache 2.0): girar la
  cabeza a cada lado y parpadear, en orden aleatorio, y volver al frente.
  Además mide la paralaje de la nariz para descartar una foto inclinada.
"""

import math
import random
import time

import cv2 as cv
import numpy as np

from comun import DIR_INSIGHTFACE, DIR_MODELOS, identificar, mostrar, verificar_modelo

# Pasiva: probabilidad mínima de "vivo". 0.8 es el valor por defecto de
# InsightFace; ellos mismos aclaran que hay que validarlo.
UMBRAL_PASIVA = 0.8

# Activa (grados de giro respecto a la pose inicial; positivo = hacia la
# izquierda de la persona).
GIRO_GRADOS = 20.0
FRENTE_GRADOS = 12.0
PARPADEO_CERRADO = 0.5  # blendshape eyeBlink: 0 abierto, 1 cerrado
PARPADEO_ABIERTO = 0.3
SEGUNDOS_POR_PASO = 5.0
# Paralaje mínima (fracción de la distancia entre ojos) que deben mostrar los
# dos giros. Con fotos planas inclinadas o rotadas MediaPipe dio hasta ~0.06.
# Valor inicial: calíbrenlo con los valores que se imprimen.
PARALAJE_MIN = 0.12

# Puntos de MediaPipe: punta de la nariz, esquinas externas de los ojos y
# comisuras de la boca.
NARIZ, OJO_A, OJO_B, BOCA_A, BOCA_B = 1, 33, 263, 61, 291


class VidaPasiva:
    def __init__(self) -> None:
        from insightface.addons.liveness import Liveness

        modelo = verificar_modelo(DIR_INSIGHTFACE / "addons" / "liveness.onnx")
        self.modelo = Liveness(str(modelo), threshold=UMBRAL_PASIVA, providers=["CPUExecutionProvider"])

    def evaluar(self, imagen: np.ndarray, puntos: np.ndarray) -> tuple[bool, str]:
        r = self.modelo.predict(imagen, puntos)
        if r["status"] != "ok":
            # No es una foto: la cara está muy cerca o en el borde del cuadro.
            return False, "pasiva_rostro_cortado(alejate_o_centrate)"
        return bool(r["is_live"]), f"pasiva={r['live_score']:.2f}"


class Pose:
    """Giro de la cabeza, parpadeo y puntos de la cara con MediaPipe."""

    def __init__(self) -> None:
        import mediapipe as mp
        from mediapipe.tasks.python import BaseOptions, vision

        self.mp = mp
        modelo = verificar_modelo(DIR_MODELOS / "mediapipe" / "face_landmarker.task")
        self.detector = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(modelo)),
            output_face_blendshapes=True, output_facial_transformation_matrixes=True,
        ))

    def medir(self, imagen: np.ndarray) -> dict | None:
        rgb = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
        r = self.detector.detect(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rgb))
        if not r.face_landmarks:
            return None
        rot = np.array(r.facial_transformation_matrixes[0])[:3, :3]
        alto, ancho = imagen.shape[:2]
        formas = {c.category_name: c.score for c in r.face_blendshapes[0]}
        return {
            "giro": math.degrees(math.atan2(rot[0, 2], rot[2, 2])),
            "parpadeo": min(formas["eyeBlinkLeft"], formas["eyeBlinkRight"]),
            "puntos": np.array([[p.x * ancho, p.y * alto] for p in r.face_landmarks[0]], np.float32),
        }


def paralaje(referencia: np.ndarray, actual: np.ndarray) -> float:
    """Cuánto se aparta la nariz de lo que predice un rostro plano.

    Con los ojos y las comisuras (4 puntos) se calcula la homografía entre la
    pose de referencia y la actual. Si el rostro fuera plano (una foto, una
    pantalla), esa homografía predice exactamente dónde queda la nariz. En una
    cara real la nariz sobresale y, al girar, se aparta de esa predicción.
    Se devuelve el error normalizado por la distancia entre los ojos.
    """
    plano = [OJO_A, OJO_B, BOCA_A, BOCA_B]
    h = cv.getPerspectiveTransform(referencia[plano], actual[plano])
    predicha = cv.perspectiveTransform(referencia[[NARIZ]][None], h)[0, 0]
    distancia_ojos = np.linalg.norm(actual[OJO_A] - actual[OJO_B])
    return float(np.linalg.norm(predicha - actual[NARIZ]) / max(distancia_ojos, 1.0))


def prueba_activa(cam, pose: Pose, inicial: dict, motor, registrados, identidad: str) -> tuple[bool, str]:
    """Reto aleatorio: girar a cada lado y parpadear, luego volver al frente.

    `inicial` es la medición de MediaPipe en el cuadro donde se reconoció a la
    persona. Al volver al frente se reconoce de nuevo para que no pueda
    cambiar la persona a mitad de la prueba. Devuelve (pasó, motivo).
    """
    pasos = random.sample(["izquierda", "derecha", "parpadea"], 3) + ["frente"]
    instrucciones = {
        "izquierda": "Gira la cabeza a tu IZQUIERDA", "derecha": "Gira la cabeza a tu DERECHA",
        "parpadea": "PARPADEA", "frente": "Mira de FRENTE",
    }
    paralajes: list[float] = []
    for paso in pasos:
        limite = time.perf_counter() + SEGUNDOS_POR_PASO
        vio_abiertos = False
        # Lo más cerca que llegó de cumplir, para el diagnóstico: grados de
        # giro hacia el lado pedido, cierre de ojos (0 a 1) o grados que le
        # faltaron para quedar de frente.
        mejor = None
        while True:
            restante = limite - time.perf_counter()
            if restante <= 0:
                if mejor is None:
                    return False, f"no_cumplio_{paso}(sin_rostro)"
                if paso == "parpadea":
                    return False, f"no_cumplio_parpadea(max_cierre={mejor:.2f})"
                if paso == "frente":
                    return False, f"no_cumplio_frente(min_giro={-mejor:.0f}°)"
                return False, f"no_cumplio_{paso}(max_giro={mejor:.0f}°)"
            ok, cuadro = cam.read()
            if not ok:
                raise SystemExit("La cámara dejó de enviar imágenes.")
            m = pose.medir(cuadro)
            if m is None:
                estado = "No veo un rostro"
            else:
                delta = m["giro"] - inicial["giro"]
                estado = f"{restante:.1f} s | giro={delta:+.0f} | parpadeo={m['parpadeo']:.2f}"
            tecla = mostrar("Reconocimiento", cuadro, None, [
                ("PRUEBA DE VIDA", (0, 255, 255)),
                (instrucciones[paso], (0, 255, 255)),
                (estado, (255, 255, 255)),
            ])
            if tecla == ord("q"):
                return False, "cancelada"
            if m is None:
                continue
            valor = {"izquierda": delta, "derecha": -delta, "parpadea": m["parpadeo"],
                     "frente": -abs(delta)}[paso]
            mejor = valor if mejor is None else max(mejor, valor)
            if paso == "izquierda" and delta >= GIRO_GRADOS or paso == "derecha" and delta <= -GIRO_GRADOS:
                paralajes.append(paralaje(inicial["puntos"], m["puntos"]))
                break
            if paso == "parpadea":
                vio_abiertos |= m["parpadeo"] < PARPADEO_ABIERTO
                if vio_abiertos and m["parpadeo"] > PARPADEO_CERRADO:
                    break
            if paso == "frente" and abs(delta) <= FRENTE_GRADOS:
                valores = "/".join(f"{p:.2f}" for p in paralajes)
                if min(paralajes) < PARALAJE_MIN:
                    return False, f"rostro_plano(paralaje={valores})"
                caras = motor.detectar(cuadro)
                if not caras:
                    continue
                otra, _ = identificar(motor, motor.vector(cuadro, caras[0]), registrados)
                if otra != identidad:
                    return False, "cambio_de_persona"
                return True, f"paralaje={valores}"
