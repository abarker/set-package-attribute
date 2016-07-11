# -*- coding: utf-8 -*-
"""

This test is for name shadowing, where the module name is the same as the package
name.  This is why the package must be (temporarily) placed at the beginning of
`sys.path`, not at the second position.  When run as a script the module's directory
is always the first thing on `sys.path`.  If it happens to have the same name as the
package (which is common) it will shadow the package name when the attempt is made
to import the package submodule unless it is first on the list.

"""

from __future__ import print_function, division, absolute_import
if __name__ == "__main__":
    import set_package_attribute
    set_package_attribute.init()

import shadow_package.dummy_module

