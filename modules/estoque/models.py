"""Modelos do módulo Estoque."""

from dataclasses import dataclass
from modules.shared.exceptions import EstoqueInsuficienteError


@dataclass
class EstoqueUnidade:
    unidade: str
    isbn: str
    quantidade: int
    setor: str = ""
    corredor: str = ""
    prateleira: str = ""

    def decrementar(self) -> None:
        if self.quantidade <= 0:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente na unidade {self.unidade} para o ISBN {self.isbn}."
            )
        self.quantidade -= 1

    def incrementar(self) -> None:
        self.quantidade += 1

    @property
    def localizacao_formatada(self) -> str:
        if self.setor and self.corredor and self.prateleira:
            return f"Setor {self.setor}, corredor {self.corredor}, prateleira {self.prateleira}"
        return "Consulte o balcão da unidade"
