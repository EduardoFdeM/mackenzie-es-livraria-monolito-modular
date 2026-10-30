"""Serviço público do módulo Catálogo."""

from typing import Optional
from .models import Livro
from .repository import CatalogoRepository
from modules.shared.exceptions import LivroNaoEncontradoError


class CatalogoService:
    """Interface pública do módulo Catálogo para a aplicação."""

    def __init__(self, repository: Optional[CatalogoRepository] = None) -> None:
        self.repository = repository or CatalogoRepository()

    def listar_todos(self) -> list[Livro]:
        return self.repository.listar_todos()

    def buscar_por_termo(self, termo: str) -> list[Livro]:
        return self.repository.buscar_por_termo(termo)

    def obter_por_isbn(self, isbn: str) -> Livro:
        livro = self.repository.buscar_por_isbn(isbn)
        if not livro:
            raise LivroNaoEncontradoError(f"Livro com ISBN {isbn} não encontrado no catálogo.")
        return livro

    def existe_livro(self, isbn: str) -> bool:
        return self.repository.buscar_por_isbn(isbn) is not None
