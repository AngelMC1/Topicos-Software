from abc import ABC, abstractmethod
from typing import Any, Dict


class AlliedServicePort(ABC):
    """Puerto (interfaz) para consumir el servicio del equipo aliado (Vis Vitalis)."""

    @abstractmethod
    def get_therapists(self) -> Dict[str, Any]:
        """Retorna el catálogo de terapeutas del equipo aliado."""
