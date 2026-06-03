from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from networkx.readwrite import json_graph

from . import __version__
from .read import read_obo


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obonet",
        description="Convert an OBO ontology to NetworkX node-link JSON.",
    )
    parser.add_argument("path", help="Path or URL to an OBO file.")
    parser.add_argument(
        "--output",
        help="Write JSON to this path instead of stdout.",
    )
    parser.add_argument(
        "--include-clauses",
        action="store_true",
        help='Include parsed OBO clauses under "_clauses".',
    )
    parser.add_argument(
        "--include-obsolete",
        action="store_true",
        help="Include terms marked is_obsolete.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Number of spaces for JSON indentation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"obonet {__version__ or 'unknown'}",
    )
    return parser


def write_json(data: object, output: str | None, indent: int) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=indent) + "\n"
    if output is None:
        sys.stdout.write(text)
        return

    with open(output, "w", encoding="utf-8") as write_file:
        write_file.write(text)


def main(argv: Sequence[str] | None = None) -> None:
    args = get_parser().parse_args(argv)
    graph = read_obo(
        args.path,
        ignore_obsolete=not args.include_obsolete,
        include_clauses=args.include_clauses,
    )
    data = json_graph.node_link_data(graph)
    write_json(data, args.output, indent=args.indent)


if __name__ == "__main__":
    main()
