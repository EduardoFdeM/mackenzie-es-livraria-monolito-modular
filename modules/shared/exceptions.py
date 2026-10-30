"""Exceções de domínio compartilhadas da Livraria Mackenzie."""


class LivrariaError(Exception):
    """Exceção base para regras de negócio da livraria."""
    pass


class EstoqueInsuficienteError(LivrariaError):
    """Lançada quando a unidade física não possui saldo suficiente."""
    pass


class LivroNaoEncontradoError(LivrariaError):
    """Lançada quando o ISBN consultado não existe no catálogo."""
    pass


class ReservaNaoEncontradaError(LivrariaError):
    """Lançada quando o código de reserva não existe."""
    pass


class ReservaJaCanceladaError(LivrariaError):
    """Lançada quando se tenta cancelar uma reserva já cancelada."""
    pass
