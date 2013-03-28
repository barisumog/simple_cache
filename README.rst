
============
simple_cache
============

A simple caching utility in Python 3.

**simple_cache** uses the ``pickle`` module to write any
``key : value`` pairs to a file on disk.

It was written as an easy way to cache http requests for
local use. It can possibly be used for caching any data,
as long as the ``key`` s are hashable and the ``value`` s are
pickleable.

It also provides a decorator to cache function calls directly.


Requirements
------------

Only standard libraries are used, so there are no dependencies.


Installing
----------

::

    pip install simple_cache


Or if you like, you can just download the ``simple_cache.py`` file and
import it locally.


Usage
-----

Each cache file contains a single dictionary, acting as the namespace
for that cache. Within the file, you can set and retrieve any ``key : value``
pairs as needed.

When setting a key, you must give a ``ttl`` value, or time to live, in seconds.
This value determines the amount of time that value will be considered valid.
After that, the value is considered expired, and will not be returned.

Calls to a non-existent cache file, a non-existent key, or an expired key
all  return ``None``.

You can set a key with a new value before or after it expires.

Whenever you ask the cache for a value, and it happens to be expired, the item
is deleted from the file. You can also manually ask the cache file at any time,
to prune all currently expired items.


API
---

::

    import simple_cache

**Using the decorator format:**

Using the same cache file for multiple functions with a decorator might
cause problems. The decorator uses the *args, **kwargs of the function as a key,
so calling to different functions with the same arguments will cause a clash.

You can specify a custom filename (and ttl) with the decorator format, overriding
the default values.

*Please note that the decorator format only supports args and kwargs with* **immutable** *types.
If one of your arguments is mutable (e.g. a list, or a dictionary), the decorator won't work.*

::

    @simple_cache.cache_it()    # uses defaults: filename = "simple.cache", ttl = 3600
    def some_function(*args, **kwargs):
        # body
        return value

::

    @simple_cache.cache_it(filename="some_function.cache", ttl=120)
    def some_function(*args, **kwargs):
        # body
        return value


**Using the module functions:**

Setting a key and value:

::

    simple_cache.save_key(filename, key, value, ttl)

Retrieving a value:

::

    simple_cache.load_key(filename, key)

Pruning all expired items in a file:

::

    simple_cache.prune_cache(filename)

Loading the whole cache dictionary from a file (possibly
for debugging or introspection):

::

    simple_cache.read_cache(filename)

Writing a whole dictionary to a file, **overwriting any
previous data in the file** (possibly for initalizing a 
cache by batch writing multiple items):

::

    simple_cache.write_cache(filename, cache)


``filename`` is a string containing a valid filename

``key`` is any hashable type, and must be unique within
each cache file (otherwise will overwrite)

``value`` is any Python type supported by the ``pickle`` module

``ttl`` is an integer or float, denoting the number of seconds
that the item will remain valid before it expires

``cache`` is a dictionary containing the key:value pairs


License
-------

**simple_cache** is open sourced under GPLv3.
