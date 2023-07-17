from PyMobileSuit.RequestStatus import RequestStatus

from abc import ABC, abstractmethod
from typing import Optional

class IHistoryService(ABC):
    """Provides request history."""

    @property
    @abstractmethod
    def Status(self) -> RequestStatus:
        """Status of last Request."""
        pass

    @Status.setter
    @abstractmethod
    def Status(self, value: RequestStatus) -> None:
        pass

    @property
    @abstractmethod
    def Response(self) -> Optional[str]:
        """Response of last Request."""
        pass

    @Response.setter
    @abstractmethod
    def Response(self, value: Optional[str]) -> None:
        pass

class HistoryService(IHistoryService):
    def __init__(self):
        self._Status = RequestStatus.Ok
        self._Response = None

    @property
    def Status(self) -> RequestStatus:
        """Status of last Request."""
        return self._Status

    @Status.setter
    def Status(self, value: RequestStatus) -> None:
        self._Status = value

    @property
    def Response(self) -> Optional[str]:
        """Response of last Request."""
        return self._Response

    @Response.setter
    def Response(self, value: Optional[str]) -> None:
        self._Response = value
