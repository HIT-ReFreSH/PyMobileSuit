import PyMobileSuit.Decorators.DecoratorNames as DecoratorNames
from PyMobileSuit.CSharp import *
from PyMobileSuit.Decorators.SuitArgParser import *


def SuitIgnore(func):
    """Represents that this member should be ignored by Mobile Suit."""
    func.____suit_ignored = True
    return func


def SuitAlias(alias: str):
    """
    Alias for a SuitObject's member

    :param alias: Alias for a SuitObject's member
    """
    def decorator(func):
        if not hasattr(func, DecoratorNames.suit_alias):
            func.____suit_alias = []
        func.____suit_alias.append(alias)
        return func
    return decorator


def SuitInfo(expr: str):
    """
    Stores the information of a member to be displayed.

    :param expr: The information.
    """
    def decorator(func):
        func.____suit_info = expr
        return func
    return decorator


def SuitArgInjected(arg_name: str):
    """
    Indicate that Mobile Suit should Inject to this argument.

    :param arg_name: The name of the argument to inject.
    """
    def decorator(func):
        if not hasattr(func, DecoratorNames.suit_injected):
            func.__suit_injected = []
        func.____suit_injected.append(str)
        return func
    return decorator


__all__ = linq_select([SuitAlias, SuitIgnore, SuitInfo, SuitArgParser], nameof)
