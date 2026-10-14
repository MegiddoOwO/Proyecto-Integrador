"""Captura evidencia real de detección de rostro y parpadeo.

Usa el módulo de pose del prototipo, sin comparar identidades ni modificar
el CSV histórico de reconocimiento. Las capturas son automáticas; Q sale.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2 as cv


ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = Path("/home/d4n/Documentos/local/reconocimiento_facial")
DEST = ROOT / "evidencias" / "avances-2026-10-13" / "camara"
sys.path.insert(0, str(PROTOTYPE))
from vida import Pose


def timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def main():
    DEST.mkdir(exist_ok=True)
    manifest = {
        "inicio": timestamp(),
        "tipo": "Prueba adicional de deteccion y parpadeo con camara en vivo",
        "modulo": "vida.Pose del prototipo de reconocimiento facial",
        "identificacion": "No se comparan identidades ni se almacenan vectores nuevos",
        "csv_historico": "Sin cambios; estas capturas no son nuevos intentos del CSV",
        "capturas": [],
    }
    camera = cv.VideoCapture(0, cv.CAP_V4L2)
    if not camera.isOpened():
        raise SystemExit("No se pudo abrir la camara 0.")
    camera.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv.CAP_PROP_FPS, 30)
    pose = Pose()
    name = "Escanea y Entra - Prueba en camara"
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.resizeWindow(name, 780, 790)
    phase = 1
    stable = None
    saw_open = False
    phase_two_start = None
    finished_at = None
    start = time.monotonic()

    def save(view, frame, measurements, event, inference_ms):
        filename = "01-deteccion.png" if event == "rostro_localizado" else "02-parpadeo.png"
        if not cv.imwrite(str(DEST / filename), view):
            raise RuntimeError("No se pudo guardar la captura.")
        cv.imwrite(str(DEST / filename.replace(".png", "-camara.png")), frame)
        manifest["capturas"].append({
            "archivo": filename, "fecha_hora": timestamp(), "evento": event,
            "parpadeo": float(measurements["parpadeo"]),
            "giro_grados": float(measurements["giro"]),
            "inferencia_cuadro_ms": round(inference_ms, 2),
            "ancho_cuadro": frame.shape[1], "alto_cuadro": frame.shape[0],
        })
        (DEST / "sesion-camara.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print("CAPTURA GUARDADA:", filename, event, flush=True)

    print("CAMARA ABIERTA: mira de frente; la primera captura se guarda al mantener el rostro visible.", flush=True)
    try:
        while time.monotonic() - start < 150:
            ok, frame = camera.read()
            if not ok:
                raise RuntimeError("La camara dejo de entregar cuadros.")
            frame = cv.flip(frame, 1)
            begin = time.perf_counter()
            measure = pose.medir(frame)
            inference_ms = (time.perf_counter() - begin) * 1000
            view = cv.copyMakeBorder(frame, 104, 120, 16, 16, cv.BORDER_CONSTANT, value=(32, 43, 49))
            width = view.shape[1]
            cv.putText(view, "ESCANEA Y ENTRA | PRUEBA EN CAMARA", (16, 27),
                       cv.FONT_HERSHEY_SIMPLEX, .58, (235, 242, 244), 1, cv.LINE_AA)
            cv.putText(view, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), (16, 52),
                       cv.FONT_HERSHEY_SIMPLEX, .5, (184, 202, 212), 1, cv.LINE_AA)
            now = time.monotonic()
            save_event = None
            if measure is None:
                stable = None
                instruction = "Mira de frente y centra el rostro"
                status = "Esperando un rostro visible"
            else:
                points = measure["puntos"]
                x1, y1 = points.min(axis=0).astype(int)
                x2, y2 = points.max(axis=0).astype(int)
                cv.rectangle(view, (max(16, x1 + 16), max(104, y1 + 104)),
                             (min(width - 16, x2 + 16), min(frame.shape[0] + 104, y2 + 104)),
                             (119, 220, 168), 2)
                if phase == 1:
                    if stable is None:
                        stable = now
                    remaining = max(0, 5 - int(now - stable))
                    instruction = f"Manten el rostro visible. Captura en {remaining} s"
                    status = "Prueba 1: rostro localizado"
                    if now - stable >= 5:
                        status = "Prueba 1: ROSTRO LOCALIZADO - captura real"
                        save_event = "rostro_localizado"
                elif phase == 2:
                    instruction = "Ahora PARPADEA; despues mira de frente"
                    status = f"Prueba 2: parpadeo = {measure['parpadeo']:.2f}"
                    saw_open |= measure["parpadeo"] < .3
                    if now - phase_two_start > 1.0 and saw_open and measure["parpadeo"] > .5:
                        instruction = "PARPADEO DETECTADO - guardando captura"
                        status = f"Prueba 2: parpadeo detectado ({measure['parpadeo']:.2f})"
                        save_event = "parpadeo_detectado"
                else:
                    instruction = "Dos capturas guardadas. Puedes cerrar con Q"
                    status = "Prueba adicional terminada"
            cv.putText(view, instruction, (16, 82), cv.FONT_HERSHEY_SIMPLEX,
                       .52, (119, 220, 168), 1, cv.LINE_AA)
            bottom = frame.shape[0] + 129
            cv.putText(view, status, (16, bottom), cv.FONT_HERSHEY_SIMPLEX,
                       .48, (235, 242, 244), 1, cv.LINE_AA)
            cv.putText(view, f"Inferencia del cuadro: {inference_ms:.1f} ms", (16, bottom + 27),
                       cv.FONT_HERSHEY_SIMPLEX, .46, (184, 202, 212), 1, cv.LINE_AA)
            cv.putText(view, "Evidencia en vivo | No modifica las 45 pruebas del CSV", (16, bottom + 53),
                       cv.FONT_HERSHEY_SIMPLEX, .44, (184, 202, 212), 1, cv.LINE_AA)
            if save_event:
                save(view, frame, measure, save_event, inference_ms)
                if phase == 1:
                    phase = 2
                    phase_two_start = now
                    print("PRUEBA 2: parpadea mirando de frente.", flush=True)
                else:
                    phase = 3
                    finished_at = now
            cv.imshow(name, view)
            key = cv.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            if finished_at is not None and now - finished_at > 5:
                break
    finally:
        camera.release()
        cv.destroyAllWindows()
        manifest["fin"] = timestamp()
        (DEST / "sesion-camara.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        print("SESION FINALIZADA:", len(manifest["capturas"]), "capturas.", flush=True)


if __name__ == "__main__":
    main()
