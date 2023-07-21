from abc import ABC, abstractmethod
from typing import List, Type, Callable

from .Core import SuitBuildUtils
from .Core.ISuitCommandServer import ISuitCommandServer
from .Core.ISuitMiddleware import ISuitMiddleware
from .Core.Middlewares.AppShellMiddleware import AppShellMiddleware
from .Core.Middlewares.FinalizeMiddleware import FinalizeMiddleware
from .Core.Middlewares.HostShellMiddleware import HostShellMiddleware
from .Core.Middlewares.PromptMiddleware import PromptMiddleware
from .Core.Middlewares.UserInputMiddleware import UserInputMiddleware
from .Core.Services.AppInfo import SuitAppInfo, ISuitAppInfo
from .Core.Services.HistoryService import IHistoryService, HistoryService
from .Core.Services.IOHub import IOHub, PureTextIOHub, IOHub4Bit
from .Core.Services.ParsingService import ParsingService, IParsingService
from .Core.Services.PromptFormatter import PromptFormatter, PromptFormatters
from .Core.Services.SuitAppShell import SuitAppShell
from .Core.Services.SuitCommandServer import SuitCommandServer
from .Core.Services.SuitExceptionHandler import ISuitExceptionHandler, SuitExceptionHandler
from .Core.Services.SuitHostShell import SuitHostShell
from .Core.Services.TaskService import TaskRecorder, ITaskService, TaskService
from .Core.SuitMethodShell import SuitMethodShell
from .Core.SuitObjectShell import SuitObjectShell
from .Core.SuitShell import SuitShell
from .IIOHub import IIOHub, IIOHubConfigurator
from .Resources import Lang,BuildInCommandInformations
from .SuitHost import SuitHost
from ..DependencyInjection import ServiceBag


class ISuitWorkFlow(ABC):
    """Describes the work flow of mobile suit."""

    @abstractmethod
    def UseCustom(self, middlewareType: Type) -> 'ISuitWorkFlow':
        """Add a custom middleware"""
        pass

    @abstractmethod
    def UsePrompt(self) -> 'ISuitWorkFlow':
        """Add suit prompt middleware"""
        pass

    @abstractmethod
    def UseInput(self) -> 'ISuitWorkFlow':
        """Add input middleware"""
        pass

    @abstractmethod
    def UseAppShell(self) -> 'ISuitWorkFlow':
        """Add AppShell middleware"""
        pass

    @abstractmethod
    def UseHostShell(self) -> 'ISuitWorkFlow':
        """Add HostShell middleware"""
        pass

    @abstractmethod
    def UseFinalize(self) -> 'ISuitWorkFlow':
        """Add Finalize middleware"""
        pass


class SuitWorkFlow(ISuitWorkFlow):
    def __init__(self):
        self._middlewares = []

    def UseCustom(self, middlewareType: Type) -> 'ISuitWorkFlow':
        if issubclass(middlewareType, ISuitMiddleware):
            self._middlewares.append(middlewareType)
        else:
            raise ValueError(f"{middlewareType} is not a subclass of ISuitMiddleware")
        return self

    def UsePrompt(self) -> 'ISuitWorkFlow':
        return self.UseCustom(PromptMiddleware)

    def UseInput(self) -> 'ISuitWorkFlow':
        return self.UseCustom(UserInputMiddleware)

    def UseAppShell(self) -> 'ISuitWorkFlow':
        return self.UseCustom(AppShellMiddleware)

    def UseHostShell(self) -> 'ISuitWorkFlow':
        return self.UseCustom(HostShellMiddleware)

    def UseFinalize(self) -> 'ISuitWorkFlow':
        return self.UseCustom(FinalizeMiddleware)

    def Build(self, serviceProvider) -> List[ISuitMiddleware]:
        if not self._middlewares:
            self.UsePrompt().UseInput().UseHostShell().UseAppShell().UseFinalize()

        r = []
        for middlewareType in self._middlewares:
            middleware = SuitBuildUtils.CreateInstanceWithProvider(middlewareType, serviceProvider)
            if isinstance(middleware, ISuitMiddleware):
                r.append(middleware)
            else:
                raise ValueError(f"{middlewareType} is not a subclass of ISuitMiddleware")

        return r


class SuitHostBuilder:
    """Builder to build a MobileSuit host."""

    def __init__(self, args: List[str] = []):
        self._clients = []
        self._workFlow = SuitWorkFlow()
        self._commandServer = SuitCommandServer
        self._cancelTasks = TaskRecorder()
        self.AppInfo = SuitAppInfo()
        self.AppInfo.StartArgs = args
        self.Services = ServiceBag()
        self.Services.AddScoped(ISuitCommandServer, TActual=SuitCommandServer)
        self.Services.AddSingletonInstance(PromptFormatter, PromptFormatters.BasicPromptFormatter)
        self.Services.AddSingletonInstance(ITaskService, TaskService(self._cancelTasks))
        self.Services.AddSingleton(IHistoryService, TActual=HistoryService)
        self.Services.AddSingleton(IIOHub, TActual=IOHub)
        self.Services.AddSingleton(IIOHubConfigurator, lambda: (lambda io: io), [])
        self.Parsing = ParsingService()
        self.Services.AddSingletonInstance(IParsingService, self.Parsing)
        self.Services.AddSingleton(ISuitExceptionHandler, SuitExceptionHandler)

    def AddClient(self, client: SuitShell):
        """Add a client shell to mobile suit"""
        self._clients.append(client)

    def UseCommandServer(self, serverType: Type):
        """Add a client shell to mobile suit"""
        if not issubclass(serverType, ISuitCommandServer):
            raise ValueError(f"{serverType} is not a subclass of ISuitCommandServer")

        self.Services.AddScoped(ISuitCommandServer, TActual=SuitCommandServer)
        self._commandServer = serverType

    def ConfigureIO(self, configure: IIOHubConfigurator):
        """config IO"""
        self.Services.AddSingleton(IIOHubConfigurator, configure)

    def Build(self) -> SuitHost:
        """Build a SuitHost."""
        self.Services.AddSingletonInstance(ISuitAppInfo, self.AppInfo)
        self.Services.AddSingletonInstance(SuitAppShell, SuitAppShell.FromClients(self._clients))
        self.Services.AddSingletonInstance(SuitHostShell, SuitHostShell.FromCommandServer(self._commandServer))

        providers = self.Services.Build()
        # Load language packages
        Lang.Load()
        BuildInCommandInformations.Load()
        return SuitHost(providers, self._workFlow.Build(providers), self._cancelTasks)

    def HasName(self, name: str) -> 'SuitHostBuilder':
        """Use given PromptGenerator for the Host"""
        self.AppInfo.AppName = name
        return self

    def MapClass(self, T, name: str = '') -> 'SuitHostBuilder':
        """Use given PromptGenerator for the Host"""
        self.AddClient(SuitObjectShell.FromType(T, name))
        return self

    def MapInstance(self, instance, name: str = '') -> 'SuitHostBuilder':
        """Use given PromptGenerator for the Host"""
        T = type(instance)
        self.AddClient(SuitObjectShell.FromInstance(T, lambda _: instance, name))
        return self

    def MapMethod(self, name: str, method: Callable) -> 'SuitHostBuilder':
        """Use given PromptGenerator for the Host"""
        self.AddClient(SuitMethodShell.FromDelegate(name, method))
        return self

    def UsePowerLine(self) -> 'SuitHostBuilder':
        """Use PowerLine PromptGenerator for the Host"""
        self.Services.AddSingletonInstance(PromptFormatter, PromptFormatters.PowerLineFormatter)
        return self

    def UsePureTextIO(self) -> 'SuitHostBuilder':
        """Use Plain text IO for the Host"""
        self.Services.AddSingleton(IIOHub, TActual=PureTextIOHub)
        return self

    def Use4BitColorIO(self) -> 'SuitHostBuilder':
        """Use 4-bit color IO for the Host"""
        self.Services.AddSingleton(IIOHub, TActual=IOHub4Bit)
        return self
