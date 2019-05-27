.. :changelog:

History
=======

0.2.2 (2019-05-27)
------------------

Changes:

* Now will only run once, even if called twice in a module.  The ``modify_syspath`` setting
  will be honored, if it wasn't done before.

0.2.1 (2019-05-27)
------------------

Changes:

* The ``mod_path`` keyword argument to ``init`` has been changed to ``modify_syspath``.

Bug Fixes:

* Fixed bug in the routine for deleting ``sys.path[0]``.

* Added a corresponding restore routine to restore it.

0.2.0 (2019-05-06)
------------------

New Features: None

Bug Fixes: None

Other changes:

* Stable version.

* Updates to docs.

0.1.2 (2019-05-05)
------------------

New Features:

* The default of the ``mod_path`` argument to ``init`` is now ``True``.  If a
  deletion is performed then the deleted ``sys.path[0]`` entry is saved as
  ``set_package_attribute.deleted_sys_path_0_value`` for informational
  purposes, replacing its default ``None`` value.

* A shortcut import ``set_package_attribute_magic`` was added which automatically
  calls ``init`` with the default argument values.

0.1.1 (2016-07-11)
------------------

New Features: None.

Bug Fixes:

* Fixed a name-shadowing bug where the module run as a script has the same name as
  the package it is in.

Other Changes: None.

0.1.0 (2016-06-11)
------------------

Initial release.

