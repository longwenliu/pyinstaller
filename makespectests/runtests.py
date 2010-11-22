#!/usr/bin/env python
import glob
import os, sys
import shutil
import unittest

MST_DIR = os.path.abspath(os.path.split(sys.argv[0])[0])
HOME = os.path.normpath(os.path.join(MST_DIR, ".."))
MAKESPEC_EXE = os.path.join(HOME, "Makespec.py")
BUILD_EXE = os.path.join(HOME, "Build.py")
SCRIPT_FOR_TEST = os.path.join(MST_DIR, "script_for_tests.py")
CLEANUP = """python_exe.build
logdict*.log
warn*.txt
*.py[co]
*/*.py[co]
*/*/*.py[co]
*.spec
build/
dist/
""".split()

class MakespecTest(unittest.TestCase):

    def setUp(self):
        """
        Init the spec files used for tests
        """
        os.system("%s -n spec_od --onedir %s" % (MAKESPEC_EXE, os.path.join(MST_DIR, SCRIPT_FOR_TEST)))
        os.system("%s -n spec_of --onefile %s" % (MAKESPEC_EXE, os.path.join(MST_DIR, SCRIPT_FOR_TEST)))

    def tearDown(self):
        """
        Clean all the directory removing files created for tests
        """
        for clean in CLEANUP:
            clean = glob.glob(clean)
            for path in clean:
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except OSError, e:
                    print e

    def test_build_onedir(self):
        os.system("%s -y spec_od.spec" % BUILD_EXE)

    def test_build_onefile(self):
        os.system("%s -y spec_of.spec" % BUILD_EXE)

    def test_switch_to_onedir(self):
        """
        Tests the validity of switching a spec file from onefile to onedir deployment
        """
        os.system("%s -n _spec_od --onedir spec_of.spec" % MAKESPEC_EXE)
        os.system("%s -y _spec_od.spec" % BUILD_EXE)

    def test_switch_to_onefile(self):
        """
        Tests the validity of switching a spec file from onedir to onefile deployment
        """
        os.system("%s -n _spec_of --onefile %s" % (MAKESPEC_EXE, "spec_od.spec"))
        os.system("%s -y _spec_of.spec" % BUILD_EXE)

if __name__ == "__main__":
    unittest.main()