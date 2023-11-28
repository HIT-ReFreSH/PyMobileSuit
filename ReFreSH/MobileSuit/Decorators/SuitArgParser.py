from typing import Generic, TypeVar, Callable, Optional

from ReFreSH.CSharp import nameof
from . import DecoratorNames

T = TypeVar('T')


class SuitArgParserInfo(Generic[T]):
    def __init__(self, parser_name: str = '', converter: Optional[Callable[[str], Optional[T]]] = None):
        self.Name = parser_name
        self.Converter = converter

    @classmethod
    def FromDecorator(cls, parser_name: str = '', TTarget=None, TConverter=None):
        if TTarget is None:
            return cls[object](parser_name, None)
        if TConverter is None:
            TConverter = TTarget
        if hasattr(TConverter, parser_name):
            return cls[TTarget](parser_name, getattr(TConverter, parser_name))
        parse_method_name = f'{parser_name}{nameof(TTarget)}'
        if hasattr(TConverter, parse_method_name):
            return cls[TTarget](parser_name, getattr(TConverter, parse_method_name))
        return cls[TTarget](parser_name, lambda x: TTarget(x))


def SuitArgParser(arg_name: str, parser_name: str = '', TTarget=None, TConverter=None):
    """
    Select the parser used for the certain argument
    """
    def decorator(func):
        if not hasattr(func, DecoratorNames.suit_alias):
            setattr(func, DecoratorNames.suit_alias,{})
        getattr(func, DecoratorNames.suit_alias)[arg_name] = SuitArgParserInfo.FromDecorator(
            parser_name, TTarget, TConverter)
        return func
    return decorator
