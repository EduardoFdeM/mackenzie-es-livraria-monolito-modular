"""Testes unitários do módulo Catálogo."""

from decimal import Decimal
import pytest
from modules.catalogo.models import Livro
from modules.catalogo.repository import CatalogoRepository
from modules.catalogo.service import CatalogoService
from modules.shared.exceptions import LivroNaoEncontradoError


def test_catalogo_service_listar_todos():
    service = CatalogoService()
    livros = service.listar_todos()
    assert len(livros) >= 2
    isbns = [l.isbn for l in livros]
    assert "9780132350884" in isbns


def test_catalogo_service_buscar_por_termo():
    service = CatalogoService()
    resultado = service.buscar_por_termo("Clean")
    assert len(resultado) >= 1
    assert any("Clean Code" in l.titulo for l in resultado)


def test_catalogo_service_obter_por_isbn_valido_e_invalido():
    service = CatalogoService()
    livro = service.obter_por_isbn("9780132350884")
    assert livro.titulo == "Clean Code"
    assert livro.preco_formatado == "R$ 89,90"

    with pytest.raises(LivroNaoEncontradoError):
        service.obter_por_isbn("0000000000000")
