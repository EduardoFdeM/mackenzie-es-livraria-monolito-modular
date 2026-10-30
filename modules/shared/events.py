"""Barramento de eventos em memória para comunicação desacoplada entre módulos."""

from dataclasses import dataclass
from typing import Callable, Type


@dataclass(frozen=True)
class ReservaCriadaEvent:
    codigo: str
    isbn: str
    unidade: str


@dataclass(frozen=True)
class ReservaCanceladaEvent:
    codigo: str
    isbn: str
    unidade: str


class EventBus:
    """Implementação simples de Mediator/EventBus para desacoplamento entre módulos."""

    def __init__(self) -> None:
        self._subscribers: dict[Type, list[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event: object) -> None:
        event_type = type(event)
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            handler(event)
