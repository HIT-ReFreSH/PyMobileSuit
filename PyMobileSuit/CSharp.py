def nameof(any):
    return any.__name__ if hasattr(any, "__name__") else any.name


def null_collapse(any, default):
    return default if any is None else any


def linq_select(list, f):
    return [f(x) for x in list]


def linq_first_or_default(list, f):
    for x in list:
        if f(x):
            return x
    return None


INT_MAX = 2147483647
