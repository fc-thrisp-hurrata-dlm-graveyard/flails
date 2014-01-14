from flask import Flask
from flask.ext.gravatar import Gravatar
from flask_flails import Flails
from tests import FlailsTest


class BaseFunctionalTest(FlailsTest):
    def test_base(self):
        self.assertIsNotNone(self.app)
        self.assertIsInstance(self.app, Flask)
        self.assertIsInstance(self.f, Flails)
        self.assertIsNotNone(self.f.generated_app)
        self.assertIsNotNone(self.f.generated_app_info.app_information)

    def test_create_app(self):
        test_app = self.f.create_app()
        self.assertIsInstance(test_app, Flask)
        self.assertIsNotNone(test_app)

    def test_extension_register(self):
        self.assertEqual(self.app.extensions, self.f.generated_app.extensions)
        self.assertIsNotNone(self.app.extensions)
        self.assertIsInstance(self.app.extensions['gravatar'], Gravatar)


class ViewsRegisterCase(FlailsTest): pass
