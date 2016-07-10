# -*- coding: utf-8 -*-
"""
Test the import of `set_package_attribute` when not inside a package.
"""

from __future__ import print_function, division, absolute_import

import set_package_attribute
set_package_attribute.init()

assert __package__ is None

