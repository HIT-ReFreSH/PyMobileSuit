from typing import List, Iterable

from ..SuitContext import SuitContext
from ..SuitMethodShell import SuitMethodShell
from ..SuitObjectShell import ISuitShellCollection, SuitObjectShell
from ..SuitShell import SuitShell
from ...RequestStatus import RequestStatus


class SuitAppShell(SuitShell, ISuitShellCollection):
    """SuitShell for Client App."""

    def __init__(self):
        super().__init__(object, lambda _: None, "SuitClient")
        self._members: List[SuitShell] = []

    @property
    def MemberCount(self) -> int:
        """Inherited from base class."""
        return len(self._members)

    def Members(self) -> Iterable[SuitShell]:
        """Ordered members of this"""
        for shell in self._members:
            if isinstance(shell, SuitMethodShell):
                yield shell
            elif isinstance(shell, SuitObjectShell):
                for objMember in shell.Members():
                    yield objMember
            else:
                yield shell

    @classmethod
    def FromClients(cls, clients: Iterable[SuitShell]) -> "SuitAppShell":
        r = cls()
        r._members.extend(clients)
        return r

    async def Execute(self, context: SuitContext) -> None:
        """Inherited from base class."""
        for shell in self._members:
            if not shell.MayExecute(context):
                continue
            await shell.Execute(context)
            if context.RequestStatus != RequestStatus.NotHandled:
                return

    def MayExecute(self, context: SuitContext) -> bool:
        """Inherited from base class."""
        return any(sys.MayExecute(context) for sys in self._members)
