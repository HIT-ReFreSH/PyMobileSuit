from typing import TypeVar, Generic, Optional, Callable, get_args


T = TypeVar('T')

class OneGeneric(Generic[T]):
    """ A generic type with one argument"""
    pass
    # @property
    # def T(self) -> object:
    #     return get_args(self.__orig_class__)[0] 