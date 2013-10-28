from unittest import TestCase
from flask import Flask
from flask_flails import Flails, ExtensionConfig
from flask.ext.gravatar import Gravatar
from flask.ext.cache import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

class TestConfig(object):
    TESTING = True
    BEFORE_REQUESTS = []
    AFTER_REQUESTS = []
    MIDDLEWARES = []
    TEMPLATE_FILTERS = []
    CONTEXT_PROCESSORS = {}
    ERROR_HANDLERS = []
    EXTENSIONS = [{'extension': Gravatar, 'size':100, 'rating':'g', 'precedence':1},
                  #ExtensionConfig(Gravatar, size=100, rating='g', precedence=1),
                  ExtensionConfig(cache, init_type='by_init', precedence=1000)]


class FlailsTest(TestCase):
    def setUp(self):
        super(FlailsTest, self).setUp()

        f = Flails(app_name='basetesting', app_config=TestConfig)
        app = f.create_app()

        self.f = f
        self.app = app
