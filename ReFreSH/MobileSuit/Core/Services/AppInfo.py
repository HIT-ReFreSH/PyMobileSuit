from abc import ABC, abstractmethod


class ISuitAppInfo(ABC):
    """provides basic info of App."""

    @property
    @abstractmethod
    def AppName(self) -> str:
        """Name of application."""
        pass

    @property
    @abstractmethod
    def StartArgs(self) -> list[str]:
        """Arguments for startup."""
        pass


class SuitAppInfo(ISuitAppInfo):
    """provides basic info of App."""

    def __init__(self):
        self._AppName = ""
        self._StartArgs = []

    @property
    def AppName(self) -> str:
        """Name of application."""
        return self._AppName

    @AppName.setter
    def AppName(self, value: str) -> None:
        self._AppName = value

    @property
    def StartArgs(self) -> list[str]:
        """Arguments for startup."""
        return self._StartArgs

    @StartArgs.setter
    def StartArgs(self, value: list[str]) -> None:
        self._StartArgs = value
