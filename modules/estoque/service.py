"""Serviço público do módulo Estoque."""

from typing import Optional
from .models import EstoqueUnidade
from .repository import EstoqueRepository
from modules.shared.exceptions import EstoqueInsuficienteError
from modules.shared.events import EventBus, ReservaCriadaEvent, ReservaCanceladaEvent


class EstoqueService:
    """Interface pública de regras de estoque e filiais físicas."""

    def __init__(self, repository: Optional[EstoqueRepository] = None) -> None:
        self.repository = repository or EstoqueRepository()

    def listar_estoques_livro(self, isbn: str) -> list[EstoqueUnidade]:
        return self.repository.listar_por_isbn(isbn)

    def obter_estoque_unidade(self, isbn: str, unidade: str) -> EstoqueUnidade:
        est = self.repository.obter_por_isbn_e_unidade(isbn, unidade)
        if not est:
            raise EstoqueInsuficienteError(f"A unidade '{unidade}' não possui cadastro de estoque para este livro.")
        return est

    def decrementar_estoque(self, isbn: str, unidade: str) -> EstoqueUnidade:
        est = self.obter_estoque_unidade(isbn, unidade)
        est.decrementar()
        self.repository.salvar(est)
        return est

    def incrementar_estoque(self, isbn: str, unidade: str) -> EstoqueUnidade:
        est = self.repository.obter_por_isbn_e_unidade(isbn, unidade)
        if not est:
            est = EstoqueUnidade(unidade=unidade, isbn=isbn, quantidade=0)
        est.incrementar()
        self.repository.salvar(est)
        return est

    def registrar_listeners(self, event_bus: EventBus) -> None:
        """Configura a assinatura de eventos do domínio para sincronização desacoplada."""
        event_bus.subscribe(ReservaCriadaEvent, self._handle_reserva_criada)
        event_bus.subscribe(ReservaCanceladaEvent, self._handle_reserva_cancelada)

    def _handle_reserva_criada(self, event: ReservaCriadaEvent) -> None:
        self.decrementar_estoque(event.isbn, event.unidade)

    def _handle_reserva_cancelada(self, event: ReservaCanceladaEvent) -> None:
        self.incrementar_estoque(event.isbn, event.unidade)
