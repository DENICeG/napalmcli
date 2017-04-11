#!/usr/bin/python

import unittest
from napalm_cli.Napalm import Napalm


class DefaultNapalm(unittest.TestCase):
    def runTest(self):
        hostname = 'localhost'
        devtype = 'iosxr'
        username = 'test'
        p = 'test'
        port = 22
        device = Napalm(hostname, devtype, username, p, port)
        self.assertEqual(device.username, 'test')
        self.assertEqual(device.password, 'test')
        pass



if __name__ == '__main__':
    unittest.main()
