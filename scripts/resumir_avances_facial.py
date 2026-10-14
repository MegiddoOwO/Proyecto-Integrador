"""Genera las tablas y la gráfica del informe a partir de la copia del CSV."""

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "evidencias" / "avances-2026-10-13"
SOURCE = DEST / "resultados" / "pruebas.csv"
CONDITIONS = [
    ("ambas", "calibracion", "Ambas", "Rostro real"),
    ("ambas", "calib_foto_s01", "Ambas", "Fotografía de s01"),
    ("ambas", "calib_otras_personas", "Ambas", "Otras personas"),
    ("pasiva", "calib_real", "Pasiva", "Rostro real"),
    ("pasiva", "calib_foto_celular", "Pasiva", "Foto en celular"),
    ("activa", "calib_real_activa", "Activa", "Rostro real"),
]


def decimal(value):
    return f"{value:.1f}".replace(".", ",")


def table(caption, label, columns, heading, rows, note):
    return (
        "\\begin{table}[htbp]\n"
        f"\\caption{{{caption}}}\n\\label{{{label}}}\n"
        "{\\small\\linespread{1}\\selectfont\n"
        f"\\begin{{tabular}}{{{columns}}}\n\\toprule\n"
        + heading + " \\\\\n\\midrule\n"
        + "\n".join(" & ".join(row) + " \\\\[0.5em]" for row in rows)
        + "\n\\bottomrule\n\\end{tabular}}\n"
        + f"\\tablenote{{{note}}}\n\\end{{table}}\n"
    )


def main():
    with SOURCE.open(newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))
    summary = []
    for mode, condition, title, condition_title in CONDITIONS:
        batch = [r for r in records if r["tecnologia"] == f"facial-buffalo_l+vida_{mode}"
                 and r["condicion"] == condition]
        if not batch:
            raise ValueError(f"Falta la condición {mode}/{condition} en la copia del CSV.")
        times = [float(r["tiempo_ms"]) for r in batch]
        correct = sum(
            (r["resultado_obtenido"] == "acepta" and r["identidad_detectada"] == r["sujeto"])
            if r["resultado_esperado"] == "acepta" else r["resultado_obtenido"] != "acepta"
            for r in batch
        )
        if correct != sum(int(r["correcto"]) for r in batch):
            raise ValueError(f"Las etiquetas de acierto no coinciden en {condition}.")
        summary.append({
            "modo": mode, "titulo_modo": title, "condicion": condition,
            "titulo_condicion": condition_title, "n": len(batch), "aciertos": correct,
            "falsos_rechazos": sum(r["resultado_esperado"] == "acepta"
                                   and r["resultado_obtenido"] != "acepta" for r in batch),
            "falsas_aceptaciones": sum(r["resultado_obtenido"] == "acepta"
                                      and (r["resultado_esperado"] == "rechaza"
                                           or r["identidad_detectada"] != r["sujeto"])
                                      for r in batch),
            "media_ms": statistics.mean(times), "mediana_ms": statistics.median(times),
            "minimo_ms": min(times), "maximo_ms": max(times),
            "resultados": dict(Counter(r["resultado_obtenido"] for r in batch)),
        })
    if sum(g["n"] for g in summary) != len(records):
        raise ValueError("Hay condiciones adicionales: actualizar el informe antes de regenerarlo.")
    (DEST / "resumen.json").write_text(json.dumps({
        "archivo": "resultados/pruebas.csv", "intentos": len(records),
        "inicio": min(r["fecha_hora"] for r in records),
        "fin": max(r["fecha_hora"] for r in records),
        "sujetos_etiquetados": sorted({r["sujeto"] for r in records}),
        "grupos": summary,
    }, ensure_ascii=False, indent=2) + "\n")

    result_rows = [[g["titulo_modo"], g["titulo_condicion"], str(g["n"]),
                    f'{g["aciertos"]}/{g["n"]}',
                    str(g["falsos_rechazos"]), str(g["falsas_aceptaciones"])] for g in summary]
    (DEST / "tabla-resultados.tex").write_text(table(
        "Decisiones Registradas en las Pruebas de Calibración", "tab:avances-resultados",
        "@{}P{1.7cm}P{3.4cm}rrrr@{}", "Modo & Condición & Intentos & Aciertos & FR & FA",
        result_rows,
        "Elaboración propia a partir del CSV vigente. Todos los registros usan "
        "el motor buffalo\\_l. FR = falsos rechazos; FA = falsas aceptaciones. "
        "Un acierto corresponde a aceptar la identidad esperada o rechazar "
        "un intento etiquetado para rechazo. Los intentos son repeticiones de calibración.",
    ))
    time_rows = [[g["titulo_modo"], g["titulo_condicion"], decimal(g["media_ms"]),
                  decimal(g["mediana_ms"]), decimal(g["maximo_ms"])] for g in summary]
    (DEST / "tabla-tiempos.tex").write_text(table(
        "Tiempos de Decisión por Condición", "tab:avances-tiempos",
        "@{}P{1.5cm}P{3.1cm}rrr@{}", "Modo & Condición & Media (ms) & Mediana (ms) & Máx. (ms)",
        time_rows,
        "Elaboración propia. Se incluyen todos los intentos de cada condición, "
        "también los rechazados. En las modalidades activa y ambas, el tiempo "
        "incluye la realización del reto. En ambas, un rechazo previo puede "
        "detener el proceso sin ejecutar el reto activo.",
    ))

    real = [next(g for g in summary if g["modo"] == mode and g["titulo_condicion"] == "Rostro real")
            for mode in ("pasiva", "activa", "ambas")]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(8.0, 4.2), constrained_layout=True)
    means = [g["media_ms"] / 1000 for g in real]
    bars = ax.barh([g["titulo_modo"] for g in real], means, height=0.5, color="#28556b")
    ax.invert_yaxis()
    ax.set_xlim(0, 8.0)
    ax.set_xlabel("Tiempo medio de decisión (segundos)")
    ax.set_title("Intentos con rostro real · buffalo_l", loc="left", pad=18, weight="bold")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#d8dfe3", linewidth=0.7)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    for bar, group, mean in zip(bars, real, means):
        ax.text(mean + 0.13, bar.get_y() + bar.get_height() / 2,
                f'{mean:.3f} s · {group["aciertos"]}/{group["n"]} aciertos'.replace(".", ","),
                va="center", fontsize=10)
    fig.savefig(DEST / "tiempos-rostro-real.pdf", bbox_inches="tight")
    fig.savefig(DEST / "tiempos-rostro-real.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Resumen generado: {len(records)} intentos, {sum(g['aciertos'] for g in summary)} aciertos.")


if __name__ == "__main__":
    main()
