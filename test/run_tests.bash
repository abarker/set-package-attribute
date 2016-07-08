#!/usr/bin/env bash
#
# Run the tests.  Always run with the test directory as the PWD.
#
# This is just a Bash script because most of the tests need to be run as
# scripts.

for p in "python"
do
   $p ./test_not_in_package.py
   echo
   $p ./test_importing_package.py

   echo
   $p ./toplevel/test_at_toplevel.py
   echo
   $p ./toplevel/subdir/test_in_subdir.py
   echo
   $p ./toplevel/subdir/subsubdir/test_in_subsubdir.py
done

