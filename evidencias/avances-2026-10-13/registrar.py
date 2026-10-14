"""Da de alta a un voluntario: captura varias fotos y guarda solo sus vectores.

Uso:
    uv run registrar.py --sujeto s01                    # los 3 motores a la vez
    uv run registrar.py --sujeto s01 --motor buffalo_l  # solo uno
    uv run registrar.py --sujeto s01 --camara http://192.168.1.50:81/stream

Teclas: ESPACIO captura (solo si hay exactamente un rostro), q cancela.
No se guardan fotos, solo los vectores en datos/rostros/<motor>/<sujeto>.npy.
Los vectores de un motor no sirven para otro, por eso se calculan todos con
las mismas capturas.
"""

import argparse
import re

import cv2 as cv
import numpy as np

from comun import DIR_ROSTROS, MOTORES, abrir_camara, crear_motor, mostrar


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sujeto", required=True, help="Identificador corto, sin espacios (p. ej. s01)")
    p.add_argument("--motor", default="todos", choices=["todos", *MOTORES])
    p.add_argument("--fotos", type=int, default=5, help="Fotos a capturar (por defecto 5)")
    p.add_argument("--camara", default="0", help="Índice de la webcam o URL del stream")
    args = p.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.sujeto):
        raise SystemExit("El sujeto solo puede tener letras, números, - y _.")
    nombres = MOTORES if args.motor == "todos" else [args.motor]
    existentes = [m for m in nombres if (DIR_ROSTROS / m / f"{args.sujeto}.npy").exists()]
    if existentes:
        raise SystemExit(f"{args.sujeto} ya está registrado en {', '.join(existentes)}. "
                         f"Bórralo con borrar_datos.py --sujeto {args.sujeto}.")

    respuesta = input(f"¿{args.sujeto} firmó el consentimiento para el uso de su rostro? (s/n): ")
    if respuesta.strip().lower() != "s":
        raise SystemExit("Registro cancelado: sin consentimiento no se registra.")

    print("Cargando motores:", ", ".join(nombres))
    motores = {n: crear_motor(n) for n in nombres}
    guia = motores[nombres[0]]  # el que decide si hay un solo rostro en la vista
    cam = abrir_camara(args.camara)
    vectores: dict[str, list[np.ndarray]] = {n: [] for n in nombres}
    capturas = 0

    while capturas < args.fotos:
        ok, cuadro = cam.read()
        if not ok:
            raise SystemExit("La cámara dejó de enviar imágenes.")
        caras = guia.detectar(cuadro)
        lineas = [
            (f"{args.sujeto}: foto {capturas + 1} de {args.fotos}", (255, 255, 255)),
            ("De frente, con la luz de las pruebas | ESPACIO captura | q cancela", (255, 255, 255)),
        ]
        if len(caras) != 1:
            lineas.append(("Debe haber exactamente un rostro", (0, 0, 255)))
        tecla = mostrar("Registro", cuadro, caras[0].caja if len(caras) == 1 else None, lineas)
        if tecla == ord("q"):
            print("Registro cancelado; no se guardó nada.")
            break
        if tecla != ord(" ") or len(caras) != 1:
            continue
        nuevos = {}
        for nombre, motor in motores.items():
            encontradas = motor.detectar(cuadro)
            if not encontradas:
                break
            nuevos[nombre] = motor.vector(cuadro, encontradas[0])
        if len(nuevos) != len(motores):
            print("Algún motor no encontró el rostro en esa captura; intenta de nuevo.")
            continue
        for nombre, v in nuevos.items():
            vectores[nombre].append(v)
        capturas += 1
        print(f"Foto {capturas} capturada.")

    cam.release()
    cv.destroyAllWindows()

    if capturas == args.fotos:
        for nombre, lista in vectores.items():
            destino = DIR_ROSTROS / nombre / f"{args.sujeto}.npy"
            destino.parent.mkdir(parents=True, exist_ok=True)
            np.save(destino, np.vstack(lista))
            print(f"Guardado {destino}")


if __name__ == "__main__":
    main()
