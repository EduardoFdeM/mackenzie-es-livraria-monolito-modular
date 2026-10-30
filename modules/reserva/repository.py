"""Repositório de dados do módulo Reserva."""

from typing import Optional
from .models import Reserva


class ReservaRepository:
    """Armazenamento e busca das reservas da livraria."""

    def __init__(self) -> None:
        self._reservas: dict[str, Reserva] = {}
        self._sequencial = 1

    def gerar_codigo(self) -> str:
        codigo = f"RES-{self._sequencial:04d}"
        self._sequencial += 1
        return codigo

    def salvar(self, reserva: Reserva) -> None:
        self._reservas[reserva.codigo] = reserva

    def buscar_por_codigo(self, codigo: str) -> Optional[Reserva]:
        return self._reservas.get(codigo)

    def listar_todas(self) -> list[Reserva]:
        return list(self._reservas.values())
