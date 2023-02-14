import logging
import os
import pathlib
import shlex
import subprocess
import unittest

logger = logging.getLogger(__name__)

GLAUTH = "glauth_0+git.2533933-dirty_amd64.snap"

class TestSnap(unittest.TestCase):
    """Unit test GLAuth snap."""

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        logger.info("Building snap")
        os.chdir("..")
        subprocess.run("snapcraft")

    @classmethod
    def tearDownClass(cls) -> None:
        """Test class teardown."""
        pathlib.Path(GLAUTH).unlink(missing_ok=True)
        subprocess.run(shlex.split("snap remove glauth"))

    def test_build(self):
        """Test snap build status."""
        self.assertTrue(pathlib.Path(GLAUTH).exists())
    
    def test_run(self):
        """Test snap run status."""
        logger.info("Installing glauth snap...")
        subprocess.run(shlex.split(f"snap install {GLAUTH} --devmode --dangerous"))
        logger.info("Finished glauth snap install!")
        version = subprocess.run(
            shlex.split("which glauth"), stdout=subprocess.PIPE, text=True
        ).stdout.strip("\n")
        self.assertEqual(version, "/snap/bin/glauth")
