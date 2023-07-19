def nameof(obj):
    return obj.__name__ if hasattr(obj, "__name__") else obj.name


def null_collapse(obj, default):
    return default if obj is None else obj




def linq_first_or_default(l, f):
    for x in l:
        if f(x):
            return x
    return None


INT_MAX = 2147483647
