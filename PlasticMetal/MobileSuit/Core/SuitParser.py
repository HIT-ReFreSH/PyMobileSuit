from typing import TypeVar, Generic, Optional, Callable, get_args, Type

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

    @property
    def TargetType(self) -> Type:
        return get_args(self.__orig_class__)[0]

    @classmethod
    def FromConverter(cls, _T, converter: Callable[[str], Optional[T]], name=''):
        """
        Create a mobile suit parser from a converter

        :param _T:
        :param converter: The converter method
        :param name: Name of the parser, if set empty, the parser will be default.
        """

        return cls[_T](name, converter)

    @classmethod
    def FromName(cls, _T, name):
        """
        Create a mobile suit parser from a func and given type

        :type _T: The type of target

        :param name: Name of the parser, if set empty, the parser will be default.
        """
        if hasattr(_T, 'Parse'):
            return cls[_T](name, _T.Parse)

        return cls[_T](name, lambda x: _T(x))
