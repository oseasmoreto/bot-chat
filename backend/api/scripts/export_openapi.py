"""Gera o openapi.json versionado a partir do código.

Uso: python -m api.scripts.export_openapi openapi.json
"""

import argparse
import json
from pathlib import Path

from api.app_run import create_app
from api.config import Settings


def export_openapi(output: Path) -> None:
    schema = create_app(Settings(docs_enabled=True)).openapi()
    output.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="arquivo de saída (ex.: openapi.json)")
    args = parser.parse_args(argv)
    export_openapi(args.output)


if __name__ == "__main__":
    main()
