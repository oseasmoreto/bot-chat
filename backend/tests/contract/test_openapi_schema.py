import json
from pathlib import Path

from fastapi import FastAPI

from api.scripts.export_openapi import main as export_openapi

OPENAPI_PATH = Path(__file__).parents[2] / "openapi.json"  # openapi.json na raiz do repositório
REGENERATE = "Rode `python -m api.scripts.export_openapi openapi.json`"


def test_committed_openapi_matches_backend(app: FastAPI) -> None:
    committed = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    generated = app.openapi()

    # Compara só o contrato (paths + schemas); info.version varia por ambiente.
    assert generated["paths"] == committed["paths"], REGENERATE
    assert generated["components"] == committed["components"], REGENERATE


def test_operation_ids_are_camel_case(app: FastAPI) -> None:
    operation_ids = [
        operation["operationId"]
        for path in app.openapi()["paths"].values()
        for operation in path.values()
    ]

    assert operation_ids == ["getPublicHealth", "getAdminHealth"]


def test_export_script_writes_contract(tmp_path: Path) -> None:
    output = tmp_path / "openapi.json"

    export_openapi([str(output)])

    assert json.loads(output.read_text(encoding="utf-8"))["paths"].keys() == {
        "/api/v1/public/health",
        "/api/v1/admin/health",
    }
