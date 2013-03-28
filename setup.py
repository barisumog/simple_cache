#!/usr/bin/env python3


from distutils.core import setup
from os.path import join, dirname


with open(join(dirname(__file__), 'README.rst')) as file:
    long_description = file.read()

setup(name='simple_cache',
      version='0.35',
      description='A simple caching utility in Python 3',
      long_description=long_description,
      author='barisumog',
      author_email='barisumog@gmail.com',
      url='https://github.com/barisumog/simple_cache',
      py_modules=['simple_cache', 'test_simple_cache'],
      data_files=[('', ['README.rst'])],
      license="GPLv3"
     )
