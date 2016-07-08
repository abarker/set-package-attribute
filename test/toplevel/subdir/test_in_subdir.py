# -*- coding: utf-8 -*-
"""

Test set_package_attribute, from the subdir level.

"""

from __future__ import print_function, division, absolute_import
if __name__ == "__main__":
    import set_package_attribute
    set_package_attribute.init()

# Import from top level.

from toplevel import toplevel_module as top_imp_1
from .. import toplevel_module as top_imp_2
assert top_imp_1 is top_imp_2
assert top_imp_1.value is top_imp_2.value

# Import from subdir level (this level).

import toplevel.subdir.subdir_module as subdir_imp_1
from toplevel.subdir import subdir_module as subdir_imp_2
from . import subdir_module as subdir_imp_3
assert subdir_imp_1 is subdir_imp_2 is subdir_imp_3

from .subdir_module import value
assert subdir_imp_1.value is value

# Import from child at subsubdir level.

import toplevel.subdir.subsubdir.subsubdir_module as subsubdir_imp_1
from toplevel.subdir.subsubdir import subsubdir_module as subsubdir_imp_2
from .subsubdir import subsubdir_module as subsubdir_imp_3
assert subsubdir_imp_1 is subsubdir_imp_2 is subsubdir_imp_3

from .subsubdir.subsubdir_module import value
assert subsubdir_imp_1.value is value

# When run as a script, make sure the package-qualified name is the same
# module as __main__.
if __name__ == "__main__":
    import sys
    assert sys.modules["__main__"] is sys.modules["toplevel.subdir.test_in_subdir"]

    import toplevel.subdir.test_in_subdir # Recursive import, just to test.
    assert sys.modules["__main__"] is sys.modules["toplevel.subdir.test_in_subdir"]

