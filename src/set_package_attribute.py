# -*- coding: utf-8 -*-
"""

Description
-----------

In order to run a module inside a package as a script and have explicit
relative imports work, the `__package__` attribute of the module should be set.
Importing this module sets the `__package__` attribute of the module
`__main__`.  This module is intended to be imported by modules which might be
run as a script inside a package which uses explicit relative imports.

To use the module, just import it before any of the non-system files, inside
any module that you want to possibly run as a script.  Nothing else is
required.  This module needs to be imported *before* any explicit relative
imports, or any modules which use such imports.  Any previously-set
`__package__` attributes (other than `None`) will be left unchanged.

Note that this module also needs to import the package directory containing the
script.  A side-effect of this is that any `__init__.py` files in the package
path down to the script (from the top package level) will be executed.  This
could give unexpected results, depending on how `__init__.py` files are used in
a given package.  The effect is essentially the same as if the script file had
been imported from another module using its fully-qualified module name.

As far as efficiency, only the first import of the module does any real work,
when it is initialized.  The module initialization only performs relatively
trivial computations.

Further details
---------------

On initial import this module searches for the module `__main__` in
`sys.modules`.  If that module is not found then the current runtime was not
started from a script and nothing is done.  If module `__main__` is found then
the current runtime was started from a script.  In that case the `__package__`
attribute for the `__main__` module is computed and set in the `__main__`
module's namespace.  Only the `__main__` module is ever modified.  If there is
already a `__package__` attribute in the namespace of `__main__` then nothing
is done.  The containing the `__main__` module is found by going up the
directory tree, from its source file.

After setting the `__package__` attribute in the `__main__` module the package
directory containing the `__main__` module is then imported, using its
fully-qualified package name.  The `__main__` module is also added to
`sys.modules` under its full package name.

.. seealso:: 

    This module is based on the basic method described in the answers on this
    StackOverflow page: http://stackoverflow.com/questions/2943847/

.. note::

    An alternative approach would be to always execute scripts inside packages
    with the `-m` flag set.  For example, to execute a script `module_name.py`,
    which is in a subdirectory inside a package `pkg_toplevel`, you would use:

    .. code:: bash

       python -m pkg_toplevel.pkg_subdir.module_name
       
    This requires the full package name to be used, however, and has a
    different invocation method than other scripts.  Also, the directory
    containing the top-level package directory `pkg_toplevel` (i.e., its parent
    directory) needs to be in Python's package search path in order for this
    approach to work.

.. note::

    As of 2007 Guido van Rossum viewed running scripts that are inside packages
    as an anti-pattern (see
    https://mail.python.org/pipermail/python-3000/2007-April/006793.html).
    Nevertheless, it can be a convenient and useful pattern in certain
    situations.  He did later approve PEP 366, which defined the `__package__`
    attribute to handle the situation.

..  Copyright (c) 2015 by Allen Barker.
    License: MIT, see LICENSE for more details.

.. default-role:: code

Main function (called on import)
--------------------------------
"""

from __future__ import print_function, division, absolute_import
import os
import sys

def set_package_attribute():
    """Set the `__package__` attribute of the module `__main__` if it is not
    already set."""
    # Get the module named __main__ from sys.modules.
    main_found = True
    try:
        main_module = sys.modules["__main__"]
        print("__main__ found!!!!!!!!!!!!")
    except KeyError:
        main_found = False
        print("no __main__ found!!!!!!!!!!!!")

    # Do nothing unless the program was started from a script.
    if main_found and main_module.__package__ is None:

        importing_file = main_module.__file__
        print("importing file is", importing_file)
        dirname, filename = os.path.split(
                               os.path.realpath(os.path.abspath(importing_file)))
        filename = os.path.splitext(filename)[0]
        print("dirname and filename are", dirname, filename)
        parent_dirs = [] # A reverse list of package name parts to build up.

        # Go up the dirname tree to find the top-level package dirname.
        while os.path.exists(os.path.join(dirname, "__init__.py")):
            dirname, name = os.path.split(dirname) 
            parent_dirs.append(name)

        if parent_dirs: # Do nothing if no __init__.py file was found.

            # Get the package name and set the __package__ variable.
            # Note: the package name does not include the name of the module itself.
            full_package_name = ".".join(reversed(parent_dirs))
            main_module.__package__ = full_package_name

            # Now do the actual import of the full package.
            print("\nfull_package_name is", full_package_name)
            # The script module is run *twice* if below line is uncommented!
            #full_package_name += "." + filename # LEAVE COMMENTED OUT
            try:
                package_module = __import__(full_package_name)
            except ImportError:
                # Failure; insert dirname in sys.path, then try the import again.
                sys.path.insert(1, dirname) # Use 1 instead of 0; 0 is script's dir.
                package_module = __import__(full_package_name)
                del sys.path[1] # Remove the added path; no longer needed.

            assert full_package_name in sys.modules # True
            # TODO: I added this part... seems like it sets the right alias to the module...
            full_package_name += "." + str(filename) # Add the filename part to the end.
            assert full_package_name not in sys.modules # True
            sys.modules[full_package_name] = main_module

            # Add the package's module to sys.modules.
            # TODO: commenting this out seems to fix problem with bottom-level import tests...
            #sys.modules[full_package_name] = package_module
            #print("set_package_attribute set sys.modules to have module", full_package_name)

set_package_attribute()

