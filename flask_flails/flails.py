from flask import Flask, Blueprint, render_template
from .flass import Flass
from .flex import Flex
from .flinf import Flinf
from .flab import Flab
from .flap import Flap
from .signals import app_created_successfully


class FlailsError(Exception): pass


class Flails(object):
    def __init__(self,
                 app_name=__name__,
                 app_config=None,
                 app_config_requires=None,
                 app_inside_module=None,
                 requested_info=None,
                 assets_do_register=True,
                 assets_do_parse_static=True,
                 assets_do_exclude_blueprints=None,
                 assets_do_write_manifests=False,
                 registration_manager_cls=Flap,
                 blueprints_manager_cls=Flab,
                 assets_manager_cls=Flass,
                 extensions_manager_cls=Flex,
                 information_manager_cls=Flinf,
                 information_page=True):
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
        self.assets_do_register = assets_do_register
        self.assets_do_parse_static = assets_do_parse_static
        self.assets_do_exclude_blueprints = assets_do_exclude_blueprints
        self.assets_do_write_manifests = assets_do_write_manifests
        self.information_page = information_page
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
                                              exclude_blueprints=self.assets_do_exclude_blueprints,
                                              parse_static_main=self.assets_do_parse_static,
                                              write_manifests=self.assets_do_write_manifests)
        self.app_extensions = self.app_extensions_cls(self)
        self.app_information = self.app_information_cls
        self.app_blueprints = self.app_blueprints_cls(self)

    @property
    def info_page_blueprint(self):
        info_bp = Blueprint('info_page', __name__, template_folder='templates')
        def info_page():
            return render_template('info_page.html', info=self.generated_app_info)
        info_bp.route('/info_page', methods=['GET'])(info_page)
        return info_bp

    def create_app(self, **kwargs):
        self.create_time_additions('EXTENSIONS',
                                   kwargs.pop('extensions', None))
        self.create_time_additions('BLUEPRINTS',
                                   kwargs.pop('blueprints', None))

        app = Flask(self.app_name)

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

        for k, v in self.app_registrations.app_actions.items():
            action = getattr(self.app_config, k.upper(), None)
            fn, values = v, action
            if values:
                fn(app, values)

        self.configure_blueprints(app, getattr(self.app_config, 'BLUEPRINTS', None))

        if self.assets_do_register:
            self.app_assets.set_env()
            self.app_assets.register_assets(app)

        if self.information_page:
            app.register_blueprint(self.info_page_blueprint)

        self.generated_app = app

        app_created_successfully.send(self)
        app.logger.info("Application {!r} successfully generated".format(self.generated_app))

        setattr(self, 'generated_app_info', self.app_information(self, self.generated_app, self.requested_info))

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
