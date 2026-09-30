"""Exceções de negócio. Python puro: podem ser levantadas pelo domínio e pelos casos de uso.

A conversão para a resposta HTTP padronizada fica em `api/core/errors.py`.
"""

from http import HTTPStatus


class DomainError(Exception):
    """Base das exceções de negócio. `code` é estável e vai para o contrato (snake_case)."""

    code: str = "domain_error"
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    code = "not_found"
    status_code = HTTPStatus.NOT_FOUND


class ConflictError(DomainError):
    code = "conflict"
    status_code = HTTPStatus.CONFLICT
