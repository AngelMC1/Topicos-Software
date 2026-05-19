import os
from typing import Any, Dict

import requests

from .allied_port import AlliedServicePort

# URL del equipo aliado (Vis Vitalis) — configurable via variable de entorno
_ALLIED_URL = os.getenv("ALLIED_SERVICE_URL", "http://98.95.25.1/api/v2/agenda/therapists/")
_TIMEOUT = 5


class AlliedServiceAdapter(AlliedServicePort):
    """
    Adapter sobre el servicio REST del equipo aliado (Vis Vitalis).
    Aísla al dominio de los detalles de la API externa (DIP).
    Cambiar de equipo aliado solo requiere actualizar ALLIED_SERVICE_URL.
    """

    def get_therapists(self) -> Dict[str, Any]:
        try:
            response = requests.get(_ALLIED_URL, timeout=_TIMEOUT)
            response.raise_for_status()
            return {
                "available": True,
                "therapists": response.json(),
                "source": _ALLIED_URL,
            }
        except requests.exceptions.ConnectionError:
            return {"available": False, "error": "El servicio aliado no está disponible", "source": _ALLIED_URL}
        except requests.exceptions.Timeout:
            return {"available": False, "error": "Timeout al conectar con el servicio aliado", "source": _ALLIED_URL}
        except ValueError:
            return {"available": False, "error": "La respuesta del aliado no es JSON válido", "source": _ALLIED_URL}
        except Exception as exc:
            return {"available": False, "error": str(exc), "source": _ALLIED_URL}
