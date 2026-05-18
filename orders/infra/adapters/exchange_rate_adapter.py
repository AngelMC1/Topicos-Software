import requests
from decimal import Decimal

from .currency_port import CurrencyRatePort

_FALLBACK_RATE = Decimal("4100")


class ExchangeRateAdapter(CurrencyRatePort):
    """
    Adapter sobre open.er-api.com (gratuito, sin API key).
    Traduce la respuesta del servicio externo al contrato definido por CurrencyRatePort.
    Principio DIP: el dominio depende de CurrencyRatePort, nunca de este adaptador concreto.
    """

    API_URL = "https://open.er-api.com/v6/latest/USD"
    TIMEOUT = 5

    def get_usd_to_cop(self) -> Decimal:
        try:
            response = requests.get(self.API_URL, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()
            rate = data["rates"]["COP"]
            return Decimal(str(rate))
        except Exception:
            return _FALLBACK_RATE
