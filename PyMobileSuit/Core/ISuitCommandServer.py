from abc import ABC, abstractmethod

from PyMobileSuit.Core.SuitContext import SuitContext

class ISuitCommandServer(ABC):
    """Built-In-Command Server's Model."""

    @abstractmethod
    async def ListCommands(self, args: list[str]) -> None:
        """Show Members of the Current SuitObject
        
        :param args: command args
        """
        pass

    @abstractmethod
    def ExitSuit(self) -> RequestStatus:
        """Exit MobileSuit"""
        pass

    @abstractmethod
    async def Join(self, index: int, context: SuitContext) -> Optional[str]:
        """Join a Running task
        
        :param index: index of the task to join
        :param context: context of the request
        """
        pass

    @abstractmethod
    async def Tasks(self) -> None:
        """Get All tasks"""
        pass

    @abstractmethod
    async def Stop(self, index: int) -> None:
        """Stop a Running task
        
        :param index: index of the task to stop
        """
        pass

    @abstractmethod
    async def ClearCompleted(self) -> None:
        """Clear all Completed Tasks."""
        pass

    @abstractmethod
    def Dir(self) -> str:
        """Get current directory"""
        pass

    @abstractmethod
    def ChDir(self, path: str) -> str:
        """Set current directory
        
        :param path: path to set as current directory
        """
        pass

    @abstractmethod
    async def Help(self, args: list[str]) -> None:
        """Show Help of MobileSuit
        
        :param args: command args
        """
        pass
