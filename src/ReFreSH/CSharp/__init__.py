def nameof(obj):
    return obj.__name__.split('.')[-1] if hasattr(obj, "__name__") else obj.name


def NullCollapse(obj, default):
    return default if obj is None else obj

INT_MAX = 2147483647