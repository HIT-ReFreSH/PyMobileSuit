import inspect
from abc import ABC, abstractmethod
from typing import Iterable, Callable, Optional, Any, List

from . import SuitBuildUtils
from ..Decorators import DecoratorUtils
from PlasticMetal.CSharp import nameof
from .SuitContext import SuitContext
from .SuitMethodShell import SuitMethodShell
from .SuitShell import SuitShell, MemberType
from ..RequestStatus import RequestStatus


class ISuitShellCollection(ABC):
    """A collection contains ordered suit shell members."""

    @abstractmethod
    def Members(self) -> Iterable[SuitShell]:
        """Ordered members of this"""
        pass


class SuitObjectShell(SuitShell, ISuitShellCollection):
    """Represents an object in Mobile Suit."""

    def __init__(self, typedef, factory: Callable[[SuitContext], Any], info, name):
        super().__init__(typedef, factory, name)
        self._instanceFactory = factory
        self._subSystems = []
        for (name, member) in inspect.getmembers(typedef):
            if name.startswith("__") or DecoratorUtils.is_ignored(member):
                continue
            if inspect.isfunction(member):
                self.AddMethod(member)
            elif isinstance(member, property):
                self.AddProperty(name, member)
        self._subSystems.sort(key=lambda x: (
            x.AbsoluteName.lower(), x.MemberCount))
        self._info = info

    @property
    def MemberCount(self):
        return len(self._subSystems)

    def Members(self):
        return self._subSystems.copy()

    @classmethod
    def FromInstanceProperty(cls, name, prop, instanceFactory) -> Optional:
        info = DecoratorUtils.get_info(prop.fget)
        sig = inspect.signature(prop.fget).return_annotation
        if sig == inspect.Parameter.empty:
            return None
        sh = cls(sig,
                 lambda c: getattr(instanceFactory(c), name),
                 info if info is not None else name,
                 name)
        sh.Type = MemberType.FieldWithInfo if info is not None else MemberType.FieldWithoutInfo
        if info is None:
            sh._info = SuitObjectShell.GetMemberInfo(sh)
        return sh

    @classmethod
    def FromInstance(cls, typedef, instanceFactory, name=""):
        info = DecoratorUtils.get_info(typedef)
        sh = cls(typedef,
                 instanceFactory,
                 info if info is not None else nameof(typedef),
                 name)
        sh.Type = MemberType.FieldWithInfo if info is not None else MemberType.FieldWithoutInfo
        if info is None:
            sh._info = SuitObjectShell.GetMemberInfo(sh)
        return sh

    @classmethod
    def FromType(cls, typedef, name=""):
        def InstanceFactory(s):
            return SuitBuildUtils.CreateInstance(typedef, s.ServiceProvider) or object()

        info = DecoratorUtils.get_info(typedef)
        return cls(typedef, InstanceFactory, info if info is not None else nameof(typedef), name)

    def AddMethod(self, method):
        self._subSystems.append(SuitMethodShell.FromInstance(
            method, self._instanceFactory))

    def AddProperty(self, name: str, prop: property):
        self._subSystems.append(self.FromInstanceProperty(
            name, prop, self._instanceFactory))

    async def Execute(self, context: SuitContext):
        origin = context.Request
        if self.AbsoluteName:
            context.Request = origin[1:]
        for sys in filter(lambda x: x.MayExecute(context.Request), self._subSystems):
            await sys.Execute(context)
            if context.RequestStatus != RequestStatus.NotHandled:
                return
        context.Request = origin

    def MayExecute(self, request: List[str]) -> bool:
        if not self.AbsoluteName:
            return len(request) > 0 and any(sys.MayExecute(request) for sys in self._subSystems)
        return len(request) > 1 and request[0].lower() in self.FriendlyNames and any(
            sys.MayExecute(request[1:]) for sys in self._subSystems)

    @staticmethod
    def GetMemberInfo(sh) -> str:
        infoSb = ''
        if sh.MemberCount > 0:
            i = 0
            for sys in sh.Members():
                infoSb += sys.AbsoluteName
                if isinstance(sys, SuitObjectShell):
                    infoSb += "()"
                elif isinstance(sys, SuitMethodShell):
                    infoSb += "{}"
                infoSb += ','
                i += 1
                if i <= 5:
                    continue
                infoSb += "...,"
                break

            return infoSb[:-1]

        return ""
