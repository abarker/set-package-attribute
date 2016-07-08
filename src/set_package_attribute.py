# -*- coding: utf-8 -*-
"""
.. default-role:: code

Description
-----------

In order to run a module inside a package as a script and have explicit
relative imports work, the `__package__` attribute of the module should be set.
Importing this module from a script sets the `__package__` attribute of the
module `__main__`.  This module is intended to be imported by modules which
might be run as scripts and which use explicit relative imports or need to
import other modules which do.

To use the module, just import it before any of the non-system files, inside
any module that you want to possibly run as a script.  The import should be
inside a guard conditional, to only run when the module is executed as a
script::

   if __name__ == "__main__": import set_package_attribute

Nothing else is required.  This module needs to be imported **before** any
explicit relative imports, and before importing any modules from the same
package which use such imports.  Any previously-set `__package__` attributes
(other than `None`) will be left unchanged.

.. note::

    Internally this module also needs to import the package directory
    containing the script module under its full package-qualified name.  A
    side-effect of this is that any `__init__.py` files in the package path
    down to the script (from the top package level) will be executed.  This
    could give unexpected results compared to running the script outside the
    package, depending on how `__init__.py` files are used in a given package.
    The effect is essentially the same as if the script file had been imported
    from another module using its full, package-qualified module name.

.. note::

    If the guard conditional `if` is left off the import it will still work.
    The problem would be when an external script, also in a package, explicitly
    or implicity imports module which imports `set_package_attribute`.  (That
    includes importing it as part of its full package.)  This would have the
    side-effect of setting the package attribute of the `__main__` module for
    the external script, which might result in unexpected behavior that could
    be difficult to trace.

Another use of this package is that it allows explicit relative imports to be
used for intra-package imports in the main module of a Python application
(i.e., in a Python application's entry-point script).  Usually, `as described
in the Python documentation
<https://docs.python.org/3/tutorial/modules.html#intra-package-references>`_,
these imports should always be absolute imports.  That is, without the
`__package__` attribute being set such modules should generally only import
intra-package modules by their full, package-qualified names).  The guard
conditional is not required in this case, assuming the application will always
be run from the entry point rather than imported.

Installation
------------

The simplest way to install is to use pip:

.. code:: bash

   pip install set-package-attribute

The package can also be installed by cloning it and running its `setup.py` file
in the usual way.  The GitHub URL is `https://github.com/abarker/pytest-helper
<https://github.com/abarker/set-package-attribute>`_.

The package currently consists of a single module, which can also simply be
copied to somewhere in the Python path (in order to avoid adding a dependency).

Further details
---------------

On initial import this module searches for the module `__main__` in
`sys.modules`.  If that module is not found then nothing is done.  If
`__main__` is found then the `__package__` attribute for the `__main__` module
is computed by going up its directory tree from its source file, looking for
`__init__.py` files.  The `__package__` attribute is then set in the `__main__`
module's namespace.  Only the `__main__` module is ever modified.  If there is
already a `__package__` attribute in the namespace of `__main__` then nothing
is done.

After setting the `__package__` attribute in the `__main__` module the package
directory containing the `__main__` module is then imported, using its
fully-qualified name.  An entry for the `__main__` module is also added to
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

Main function (called on import initialization)
------------------------------------------------
"""

# TODO: delete this comment below after reviewing.......
# TODO: we ONLY want to run if we are invoked *as* __main__, not any time when
# imported.  Maybe when package that imports imports, but better *not* to.
# Otherwise, we *always* set the package for __main__ any time thing is run as
# a script -- even when it is *normally* imported by a script which import the
# regular package.  So something outside the package of the file with the
# import is having its __package__ attribute set and its __init__ files run!
# Not good!  At WORST you could pass __name__ to the init function, and be
# required to init.  That would be easy.  Is there a way to keep the regular
# import thing?
#
# Summary: we don't want modify __main__, with the side effects of __init__
# runs too, when package imported as a package.  Only when run as script
# itself.
#
# Alternative: use a guard clause, if __name__ == "__main__": import
# set_package_attribute

# TODO: maybe note describing explicit relative imports, i.e., imports with a
# leading period in them.  (Does that cover all cases?)
# TODO: maybe give explicit clone command rather than just address...

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
                print("\ndebug: Had to add to sys.path and remove dirname", dirname, "\n")

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

