# -*- coding: utf-8 -*-
"""

Test set_package_attribute, at the top package level.

"""

from __future__ import print_function, division, absolute_import
if __name__ == "__main__":
    import set_package_attribute_magic

# Import from top level (this level).

import toplevel.toplevel_module as top_imp_1
from . import toplevel_module as top_imp_2
assert top_imp_1 is top_imp_2
assert top_imp_1.value is top_imp_2.value

# Import from child at subdir level.

import toplevel.subdir.subdir_module as subdir_imp_1
from toplevel.subdir import subdir_module as subdir_imp_2
from .subdir import subdir_module as subdir_imp_3
assert subdir_imp_1 is subdir_imp_2 is subdir_imp_3

from .subdir.subdir_module import value
assert subdir_imp_1.value is value

# Import from grandchild at subsubdir level.

import toplevel.subdir.subsubdir.subsubdir_module as subsubdir_imp_1
from toplevel.subdir.subsubdir import subsubdir_module as subsubdir_imp_2
from .subdir.subsubdir import subsubdir_module as subsubdir_imp_3
assert subsubdir_imp_1 is subsubdir_imp_2 is subsubdir_imp_3

from .subdir.subsubdir.subsubdir_module import value
assert subsubdir_imp_1.value is value

# When run as a script, make sure the package-qualified name is the same
# module as __main__.
if __name__ == "__main__":
    import sys
    assert sys.modules["__main__"] is sys.modules["toplevel.test_magic_import"]

    import toplevel.test_magic_import # Recursive import, just to test.
    assert sys.modules["__main__"] is sys.modules["toplevel.test_magic_import"]

