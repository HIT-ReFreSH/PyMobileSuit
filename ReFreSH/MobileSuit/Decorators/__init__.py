from . import DecoratorNames
from ..Decorators.SuitArgParser import *


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
            setattr(func, DecoratorNames.suit_alias, [])
        getattr(func, DecoratorNames.suit_alias).append(alias)
        return func

    return decorator


def SuitInfo(expr: str, resObj=None):
    """
    Stores the information of a member to be displayed.

    :param resObj: Resource class
    :param expr: The information.
    """

    def decorator(func):
        setattr(func, DecoratorNames.suit_info, (expr, resObj))
        return func

    return decorator


def SuitArgInjected(arg_name: str):
    """
    Indicate that Mobile Suit should Inject to this argument.

    :param arg_name: The name of the argument to inject.
    """

    def decorator(func):
        if not hasattr(func, DecoratorNames.suit_injected):
            setattr(func, DecoratorNames.suit_injected, [])
        getattr(func, DecoratorNames.suit_injected).append(arg_name)
        return func

    return decorator


__all__ = [nameof(x) for x in [SuitAlias, SuitIgnore, SuitInfo, SuitArgParser, SuitArgInjected]]
