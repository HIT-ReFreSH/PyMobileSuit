from typing import Type

from ..ISuitCommandServer import ISuitCommandServer
from ..SuitBuildUtils import InstanceFactory
from ..SuitObjectShell import SuitObjectShell


class SuitHostShell(SuitObjectShell):
    """A SuitShell over SuitServer"""

    def __init__(self, otype: Type, factory: InstanceFactory, info: str):
        super().__init__(otype, factory, info, "")

    @classmethod
    def FromCommandServer(cls, serverType: Type) -> "SuitHostShell":
        """Create a Host shell from command server."""
        if not issubclass(serverType, ISuitCommandServer):
            raise ValueError(f"{serverType} must implement ISuitCommandServer")
        return cls(serverType, lambda s: s.ServiceProvider.GetRequiredService(ISuitCommandServer),
                   "SuitServer")
