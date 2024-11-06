"""
Includes some Language Sugar from C#
"""

from collections.abc import Iterable
from typing import Any, Callable


def nameof(obj: Any) -> str:
    """
    Gets the name of the object.

    Args:
        obj (Any): The object whose name needs to be obtained.

    Returns:
        str: The name of the object.
    """
    return obj.__name__.split('.')[-1] if hasattr(obj, "__name__") else obj.name


def ExtensionMethod(T):
    """
    Marks a method as an extension method of certain type <T>.

    Example usage:
    ```python
    @ExtensionMethod(Iterable)
    def where(self, predicate):
        return (item for item in self if predicate(item))
    ```
    Args:
        T: The type of the extension method.

    Returns:
        callable: The decorator function.
    """

    def decorator(func):
        setattr(T, func.__name__, func)
        return func

    return decorator


def NullCollapse(obj, default):
    """
    Collapses None to a default value.

    Args:
        obj: The object to collapse.
        default: The default value to return if obj is None.

    Returns:
        Any: The collapsed object.
    """
    return default if obj is None else obj


INT_MAX = 2147483647
