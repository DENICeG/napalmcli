#!/usr/bin/python

import unittest
import os
import subprocess

class NapalmCli(unittest.TestCase):
    def runTest(self):
        cwd = os.getcwd()
        cmd = cwd + "/bin/napalmcli.py"
        out = subprocess.check_output([cmd, "-h"])
        self.assertIn('Usage', out, 'test help message')
