"""Prueba de reconocimiento: cada ESPACIO es un intento que se guarda en el CSV.

Uso (una corrida por combinación y condición):
    uv run reconocer.py --sujeto s01 --condicion luz_normal --esperado acepta
    uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion luz_normal --esperado acepta
    uv run reconocer.py --motor buffalo_l --vida ambas --sujeto s01 --condicion foto_celular --esperado rechaza

--motor: sface (por defecto), buffalo_s o buffalo_l.
--vida:  no (por defecto), pasiva (modelo de InsightFace, un cuadro),
         activa (reto de girar y parpadear con MediaPipe) o ambas.

--sujeto es quien está frente a la cámara (o de quién es la foto en una
suplantación). Todos los intentos de una corrida deben ser de la misma
condición. Teclas: ESPACIO registra un intento, q termina.

En el CSV, la columna tecnologia queda como facial-<motor>+vida_<modo>.

tiempo_ms va desde ESPACIO hasta la decisión. Sin vida activa es solo el
procesamiento de un cuadro; con vida activa incluye el tiempo que la persona
tarda en hacer el reto.
"""

import argparse
import csv
import time
from datetime import datetime

import cv2 as cv

from comun import CSV_RESULTADOS, MOTORES, abrir_camara, cargar_registrados, crear_motor, identificar, mostrar

COLUMNAS = [
    "fecha_hora", "tecnologia", "sujeto", "condicion", "resultado_esperado",
    "resultado_obtenido", "identidad_detectada", "similitud", "tiempo_ms", "correcto",
    "detalle",  # puntajes de vida (pasiva=…, paralaje=…) o motivo del rechazo
]


def preparar_csv() -> bool:
    """Crea la carpeta y agrega la columna detalle a un CSV anterior sin ella.

    Devuelve True si el archivo no existe y hay que escribir el encabezado.
    """
    CSV_RESULTADOS.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_RESULTADOS.exists():
        return True
    with CSV_RESULTADOS.open(encoding="utf-8") as f:
        filas = list(csv.reader(f))
    if filas and filas[0] != COLUMNAS:
        with CSV_RESULTADOS.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(COLUMNAS)
            escritor.writerows(fila + [""] * (len(COLUMNAS) - len(fila)) for fila in filas[1:])
    return False


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sujeto", required=True, help="Quién está frente a la cámara")
    p.add_argument("--condicion", required=True, help="p. ej. luz_normal, luz_baja, lejos, foto_impresa, foto_celular")
    p.add_argument("--esperado", required=True, choices=["acepta", "rechaza"])
    p.add_argument("--motor", default="sface", choices=MOTORES)
    p.add_argument("--vida", default="no", choices=["no", "pasiva", "activa", "ambas"])
    p.add_argument("--camara", default="0", help="Índice de la webcam o URL del stream")
    p.add_argument("--intentos", type=int, default=20, help="Intentos de la corrida (por defecto 20)")
    args = p.parse_args()

    registrados = cargar_registrados(args.motor)
    if not registrados:
        raise SystemExit(f"No hay nadie registrado con {args.motor}. Usa registrar.py primero.")
    tecnologia = f"facial-{args.motor}+vida_{args.vida}"

    motor = crear_motor(args.motor)
    pasiva = pose = None
    if args.vida in ("pasiva", "ambas"):
        from vida import VidaPasiva
        pasiva = VidaPasiva()
    if args.vida in ("activa", "ambas"):
        from vida import Pose, prueba_activa
        pose = Pose()
    print(f"Registrados: {', '.join(registrados)} | umbral {motor.umbral} | {tecnologia}")

    cam = abrir_camara(args.camara)
    nuevo = preparar_csv()
    hechos, aciertos, ultimo = 0, 0, ""

    with CSV_RESULTADOS.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if nuevo:
            escritor.writerow(COLUMNAS)

        while hechos < args.intentos:
            ok, cuadro = cam.read()
            if not ok:
                raise SystemExit("La cámara dejó de enviar imágenes.")
            caras = motor.detectar(cuadro)
            lineas = [
                (f"{args.sujeto} | {args.condicion} | esperado: {args.esperado}", (255, 255, 255)),
                (f"{args.motor} | vida: {args.vida}", (255, 255, 255)),
                (f"Intento {hechos + 1} de {args.intentos} | aciertos {aciertos} | ESPACIO intento | q termina", (255, 255, 255)),
            ]
            if ultimo:
                lineas.append((ultimo, (0, 255, 0) if ultimo.startswith("OK") else (0, 0, 255)))
            tecla = mostrar("Reconocimiento", cuadro, caras[0].caja if caras else None, lineas)
            if tecla == ord("q"):
                break
            if tecla != ord(" "):
                continue

            inicio = time.perf_counter()
            identidad, sim, motivos = "", float("nan"), []
            caras = motor.detectar(cuadro)
            if not caras:
                resultado = "sin_rostro"
            else:
                encontrada, sim = identificar(motor, motor.vector(cuadro, caras[0]), registrados)
                identidad = encontrada or ""
                resultado = "acepta" if encontrada else "rechaza"
            if resultado == "acepta" and pasiva:
                vivo, motivo = pasiva.evaluar(cuadro, caras[0].puntos)
                motivos.append(motivo)
                if not vivo:
                    resultado = "rechaza_vida"
            if resultado == "acepta" and pose:
                inicial = pose.medir(cuadro)
                if inicial is None:
                    resultado, motivo = "rechaza_vida", "activa_sin_rostro"
                else:
                    vivo, motivo = prueba_activa(cam, pose, inicial, motor, registrados, identidad)
                    if not vivo:
                        resultado = "rechaza_vida"
                motivos.append(motivo)
            ms = (time.perf_counter() - inicio) * 1000

            if args.esperado == "acepta":
                correcto = resultado == "acepta" and identidad == args.sujeto
            else:
                correcto = resultado != "acepta"
            escritor.writerow([
                datetime.now().isoformat(timespec="seconds"), tecnologia, args.sujeto,
                args.condicion, args.esperado, resultado, identidad,
                f"{sim:.4f}", f"{ms:.1f}", int(correcto), " ".join(motivos),
            ])
            f.flush()
            hechos += 1
            aciertos += correcto
            ultimo = (f"{'OK' if correcto else 'ERROR'}: {resultado} {identidad} sim={sim:.3f} "
                      f"{' '.join(motivos)} {ms:.0f} ms")
            print(ultimo)

    cam.release()
    cv.destroyAllWindows()
    print(f"{hechos} intentos, {aciertos} correctos. Resultados en {CSV_RESULTADOS}")


if __name__ == "__main__":
    main()
