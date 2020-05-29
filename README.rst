
.. default-role:: code

set-package-attribute
=====================

Run modules inside packages as scripts.  Automatically sets the `__package__`
attribute of any script which imports it and calls the initialization function
`set_package_attribute.init()`.  This allows the script to use explicit relative
imports, which fail otherwise.

For full documentation, see https://abarker.github.io/set-package-attribute.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Also available on PyPI for installation with pip.

Brief usage summary
===================

To use the package just import it before any of the non-system files, inside any
module that you might want to run as a script, and call the `init` function.
These statements should be inside a guard conditional, so that they only run
when the module is executed as a script::

   if __name__ == "__main__":
       import set_package_attribute
       set_package_attribute.init()

The guard conditional is not required if the module is *only* ever run as a
script, i.e., if it is never imported by any module.  The `init` function must
be called **before** any explicit relative imports, and before importing any
modules from within the same package which themselves use such imports.  

If you are happy with the default `init` arguments then there is a shortcut
import which automatically calls `init` for you::

   if __name__ == "__main__":
       import set_package_attribute_magic

