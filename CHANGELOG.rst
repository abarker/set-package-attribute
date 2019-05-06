.. :changelog:

History
=======

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

