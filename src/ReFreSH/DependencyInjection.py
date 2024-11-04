from enum import Enum, auto
from typing import Callable, Iterable, Type, Any, Optional, List
import inspect

from .CSharp import nameof


class ServiceType(Enum):
    """
    Enumeration representing the lifetime of a service.

    Attributes:
        Singleton: Service will only be instantiated once.
        Scoped: Service will be instantiated for each request.
    """
    Singleton = 0
    """
    Service will only be instantiated once
    """
    Scoped = auto()
    """
    Service will be instantiated for each request
    """


class ServiceDescriptor(object):
    """
    Descriptor for injected services
    """

    def __init__(self, TService: Type, stype: ServiceType, factory: Optional[Callable] = None,
                 dependencies: Optional[Iterable] = None, TActual=None):
        """Initialize a service descriptor

        Args:
            TService (Type): Type of described service
            dependencies (Iterable[Type]): Type of required services to create described service
            factory (Callable[dependencies,TService]):
                A factory function producing a described service instance with the required services
            stype (ServiceType): Lifetime of the service
        """
        self.TService = TService
        self.Type = stype
        if TActual is None:
            TActual = TService
        self.TActual = TActual
        if factory is None:
            factory = getattr(TActual, "__init__")
        factorySig = inspect.signature(factory).parameters
        factoryParams = [(name, param) for name, param in
                         filter(lambda x: x[0] != 'self', factorySig.items())]
        if 'self' in factorySig:
            factory = TActual
        if dependencies is None:
            dependencies = []
            for _, param in factoryParams:
                if param.annotation == inspect.Parameter.empty:
                    raise ServiceInstantiationFailure(TService, None, self)
                dependencies.append(param.annotation)
        self.Factory = factory
        self.Dependencies = dependencies

    def CreateInstance(self, provider):
        args = []
        for dependency in self.Dependencies:
            depdInstance = provider.GetRequiredService(dependency)
            args.append(depdInstance)

        return self.Factory(*args)


class ServiceNotFound(Exception):
    def __init__(self, TService, provider):
        self.TService = TService
        self.Provider = provider

    def __str__(self):
        return f'Service {nameof(self.TService)} not found.'


class GetScopedServiceFromRootProviderException(Exception):
    def __init__(self, TService, provider):
        self.TService = TService
        self.Provider = provider

    def __str__(self):
        return f'Service {nameof(self.TService)} not found.'


class DagJudge:
    @classmethod
    def dfs(cls, graph: dict[Any, Iterable[Any]], node: Any, visited: dict[Any, bool], stack: dict[Any, bool]):
        visited[node] = True
        stack[node] = True
        for neighbor in graph[node]:
            if neighbor not in visited:
                raise ServiceNotFound(neighbor, graph)
            if not visited[neighbor]:
                if cls.dfs(graph, neighbor, visited, stack):
                    return True
            elif stack[neighbor]:
                return True
        stack[node] = False
        return False

    @classmethod
    def has_cycle(cls, graph: dict[Any, Iterable[Any]]):
        visited = {s: False for s in graph.keys()}
        stack = {s: False for s in graph.keys()}
        for node in graph.keys():
            if not visited[node]:
                if cls.dfs(graph, node, visited, stack):
                    return True
        return False

    @classmethod
    def check(cls, services: Iterable) -> bool:
        graph: dict[Any, Iterable[Any]] = {}
        for service in services:
            graph[service.TService] = service.Dependencies
        return cls.has_cycle(graph)


class ServiceProvider(object):
    """
    A bag of services
    """

    def __init__(self, services: dict[Any, Any] = {}, instances: dict[Any, Any] = {}):
        self._Services: dict[Any, ServiceDescriptor] = services
        self.Instances: dict[Any, Any] = instances
        self.Managed = []
        self._Scoped = False
        self._SubScopes = []

    @staticmethod
    def IsLifetimeManaged(TService):
        return hasattr(TService, '__enter__') and hasattr(TService, '__exit__')

    @staticmethod
    def StartLifeTime(instance: Any):
        instance.__enter__()

    @staticmethod
    def EndLifeTime(instance: Any):
        instance.__exit__(None, None, None)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, trace):
        for scope in self._SubScopes:
            ServiceProvider.EndLifeTime(scope)
        for instance in self.Managed:
            ServiceProvider.EndLifeTime(instance)
        self._SubScopes = []
        self.Managed = []

    def EnsureInstance(self, TService):
        desc: ServiceDescriptor = self._Services[TService]
        if not self._Scoped and desc.Type == ServiceType.Scoped:
            raise GetScopedServiceFromRootProviderException(TService, self)
        instance = desc.CreateInstance(self)
        self.Instances[TService] = instance
        if ServiceProvider.IsLifetimeManaged(TService):
            ServiceProvider.StartLifeTime(instance)
        for scope in self._SubScopes:
            scope.Instances[TService] = instance
        return instance

    def GetRequiredService(self, TService):
        instance = self.GetService(TService)
        if instance is None:
            raise ServiceNotFound(TService, self)
        return instance

    def GetService(self, TService):
        if TService in self.Instances:
            return self.Instances[TService]
        if TService in self._Services:
            return self.EnsureInstance(TService)
        return None

    def CreateScope(self):
        subScope = ScopedServiceProvider(
            [self], self._Services, self.Instances)
        self._SubScopes.append(subScope)
        return subScope

    def Dispose(self):
        self.__exit__(None, None, None)


class ScopedServiceProvider(ServiceProvider):
    """
    A bag of services
    """

    def __init__(self, superScopes: List, services: dict[Any, Any] = {}, instances: dict[Any, Any] = {}):
        super().__init__(services, instances)
        self._Scoped = True
        self._SuperScopes = superScopes

    def EnsureInstance(self, TService):
        instance = ServiceProvider.EnsureInstance(self, TService)
        if self._Services[TService].Type == ServiceType.Singleton:
            managed = instance in self.Managed
            for scope in self._SuperScopes:
                scope.Instances[TService] = instance
                if not isinstance(scope, ScopedServiceProvider) and managed:
                    self.Managed.remove(instance)
                    scope.Managed.append(instance)
        return instance

    def CreateScope(self):
        subScope = ScopedServiceProvider(
            self._SuperScopes + [self], self._Services, self.Instances)
        self._SubScopes.append(subScope)
        return subScope


class DependencyRingError(Exception):
    pass


class ServiceBag(object):
    """
    A bag of services
    """

    def __init__(self):
        self._Services = {}

    def Build(self) -> ServiceProvider:
        if DagJudge.check(self._Services.values()):
            raise DependencyRingError
        return ServiceProvider({s.TService: s for s in self._Services.values()}, {})

    def AddDescriptor(self, desc: ServiceDescriptor) -> None:
        self._Services[desc.TService] = desc

    def AddSingleton(self, TService, factory: Optional[Callable] = None,
                     dependencies: Optional[Iterable] = None, TActual=None) -> None:
        self.AddDescriptor(ServiceDescriptor(
            TService, ServiceType.Singleton, factory, dependencies, TActual))

    def AddSingletonInstance(self, TService, instance) -> None:
        self.AddDescriptor(ServiceDescriptor(
            TService, ServiceType.Singleton, lambda: instance, [], type(instance)))

    def AddScoped(self, TService, dependencies: Optional[Iterable] = None, factory: Optional[Callable] = None,
                  TActual=None) -> None:
        self.AddDescriptor(ServiceDescriptor(
            TService, ServiceType.Scoped, factory, dependencies, TActual))


class ServiceInstantiationFailure(Exception):

    def __init__(self, TService, provider: Optional[ServiceProvider], desc: ServiceDescriptor = None):
        self.TService = TService
        self._Service = desc
        self._Provider = provider
