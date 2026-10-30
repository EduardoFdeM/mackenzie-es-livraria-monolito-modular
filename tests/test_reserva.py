"""Testes unitários do módulo Reserva e regras de negócio."""

import pytest
from modules.shared.events import EventBus
from modules.catalogo.service import CatalogoService
from modules.estoque.service import EstoqueService
from modules.reserva.service import ReservaService
from modules.reserva.models import StatusReserva
from modules.shared.exceptions import (
    EstoqueInsuficienteError,
    LivroNaoEncontradoError,
    ReservaJaCanceladaError,
    ReservaNaoEncontradaError,
)


@pytest.fixture
def reserva_setup():
    bus = EventBus()
    c_service = CatalogoService()
    e_service = EstoqueService()
    e_service.registrar_listeners(bus)
    r_service = ReservaService(
        catalogo_service=c_service,
        estoque_service=e_service,
        event_bus=bus,
    )
    return c_service, e_service, r_service


def test_criar_e_cancelar_reserva_com_sucesso(reserva_setup):
    _, e_service, r_service = reserva_setup

    saldo_inicial = e_service.obter_estoque_unidade("9780132350884", "Paulista").quantidade
    assert saldo_inicial == 1

    # Cria reserva
    reserva = r_service.criar_reserva("9780132350884", "Paulista")
    assert reserva.codigo == "RES-0001"
    assert reserva.status == StatusReserva.ATIVA
    assert e_service.obter_estoque_unidade("9780132350884", "Paulista").quantidade == 0

    # Cancela reserva
    reserva_cancelada = r_service.cancelar_reserva("RES-0001")
    assert reserva_cancelada.status == StatusReserva.CANCELADA
    assert e_service.obter_estoque_unidade("9780132350884", "Paulista").quantidade == 1


def test_criar_reserva_sem_estoque_lanca_excecao(reserva_setup):
    _, _, r_service = reserva_setup
    # Pinheiros possui 0 exemplares de Clean Code
    with pytest.raises(EstoqueInsuficienteError):
        r_service.criar_reserva("9780132350884", "Pinheiros")


def test_cancelamento_duplo_lanca_excecao(reserva_setup):
    _, _, r_service = reserva_setup
    r_service.criar_reserva("9780132350884", "Paulista")
    r_service.cancelar_reserva("RES-0001")

    with pytest.raises(ReservaJaCanceladaError):
        r_service.cancelar_reserva("RES-0001")


def test_cancelar_reserva_inexistente(reserva_setup):
    _, _, r_service = reserva_setup
    with pytest.raises(ReservaNaoEncontradaError):
        r_service.cancelar_reserva("RES-9999")
