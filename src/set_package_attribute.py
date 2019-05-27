# -*- coding: utf-8 -*-
"""
.. default-role:: code

Description
-----------

In order to run a module inside a package as a script and have explicit
relative imports work, the `__package__` attribute of the module should be set.
Importing `set_package_attribute` from such a script and running its `init`
function will set the `__package__` attribute of the script's module (which is
always `__main__`).  This is intended for use in any module inside a package which
might ever be run as a script and which either uses intra-package imports or else
imports other modules from within the same package which do so.

To use `set_package_attribute` just import it before any of the non-system
files, inside any module that you might want to run as a script, and call the
`init` function.  This should be done inside a guard conditional, so that it
only runs when the module is executed as a script::

   if __name__ == "__main__":
       import set_package_attribute
       set_package_attribute.init()

Nothing else is required.  The `init` function must be called **before** any
within-package explicit relative imports, and before importing any modules from
within the same package which themselves use such imports.  Any previously-set
`__package__` attribute (other than `None`) will be left unchanged.

If you are happy with the default values to the `init` arguments then as a
shortcut you can perform a single import which will call `init` automatically::

   if __name__ == "__main__":
       import set_package_attribute_magic

The `init` function takes one optional boolean parameter, `modify_syspath`.  If
`modify_syspath` is true then whenever the `__package__` attribute is set by `init`
the first element of `sys.path` is also deleted.  This avoids some of the
potential aliasing and shadowing problems that can arise when directories
inside packages are added to `sys.path` (since Python automatically inserts a
script's directory as the first element of `sys.path`).  This is not guaranteed
not to create other problems, but it works in test cases.  The default is true,
i.e., `sys.path` has the first element deleted by default on a call to `init`.
If such a deletion is performed the `sys.path` entry is saved as
`set_package_attribute.deleted_sys_path_0_value` for informational purposes
(replacing the default `None` value).

Even the use of absolute intra-package imports within a script requires that
the package itself be discoverable on `sys.path`.  This module also takes care
of that, temporarily adding the directory containing the package's root
directory to `sys.path` and then restoring the original `sys.path` after doing
the import.

Another use of the `set_package_attribute` module is that it allows explicit
relative imports to be used for intra-package imports in the main module of a
Python application (i.e., in a Python application's entry-point script).
Usually, `as described in the Python documentation
<https://docs.python.org/3/tutorial/modules.html#intra-package-references>`_,
these imports should always be absolute imports.  That is, without the
`__package__` attribute being set such modules should generally only import
intra-package modules by their full, package-qualified names (with the package
itself being discoverable on `sys.path`).  The guard conditional would not be
required in this case, assuming the entry-point module is only ever used to
start the application and is not imported from another Python file.

Installation
------------

The simplest way to install is to use pip:

.. code:: bash

   pip install set-package-attribute

The module can also be installed by `downloading it
<https://github.com/abarker/set-package-attribute>`_ or cloning it from GitHub
and running its `setup.py` file in the usual way.  The clone command is:

.. code:: bash

   git clone https://github.com/abarker/set-package-attribute

The distribution currently consists of a single module, which could also simply
be copied to somewhere in the Python path (to avoid adding a dependency).

Some technical notes
--------------------

* Internally, this module also needs to import the package directory
  containing the script module (under its full package-qualified name).  A
  side-effect of this is that any `__init__.py` files in the package path down
  to the script (from the top package level) will be executed.  Similarly, any
  modules you import as intra-package imports will cause the init files down to
  them to be run.  This could give unexpected results as compared with simply
  running the script not as a part of the package, depending on how
  `__init__.py` files are used in a given package.  The effect is essentially
  the same as if the script file had been imported using its full,
  package-qualified module name.

* The basic mechanism still works if the guard conditional is left off.
  Without it, though, if a script in a *different* package/project were to
  explicitly or implicity import a module which itself imports and uses
  `set_package_attribute`, a potential problem would occur.  This includes
  importing that module as part of its full package, say if the `__init__.py`
  of that imported package imports the module (which happens quite often).
  This would have the side-effect of setting the package attribute of the
  `__main__` module, which in this case is the module for a script in an
  entirely different package.  Often this would not cause a problem, since it
  would at least be set correctly, but it might result in unexpected behavior
  that could be difficult to trace.

* This only works for intra-package imports, i.e., for a module importing
  another module from within *its own* package.  You still cannot directly
  import a module from inside a *different* package and expect its
  intra-package imports to work.

* An alternative approach is to always execute scripts inside packages with
  the `-m` flag set.  For example, to execute a script `module_name.py`,
  which is in a subdirectory inside a package `pkg_toplevel`, you would use:

  .. code:: bash

     python -m pkg_toplevel.pkg_subdir.module_name

  This requires the full package name to be used, however, and has a
  different invocation method than other scripts.  Also, the directory
  containing the top-level package directory `pkg_toplevel` (i.e., its parent
  directory) needs to be in Python's package search path in order for this
  approach to work.

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

# TODO:
#
# Maybe: the set_package_attribute_magic could introspect to find the calling module,
# like pytest-helper, and test itself whether it is `__main__`.  That adds a little
# overhead at startup, but if used inside a guard conditional it only runs when actually
# running as a script.  Adding this would be backward compatible, so no rush.

from __future__ import print_function, division, absolute_import
import os
import sys

already_set_attribute = False # Used to avoid problems if called twice.

def _set_package_attribute(modify_syspath):
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
        script_module_name = os.path.splitext(script_filename)[0]
        parent_dirs = [] # A reversed list of package name parts, to build up.

        # Go up the directory tree to find the top-level package directory.
        dirname = script_dirname
        while os.path.exists(os.path.join(dirname, "__init__.py")):
            dirname, name = os.path.split(dirname)
            parent_dirs.append(name)

        if parent_dirs: # Does nothing if no __init__.py file was found.
            #assert os.path.abspath(sys.path[0]) == script_dirname # True
            if modify_syspath:
                _delete_sys_path_0()

            global already_set_attribute
            if not already_set_attribute:
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
                full_module_name = full_subpackage_name + "." + script_module_name
                #assert full_module_name not in sys.modules # True
                sys.modules[full_module_name] = main_module
                #assert full_module_name in sys.modules # True

            already_set_attribute = True

deleted_sys_path_0_value = None

def _delete_sys_path_0():
    """Delete the first entry on `sys.path`, but only if this routine has not deleted it
    already."""
    global deleted_sys_path_0_value
    if deleted_sys_path_0_value is None:
        deleted_sys_path_0_value = sys.path[0]
        del sys.path[0]

def _restore_sys_path_0():
    """Delete the first entry on `sys.path`, but only if this routine has not deleted it
    already."""
    global deleted_sys_path_0_value
    if deleted_sys_path_0_value is not None:
        sys.path.insert(0, deleted_sys_path_0_value)
        deleted_sys_path_0_value = None

def init(modify_syspath=True):
    """Set the `__package__` attribute of the module `__main__` if it is not
    already set.

    If `modify_syspath` is true then whenever the `__package__` attribute is set
    the first element of `sys.path` (the current
    directory of the script) is also deleted from the path list."""
    _set_package_attribute(modify_syspath=modify_syspath)

