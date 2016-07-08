# -*- coding: utf-8 -*-
"""

Test set_package_attribute.

"""

from __future__ import print_function, division, absolute_import, unicode_literals
import sys
if __name__ == "__main__": import set_package_attribute
# Deleting all refs to the current dir is sys.path does *not* fix below....
#del sys.path[1]
#del sys.path[3]
#del sys.path[2]
print("\nThe sys.path is", sys.path, "\n")
print("\nThe __package__ in 'test_in_subsubdir.py' module is", __package__, "\n")
print("\nModules")
#for m in sys.modules:
#    print("  ", m)
#print("\nmodule toplevel.subdir.subsubdir.subsubdir_module:")
#print("   ", sys.modules["toplevel.subdir.subsubdir.subsubdir_module"])

# Import from top level.

from toplevel import toplevel_module
from ... import toplevel_module
assert toplevel_module.value

# Import from subdir level (parent).

from toplevel.subdir import subdir_module
import toplevel.subdir.subdir_module
assert subdir_module.value

# Import from sibling dir.

from ..subsubdir_sibling import subsubdir_sibling_module
from toplevel.subdir.subsubdir_sibling import subsubdir_sibling_module
assert subsubdir_sibling_module.value

# Import from current dir (subsubdir).

import toplevel.subdir.subsubdir.subsubdir_module
from toplevel.subdir.subsubdir import subsubdir_module
from . import subsubdir_module
from ..subsubdir import subsubdir_module
from .subsubdir_module import value # Import module attribute.
# Below line works but causes double import of module with above.  The
# script dir is placed on sys.path, where it is found and re-imported.
#from subsubdir_module import value
assert subsubdir_module.value
assert value

