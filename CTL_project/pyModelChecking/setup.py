#!/usr/bin/env python

from setuptools import setup, find_packages
from pyModelChecking import __version__

with open('README.md') as f:
    long_desc = f.read()

setup(name='pyModelChecking',
      version=__version__,
      description='A simple Python model checking package',
      long_description=long_desc,
      long_description_content_type='text/markdown', 
      packages=find_packages(),
      install_requires=[
          'lark-parser',
      ],
      python_requires='>=3.6',
     )
