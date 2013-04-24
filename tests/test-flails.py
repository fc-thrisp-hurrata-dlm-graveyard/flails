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
from test_app.app import flails_instance, test_application
from test_app.blueprints import post

class FlailsInstantiateCase(unittest.TestCase):

    def test_instantiate_instance(self):
        f = Flails('test', DefaultConfig)
        self.assertIsInstance(f, Flails)
        with self.assertRaises(Exception):
            g = Flails('test', NonDefaultConfig)


class CreateAppCase(unittest.TestCase):

    def setUp(self):
        self.f = Flails('test', DefaultConfig)
        self.a = self.f.create_app()

    def test_create_app(self):
        self.assertIsNotNone(self.f.generated_app)
        self.assertIsInstance(self.a, Flask)

    def test_routes_registered(self):
        pass

    def test_extensions_registered(self):
        self.assertEqual(self.a.extensions, self.f.generated_app.extensions)
        #self.assertIsNotNone(self.a.extensions[''])
        #self.assertIsInstance()

    def test_app_info(self):
        self.assertIsNotNone(self.f.app_info('blueprints', 'extensions', 'jinja_env'))


class CreatedAppCase(unittest.TestCase):

    def setUp(self):
        self.f = flails_instance
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
