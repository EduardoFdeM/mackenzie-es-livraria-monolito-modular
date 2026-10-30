"""Testes de integração ponta a ponta do Monólito Modular."""

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_fluxo_completo_catalogo_busca_reserva_cancelamento(client):
    # 1. Página inicial lista os livros
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "Catálogo de Livros e Exemplares" in res_home.text
    assert "Clean Code" in res_home.text
    assert "Arquitetura Limpa" in res_home.text

    # 2. Busca por termo
    res_busca = client.get("/?q=Pragmático")
    assert res_busca.status_code == 200
    assert "O Programador Pragmático" in res_busca.text

    # 3. Detalhes de um livro e filiais
    res_detalhes = client.get("/livros/9780132350884")
    assert res_detalhes.status_code == 200
    assert "Clean Code" in res_detalhes.text
    assert "Higienópolis" in res_detalhes.text
    assert "Setor Tecnologia" in res_detalhes.text

    # 4. Criar reserva via POST
    res_criar = client.post(
        "/reservas",
        data={"isbn": "9780132350884", "unidade": "Paulista"},
        follow_redirects=True,
    )
    assert res_criar.status_code == 200
    assert "RES-0001" in res_criar.text
    assert "Ativa" in res_criar.text
    assert "realizada com sucesso" in res_criar.text

    # 5. Cancelar reserva via POST e verificar mensagem de devolução de estoque
    res_cancelar = client.post("/reservas/RES-0001/cancelar", follow_redirects=True)
    assert res_cancelar.status_code == 200
    assert "cancelada com sucesso" in res_cancelar.text
    assert "Cancelada" in res_cancelar.text
    assert "Exemplar devolvido" in res_cancelar.text


def test_reserva_unidade_sem_estoque_redireciona_com_erro(client):
    # Pinheiros possui 0 unidades de Clean Code
    res = client.post(
        "/reservas",
        data={"isbn": "9780132350884", "unidade": "Pinheiros"},
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert "Não há exemplares disponíveis" in res.text


def test_detalhes_livro_inexistente_redireciona_com_erro(client):
    res = client.get("/livros/9999999999999", follow_redirects=True)
    assert res.status_code == 200
    assert "não foi encontrado no catálogo" in res.text


def test_reserva_com_campos_vazios_ou_livro_inexistente(client):
    # Campos vazios
    res_vazio = client.post("/reservas", data={"isbn": "", "unidade": ""}, follow_redirects=True)
    assert res_vazio.status_code == 200
    assert "Informe o ISBN e a unidade desejada" in res_vazio.text

    # Livro inexistente
    res_inexistente = client.post(
        "/reservas",
        data={"isbn": "9999999999999", "unidade": "Paulista"},
        follow_redirects=True,
    )
    assert res_inexistente.status_code == 200
    assert "não encontrado no catálogo" in res_inexistente.text
