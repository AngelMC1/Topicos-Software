from abc import ABC, abstractmethod
from typing import Any, Dict


class AlliedServicePort(ABC):
    """Puerto (interfaz) para consumir el servicio del equipo aliado."""

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Retorna información de estado del servicio aliado."""
