from typing import Callable, Dict, Type, TypeVar
from json import loads as deserialize
from abc import ABC, abstractmethod
from ..SuitParser import SuitParser

T = TypeVar('T')


class IParsingService(ABC):
    """
    Get parsers for certain type.
    """
    @abstractmethod
    def Get(self, type: Type, name: str = "") -> Callable[[str], object]:
        """
        Get a parser for certain type with certain name.

        :param type: certain type
        :param name: certain name
        :return:
        """
        raise NotImplementedError
    @abstractmethod
    def Add(self, _T, converter: Callable[[str], T], name: str = "") -> None:
        """
        Add a parser with certain name to parsing service.

        :param _T:
        :param converter:
        :param name:
        """
        raise NotImplementedError
    @abstractmethod
    def AddParser(self, parser: SuitParser[T]) -> None:
        """
        Add a parser.

        :param parser:
        """
        raise NotImplementedError
    @abstractmethod
    def AddName(self, _T:Type, name: str = "") -> None:
        """
        Add a parser.

        :param _T:
        :param name:
        """
        raise NotImplementedError


class ParsingService(IParsingService):
    def __init__(self):
        self._parsers: Dict[Type, Dict[str, Callable[[str], object]]] = {}
        self.AddName(int)
        self.AddName(float)
        self.AddName(bool)
        
    def Add(self, _T: Type, converter: Callable[[str], T], name: str = "") -> None:
        self.AddParser(SuitParser.FromConverter(_T, converter, name))

    def AddParser(self, parser: SuitParser[T]) -> None:
        if not parser.TargetType in self._parsers:
            self._parsers[parser.TargetType] = {}

        if parser.Name in self._parsers[parser.TargetType]:
            del self._parsers[parser.TargetType][parser.Name]

        self._parsers[parser.TargetType][parser.Name] = parser.Parser

    def AddName(self, _T: Type, name: str = "") -> None:
        self.AddParser(SuitParser.FromName(_T, name))

    def Get(self, type: Type, name: str = "") -> Callable[[str], object]:
        if type in self._parsers and name in self._parsers[type]:
            return self._parsers[type][name]

        return lambda s: deserialize(s,type)
