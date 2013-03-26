#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# simple_cache
#
# Copyright (C) 2013 barisumog at gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import pickle
import time
from functools import wraps


#
# Implements a simple caching utility via pickling to disk
#


def write_cache(filename, cache):
    """Write the cache dictionary to disk."""
    with open(filename, "w+b") as file:
        pickle.dump(cache, file)


def read_cache(filename):
    """Read a cache dictionary from disk."""
    try:
        with open(filename, "r+b") as file:
            cache = pickle.load(file)
    except FileNotFoundError:
        cache = {}
    return cache


def save_key(filename, key, value, ttl):
    """Write a key:value pair to cache."""
    # ttl is "time to live" of the item in seconds
    cache = read_cache(filename)
    expiry = int(time.time() + ttl)
    cache[key] = (expiry, value)
    write_cache(filename, cache)


def load_key(filename, key):
    """Read the value for given key from cache."""
    cache = read_cache(filename)
    try:
        expiry, value = cache[key]
    except KeyError:
        return None
    if time.time() > expiry:
        # Expired key, delete it
        del cache[key]
        write_cache(filename, cache)
        return None
    return value


def prune_cache(filename):
    """Go through the file and delete any expired items."""
    cache = read_cache(filename)
    now = time.time()
    for key in list(cache.keys()):
    # Creating a list because we're modifying cache
        expiry, __ = cache[key]
        if now > expiry:
            del cache[key]
    write_cache(filename, cache)
