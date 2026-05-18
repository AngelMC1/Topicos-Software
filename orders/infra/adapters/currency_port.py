from abc import ABC, abstractmethod
from decimal import Decimal


class CurrencyRatePort(ABC):
    """Puerto (interfaz) para consultar el tipo de cambio. Depende de la abstracción, no de la API concreta."""

    @abstractmethod
    def get_usd_to_cop(self) -> Decimal:
        """Retorna cuántos COP equivalen a 1 USD."""
