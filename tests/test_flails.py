"""
test-flails.py
==============
This tests the Flask-Flails extension.
"""

from __future__ import with_statement
import unittest
import os
from flask import Flask
from flask.ext.flails import Flails, ExtensionConfig
from test_app.config.settings.default_settings import DefaultConfig, NonDefaultConfig
from test_app.app import flails_instance, test_application
from test_app.blueprints import post
from flask.ext.gravatar import Gravatar
from flask.ext.cache import Cache
import pprint

class SetupInstance(unittest.TestCase):
    def setUp(self):
        self.f = Flails('test', DefaultConfig)
        self.a = self.f.create_app()
        self.flails_instance = flails_instance
        self.test_application = test_application


class FlailsInstantiateCase(SetupInstance):
    def test_instantiate_instance(self):
        self.assertIsInstance(self.f, Flails)
        with self.assertRaises(Exception):
            Flails('test', NonDefaultConfig)


class AppInfoCase(SetupInstance):
    def test_app_info(self):
        self.assertIsNotNone(self.f.generated_app_info.app_information)
        self.flails_instance.generated_app_info.formatted


class CreateAppCase(SetupInstance):
    def test_create_app(self):
        self.assertIsNotNone(self.f.generated_app)
        self.assertIsInstance(self.a, Flask)


class ExtensionRegisterCase(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(config={'CACHE_TYPE': 'simple'})
        DefaultConfig.EXTENSIONS = [ExtensionConfig(Gravatar, size=100, rating='g'),
                                    ExtensionConfig(self.cache, init_type='by_init')]
        self.f = Flails('test_extensions', DefaultConfig)
        self.a = self.f.create_app()

    def test_extension_register(self):
        self.assertEqual(self.a.extensions, self.f.generated_app.extensions)
        self.assertIsNotNone(self.a.extensions)
        self.assertIsInstance(self.a.extensions['gravatar'], Gravatar)


class CreatedAppCase(SetupInstance):
    def test_test_application(self):
        self.assertIsInstance(self.flails_instance, Flails)
        self.assertIsInstance(self.test_application, Flask)
        self.g = Flails(app_name='test_application', config_obj=DefaultConfig, requested_info=['jinja_env', 'blueprints', 'asset_env'])
        self.alternate_test_application = self.g.create_app()
        self.assertEqual(self.test_application.static_folder, self.alternate_test_application.static_folder)
        self.assertEqual(self.f.generated_app_info.formatted, self.g.generated_app_info.formatted)
        self.f.generated_app_info.formatted


class generatedAssetsCase(SetupInstance):
    def test_assets(self):
        self.assertIsNotNone(self.a.jinja_env.assets_environment)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FlailsInstantiateCase))
    suite.addTest(unittest.makeSuite(AppInfoCase))
    suite.addTest(unittest.makeSuite(CreateAppCase))
    suite.addTest(unittest.makeSuite(ExtensionRegisterCase))
    suite.addTest(unittest.makeSuite(CreatedAppCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
