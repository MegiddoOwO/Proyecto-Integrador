"""Piezas compartidas: motores de reconocimiento, cámara, registros y dibujo.

Motores (--motor):
- sface:     detector YuNet + reconocimiento SFace (OpenCV, Apache 2.0).
- buffalo_s: detector SCRFD-500MF + ArcFace MobileFaceNet (InsightFace).
- buffalo_l: detector SCRFD-10GF + ArcFace ResNet50 (InsightFace).
Los modelos de InsightFace son solo para investigación no comercial.
"""

import os
import warnings
from dataclasses import dataclass
from pathlib import Path

# El Qt que trae opencv-python no tiene plugin de Wayland ni fuentes: se usa
# X11 (XWayland) y las fuentes del sistema para evitar avisos en la terminal.
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
if Path("/usr/share/fonts/dejavu-sans-fonts").is_dir():
    os.environ.setdefault("QT_QPA_FONTDIR", "/usr/share/fonts/dejavu-sans-fonts")
# Avisos de obsolescencia internos de InsightFace.
warnings.filterwarnings("ignore", category=FutureWarning, module="insightface")

import cv2 as cv  # noqa: E402
import numpy as np  # noqa: E402

cv.utils.logging.setLogLevel(cv.utils.logging.LOG_LEVEL_ERROR)

RAIZ = Path(__file__).resolve().parent
DIR_MODELOS = RAIZ / "modelos"
DIR_INSIGHTFACE = DIR_MODELOS / "insightface"
DIR_ROSTROS = RAIZ / "datos" / "rostros"
CSV_RESULTADOS = RAIZ / "resultados" / "pruebas.csv"
MOTORES = ["sface", "buffalo_s", "buffalo_l"]


@dataclass
class Cara:
    caja: np.ndarray  # x, y, ancho, alto
    puntos: np.ndarray  # 5 x 2: ojo (izq. de la imagen), ojo, nariz, boca, boca
    datos: object  # lo que el motor necesita para obtener el vector


def verificar_modelo(ruta: Path) -> Path:
    if not ruta.exists():
        raise SystemExit(f"Falta el modelo {ruta}. Ver README.md.")
    return ruta


class MotorSFace:
    """YuNet + SFace. Umbral 0.363: el que recomienda la documentación de OpenCV."""

    umbral = 0.363

    def __init__(self) -> None:
        self.detector = cv.FaceDetectorYN.create(
            str(verificar_modelo(DIR_MODELOS / "face_detection_yunet_2023mar.onnx")),
            "", (320, 320), 0.9, 0.3, 5000,
        )
        self.reconocedor = cv.FaceRecognizerSF.create(
            str(verificar_modelo(DIR_MODELOS / "face_recognition_sface_2021dec.onnx")), ""
        )

    def detectar(self, imagen: np.ndarray) -> list[Cara]:
        alto, ancho = imagen.shape[:2]
        self.detector.setInputSize((ancho, alto))
        _, filas = self.detector.detect(imagen)
        if filas is None:
            return []
        caras = [Cara(f[:4].copy(), f[4:14].reshape(5, 2).copy(), f) for f in filas]
        return sorted(caras, key=lambda c: -c.caja[2] * c.caja[3])

    def vector(self, imagen: np.ndarray, cara: Cara) -> np.ndarray:
        alineado = self.reconocedor.alignCrop(imagen, cara.datos)
        return self.reconocedor.feature(alineado).flatten().copy()


class MotorInsightFace:
    """SCRFD + ArcFace de un paquete de InsightFace (buffalo_s o buffalo_l).

    Umbral 0.40: el valor base de similitud coseno que usa la propia
    InsightFace en su configuración de PrivateFrame. Hay que calibrarlo.
    """

    umbral = 0.40

    def __init__(self, paquete: str) -> None:
        from insightface.app import FaceAnalysis

        verificar_modelo(DIR_INSIGHTFACE / "models" / paquete)
        self.app = FaceAnalysis(
            name=paquete, root=str(DIR_INSIGHTFACE),
            allowed_modules=["detection", "recognition"], providers=["CPUExecutionProvider"],
        )
        self.app.prepare(ctx_id=-1, det_size=(640, 640))

    def detectar(self, imagen: np.ndarray) -> list[Cara]:
        from insightface.app.common import Face

        cajas, puntos = self.app.det_model.detect(imagen, max_num=0)
        caras = []
        for caja, kps in zip(cajas, puntos):
            x1, y1, x2, y2 = caja[:4]
            caras.append(Cara(np.array([x1, y1, x2 - x1, y2 - y1]), kps.copy(),
                              Face(bbox=caja[:4], kps=kps, det_score=caja[4])))
        return sorted(caras, key=lambda c: -c.caja[2] * c.caja[3])

    def vector(self, imagen: np.ndarray, cara: Cara) -> np.ndarray:
        return self.app.models["recognition"].get(imagen, cara.datos).flatten().copy()


def crear_motor(nombre: str):
    return MotorSFace() if nombre == "sface" else MotorInsightFace(nombre)


def similitud(v1: np.ndarray, v2: np.ndarray) -> float:
    """Similitud coseno entre dos vectores (1 = idénticos)."""
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def abrir_camara(fuente: str) -> cv.VideoCapture:
    """Abre la webcam (índice, p. ej. "0") o un stream (URL del ESP32-CAM)."""
    cam = cv.VideoCapture(int(fuente) if fuente.isdigit() else fuente)
    if not cam.isOpened():
        raise SystemExit(f"No se pudo abrir la cámara: {fuente}")
    return cam


def cargar_registrados(motor: str) -> dict[str, np.ndarray]:
    """Vectores guardados por sujeto para un motor: {sujeto: (n_fotos, dim)}."""
    return {p.stem: np.load(p) for p in sorted((DIR_ROSTROS / motor).glob("*.npy"))}


def identificar(motor, vector: np.ndarray, registrados: dict[str, np.ndarray]) -> tuple[str | None, float]:
    """Sujeto más parecido y su similitud; None si nadie supera el umbral."""
    mejor, mejor_sim = None, -1.0
    for sujeto, vectores in registrados.items():
        sim = max(similitud(vector, v) for v in vectores)
        if sim > mejor_sim:
            mejor, mejor_sim = sujeto, sim
    return (mejor if mejor_sim >= motor.umbral else None), mejor_sim


def dibujar_caja(imagen: np.ndarray, caja: np.ndarray, color) -> None:
    x, y, w, h = caja.astype(int)
    cv.rectangle(imagen, (x, y), (x + w, y + h), color, 2)


def texto(imagen: np.ndarray, mensaje: str, fila: int, color=(255, 255, 255)) -> None:
    pos = (10, 30 + 30 * fila)
    cv.putText(imagen, mensaje, pos, cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
    cv.putText(imagen, mensaje, pos, cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def mostrar(ventana: str, cuadro: np.ndarray, caja, lineas: list[tuple[str, tuple]]) -> int:
    """Muestra el cuadro en espejo (más natural para quien se ve) y lee tecla."""
    vista = cuadro.copy()
    if caja is not None:
        dibujar_caja(vista, caja, (255, 255, 0))
    vista = cv.flip(vista, 1)
    for i, (mensaje, color) in enumerate(lineas):
        texto(vista, mensaje, i, color)
    cv.imshow(ventana, vista)
    return cv.waitKey(1) & 0xFF
