import logging
from collections.abc import Awaitable, Callable
from http import HTTPStatus
from typing import Any, Final

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.core.exceptions import DomainError
from api.core.request_id import get_request_id
from api.core.schemas import BaseSchema

logger = logging.getLogger(__name__)


class ErrorDetail(BaseSchema):
    field: str | None = None
    message: str


class ErrorBody(BaseSchema):
    code: str
    message: str
    details: list[ErrorDetail] | None = None
    request_id: str | None = None


class ErrorResponse(BaseSchema):
    """Formato padrão de erro (docs/06-contratos-api.md#formato-padrão-de-erro)."""

    error: ErrorBody


# Códigos dos erros HTTP gerados pelo próprio framework (rota inexistente, método errado…).
_HTTP_ERROR_CODES: Final[dict[int, str]] = {
    HTTPStatus.BAD_REQUEST: "bad_request",
    HTTPStatus.UNAUTHORIZED: "unauthorized",
    HTTPStatus.FORBIDDEN: "forbidden",
    HTTPStatus.NOT_FOUND: "not_found",
    HTTPStatus.METHOD_NOT_ALLOWED: "method_not_allowed",
    HTTPStatus.CONFLICT: "conflict",
    HTTPStatus.REQUEST_ENTITY_TOO_LARGE: "payload_too_large",
    HTTPStatus.UNSUPPORTED_MEDIA_TYPE: "unsupported_media_type",
    HTTPStatus.TOO_MANY_REQUESTS: "too_many_requests",
}
_HTTP_ERROR_MESSAGES: Final[dict[int, str]] = {
    HTTPStatus.NOT_FOUND: "Recurso não encontrado",
    HTTPStatus.METHOD_NOT_ALLOWED: "Método não permitido",
}


def error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorBody(
            code=code,
            message=message,
            details=details,
            request_id=get_request_id(request),
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(mode="json", by_alias=True, exclude_none=True),
    )


async def _handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
    return error_response(request, status_code=exc.status_code, code=exc.code, message=exc.message)


async def _handle_http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    response = error_response(
        request,
        status_code=exc.status_code,
        code=_HTTP_ERROR_CODES.get(exc.status_code, "http_error"),
        message=_HTTP_ERROR_MESSAGES.get(exc.status_code, HTTPStatus(exc.status_code).phrase),
    )
    response.headers.update(exc.headers or {})  # ex.: Allow no 405
    return response


async def _handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(field=".".join(str(part) for part in error["loc"]), message=error["msg"])
        for error in exc.errors()
    ]
    return error_response(
        request,
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code="validation_error",
        message="Dados de entrada inválidos",
        details=details,
    )


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    # Stack trace só no log; a resposta nunca expõe detalhes internos.
    logger.exception("http.unhandled_error", exc_info=exc)
    return error_response(
        request,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        code="internal_error",
        message="Erro interno",
    )


# Any na fronteira com o Starlette: ele tipa o handler com `Exception`, mas o registro por
# classe garante que cada handler só recebe o próprio tipo.
_HANDLERS: Final[dict[type[Exception], Callable[[Request, Any], Awaitable[JSONResponse]]]] = {
    DomainError: _handle_domain_error,
    StarletteHTTPException: _handle_http_error,
    RequestValidationError: _handle_validation_error,
    Exception: _handle_unexpected_error,
}


def register_error_handlers(app: FastAPI) -> None:
    for exception_class, handler in _HANDLERS.items():
        app.add_exception_handler(exception_class, handler)
