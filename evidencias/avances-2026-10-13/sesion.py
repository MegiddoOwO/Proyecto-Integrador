"""Guía una sesión completa con un voluntario, condición por condición.

Uso:
    uv run sesion.py --sujeto s02             # voluntario registrado
    uv run sesion.py --sujeto x01 --impostor  # persona NO registrada

Para cada condición explica qué preparar y corre reconocer.py con todas las
combinaciones de la matriz, así ninguna corrida queda mal etiquetada. Las
combinaciones de una misma condición van seguidas para no cambiar la luz o la
foto entre ellas. En cada paso: Enter empieza, s lo salta, q termina.
"""

import argparse
import subprocess
import sys

from comun import DIR_ROSTROS, RAIZ

# Combinaciones a comparar: (motor, vida).
MATRIZ = [("sface", "no"), ("buffalo_l", "no"), ("buffalo_l", "pasiva")]

# (condicion, esperado, qué preparar)
CONDICIONES = [
    ("luz_normal", "acepta", "El voluntario de frente a la cámara, con la luz normal del lugar."),
    ("luz_baja", "acepta", "Bajen la luz (apaguen la del techo o cierren cortinas). Anoten cómo quedó."),
    ("foto_celular", "rechaza", "El voluntario muestra en SU celular una foto de su cara, a la distancia de su rostro."),
]
CONDICIONES_IMPOSTOR = [
    ("no_registrado", "rechaza", "La persona NO registrada se pone frente a la cámara, con la luz normal."),
]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sujeto", required=True)
    p.add_argument("--impostor", action="store_true", help="La persona no está registrada")
    p.add_argument("--intentos", type=int, default=20)
    p.add_argument("--camara", default="0")
    args = p.parse_args()

    registrado = all((DIR_ROSTROS / m / f"{args.sujeto}.npy").exists() for m, _ in MATRIZ)
    if args.impostor and registrado:
        raise SystemExit(f"{args.sujeto} está registrado; un impostor no debe estarlo.")
    if not args.impostor and not registrado:
        print(f"{args.sujeto} no está registrado. Primero el registro (5 capturas de frente, luz normal).")
        subprocess.run([sys.executable, str(RAIZ / "registrar.py"), "--sujeto", args.sujeto,
                        "--camara", args.camara], check=True)
        if not all((DIR_ROSTROS / m / f"{args.sujeto}.npy").exists() for m, _ in MATRIZ):
            raise SystemExit("El registro no se completó.")

    condiciones = CONDICIONES_IMPOSTOR if args.impostor else CONDICIONES
    total = len(condiciones) * len(MATRIZ)
    paso = 0
    for condicion, esperado, preparar in condiciones:
        print(f"\n=== Condición: {condicion} (esperado: {esperado}) ===\n{preparar}")
        for motor, vida in MATRIZ:
            paso += 1
            r = input(f"[{paso}/{total}] {motor} + vida {vida}, {args.intentos} intentos. "
                      "Enter empieza, s salta, q termina: ").strip().lower()
            if r == "q":
                return
            if r == "s":
                continue
            subprocess.run([
                sys.executable, str(RAIZ / "reconocer.py"), "--sujeto", args.sujeto,
                "--condicion", condicion, "--esperado", esperado, "--motor", motor,
                "--vida", vida, "--intentos", str(args.intentos), "--camara", args.camara,
            ], check=True)
    print(f"\nSesión de {args.sujeto} terminada. Resumen: uv run analizar.py")


if __name__ == "__main__":
    main()
