import os
import pprint
from flask import Flask, Blueprint
from werkzeug import import_string
from flrm import Flrm
from flass import Flass
from flex import Flex

class Flails(object):
    def __init__(self, app_name=None,
                       config_obj=None,
                       requested_info=None,
                       do_register_assets=True):
        self.generated_app = None
        self.generated_app_info = None
        self.app_name = app_name
        self.config_obj = self.check_config(config_obj)
        self.app_root = config_obj.ROOT_DIR
        self.app_routes = Flrm()
        self.app_assets = Flass()
        self.app_extensions = Flex()
        self.requested_info = requested_info
        self.do_register_assets = do_register_assets


    def check_config(self, config_obj):
        check_for = ['ROOT_DIR']
        for c in check_for:
            if not hasattr(config_obj, c):
                raise Exception('Configuration MUST contain or specify in some manner: {}'.format(c))
        return config_obj


    def create_app(self, **kwargs):

        self.create_time_additions('EXTENSIONS', kwargs.pop('extensions', None))
        self.create_time_additions('BLUEPRINTS', kwargs.pop('blueprints', None))

        app = Flask(self.app_name)

        for k in kwargs:
            if k in ('import_name',
                     'static_url_path',
                     'static_folder',
                     'template_folder',
                     'instance_path',
                     'instance_relative_config'):
                setattr(app, k, kwargs.pop(k))

        self.configure_app(app, kwargs.pop('create_time_settings', None))

        for fn, values in [(self.configure_routes,
                            getattr(self.config_obj, 'APP_ROUTES', None)),
                           (self.configure_extensions,
                            getattr(self.config_obj, 'EXTENSIONS', None)),
                           (self.configure_middlewares,
                            getattr(self.config_obj, 'MIDDLEWARES', None)),
                           (self.configure_context_processors,
                            getattr(self.config_obj, 'CONTEXT_PROCESSORS', None)),
                           (self.configure_template_filters,
                            getattr(self.config_obj, 'TEMPLATE_FILTERS', None)),
                           (self.configure_before_handlers,
                            getattr(self.config_obj, 'BEFORE_REQUESTS', None)),
                           (self.configure_after_handlers,
                            getattr(self.config_obj, 'AFTER_REQUESTS', None)),
                           (self.configure_log_handlers,
                            getattr(self.config_obj, 'LOG_HANDLERS', None)),
                           (self.configure_error_handlers,
                            getattr(self.config_obj, 'ERROR_HANDLERS', None)),
                           (self.configure_blueprints,
                            getattr(self.config_obj, 'BLUEPRINTS', None))]:
            if values:
                fn(app, values)

        if self.do_register_assets:
            self.app_assets.register_assets(app)

        self.generated_app = app

        setattr(self, 'generated_app_info', Flinf(self.generated_app,
                                                  self.requested_info))

        return self.generated_app


    def create_time_additions(self, what, to_add):
        if to_add and hasattr(self.config_obj, what):
            x = getattr(self.config_obj, what)
            x.extend(to_add)
        elif to_add:
            setattr(self.config_obj, what, to_add)
        else:
            pass


    def configure_app(self, app, create_time_settings):
        app.config.from_object(self.config_obj)
        if create_time_settings:
            app.config.from_object(create_time_settings)
        app.config.from_envvar("{}_APP_CONFIG".format(self.app_name.upper()), silent=True)


    def configure_routes(self, app, routes):
        """
        Sets application routes from config information provided by both app and blueprints
        using the route manager.
        """
        self.app_routes.configure_urls(app, routes)


    def configure_extensions(self, app, extensions):
        self.app_extensions.configure_extensions(app, extensions)


    def configure_middlewares(self, app, middlewares):
        """
        Adds middlewares to the app.
        """
        if middlewares:
            for m in middlewares:
                if isinstance(m, list) or isinstance(m, tuple):
                    if len(m) == 3:
                        mware, args, kwargs = m
                        new_mware = mware(app.wsgi_app, *args, **kwargs)
                    elif len(m) == 2:
                        mware, args = m
                        if isinstance(args, dict):
                            new_mware = mware(app.wsgi_app, **args)
                        elif isinstance(args, list) or isinstance(args, tuple):
                            new_mware = mware(app.wsgi_app, *args)
                        else:
                            new_mware = mware(app.wsgi_app, args)
                else:
                    new_mware = m(app.wsgi_app)
                app.wsgi_app = new_mware


    def configure_context_processors(self, app, context_processors):
        """
        Sets app wide context processors.
        """
        app.context_processor(lambda: context_processors)


    def configure_app_context_processors(self, app, context_processors):
        """
        Sets app wide context processors from a blueprint.
        """
        app.app_context_processor(lambda: context_processors)


    def configure_template_filters(self, app, template_filters):
        """
        Sets template filters on the jinja2 environment.
        """
        for filter_name, filter_fn in template_filters:
            app.jinja_env.filters[filter_name] = filter_fn


    def configure_before_handlers(self, app, before_handlers):
        """
        Sets before handlers.
        """
        for before in before_handlers:
            before = app.before_request(before)


    def configure_before_app_handlers(self, bp, before_handlers):
        """
        Sets app wide before handlers from a blueprint.
        """
        for before in before_handlers:
            before = bp.before_app_request(before)


    def configure_after_handlers(self, app, after_handlers):
        """
        Sets after handlers.
        """
        for after in after_handlers:
            after = app.after_request(after)


    def configure_after_app_handlers(self, bp, after_handlers):
        """
        Sets app wide after handlers from a blueprint.
        """
        for after in after_handlers:
            after = bp.after_app_request(after)


    def configure_log_handlers(self, app, log_handlers):
        """
        Sets log handlers for the app.
        """
        for handler in log_handlers:
            app.logger.addHandler(handler)


    def configure_error_handlers(self, app, error_handlers):
        """
        Sets custom error handlers.
        """
        for code, fn in error_handlers:
            fn = app.errorhandler(code)(fn)


    def configure_app_error_handlers(self, app, error_handlers):
        """
        Sets app wide custom error handlers from a blueprint.
        """
        for code, fn in error_handlers:
            fn = app.app_errorhandler(code)(fn)


    def configure_blueprints(self, app, blueprints):
        """
        Registers blueprints with the app.
        If you have a preconfigured/complete blueprint, you can skip most of this by
        naming the exportable blueprint as BLUEPRINT
        """
        for blueprint in blueprints:
            url_prefix = None
            if len(blueprint) == 2:
                blueprint, url_prefix = blueprint
            blueprint_object = import_string("{}:BLUEPRINT".format(blueprint), silent=True)#seek multiple
            if not blueprint_object:
                blueprint_name, blueprint_import_name = blueprint.split('.')[-1], blueprint
                options = dict(static_folder='static', template_folder='templates')
                blueprint_object = Blueprint(blueprint_name, blueprint_import_name, **options)
                blueprint_routes = import_string('{}.urls:routes'.format(blueprint_import_name), silent=True)#seek multiple
                if blueprint_routes:
                    self.app_routes.routes.extend(blueprint_routes)
                    self.app_routes.configure_urls(blueprint_object, blueprint_routes)

                for fn, values in [(self.configure_before_handlers,
                                    import_string('{}:BEFORE_REQUESTS'.format(blueprint), silent=True)),
                                   (self.configure_before_app_handlers,
                                    import_string('{}:BEFORE_APP_REQUESTS'.format(blueprint), silent=True)),
                                   (self.configure_after_handlers,
                                    import_string('{}:AFTER_REQUESTS'.format(blueprint), silent=True)),
                                   (self.configure_after_app_handlers,
                                    import_string('{}:AFTER_APP_REQUESTS'.format(blueprint), silent=True)),
                                   (self.configure_context_processors,
                                    import_string('{}:CONTEXT_PROCESSORS'.format(blueprint), silent=True)),
                                   (self.configure_app_context_processors,
                                    import_string('{}:APP_CONTEXT_PROCESSORS'.format(blueprint), silent=True)),
                                   (self.configure_error_handlers,
                                    import_string('{}:ERROR_HANDLERS'.format(blueprint), silent=True)),
                                   (self.configure_app_error_handlers,
                                    import_string('{}:APP_ERROR_HANDLERS'.format(blueprint), silent=True)),
                                 ]:
                    if values:
                        fn(blueprint_object, values)

            if url_prefix:
                app.register_blueprint(blueprint_object, url_prefix=url_prefix)
            else:
                app.register_blueprint(blueprint_object)


class Flinf(object):
    """
    Information about a generated flask application.

    By default, provides the url map and configuration variables of the generated application.

    To return additional information pass a list to requested.
    """

    def __init__(self, app, requested=None):
        self.app = app
        self.provide_information = ['url_map', 'config_vars']
        if requested:
            self.provide_information.extend(requested)
        self.printer = pprint.PrettyPrinter(indent=4)


    @property
    def config_vars(self):
        return {k: v for k,v in self.app.config.iteritems()}


    @property
    def url_map(self):
        return [r for r in self.app.url_map.iter_rules()]


    @property
    def jinja_env(self):
        return self.app.jinja_env.__dict__


    @property
    def asset_env(self):
        return self.jinja_env.get('assets_environment').__dict__


    def return_basic(self, item):
        return getattr(self.app, item, None)


    @property
    def app_information(self):
        to_return  = {}
        for item in self.provide_information:
            to_return[item] = getattr(self, item, self.return_basic(item))
        return to_return


    @property
    def formatted(self):
        self.printer.pprint(self.app_information)
