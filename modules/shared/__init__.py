"""Módulo compartilhado (Shared Kernel)."""
from .exceptions import (
    LivrariaError,
    EstoqueInsuficienteError,
    LivroNaoEncontradoError,
    ReservaNaoEncontradaError,
    ReservaJaCanceladaError,
)
from .events import EventBus, ReservaCriadaEvent, ReservaCanceladaEvent

__all__ = [
    "LivrariaError",
    "EstoqueInsuficienteError",
    "LivroNaoEncontradoError",
    "ReservaNaoEncontradaError",
    "ReservaJaCanceladaError",
    "EventBus",
    "ReservaCriadaEvent",
    "ReservaCanceladaEvent",
]
