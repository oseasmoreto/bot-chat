from enum import StrEnum


class Scope(StrEnum):
    """Escopo de acesso da aplicação. Define prefixos de rota e regras futuras de auth."""

    PUBLIC = "public"
    ADMIN = "admin"
