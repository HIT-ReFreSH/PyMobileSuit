from abc import ABC,abstractmethod

from .HistoryService import IHistoryService
from ..SuitContext import SuitContext
from ... import SuitConfig
from ...IIOHub import IIOHub
from ...OutputType import OutputType
from ...RequestStatus import RequestStatus
from ...Resources import Lang


class ISuitExceptionHandler(ABC):
    """The handler"""
    @abstractmethod
    async def InvokeAsync(self, context: SuitContext):
        """To invoke the middleware

        Args:
            context: Context of the request.
        """
        raise NotImplementedError


class SuitExceptionHandler(ISuitExceptionHandler):
    def __init__(self, history: IHistoryService, io: IIOHub):
        self.History = history
        self.IO = io

    async def InvokeAsync(self, context: SuitContext):
        if context.Exception is None:
            self.History.Status = RequestStatus.Faulted
            self.History.Response = Lang.ApplicationError
        else:
            if SuitConfig.THROW:
                raise context.Exception
            self.History.Status = RequestStatus.Faulted
            self.History.Response = str(context.Exception)
            self.IO.WriteLine(str(context.Exception), OutputType.Error)
