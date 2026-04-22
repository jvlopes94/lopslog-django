import logging
from apps.domain.events import DomainEvent, event_bus

logger = logging.getLogger(__name__)
_registered = False


def log_domain_event(event: DomainEvent) -> None:
    logger.info("domain_event=%s payload=%s", event.name, event.payload)


def register_domain_handlers() -> None:
    global _registered
    if _registered:
        return

    for event_name in [
        "driver.created",
        "driver.updated",
        "driver.deleted",
        "vehicle.created",
        "vehicle.updated",
        "vehicle.deleted",
        "vehicle.driver_assigned",
    ]:
        event_bus.subscribe(event_name, log_domain_event)
    _registered = True
