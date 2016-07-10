# -*- coding: utf-8 -*-
"""

Test importing code as a package.  The code is part of a package and some of
the modules import set_package_attribute so that they can also be run as
scripts.  This test is to make sure they still import OK as package modules.

"""

from __future__ import print_function, division, absolute_import
import sys

import toplevel # The package being tested, imported as a package.

# Import from top level.

from toplevel import toplevel_module as toplevel_imp_1
assert toplevel_imp_1.value

from toplevel import test_at_toplevel # Import does within-package imports.

# Import from subdir level.

from toplevel.subdir import subdir_module as subdir_imp_1
import toplevel.subdir.subdir_module as subdir_imp_2
assert subdir_imp_1.value
assert subdir_imp_1 is subdir_imp_2

from toplevel.subdir import test_in_subdir # Import does within-package imports.

# Import from subsubdir level.

import toplevel.subdir.subsubdir.subsubdir_module
from toplevel.subdir.subsubdir import subsubdir_module
assert subsubdir_module.value
assert toplevel.subdir.subsubdir.subsubdir_module.value

from toplevel.subdir.subsubdir import test_in_subsubdir # Does within-package imports.
import toplevel.subdir.subsubdir.test_in_subsubdir
assert  toplevel.subdir.subsubdir.test_in_subsubdir is test_in_subsubdir

