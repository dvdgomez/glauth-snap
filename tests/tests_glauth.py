import logging
import os
import pathlib
import re
import shlex
import subprocess
import unittest

logger = logging.getLogger(__name__)

class TestSnap(unittest.TestCase):
    """Unit test GLAuth snap."""

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        logger.info("Building snap")
        os.chdir("..")
        subprocess.run("snapcraft")
        cls.GLAUTH = re.findall(r'(glauth.*?snap)', " ".join(os.listdir()))[0]

    @classmethod
    def tearDownClass(cls) -> None:
        """Test class teardown."""
        pathlib.Path(cls.GLAUTH).unlink(missing_ok=True)
        subprocess.run(shlex.split("snap remove glauth"))

    def test_build(self):
        """Test snap build status."""
        logger.info(f"Checking for snap {TestSnap.GLAUTH}...")
        self.assertTrue(pathlib.Path(TestSnap.GLAUTH).exists())
    
    def test_run(self):
        """Test snap run status."""
        logger.info(f"Installing glauth snap {TestSnap.GLAUTH}...")
        subprocess.run(shlex.split(f"sudo snap install {TestSnap.GLAUTH} --devmode --dangerous"))
        logger.info("Finished glauth snap install!")
        source = subprocess.run(
            shlex.split("which glauth"), stdout=subprocess.PIPE, text=True
        ).stdout.strip("\n")
        self.assertEqual(source, "/snap/bin/glauth")
