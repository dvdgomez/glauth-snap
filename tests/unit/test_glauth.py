# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Test minimal snap."""

import logging
import os
import pathlib
import re
import shlex
import subprocess
import time
import unittest

import requests

logger = logging.getLogger(__name__)


class TestSnap(unittest.TestCase):
    """Unit test GLAuth snap."""

    @classmethod
    def setUpClass(cls) -> None:
        """Test class setup."""
        logger.info("Building snap")
        # Go up 3 levels from test file
        os.chdir("/".join(__file__.split("/")[:-3]))
        subprocess.run("snapcraft")
        # Find generated snap
        cls.GLAUTH = re.findall(r"(glauth.*?snap)", " ".join(os.listdir()))[0]

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

    def test_run_config(self):
        """Test snap network status."""
        logger.info("Testing network status")
        wait = subprocess.Popen(shlex.split("glauth -c sample-simple.cfg"))
        time.sleep(5)
        # Check snap responses
        response = requests.get("http://localhost:5555")
        self.assertEqual(response.status_code, 200)
        wait.kill()
