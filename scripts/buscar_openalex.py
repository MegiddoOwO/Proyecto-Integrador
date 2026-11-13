#!/usr/bin/env python3
"""Búsqueda de fuentes en OpenAlex sin dependencias externas.

Sustituye al MCP `paper-search` cuando no está disponible (requiere `uvx`).
Solo usa la biblioteca estándar de Python.

Ejemplos:
    python3 scripts/buscar_openalex.py buscar "QR code access control queue" --desde 2024
    python3 scripts/buscar_openalex.py buscar "control de acceso QR" --desde 2025 --resumen
    python3 scripts/buscar_openalex.py doi 10.63371/ic.v4.n4.a595

La llave de API es opcional (sin llave hay un límite diario menor). Si el
equipo tiene una, se pone en la variable de entorno OPENALEX_API_KEY; nunca se
escribe en el repositorio.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.openalex.org"
CAMPOS = (
    "id,doi,display_name,publication_year,type,language,authorships,"
    "primary_location,cited_by_count,open_access,abstract_inverted_index"
)


def consultar(ruta, parametros):
    llave = os.environ.get("OPENALEX_API_KEY")
    if llave:
        parametros["api_key"] = llave
    url = f"{BASE}{ruta}?{urllib.parse.urlencode(parametros)}"
    peticion = urllib.request.Request(url, headers={"User-Agent": "buscar-openalex/1.0"})
    try:
        with urllib.request.urlopen(peticion, timeout=30) as respuesta:
            return json.load(respuesta)
    except urllib.error.HTTPError as error:
        sys.exit(f"OpenAlex respondió {error.code}: {error.read().decode()[:300]}")
    except urllib.error.URLError as error:
        sys.exit(f"No se pudo conectar con OpenAlex: {error.reason}")


def resumen(indice):
    """Reconstruye el resumen a partir del índice invertido de OpenAlex."""
    if not indice:
        return ""
    posiciones = {p: palabra for palabra, lista in indice.items() for p in lista}
    return " ".join(posiciones[p] for p in sorted(posiciones))


def mostrar(obra, con_resumen):
    autores = [a["author"]["display_name"] for a in obra.get("authorships") or []]
    if len(autores) > 4:
        autores = autores[:4] + ["et al."]
    fuente = ((obra.get("primary_location") or {}).get("source") or {}).get("display_name")
    oa = obra.get("open_access") or {}
    print(f"- {obra.get('display_name')}")
    print(f"  {', '.join(autores) or 'Sin autores'} ({obra.get('publication_year')})")
    print(f"  {fuente or 'Sin fuente'} | tipo: {obra.get('type')} | idioma: {obra.get('language')}"
          f" | citas: {obra.get('cited_by_count')}")
    print(f"  DOI: {obra.get('doi') or 'sin DOI'} | OpenAlex: {obra.get('id')}")
    if oa.get("oa_url"):
        print(f"  Acceso abierto: {oa['oa_url']}")
    if con_resumen:
        texto = resumen(obra.get("abstract_inverted_index"))
        print(f"  Resumen: {texto[:1200] or 'no disponible en OpenAlex'}")
    print()


def buscar(args):
    filtros = []
    if args.desde:
        filtros.append(f"publication_year:>{args.desde - 1}")
    if args.hasta:
        filtros.append(f"publication_year:<{args.hasta + 1}")
    if args.tipo:
        filtros.append(f"type:{args.tipo}")
    if args.abierto:
        filtros.append("open_access.is_oa:true")
    parametros = {
        "search": args.consulta,
        "per_page": args.n,
        "select": CAMPOS,
    }
    if filtros:
        parametros["filter"] = ",".join(filtros)
    if args.orden == "citas":
        parametros["sort"] = "cited_by_count:desc"
    elif args.orden == "fecha":
        parametros["sort"] = "publication_date:desc"
    datos = consultar("/works", parametros)
    total = datos.get("meta", {}).get("count")
    print(f"{total} resultados para «{args.consulta}». Primeros {len(datos['results'])}:\n")
    for obra in datos["results"]:
        mostrar(obra, args.resumen)


def por_doi(args):
    doi = args.doi.removeprefix("https://doi.org/").removeprefix("doi:")
    obra = consultar(f"/works/doi:{doi}", {"select": CAMPOS})
    mostrar(obra, True)


def main():
    analizador = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = analizador.add_subparsers(dest="comando", required=True)

    b = sub.add_parser("buscar", help="buscar obras por palabras clave")
    b.add_argument("consulta")
    b.add_argument("--desde", type=int, help="año mínimo de publicación")
    b.add_argument("--hasta", type=int, help="año máximo de publicación")
    b.add_argument("--tipo", help="tipo de obra: article, review, book, dissertation...")
    b.add_argument("--abierto", action="store_true", help="solo acceso abierto")
    b.add_argument("--orden", choices=["relevancia", "citas", "fecha"], default="relevancia")
    b.add_argument("-n", type=int, default=10, help="número de resultados (máx. 100)")
    b.add_argument("--resumen", action="store_true", help="mostrar el resumen")
    b.set_defaults(func=buscar)

    d = sub.add_parser("doi", help="consultar una obra por DOI (incluye resumen)")
    d.add_argument("doi")
    d.set_defaults(func=por_doi)

    args = analizador.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
