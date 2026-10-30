"""Testes unitários do módulo Estoque."""

import pytest
from modules.estoque.models import EstoqueUnidade
from modules.estoque.repository import EstoqueRepository
from modules.estoque.service import EstoqueService
from modules.shared.exceptions import EstoqueInsuficienteError
from modules.shared.events import EventBus, ReservaCriadaEvent, ReservaCanceladaEvent


def test_estoque_modelo_decrementar_e_incrementar():
    est = EstoqueUnidade("Higienópolis", "123", 2, "Tec", "1", "A")
    assert est.localizacao_formatada == "Setor Tec, corredor 1, prateleira A"
    est.decrementar()
    assert est.quantidade == 1
    est.incrementar()
    assert est.quantidade == 2


def test_estoque_modelo_insuficiente_lanca_excecao():
    est = EstoqueUnidade("Higienópolis", "123", 0)
    with pytest.raises(EstoqueInsuficienteError):
        est.decrementar()


def test_estoque_service_e_listeners_de_eventos():
    repo = EstoqueRepository()
    service = EstoqueService(repo)
    bus = EventBus()
    service.registrar_listeners(bus)

    # Clean Code em Higienópolis começa com 3
    est = service.obter_estoque_unidade("9780132350884", "Higienópolis")
    saldo_inicial = est.quantidade

    # Publica evento de criação de reserva
    bus.publish(ReservaCriadaEvent(codigo="RES-0001", isbn="9780132350884", unidade="Higienópolis"))
    est_depois = service.obter_estoque_unidade("9780132350884", "Higienópolis")
    assert est_depois.quantidade == saldo_inicial - 1

    # Publica evento de cancelamento de reserva
    bus.publish(ReservaCanceladaEvent(codigo="RES-0001", isbn="9780132350884", unidade="Higienópolis"))
    est_final = service.obter_estoque_unidade("9780132350884", "Higienópolis")
    assert est_final.quantidade == saldo_inicial
