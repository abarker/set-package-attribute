# -*- coding: utf-8 -*-
"""
.. default-role:: code

Description
-----------

In order to run a module inside a package as a script and have explicit
relative imports work, the `__package__` attribute of the module should be set.
Importing `set_package_attribute` from a script and running its `init` function
sets the `__package__` attribute of the module `__main__`.  This is intended to
be used in modules which might be run as scripts and which either use
intra-package imports or else need to import other modules from within the same
package which do.

To use the package just import it before any of the non-system files, inside any
module that you might want to run as a script, and call the `init` function.
These statements should be inside a guard conditional, so that they only run
when the module is executed as a script::

   if __name__ == "__main__":
       import set_package_attribute
       set_package_attribute.init()

Nothing else is required.  The `init` function must be called **before** any
within-package explicit relative imports, and before importing any modules from
within the same package which themselves use such imports.  Any previously-set
`__package__` attribute (other than `None`) will be left unchanged.

To even use absolute intra-package imports within a script the package itself
needs to be found on Python's package search path.  This package also takes
care of that, temporarily adding the directory containing the package root to
`sys.path` if necessary, and then deleting it again.

The `init` function takes one optional boolean parameter `mod_path`.  If it is
set true then whenever `__package__` is set the first element of `sys.path` is
also deleted.  This avoids some of the aliasing problems that can arise from
directories inside packages being automatically added to the package search
path when scripts inside the package are run.  It is not guaranteed not to
create other problems, but it works in test cases.  The default is false, i.e.,
the path is not modified.

Some notes:

* Internally, this module also needs to import the package directory
  containing the script module (under its full package-qualified name).  A
  side-effect of this is that any `__init__.py` files in the package path down
  to the script (from the top package level) will be executed.  Similarly, any
  modules you import within the package will cause the init files down to them
  to be run.  This could give unexpected results compared to running the script
  outside the package, depending on how `__init__.py` files are used in a given
  package.  The effect is essentially the same as if the script file had been
  imported using its full, package-qualified module name.

* The basic mechanism will still work if the guard conditional is left off.
  But a problem would occur if an external script in a *different* package were
  to explicitly or implicity import a module which itself imports
  `set_package_attribute`.  This includes importing it as part of its full
  package, say if the init module imports it.  This would have the side-effect
  of setting the package attribute of the `__main__` module, which in this case
  is the module for the external script.  Often this would not be a problem,
  since it will be correctly set, but it might result in unexpected behavior
  that could be difficult to trace.

* This only works for intra-package imports, i.e., a module importing another
  module from within the same package (using explicit relative imports within
  that package).  You still cannot import a module from inside a *different*
  package and have its intra-package explicit relative imports work.

Another use of this package is that it allows explicit relative imports to be
used for intra-package imports in the main module of a Python application
(i.e., in a Python application's entry-point script).  Usually, `as described
in the Python documentation
<https://docs.python.org/3/tutorial/modules.html#intra-package-references>`_,
these imports should always be absolute imports.  That is, without the
`__package__` attribute being set such modules should generally only import
intra-package modules by their full, package-qualified names).  The guard
conditional is not required in this case, assuming the application will always
be run from the entry point rather than imported from another Python file.

Installation
------------

The simplest way to install is to use pip:

.. code:: bash

   pip install set-package-attribute

The package can also be installed by cloning it and running its `setup.py` file
in the usual way.  The clone command is:

.. code:: bash

   git clone https://github.com/abarker/set-package-attribute

The package currently consists of a single module, which could also simply be
copied to somewhere in the Python path (to avoid adding a dependency).

Further details
---------------

When `init` is run this module searches for the module `__main__` in
`sys.modules`.  If that module is not found then nothing is done.  If
`__main__` is found then the `__package__` attribute for the `__main__` module
is computed by going up the directory tree from its source file, looking for
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

    An alternative approach is to always execute scripts inside packages with
    the `-m` flag set.  For example, to execute a script `module_name.py`,
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

Functions
---------
"""

from __future__ import print_function, division, absolute_import
import os
import sys

def _set_package_attribute(mod_path=False):
    """Set the `__package__` attribute of the module `__main__` if it is not
    already set."""
    # Get the module named __main__ from sys.modules.
    main_found = True
    try:
        main_module = sys.modules["__main__"]
    except KeyError:
        main_found = False

    # Do nothing unless the program was started from a script.
    if main_found and main_module.__package__ is None:

        importing_file = main_module.__file__
        script_dirname, script_filename = os.path.split(
                               os.path.realpath(os.path.abspath(importing_file)))
        filename = os.path.splitext(script_filename)[0]
        parent_dirs = [] # A reversed list of package name parts, to build up.

        # Go up the directory tree to find the top-level package directory.
        dirname = script_dirname
        while os.path.exists(os.path.join(dirname, "__init__.py")):
            dirname, name = os.path.split(dirname) 
            parent_dirs.append(name)

        if parent_dirs: # Does nothing if no __init__.py file was found.

            # Build the name of the subpackage the "__main__" module is in, and set
            # the __package__ variable to it.
            # Note: the subpackage name does not include the name of the module itself.
            full_subpackage_name = ".".join(reversed(parent_dirs))
            main_module.__package__ = full_subpackage_name

            # Now do the actual import of the subpackage.
            # Note: the script's module loads and initializes *twice* if you import
            # full_module_name rather than subpackage_module!

            # Normally you insert to sys.path as position one, leaving the script's
            # directory in position zero.  Here, though, it is temporary and we want
            # to avoid name shadowing so we insert at position zero.
            sys.path.insert(0, dirname)
            subpackage_module = __import__(full_subpackage_name)
            del sys.path[0] # Remove the added path; no longer needed.

            #assert full_subpackage_name in sys.modules # True
            full_module_name = full_subpackage_name + "." + filename
            #assert full_module_name not in sys.modules # True
            sys.modules[full_module_name] = main_module
            #assert full_module_name in sys.modules # True

            #assert os.path.abspath(sys.path[0]) == script_dirname # True
            if mod_path: del sys.path[0]

def init(mod_path=False):
    """Set the `__package__` attribute of the module `__main__` if it is not
    already set.

    If `mod_path` is true then whenever the `__package__` attribute is set
    the first element of `sys.path` (the current
    directory of the script) is also deleted from the path list."""
    _set_package_attribute(mod_path=mod_path)

