"""
test-flails.py
==============
This tests the Flask-Flails extension.
"""

from __future__ import with_statement
import unittest

import os
from flask import Flask
from flask.ext.flails import Flails
from test_app.config.settings.default_settings import DefaultConfig

TESTS = os.path.dirname(__file__)
join = os.path.join


class FlailsInstantiateCase(unittest.TestCase):

    def test_instantiate_instance(self):
        f = Flails('test', DefaultConfig)
        self.assertIsInstance(f, Flails)

class CreateAppCase(unittest.TestCase):

    def test_create_app(self):
        f = Flails('test', DefaultConfig)
        a = f.create_app()
        self.assertIsInstance(a, Flask)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlailsInstantiateCase))
    suite.addTest(unittest.makeSuite(CreateAppCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
