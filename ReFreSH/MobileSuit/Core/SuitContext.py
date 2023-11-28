from ..RequestStatus import RequestStatus
from ReFreSH.DependencyInjection import ServiceProvider

from typing import Optional, Any


class SuitContext(object):
    """

    Context through the lifetime of a SuitRequest(A Command)
    """

    def __init__(self, sp: ServiceProvider):
        self.Properties: dict[str, object] = {}

        """Properties of current request."""

        self.RequestStatus: RequestStatus = RequestStatus.NoRequest

        """The execution status of current request."""

        self.Exception: Optional[Exception] = None

        """The exception caught in the execution."""

        self.Request: list[str] = []

        """A command from input stream"""

        self.ServiceProvider = sp

        """The ServiceProvider who provides services through whole request."""

        self.Response: Optional[str] = None

        """Output to the output stream"""

    def GetRequiredService(self, T) -> Any:
        return self.ServiceProvider.GetRequiredService(T)

    def GetService(self, T) -> Optional[Any]:
        return self.ServiceProvider.GetService(T)

    def Dispose(self):
        self.ServiceProvider.Dispose()
