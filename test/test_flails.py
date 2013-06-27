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


class AppInfoCase(SetupInstance):
    def test_app_info(self):
        self.assertIsNotNone(self.f.generated_app_info.app_information)
        #self.flails_instance.generated_app_info.info_dump_applog


class CreateAppCase(SetupInstance):
    def test_create_app(self):
        self.assertIsNotNone(self.f.generated_app)
        self.assertIsInstance(self.a, Flask)


class ExtensionRegisterCase(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(config={'CACHE_TYPE': 'simple'})
        DefaultConfig.EXTENSIONS = [ExtensionConfig(Gravatar, size=100, rating='g', precedence=1),
                                    ExtensionConfig(self.cache, init_type='by_init', precedence=1000)]
        self.f = Flails('test_extensions', DefaultConfig)
        self.a = self.f.create_app()

    def test_extension_register(self):
        self.assertEqual(self.a.extensions, self.f.generated_app.extensions)
        self.assertIsNotNone(self.a.extensions)
        self.assertIsInstance(self.a.extensions['gravatar'], Gravatar)


class ViewsRegisterCase(unittest.TestCase):
    def setUp(self):
        self.views_register_app = flails_instance.create_app(app_name='view_register_test_application',
                                                             app_config=DefaultConfig)

    def test_view_register(self):
        pass

class CreatedAppCase(SetupInstance):
    def test_test_application(self):
        self.assertIsInstance(self.flails_instance, Flails)
        self.assertIsInstance(self.test_application, Flask)
        self.g = Flails(app_name='test_application',
                        app_config=DefaultConfig,
                        requested_info=['jinja_env',
                                        'blueprints',
                                        'asset_env'])
        self.alternate_test_application = self.g.create_app()
        self.assertEqual(self.f.generated_app_info.info_dump_out,
                         self.g.generated_app_info.info_dump_out)


class GeneratedAssetsCase(SetupInstance):
    def test_assets(self):
        self.assertIsNotNone(self.a.jinja_env.assets_environment)

def suite():
    suites = [FlailsInstantiateCase, AppInfoCase, CreateAppCase,
            ExtensionRegisterCase, ViewsRegisterCase, CreatedAppCase,
            GeneratedAssetsCase]
    suite = unittest.TestSuite()
    for s in suites:
        suite.addTest(unittest.makeSuite(s))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
