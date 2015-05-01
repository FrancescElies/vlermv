Using Vlermv Cache
-------------------
A function receives input, does something, and then returns output.
If you decorate a function with Vlermv Cache, it caches the output;
if you call the function again with the same input, it loads the
output from the cache instead of doing what it would normally do.

The simplest usage is to decorate the function with ``@vlermv.cache()``.
For example, ::

    @vlermv.cache()
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

Now you can call ``is_prime`` as if it's a normal function, and
if you call it twice, the second call will load from the cache.

Some fancier uses are discussed below.

Non-default directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you pass no arguments to cache, as in the example above,
the cache will be stored in a directory named after the function.
To set a different directory, pass it as an argument. ::

    @vlermv.cache('~/.primes')
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

I recommend storing your caches in dotted directories under your
home directory, as you see above.

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The kwargs get passed to ``vlermv.Vlermv``, so you
can do fun things like changing the serialization function. ::

    @vlermv.cache('~/.http', serializer = vlermv.serializers.identity)
    def get(url):
        return requests.get(url).text

Read more about the keyword arguments in the Vlermv section above.

Non-identifying arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to pass an argument but not use it as an identifier,
pass a non-keyword argument; those get passed along to the function
but don't form the identifier. For example, ::

    @vlermv.cache('~/.http')
    def get(url, auth = None):
        return requests.get(url, auth = auth)

    get('http://this.website.com', auth = ('username', 'password')

Refreshing the cache
~~~~~~~~~~~~~~~~~~~~~~~~~~
I find that I sometimes want to refresh the cache for a particular
file, only. This is usually because an error occurred and I have fixed
the error. You can delete the cache like this. ::

    @vlermv.cache()
    def is_prime(number):
        for n in range(2, number):
            if number % n == 0:
                return False
        return True

    is_prime(100)
    del(is_prime[100])

Vlermv Cache has all of Vlermv's features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The above method for refreshing the cache works because ``is_prime``
isn't really a function; it's actually a ``VlermvCache`` object, which
is a sub-class of ``Vlermv``. Thus, you can use it in all of the ways
that you can use ``Vlermv``. ::

    @vlermv.cache()
    def f(x, y):
        return x + y

    print(f(3,4))
    # 7

    print(list(f.keys()))
    # ['3/4']

You can even set the value to be something weird. ::

    f[('a', 8)] = None, {'key':'value'}
    print(f('a', 8))
    # 0

Each value in ``f`` is a tuple of the error and the actual value.
Exactly one of these is always ``None``. If the error is None, the
value is returned, and if the value is None, the error is raised.
