#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""

A setuptools-based setup module (not distutils).

See:
   https://packaging.python.org/en/latest/distributing.html

Docs on the setup function kwargs:
   https://packaging.python.org/distributing/#setup-args

"""

from __future__ import absolute_import, print_function
import glob
import os.path
from setuptools import setup, find_packages
import codecs # Use a consistent encoding.

# Get the long description from the README.rst file.
current_dir = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(current_dir, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="set-package-attribute",
    version="0.2.5", # major version, minor version, patch (see PEP440)
    description="Automatically set the __package__ attribute of a script.",
    keywords=["module", "package", "import", "relative import", "script"],
    install_requires=["wheel"],
    url="https://github.com/abarker/set-package-attribute",

    license="MIT",
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # Development Status: Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # uncomment if you test on these interpreters:
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: Stackless",
        "Topic :: Utilities",
    ],

    # Settings usually the same.
    author="Allen Barker",
    author_email="Allen.L.Barker@gmail.com",
    include_package_data=True,
    zip_safe=False,

    # Automated stuff below
    long_description=long_description,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[os.path.splitext(os.path.basename(path))[0]
                for path in glob.glob("src/*.py")],

)

