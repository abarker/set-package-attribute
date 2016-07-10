# -*- coding: utf-8 -*-
"""

Test set_package_attribute, from the subsubdir level.

"""

from __future__ import print_function, division, absolute_import
if __name__ == "__main__":
    import set_package_attribute
    set_package_attribute.init(mod_path=True)

# Import from top level.

from toplevel import toplevel_module as top_imp_1
from ... import toplevel_module as top_imp_2
assert top_imp_1 is top_imp_2
assert top_imp_1.value is top_imp_2.value

# Import from subdir level (parent).

import toplevel.subdir.subdir_module as subdir_imp_1
from toplevel.subdir import subdir_module as subdir_imp_2
assert subdir_imp_1 is subdir_imp_2

# Import from sibling dir.

import toplevel.subdir.subsubdir_sibling.subsubdir_sibling_module as sibling_imp_1
from toplevel.subdir.subsubdir_sibling import subsubdir_sibling_module as sibling_imp_2
from ..subsubdir_sibling import subsubdir_sibling_module as sibling_imp_3
assert sibling_imp_1 is sibling_imp_2 is sibling_imp_3

from ..subsubdir_sibling.subsubdir_sibling_module import value
assert value is sibling_imp_1.value

# Import from current dir (subsubdir).

import toplevel.subdir.subsubdir.subsubdir_module as subsubdir_imp_1
from toplevel.subdir.subsubdir import subsubdir_module as subsubdir_imp_2
from . import subsubdir_module as subsubdir_imp_3
from ..subsubdir import subsubdir_module as subsubdir_imp_4
assert subsubdir_imp_1 is subsubdir_imp_2 is subsubdir_imp_3 is subsubdir_imp_4

from .subsubdir_module import value
assert subsubdir_imp_1.value is value

# Below line works as a script but causes double import of module with above.
# The script's dir is placed on sys.path, where it is found and re-imported
# with a different name.  The import FAILS when this module is imported as a
# regular package in Python 3, though, because it is not on sys.path and no
# implicit relative imports are allowed.
try:
    from subsubdir_module import value
except ImportError:
    # As ordinary package, fail since absolue_import is used (from future for Py2).
    # When run as script, fail since mod_path=True will remove the script's dir.
    assert True
else:
    assert not "Import still worked after removing sys.path[0], is dir on path elsewhere?"

# When run as a script, make sure the package-qualified name is the same
# module as __main__.
if __name__ == "__main__":
    import sys
    assert sys.modules["__main__"] is sys.modules[
            "toplevel.subdir.subsubdir.test_in_subsubdir"]

    import toplevel.test_at_toplevel # Recursive import, just to test.
    assert sys.modules["__main__"] is sys.modules[
            "toplevel.subdir.subsubdir.test_in_subsubdir"]

