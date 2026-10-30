"""Modelos do módulo Reserva."""

from dataclasses import dataclass
from enum import Enum
from modules.shared.exceptions import ReservaJaCanceladaError


class StatusReserva(str, Enum):
    ATIVA = "Ativa"
    CANCELADA = "Cancelada"


@dataclass
class Reserva:
    codigo: str
    isbn: str
    titulo: str
    unidade: str
    status: StatusReserva = StatusReserva.ATIVA

    def cancelar(self) -> None:
        if self.status == StatusReserva.CANCELADA:
            raise ReservaJaCanceladaError(f"A reserva {self.codigo} já se encontra cancelada.")
        self.status = StatusReserva.CANCELADA
