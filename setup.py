#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='media_utils',
      version='0.2.0',
      description='Python media utilities such as metadata',
      url='http://github.com/asundaresan/media_utils',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=['media_utils'],
      scripts=[
        "bin/get_metadata.py",
        "bin/set_datetime.py",
        ],
      zip_safe=False,
      install_requires = [
          "PyYAML"
        ]
      )

