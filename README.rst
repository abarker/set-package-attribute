
.. default-role:: code

set-package-attribute
=====================

A package which sets the `__package__` attribute of any script which imports
it, so that explicit relative imports work.

For full documentation, see https://abarker.github.io/set-package-attribute.

Also available on PyPI at: <coming soon>

Brief usage summary
===================

To use the package just import it before any of the non-system files, inside any
module that you might want to run as a script, and call its `init` function.
These statements should be inside a guard conditional, so that they only run
when the module is executed as a script::

   if __name__ == "__main__":
       import set_package_attribute
       set_package_attribute.init()

Nothing else is required.  The `init` function must be called **before** any
within-package explicit relative imports, and before importing any modules from
within the same package which themselves use such imports.  
