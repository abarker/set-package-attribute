# -*- coding: utf-8 -*-
"""

"""

from __future__ import print_function, division, absolute_import
import sys
import toplevel # The package being tested, imported as a package.

"""
# Import from top level.

from toplevel import toplevel_module
assert toplevel_module.value

# Import from subdir level.

from toplevel.subdir import subdir_module
import toplevel.subdir.subdir_module
assert subdir_module.value
"""
# Import from subsubdir level.

import toplevel.subdir.subsubdir.subsubdir_module
from toplevel.subdir.subsubdir import subsubdir_module
assert subsubdir_module.value

from toplevel.subdir.subsubdir import test_in_subsubdir
import toplevel.subdir.subsubdir.test_in_subsubdir

print("The __package__ is", __package__)

