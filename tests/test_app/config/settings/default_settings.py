#site
from flask import render_template
from os import path, urandom
from url_settings import UrlConfig
from blueprint_settings import BlueprintConfig
from flask.ext.macro4 import Macro4
from flask.ext.misaka import Misaka

PROJECT = "test_app"

class BaseConfig(object):

    DEBUG = False
    TESTING = False

    SITE_NAME = "DEFAULT"
    SITE_DOMAIN = "DEFAULT.COM"

    SECRET_KEY = 'secret_key'
    SECRET_SALT = 'secret_salt'


class DefaultConfig(BaseConfig, BlueprintConfig, UrlConfig):

    DEBUG = True

    # To create log folder.
    # $ sudo mkdir -p /var/log/<PROJECT>
    # $ sudo chown $USER /var/log/<PROJECT>
    DEBUG_LOG = '/var/log/{}/debug.log'.format(PROJECT)


    ROOT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    #: Before request middlewares.
    BEFORE_REQUESTS = []

    #: After request middlewares.
    AFTER_REQUESTS = []

    #: Middlewares to enable.
    #: Middlewares are executed in the order specified.
    MIDDLEWARES = [
        #: Emulate RESTFul API for client that dont' directly
        #: support REST.
        # (middleware, *args, **kwargs)
        #MethodRewriteMiddleware,
    ]

    #: Jinja2 filters.
    #TEMPLATE_FILTERS = [('custom_reverse', lambda x: x[::-1])]
    TEMPLATE_FILTERS = []

    #: Jinja2 context processors.
    #CONTEXT_PROCESSORS = {'inflectorize': inflectorize,
    #                      'baseextend': SITE_INDEX_EXTENDS}
    CONTEXT_PROCESSORS = {}

    #: Error handlers for http and other arbitrary exceptions.
    ERROR_HANDLERS = [
        (403, lambda error: (render_template("errors/forbidden_page.html"), 403)),
        (404, lambda error: (render_template("errors/page_not_found.html"), 404)),
        (405, lambda error: (render_template("errors/method_not_allowed.html"), 405)),
        (500, lambda error: (render_template("errors/server_error.html"), 500))
    ]

    EXTENSIONS = [Macro4, Misaka]

class NonDefaultConfig(BaseConfig, BlueprintConfig):

    DEBUG = True

    # To create log folder.
    # $ sudo mkdir -p /var/log/<PROJECT>
    # $ sudo chown $USER /var/log/<PROJECT>
    DEBUG_LOG = '/var/log/{}/debug.log'.format(PROJECT)


    #ROOT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    #: Before request middlewares.
    BEFORE_REQUESTS = []

    #: After request middlewares.
    AFTER_REQUESTS = []

    #: Middlewares to enable.
    #: Middlewares are executed in the order specified.
    MIDDLEWARES = [
        #: Emulate RESTFul API for client that dont' directly
        #: support REST.
        # (middleware, *args, **kwargs)
        #MethodRewriteMiddleware,
    ]

    #: Jinja2 filters.
    #TEMPLATE_FILTERS = [('custom_reverse', lambda x: x[::-1])]
    TEMPLATE_FILTERS = []

    #: Jinja2 context processors.
    #CONTEXT_PROCESSORS = {'inflectorize': inflectorize,
    #                      'baseextend': SITE_INDEX_EXTENDS}
    CONTEXT_PROCESSORS = {}

    #: Error handlers for http and other arbitrary exceptions.
    ERROR_HANDLERS = [
        (403, lambda error: (render_template("errors/forbidden_page.html"), 403)),
        (404, lambda error: (render_template("errors/page_not_found.html"), 404)),
        (405, lambda error: (render_template("errors/method_not_allowed.html"), 405)),
        (500, lambda error: (render_template("errors/server_error.html"), 500))
    ]

class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
