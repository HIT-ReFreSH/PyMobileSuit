from enum import Enum
from typing import List, Optional
class ServiceType(Enum):
    Singleton = 1
    Transient = 2
class ServiceDescriptor:
    def __init__(self, service_type: ServiceType, factory, dependencies: List[type]):
        self.service_type = service_type
        self.factory = factory
        self.dependencies = dependencies
    def CreateInstance(self, provider) -> object:
        args = []
        for dep in self.dependencies:
            args.append(provider.getRequiredService(dep))
        return self.factory(*args)
class ServiceBag:
    def __init__(self):
        self.descriptors: List[ServiceDescriptor] = []
    def addDescriptor(self, descriptor: ServiceDescriptor):
        self.descriptors.append(descriptor)
    def build(self) -> 'ServiceProvider':
        return ServiceProvider(self)
class ServiceNotFound(Exception):
    pass
class ServiceProvider:
    def __init__(self, service_bag: ServiceBag):
        self.service_bag = service_bag
        self.services = {}
        for descriptor in service_bag.descriptors:
            if descriptor.service_type == ServiceType.Singleton:
                instance = descriptor.CreateInstance(self)
                self.services[descriptor.factory] = instance
    def getRequiredService(self, service_type) -> object:
        for descriptor in self.service_bag.descriptors:
            if descriptor.factory == service_type:
                if descriptor.service_type == ServiceType.Singleton:
                    if descriptor.factory not in self.services:
                        instance = descriptor.CreateInstance(self)
                        self.services[descriptor.factory] = instance
                    return self.services[descriptor.factory]
                else:
                    return descriptor.CreateInstance(self)
        raise ServiceNotFound()
    def createScope(self) -> 'ScopedServiceProvider':
        return ScopedServiceProvider(self)
class ScopedServiceProvider:
    def __init__(self, parent_provider: ServiceProvider):
        self.parent_provider = parent_provider
        self.scoped_services = {}
    def getRequiredService(self, service_type) -> object:
        try:
            return self.scoped_services[service_type]
        except KeyError:
            service = self.parent_provider.getRequiredService(service_type)
            self.scoped_services[service_type] = service
            return service