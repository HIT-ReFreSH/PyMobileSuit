import os
from typing import List, Tuple

from .SuitAppShell import SuitAppShell
from .SuitHostShell import SuitHostShell
from .TaskService import ITaskService
from ..ISuitCommandServer import ISuitCommandServer
from ..SuitContext import SuitContext
from ..SuitObjectShell import ISuitShellCollection
from ..SuitShell import MemberType
from ...Decorators import *
from ...IIOHub import IIOHub
from ...OutputType import OutputType
from ...RequestStatus import RequestStatus
from ...Resources import Lang, BuildInCommandInformations
from ....ConsoleColor import ConsoleColor


class SuitCommandServer(ISuitCommandServer):
    """Built-In-Command Server. May be Override if necessary."""

    def __init__(self, io: IIOHub, app: SuitAppShell, host: SuitHostShell, taskService: ITaskService):
        """Initialize a BicServer with the given SuitHost."""
        self.IO = io
        self.App = app
        self.Host = host
        self.TaskService = taskService

    @SuitAlias("help")
    @SuitInfo("List", BuildInCommandInformations)
    async def ListCommands(self, args: List[str]) -> None:
        """Inherited from base class."""
        self.IO.WriteLine(Lang.Members, OutputType.Title)
        await self.ListMembersAsync(self.App)
        self.IO.WriteLine()
        self.IO.WriteLine([
            (Lang.ViewBic, None),
            ("@SuitHelp", ConsoleColor.Cyan),
            ("'", None)
        ], OutputType.Ok)

    @SuitAlias("Exit")
    @SuitInfo("Exit", BuildInCommandInformations)
    def ExitSuit(self) -> RequestStatus:
        """Inherited from base class."""
        return RequestStatus.OnExit

    @SuitInfo("Join", BuildInCommandInformations)
    async def Join(self, index: int, context: SuitContext) -> Optional[str]:
        """Inherited from base class."""
        if self.TaskService.HasTask(index):
            await self.TaskService.Join(index, context)
            return context.Response

        self.IO.WriteLine(BuildInCommandInformations.TaskNotFound, OutputType.Error)
        return None

    @SuitInfo("Tasks", BuildInCommandInformations)
    async def Tasks(self) -> None:
        """Inherited from base class."""
        self.IO.WriteLine(BuildInCommandInformations.Tasks_Title, OutputType.Title)
        for task in self.TaskService.GetTasks():
            line: List[Tuple[str, Optional[ConsoleColor], Optional[ConsoleColor]]] = [
                (str(task.Index), None, None),
                ("\t", None, None),
                (task.Request, self.IO.ColorSetting.InformationColor, None),
                ("\t", None, None),
                {
                    RequestStatus.Ok or RequestStatus.NoRequest or RequestStatus.Handled: (Lang.Done,
                                                                                           self.IO.ColorSetting.OkColor),
                    RequestStatus.Running: (Lang.Running, self.IO.ColorSetting.WarningColor),
                    RequestStatus.CommandParsingFailure: (Lang.InvalidCommand, self.IO.ColorSetting.ErrorColor),
                    RequestStatus.CommandNotFound: (Lang.MemberNotFound, self.IO.ColorSetting.ErrorColor),
                    RequestStatus.Interrupt: (Lang.Interrupt, self.IO.ColorSetting.ErrorColor),
                    RequestStatus.Faulted: (Lang.OnError, self.IO.ColorSetting.ErrorColor)
                }[task.Status],
                ("\t", None, None),
                (task.Response or "-", self.IO.ColorSetting.InformationColor, None)
            ]
            self.IO.WriteLine(line)

    @SuitInfo("Stop", BuildInCommandInformations)
    async def Stop(self, index: int) -> None:
        """Inherited from base class."""
        if self.TaskService.HasTask(index):
            self.TaskService.Stop(index)
        else:
            self.IO.WriteLine(BuildInCommandInformations.TaskNotFound, OutputType.Error)

    @SuitInfo("ClearCompleted", BuildInCommandInformations)
    @SuitAlias("Cct")
    async def ClearCompleted(self) -> None:
        """Inherited from base class."""
        self.TaskService.ClearCompleted()
        await self.Tasks()

    @SuitInfo("Dir", BuildInCommandInformations)
    @SuitAlias("pwd")
    def Dir(self) -> str:
        """Inherited from base class."""
        return os.getcwd()

    @SuitInfo("ChDir", BuildInCommandInformations)
    @SuitAlias("cd")
    def ChDir(self, path: str) -> str:
        """Inherited from base class."""
        if not os.path.exists(path):
            return BuildInCommandInformations.DirectoryNotFound
        os.chdir(path)
        return os.getcwd()

    @SuitInfo("Help", BuildInCommandInformations)
    @SuitAlias("shelp")
    async def SuitHelp(self) -> None:
        """Inherited from base class."""
        self.IO.WriteLine(Lang.Bic, OutputType.Title)
        await self.ListMembersAsync(self.Host)
        self.IO.WriteLine()
        self.IO.WriteLine([
            (Lang.BicExp1, None),
            ("@", ConsoleColor.Cyan),
            (Lang.BicExp2, None)
        ], OutputType.Ok)

    @SuitIgnore
    async def ListMembersAsync(self, suitObject: ISuitShellCollection) -> None:
        """List members of a SuitObject"""
        if suitObject is None:
            return
        self.IO.AppendWriteLinePrefix()

        for shell in suitObject.Members():
            infoColor, lChar, rChar = {
                MemberType.MethodWithInfo: (ConsoleColor.Blue, '[', ']'),
                MemberType.MethodWithoutInfo: (ConsoleColor.DarkBlue, '(', ')'),
                MemberType.FieldWithInfo: (ConsoleColor.Green, '<', '>'),
                MemberType.FieldWithoutInfo: (ConsoleColor.DarkGreen, '{', '}')
            }[shell.Type]
            aliasesExpression = "".join(f"/{alias}" for alias in shell.Aliases)
            self.IO.WriteLine([
                (shell.AbsoluteName, None),
                (aliasesExpression, ConsoleColor.DarkYellow),
                (f" {lChar}{shell.Information}{rChar}", infoColor)
            ])

        self.IO.SubtractWriteLinePrefix()
