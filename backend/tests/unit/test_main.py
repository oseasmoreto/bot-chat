from fastapi import FastAPI
from pytest_mock import MockerFixture

import main


def test_exposes_asgi_app_for_servers() -> None:
    assert isinstance(main.app, FastAPI)


def test_run_starts_uvicorn_with_settings(mocker: MockerFixture) -> None:
    uvicorn_run = mocker.patch("main.uvicorn.run")

    main.run()

    uvicorn_run.assert_called_once_with(
        main.app,
        host=main.settings.host,
        port=main.settings.port,
        proxy_headers=True,
        log_config=None,
    )
