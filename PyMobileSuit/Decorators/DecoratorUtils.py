import PyMobileSuit.Decorators.DecoratorNames as DecoratorNames
from typing import Callable, Optional


def get_alias(func: Callable):
    has_attr = hasattr(func, DecoratorNames.suit_alias)
    return func.____suit_alias if has_attr else []


def is_ignored(func: Callable):
    check_a = hasattr(func, DecoratorNames.suit_ignored)
    return check_a and func.____suit_ignored


def get_info(func: Callable) -> Optional[str]:
    return func.____suit_info if hasattr(func, DecoratorNames.suit_info) else None


def get_parser(func: Callable, arg_name: str) -> Optional[str]:
    dic = func.____suit_parser if hasattr(
        func, DecoratorNames.suit_parser) else {}
    return None if arg_name not in dic else dic[arg_name]


def get_injected(func: Callable, arg_name: str) -> bool:
    arr = func.____suit_injected if hasattr(
        func, DecoratorNames.suit_injected) else []
    return arg_name in arr
