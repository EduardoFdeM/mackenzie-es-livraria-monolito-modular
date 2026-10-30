"""Serviço de negócio do módulo Reserva."""

from typing import Optional
from .models import Reserva, StatusReserva
from .repository import ReservaRepository
from modules.catalogo.service import CatalogoService
from modules.estoque.service import EstoqueService
from modules.shared.events import EventBus, ReservaCriadaEvent, ReservaCanceladaEvent
from modules.shared.exceptions import ReservaNaoEncontradaError, EstoqueInsuficienteError


class ReservaService:
    """Orquestrador do ciclo de vida das reservas com desacoplamento por eventos."""

    def __init__(
        self,
        repository: Optional[ReservaRepository] = None,
        catalogo_service: Optional[CatalogoService] = None,
        estoque_service: Optional[EstoqueService] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.repository = repository or ReservaRepository()
        self.catalogo_service = catalogo_service or CatalogoService()
        self.estoque_service = estoque_service or EstoqueService()
        self.event_bus = event_bus or EventBus()

    def criar_reserva(self, isbn: str, unidade: str) -> Reserva:
        # 1. Valida existência do livro no módulo Catálogo
        livro = self.catalogo_service.obter_por_isbn(isbn)

        # 2. Valida saldo disponível no módulo Estoque
        estoque = self.estoque_service.obter_estoque_unidade(isbn, unidade)
        if estoque.quantidade <= 0:
            raise EstoqueInsuficienteError(f"Não há exemplares disponíveis na unidade {unidade}.")

        # 3. Gera código da reserva
        codigo = self.repository.gerar_codigo()
        reserva = Reserva(
            codigo=codigo,
            isbn=livro.isbn,
            titulo=livro.titulo,
            unidade=unidade,
            status=StatusReserva.ATIVA,
        )

        # 4. Publica evento no EventBus (Estoque escuta e realiza baixa)
        self.event_bus.publish(ReservaCriadaEvent(codigo=codigo, isbn=isbn, unidade=unidade))

        # 5. Persiste reserva
        self.repository.salvar(reserva)
        return reserva

    def cancelar_reserva(self, codigo: str) -> Reserva:
        reserva = self.repository.buscar_por_codigo(codigo)
        if not reserva:
            raise ReservaNaoEncontradaError(f"Reserva {codigo} não encontrada.")

        # Altera estado no domínio (lança exceção se já cancelada)
        reserva.cancelar()

        # Publica evento para devolução de saldo ao estoque físico da unidade
        self.event_bus.publish(ReservaCanceladaEvent(codigo=codigo, isbn=reserva.isbn, unidade=reserva.unidade))

        self.repository.salvar(reserva)
        return reserva

    def listar_reservas(self) -> list[Reserva]:
        return self.repository.listar_todas()

    def obter_reserva(self, codigo: str) -> Reserva:
        reserva = self.repository.buscar_por_codigo(codigo)
        if not reserva:
            raise ReservaNaoEncontradaError(f"Reserva {codigo} não encontrada.")
        return reserva
