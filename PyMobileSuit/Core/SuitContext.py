from PyMobileSuit.RequestStatus import RequestStatus

from typing import Optional


class SuitContext(object):
    """

    Context through the lifetime of a SuitRequest(A Command)
    """


    def __init__(self, ServiceProvider: dict):


        self.Properties: dict[str, object] = {}

        """Properties of current request."""

        self.RequestStatus: RequestStatus = RequestStatus.NoRequest

        """The execution status of current request."""

        self.Exception: Optional[Exception] = None

        """The exception caught in the execution."""

        self.Request: list[str] = []

        """A command from input stream"""

        self.ServiceProvider: dict = ServiceProvider

        """The ServiceProvider who provides services through whole request."""

        self.Response: Optional[str] = None

        """Output to the output stream"""


    def GetRequiredService(self, T)->object:

        return self.ServiceProvider[T]

    def GetService(self, T)->Optional[object]:

        return self.ServiceProvider[T]

