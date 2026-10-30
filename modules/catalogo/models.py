"""Modelos do módulo Catálogo."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Livro:
    isbn: str
    titulo: str
    autor: str
    preco: Decimal

    @property
    def preco_formatado(self) -> str:
        return f"R$ {self.preco:.2f}".replace(".", ",")
