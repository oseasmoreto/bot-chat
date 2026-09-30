import json
import logging

import pytest
from freezegun import freeze_time

from api.core.logs import JsonFormatter, configure_logging
from api.core.request_id import request_id_var


def make_record(**extra: object) -> logging.LogRecord:
    record = logging.makeLogRecord(
        {"name": "api.test", "levelname": "INFO", "msg": "evento %s", "args": ("x",)}
    )
    for key, value in extra.items():
        setattr(record, key, value)
    return record


@freeze_time("2026-09-29T14:30:00Z")
def test_formats_record_as_json_with_extra_fields() -> None:
    line = JsonFormatter().format(make_record(scope="admin"))

    assert json.loads(line) == {
        "timestamp": "2026-09-29T14:30:00+00:00",
        "level": "INFO",
        "logger": "api.test",
        "message": "evento x",
        "scope": "admin",
    }


def test_includes_request_id_of_current_request() -> None:
    token = request_id_var.set("abc123")
    try:
        line = JsonFormatter().format(make_record())
    finally:
        request_id_var.reset(token)

    assert json.loads(line)["requestId"] == "abc123"


def test_includes_exception_traceback() -> None:
    try:
        raise RuntimeError("falhou")
    except RuntimeError as exc:
        record = make_record(exc_info=(type(exc), exc, exc.__traceback__))

    assert "RuntimeError: falhou" in json.loads(JsonFormatter().format(record))["exception"]


def test_configure_logging_writes_json_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging("DEBUG")

    logging.getLogger("api.test").debug("ligado")

    assert json.loads(capsys.readouterr().out)["message"] == "ligado"
