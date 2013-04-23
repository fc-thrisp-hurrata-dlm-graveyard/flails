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
from test_app.config.settings.default_settings import DefaultConfig, NonDefaultConfig
from test_app.app import f, test_application

TESTS = os.path.dirname(__file__)
join = os.path.join


class FlailsInstantiateCase(unittest.TestCase):

    def test_instantiate_instance(self):
        f = Flails('test', DefaultConfig)
        self.assertIsInstance(f, Flails)
        with self.assertRaises(Exception):
            g = Flails('test', NonDefaultConfig)

class CreateAppCase(unittest.TestCase):

    def test_create_app(self):
        f = Flails('test', DefaultConfig)
        a = f.create_app()
        self.assertIsInstance(a, Flask)
        self.assertIsNotNone(f.app_info)

class CreatedAppCase(unittest.TestCase):

    def setUp(self):
        self.f = f
        self.app = test_application
        self.template_path = os.path.join(os.path.dirname(os.path.abspath(DefaultConfig.ROOT_DIR)), 'templates')
        self.static_path = os.path.join(os.path.dirname(os.path.abspath(DefaultConfig.ROOT_DIR)), 'static')

    def test_test_application(self):
        self.assertIsInstance(self.f, Flails)
        self.assertIsInstance(self.app, Flask)
        self.assertEqual(self.app.static_folder, self.static_path)
        self.assertEqual(self.app.template_folder, self.template_path)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlailsInstantiateCase))
    suite.addTest(unittest.makeSuite(CreateAppCase))
    suite.addTest(unittest.makeSuite(CreatedAppCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
