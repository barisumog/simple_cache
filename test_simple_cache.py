#
# Tests for simple_cache
# To be used with py.test
#
# NOTE :
# Running the tests will create a file in the current
# directory named "testing.cache"
#


import simple_cache


def test_write_read():
    filename = "testing.cache"
    original = {"answer": (3, 42)}
    simple_cache.write_cache(filename, original)
    returned = simple_cache.read_cache(filename)
    assert returned == original


def test_file_not_found_error():
    filename = "some_non-existent_cache_file.cache"
    cache = simple_cache.read_cache(filename)
    assert cache == {}


def test_save_load_key():
    filename = "testing.cache"
    key = "answer"
    value = 42
    ttl = 3
    simple_cache.save_key(filename, key, value, ttl)
    returned = simple_cache.load_key(filename, key)
    assert returned == value


def test_absent_key():
    filename = "testing.cache"
    key = "this key does not exist"
    returned = simple_cache.load_key(filename, key)
    assert returned is None


def test_expiry():
    filename = "testing.cache"
    key = "answer"
    value = 42
    ttl = 1
    simple_cache.save_key(filename, key, value, ttl)
    simple_cache.time.sleep(3)
    returned = simple_cache.load_key(filename, key)
    assert returned is None


def test_prune():
    filename = "testing.cache"
    key = "answer"
    value = 42
    ttl = 1
    simple_cache.save_key(filename, key, value, ttl)
    simple_cache.time.sleep(3)
    simple_cache.prune_cache(filename)
    cache = simple_cache.read_cache(filename)
    assert cache == {}


def test_tuple_kwargs():
    d1 = {"a": 1, "b": 2, "c": "3"}
    d2 = {"b": 2, "c": "3", "a": 1}
    assert simple_cache.tuple_kwargs(d1) == simple_cache.tuple_kwargs(d2)


def test_decorator():
    @simple_cache.cache_it(filename="testing.cache", ttl=10)
    def adder(a, b=1, c=1):
        simple_cache.time.sleep(3)
        return a + b + c
    x = adder(3, b=5, c=2)
    t0 = simple_cache.time.time()
    y = adder(3, c=2, b=5)
    t1 = simple_cache.time.time()
    assert t1 - t0 < 2
