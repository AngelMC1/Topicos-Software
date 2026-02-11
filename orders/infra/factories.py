import os
from .notifier import ConsoleNotifier, EmailNotifier, Notifier

class NotifierFactory:
    @staticmethod
    def create() -> Notifier:
        env_type = os.getenv("ENV_TYPE", "MOCK").upper()
        return EmailNotifier() if env_type == "REAL" else ConsoleNotifier()
