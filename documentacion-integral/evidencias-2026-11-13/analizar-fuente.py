"""Resume resultados/pruebas.csv por tecnología y condición.

Uso:
    uv run analizar.py
    uv run analizar.py --csv otra_ruta.csv

Por cada grupo reporta: intentos, % correctos, falsos rechazos (el titular no
pasó), falsas aceptaciones (pasó quien no debía o fue confundido con otro) y el
tiempo en ms (media, mediana y máximo).
"""

import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

from comun import CSV_RESULTADOS


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", type=Path, default=CSV_RESULTADOS)
    args = p.parse_args()
    if not args.csv.exists():
        raise SystemExit(f"No existe {args.csv}. Corre reconocer.py primero.")

    grupos: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    with args.csv.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            grupos[(fila["tecnologia"], fila["condicion"], fila["resultado_esperado"])].append(fila)

    print(f"{'tecnologia':<30} {'condicion':<22} {'esperado':<8} {'n':>4} {'%ok':>6} "
          f"{'f.rech':>6} {'f.acep':>6} {'media':>7} {'mediana':>8} {'max':>7}")
    for (tec, cond, esp), filas in sorted(grupos.items()):
        n = len(filas)
        ok = sum(int(f["correcto"]) for f in filas)
        if esp == "acepta":
            f_rech = sum(f["resultado_obtenido"] != "acepta" for f in filas)
            # Aceptado, pero como otra persona.
            f_acep = sum(f["resultado_obtenido"] == "acepta" and f["identidad_detectada"] != f["sujeto"] for f in filas)
        else:
            f_rech = 0
            f_acep = sum(f["resultado_obtenido"] == "acepta" for f in filas)
        tiempos = [float(f["tiempo_ms"]) for f in filas]
        print(f"{tec:<30} {cond:<22} {esp:<8} {n:>4} {100 * ok / n:>5.1f}% "
              f"{f_rech:>6} {f_acep:>6} {statistics.mean(tiempos):>7.1f} "
              f"{statistics.median(tiempos):>8.1f} {max(tiempos):>7.1f}")


if __name__ == "__main__":
    main()
