from collections.abc import Callable
from typing import Any


class PendingCodeConfirmation:
    def __init__(self, callback: Callable) -> None:
        self.callback = callback

    def submit(self, code: str) -> Any:
        return self.callback(code)
