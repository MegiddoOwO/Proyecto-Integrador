"""Prepara vistas del análisis real del CSV y de un fragmento del programa.

Las páginas HTML se capturan con un navegador. No representan imágenes de
la cámara ni una sesión de reconocimiento en vivo.
"""

import argparse
import csv
import html
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidencias" / "avances-2026-10-13"
DEST = EVIDENCE / "capturas"


def analysis():
    with (EVIDENCE / "resultados" / "pruebas.csv").open(newline="") as source:
        records = list(csv.DictReader(source))
    groups = defaultdict(list)
    for record in records:
        mode = record["tecnologia"].split("+vida_")[1]
        groups[(mode, record["condicion"])].append(record)
    names = {
        "calibracion": "rostro real", "calib_foto_s01": "fotografia s01",
        "calib_otras_personas": "otras personas", "calib_real": "rostro real",
        "calib_foto_celular": "foto en celular", "calib_real_activa": "rostro real",
    }
    print("ARCHIVO: resultados/pruebas.csv")
    print(f"CORTE: 13/10/2026 | MOTOR: buffalo_l | INTENTOS: {len(records)}")
    print()
    print(f"{'MODO':<8} {'CONDICION':<17} {'n':>2} {'OK':>5} {'FR':>2} {'FA':>2} {'MEDIA ms':>8}")
    print("-" * 54)
    for (mode, condition), batch in sorted(groups.items()):
        correct = sum(int(r["correcto"]) for r in batch)
        false_reject = sum(r["resultado_esperado"] == "acepta"
                           and r["resultado_obtenido"] != "acepta" for r in batch)
        false_accept = sum(r["resultado_obtenido"] == "acepta"
                           and (r["resultado_esperado"] == "rechaza"
                                or r["identidad_detectada"] != r["sujeto"]) for r in batch)
        mean = statistics.mean(float(r["tiempo_ms"]) for r in batch)
        print(f"{mode:<8} {names[condition]:<17} {len(batch):>2} "
              f"{correct:>2}/{len(batch):<2} {false_reject:>2} {false_accept:>2} {mean:>8.1f}")
    print()
    print(f"TOTAL: {sum(int(r['correcto']) for r in records)} aciertos / {len(records)} intentos")
    print("FR: falso rechazo | FA: falsa aceptacion")
    print()
    print("INTENTOS QUE REQUIEREN REVISION")
    for record in records:
        if record["correcto"] == "0":
            print(f"{record['fecha_hora'][11:]} | {record['tiempo_ms']} ms | {record['detalle']}")
    print()
    print("Lectura de registros existentes; sin nueva captura de camara.")


def page(title, subtitle, body, kind):
    return f"""<!doctype html><html lang="es"><meta charset="utf-8">
<title>{html.escape(title)}</title><style>
*{{box-sizing:border-box}} body{{margin:0;background:#fff;color:#14272e;
font-family:Arial,sans-serif;padding:36px 40px;width:1000px}}
.eyebrow{{font-size:16px;font-weight:700;letter-spacing:1.5px;color:#28556b}}
h1{{font-size:30px;line-height:1.18;margin:12px 0 9px}}
p{{font-size:18px;margin:0 0 23px;line-height:1.4;color:#526269}}
.terminal{{background:#15252d;color:#edf2f4;padding:24px;border-radius:5px}}
.command{{font:19px/1.4 'DejaVu Sans Mono',monospace;color:#9ed3c7;
margin-bottom:15px;white-space:pre-wrap;overflow-wrap:anywhere}}
pre{{margin:0;font:21px/1.43 'DejaVu Sans Mono',monospace;white-space:pre-wrap;
overflow-wrap:anywhere}} .source{{border-top:2px solid #28556b;background:#f3f6f7;
padding:18px 16px}} .line{{display:flex;min-height:29px}}
.num{{color:#627a84;min-width:45px;font:18px/1.5 monospace;user-select:none}}
.line code{{font:19px/1.5 'DejaVu Sans Mono',monospace;white-space:pre-wrap;
overflow-wrap:anywhere;min-width:0}} .gap{{color:#627a84;font:18px/1.6 monospace}}
footer{{margin-top:20px;font-size:16px;line-height:1.4;color:#526269;
border-top:1px solid #ccd5d9;padding-top:13px}}
</style><body><div class="eyebrow">ESCANEA Y ENTRA · EVIDENCIA DOCUMENTAL</div>
<h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p>{body}
<footer>{html.escape(kind)}</footer></body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--texto", action="store_true")
    args = parser.parse_args()
    if args.texto:
        analysis()
        return
    DEST.mkdir(exist_ok=True)
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--texto"],
                            check=True, capture_output=True, text=True)
    (DEST / "analisis-ejecutado.txt").write_text(result.stdout)
    body = ('<div class="terminal"><div class="command">$ python3 '
            'scripts/preparar_capturas_avances.py --texto</div><pre>'
            + html.escape(result.stdout) + '</pre></div>')
    (DEST / "analisis.html").write_text(page(
        "Análisis de los intentos registrados",
        "Salida obtenida al procesar la copia del archivo de resultados.", body,
        "La vista documenta el análisis del CSV de calibración. "
        "Los tiempos incluyen el reto en los modos activa y ambas.",
    ))

    lines = (EVIDENCE / "reconocer.py").read_text().splitlines()
    blocks = []
    for start_marker, end_marker in [
        ('            if tecla != ord(" "):', '            inicio = time.perf_counter()'),
        ('            if resultado == "acepta" and pasiva:',
         '            if resultado == "acepta" and pose:'),
        ('            escritor.writerow([', '            hechos += 1'),
    ]:
        start = lines.index(start_marker)
        end = lines.index(end_marker, start)
        block = []
        for number in range(start, end):
            line = lines[number][12:] if lines[number].startswith(" " * 12) else lines[number]
            block.append(f'<div class="line"><span class="num">{number + 1}</span>'
                         f'<code>{html.escape(line)}</code></div>')
        blocks.append("".join(block))
    body = '<div class="source">' + '<div class="gap">…</div>'.join(blocks) + '</div>'
    (DEST / "programa.html").write_text(page(
        "Cómo se inicia y registra un intento",
        "Fragmentos de reconocer.py conservados en la copia de evidencias.", body,
        "La tecla ESPACIO inicia el intento; el programa evalúa la vida "
        "pasiva cuando corresponde y guarda la decisión y el tiempo en CSV. "
        "Los puntos suspensivos indican código omitido.",
    ))
    print("Vistas creadas:", DEST / "analisis.html", DEST / "programa.html", sep="\n")


if __name__ == "__main__":
    main()
