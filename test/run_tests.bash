#!/usr/bin/env bash
#
# Run the tests.  Always run with the test directory as the PWD.
#
# This is just a Bash script because most of the tests need to be run as
# scripts.

for p in "python"
do
   echo
   echo "Test running from a module not in a package."
   $p ./test_not_in_package.py

   echo
   echo "Test importing modules as part of a package."
   $p ./test_importing_package.py

   echo
   echo "Test as script at toplevel of package tree."
   $p ./toplevel/test_at_toplevel.py

   echo
   echo "Test at as script at subdir level of package tree."
   $p ./toplevel/subdir/test_in_subdir.py

   echo
   echo "Test as script at subdir level, run from the subdir as PWD."
   cd toplevel/subdir
   $p test_in_subdir.py
   
   echo
   echo "Test as script at subdir level, run from parent directory."
   cd ..
   $p subdir/test_in_subdir.py
   cd .. # go back to test dir

   echo
   echo "Test as script at subsubdir level."
   $p ./toplevel/subdir/subsubdir/test_in_subsubdir.py
   
   echo
   echo "Test package name shadowed by module with the same name."
   $p ./shadow_package/shadow_package.py
done

echo
