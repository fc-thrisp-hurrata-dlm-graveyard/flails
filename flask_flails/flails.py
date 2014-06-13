from flask import Flask, Blueprint, render_template
from .flass import Flass
from .flex import Flex
from .flinf import Flinf
from .flab import Flab
from .flap import Flap
from .signals import app_created_successfully


class FlailsError(Exception):
    pass


class Flails(object):
    registration_manager_cls = Flap
    blueprints_manager_cls = Flab
    assets_manager_cls = Flass
    extensions_manager_cls = Flex
    information_manager_cls = Flinf
    initialize = {'app_name': __name__,
                  'app_config_requires': None,
                  'app_inside_module': None,
                  'requested_info': None,
                  'assets_env': None,
                  'assets_do_register': True,
                  'assets_do_parse_static': True,
                  'assets_do_exclude_blueprints': None,
                  'assets_do_log': True,
                  'information_page': True}

    def __init__(self, initialize=initialize, **kwargs):
        for k, v in initialize.items():
            setattr(self, k, kwargs.pop(k, v))
        self.app_config = self.check_config(kwargs.pop('app_config', None),
                                            kwargs.pop('app_config_requires',
                                                       None))
        self.initialize_managers(**kwargs)

    def check_config(self, app_config, app_config_requires):
        """Forces a check on your configuration file"""
        if app_config_requires is not None:
            for c in app_config_requires:
                if not hasattr(app_config, c):
                    raise FlailsError('Configuration MUST contain or specify in some manner: {}'.format(c))
        return app_config

    def initialize_managers(self, **kwargs):
        self.app_registrations = self.registration_manager_cls(self)
        self.app_assets = self.assets_manager_cls(self,
                                                  app_asset_env=kwargs.pop('assets_env', None),
                                                  do_exclude_blueprints=kwargs.pop('assets_do_exclude_blueprints', None),
                                                  do_parse_static_main=kwargs.pop('assets_do_parse_static', True),
                                                  do_exclude_files=kwargs.pop('assets_do_exclude_files', []),
                                                  do_log=kwargs.pop('assets_do_log', True))
        self.app_extensions = self.extensions_manager_cls(self)
        self.app_information = self.information_manager_cls
        self.app_blueprints = self.blueprints_manager_cls(self)

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
            self.app_assets.register_assets(app)

        if self.information_page:
            app.register_blueprint(self.info_page_blueprint)

        setattr(self, 'generated_app', app)

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
