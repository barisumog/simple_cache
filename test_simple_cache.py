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
