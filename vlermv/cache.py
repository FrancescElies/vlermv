from functools import partial

from .vlermv import Vlermv

def cache(*args, **kwargs):
    '''
    Cache a function with a vlermv.Vlermv.

    Decorate the function with @cache(*args, **kwargs).
    The args and kwargs get passed to the Vlermv.
    For example::

        @cache('~/.http')
        def get(url):
            return requests.get(url, auth = ('username', 'password'))

    vlermv.Vlermv would ordinarily fail if no arguments were passed to it.
    If you pass no arguments to cache, the Vlermv directory argument
    (the one required argument) will be set to the name of the function.
    '''
    def decorator(func):
        if len(args) == 0:
            _args = (func.__name__,)
        else:
            _args = args
        v = Vlermv(*_args, **kwargs)
        v.func = func
        return v
    return decorator
