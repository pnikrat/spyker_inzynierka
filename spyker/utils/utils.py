from collections import OrderedDict
import inspect
import os


def is_valid_path(path):
    try:
        open(path, 'w')
        os.unlink(path)
        return True
    except (IOError, OSError):
        return False


def is_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def get_kwargs(function):
    argspec = inspect.getargspec(function)
    kwarg_values = argspec.defaults
    kwarg_keys = argspec.args[-len(kwarg_values):]
    return OrderedDict(zip(kwarg_keys, kwarg_values))
