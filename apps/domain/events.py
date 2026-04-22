from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class DomainEvent:
    name: str
    payload: dict


Handler = Callable[[DomainEvent], None]


class InMemoryEventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Handler]] = {}

    def subscribe(self, event_name: str, handler: Handler) -> None:
        self._handlers.setdefault(event_name, []).append(handler)

    def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers.get(event.name, []):
            handler(event)

    def unsubscribe(self, event_name: str, handler: Handler) -> None:
        handlers = self._handlers.get(event_name, [])
        if handler in handlers:
            handlers.remove(handler)


event_bus = InMemoryEventBus()
