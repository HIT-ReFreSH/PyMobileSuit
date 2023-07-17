from typing import TypeVar, Generic, Optional, Callable, get_args
from PyMobileSuit.ObjectModel import OneGeneric

T = TypeVar('T')


class SuitParser(Generic[T]):
    """ A data parser of MobileSuit"""

    def __init__(self, name: str, parser: Callable[[str], Optional[T]]):
        self.Name = name
        """Name of the Parser"""
        self.Parser = parser
        """The parser which convert string argument to certain type."""

    def __call__(self, x: str) -> object:
        return self.Parser(x)

    def TargetType(self) -> object:
        return get_args(self.__orig_class__)[0]

    @classmethod
    def FromConverter(cls,_T, converter: Callable[[str], Optional[T]], name=''):
        """
        Create a mobile suit parser from a converter

        :param converter: The converter method
        :param name: Name of the parser, if set empty, the parser will be default.
        """

        return cls[_T](name, converter)

    @classmethod
    def FromName(cls,T, name):
        """
        Create a mobile suit parser from a func and given type

        :type T: The type of target

        :param name: Name of the parser, if set empty, the parser will be default.
        """
        if hasattr(T, 'Parse'):
            return cls[T](name, T.Parse)

        return cls[T](name, lambda x: T(x))


class SuitParserProvider(dict[str, SuitParser]):
    def __init__(self):
        pass
