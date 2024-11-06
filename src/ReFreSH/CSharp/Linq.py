from collections.abc import Iterable, Callable

from .Sugar import ExtensionMethod


@ExtensionMethod(Iterable)
def FirstOrDefault(self, func: Callable or None = None):
    return next((x for x in self)) if func is None else next((x for x in self if func(x)), None)
