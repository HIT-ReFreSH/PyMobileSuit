from collections.abc import Iterable, Callable

def FirstOrDefault(enumerable: Iterable, func: Callable):
    return next((x for x in enumerable if func(x)), None)