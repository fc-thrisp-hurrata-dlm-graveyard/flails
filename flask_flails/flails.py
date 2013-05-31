from flask import Flask, Blueprint
from werkzeug import import_string
from flass import Flass
from flex import Flex
from flinf import Flinf
from flab import Flab
from flap import Flap
from flask.ext.classy import FlaskView as FlailsView

class FlailsException(Exception):
    pass

class Flails(object):
    def __init__(self, app_name=__name__,
                       app_config=None,
                       app_config_requires=None,
                       app_inside_module=None,
                       requested_info=None,
                       do_register_assets=True,
                       do_parse_static_main=True,
                       do_exclude_blueprints=None,
                       registration_manager_cls=Flap,
                       blueprints_manager_cls=Flab,
                       assets_manager_cls=Flass,
                       extensions_manager_cls=Flex,
                       information_manager_cls=Flinf):
        self.generated_app = None
        self.generated_app_info = None
        self.app_name = app_name
        self.app_config = self.check_config(app_config, app_config_requires)
        self.app_inside_module = app_inside_module
        self.app_registrations_cls = registration_manager_cls
        self.app_blueprints_cls = blueprints_manager_cls
        self.app_assets_cls = assets_manager_cls
        self.app_extensions_cls = extensions_manager_cls
        self.app_information_cls = information_manager_cls
        self.requested_info = requested_info
        self.do_register_assets = do_register_assets
        self.do_parse_static_main = do_parse_static_main
        self.do_exclude_blueprints = do_exclude_blueprints
        self.initialize_managers()

    def check_config(self, app_config, app_config_requires):
        """Forces a check on your configuration file"""
        if app_config_requires is not None:
            for c in app_config_requires:
                if not hasattr(app_config, c):
                    raise FlailsException('Configuration MUST contain or specify in some manner: {}'.format(c))
        return app_config

    def initialize_managers(self):
        self.app_registrations = self.app_registrations_cls(self)
        self.app_assets = self.app_assets_cls(self,
                                              exclude_blueprints=self.do_exclude_blueprints,
                                              parse_static_main=self.do_parse_static_main)
        self.app_extensions = self.app_extensions_cls(self)
        self.app_information = self.app_information_cls
        self.app_blueprints = self.app_blueprints_cls(self)

    def create_app(self, **kwargs):
        self.create_time_additions('EXTENSIONS', kwargs.pop('extensions', None))
        self.create_time_additions('BLUEPRINTS', kwargs.pop('blueprints', None))

        app = Flask(self.app_name)

        self.app_assets.set_env()

        for k in kwargs:
            if k in ('import_name',
                     'static_url_path',
                     'static_folder',
                     'template_folder',
                     'views_folder',
                     'blueprints_folder',
                     'instance_path',
                     'instance_relative_config'):
                setattr(app, k, kwargs.get(k))

        self.configure_app(app, kwargs.pop('create_time_settings', None))

        self.configure_extensions(app, self.app_config)

        for k,v in self.app_registrations.app_actions.iteritems():
            action = getattr(self.app_config, k.upper(), None)
            fn, values = v, action
            if values:
                fn(app, values)

        self.configure_blueprints(app, getattr(self.app_config, 'BLUEPRINTS', None))

        if self.do_register_assets:
            self.app_assets.register_assets(app)

        self.generated_app = app

        setattr(self,
                'generated_app_info',
                self.app_information(self,
                                     self.generated_app,
                                     self.requested_info))

        return self.generated_app

    def create_time_additions(self, what, to_add):
        if to_add and hasattr(self.app_config, what):
            x = getattr(self.app_config, what)
            x.extend(to_add)
        elif to_add:
            setattr(self.app_config, what, to_add)
        else:
            pass

    def configure_app(self, app, create_time_settings):
        app.config.from_object(self.app_config)
        if create_time_settings:
            app.config.from_object(create_time_settings)
        app.config.from_envvar("{}_APP_CONFIG".format(self.app_name.upper()),
                                                      silent=True)

    def configure_extensions(self, app, app_config):
        self.app_extensions.configure_extensions(app, app_config)

    def configure_blueprints(self, app, blueprints):
        self.app_blueprints.configure_blueprints(app, blueprints)
