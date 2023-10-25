import logging

from abc import ABC, abstractmethod
from typing import Any


class AbstractTask(ABC):
    logger = logging.getLogger()

    def run(self) -> Any:
        try:
            return self._run()
        except Exception as e:
            return self._on_exception(e)

    @abstractmethod
    def _run(self) -> Any:
        pass

    @abstractmethod
    def _on_exception(self, exception: Exception) -> Any:
        pass
