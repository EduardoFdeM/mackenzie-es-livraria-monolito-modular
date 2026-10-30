"""Repositório de dados do módulo Estoque."""

from typing import Optional
from .models import EstoqueUnidade


class EstoqueRepository:
    """Persistência em memória dos estoques físicos por unidade."""

    def __init__(self) -> None:
        # chave: (isbn, unidade)
        self._estoques: dict[tuple[str, str], EstoqueUnidade] = {}
        self._popular_estoques_iniciais()

    def _popular_estoques_iniciais(self) -> None:
        dados = [
            # Clean Code (9780132350884)
            EstoqueUnidade("Higienópolis", "9780132350884", 3, "Tecnologia", "4", "B"),
            EstoqueUnidade("Paulista", "9780132350884", 1, "Informática", "1", "A"),
            EstoqueUnidade("Pinheiros", "9780132350884", 0, "Geral", "2", "C"),

            # Arquitetura Limpa (9788550804606)
            EstoqueUnidade("Higienópolis", "9788550804606", 2, "Tecnologia", "4", "C"),
            EstoqueUnidade("Paulista", "9788550804606", 0, "Informática", "1", "B"),

            # O Programador Pragmático (9788577807000)
            EstoqueUnidade("Higienópolis", "9788577807000", 4, "Tecnologia", "5", "A"),
            EstoqueUnidade("Pinheiros", "9788577807000", 2, "Geral", "3", "D"),

            # Engenharia de Software Moderna (9786500019506)
            EstoqueUnidade("Paulista", "9786500019506", 5, "Informática", "2", "E"),
            EstoqueUnidade("Higienópolis", "9786500019506", 1, "Tecnologia", "4", "D"),
        ]
        for est in dados:
            self.salvar(est)

    def salvar(self, estoque: EstoqueUnidade) -> None:
        self._estoques[(estoque.isbn, estoque.unidade)] = estoque

    def obter_por_isbn_e_unidade(self, isbn: str, unidade: str) -> Optional[EstoqueUnidade]:
        return self._estoques.get((isbn, unidade))

    def listar_por_isbn(self, isbn: str) -> list[EstoqueUnidade]:
        return [
            est for (book_isbn, _), est in self._estoques.items()
            if book_isbn == isbn
        ]

    def listar_todas_unidades(self) -> list[str]:
        return sorted({unidade for (_, unidade) in self._estoques.keys()})
