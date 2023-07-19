from abc import ABC, abstractmethod
from typing import Callable, Awaitable
from .SuitContext import SuitContext


SuitRequestDelegate = Callable[[SuitContext], Awaitable]


class ISuitMiddleware(ABC):
    """A middleware of Mobile Suit."""

    @abstractmethod
    async def InvokeAsync(self, context: SuitContext, nextStep: SuitRequestDelegate):
        """
        To invoke the middleware
        """
        raise NotImplementedError
