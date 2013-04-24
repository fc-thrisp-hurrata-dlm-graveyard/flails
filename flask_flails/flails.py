import os
import pprint
from flask import Flask, Blueprint, current_app
from werkzeug import import_string, cached_property

class Flails(object):

    def __init__(self, app_name=None, config_obj=None):
        self.generated_app = None
        self.app_name = app_name
        self.check_config(config_obj)
        self.config_obj = config_obj
        self.app_root = config_obj.ROOT_DIR
        self.app_routes = RoutesManager()


    def check_config(self, config_obj):
        check_for = ['ROOT_DIR']
        for c in check_for:
            if not hasattr(config_obj, c):
                raise Exception('Configuration MUST contain or specify in some manner: {}'.format(c))


    @cached_property
    def template_dir(self):
        return os.path.join(os.path.dirname(os.path.abspath(self.app_root)), 'templates')


    @cached_property
    def static_dir(self):
        return os.path.join(os.path.dirname(os.path.abspath(self.app_root)), 'static')


    def create_time_additions(self, what, to_add):
        if to_add and hasattr(self.config_obj, what):
            x = getattr(self.config_obj, what)
            x.extend(to_add)
        elif to_add:
            setattr(self.config_obj, what, to_add)
        else:
            pass

    def create_app(self,
                   settings=None,
                   extensions=None,
                   blueprints=None):

        self.create_time_additions('EXTENSIONS', extensions)
        self.create_time_additions('BLUEPRINTS', blueprints)

        app = Flask(self.app_name,
                    template_folder=self.template_dir,
                    static_folder=self.static_dir)

        self.configure_app(app, settings)

        for fn, values in [(self.configure_extensions,
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

        if hasattr(self.config_obj, 'APP_ROUTES'):
            self.app_routes.set_urls(app, self.config_obj.APP_ROUTES)
        self.generated_app = app
        return self.generated_app


    def configure_app(self, app, config):
        app.config.from_object(self.config_obj)
        if config is not None:
            app.config.from_object(config)
        app.config.from_envvar("{}_APP_CONFIG".format(self.app_name.upper()), silent=True)


    def configure_extensions(self, app, extensions):
        for extension in extensions:
            try:
                extension.initiate(app)
            except Exception as e:
               raise Exception("""
                               could not register extension with application\n
                               {}
                               """.format(e))


    def configure_middlewares(self, app, middlewares):
        pass


    def configure_context_processors(self, app, context_processors):
        app.context_processor(lambda: context_processors)


    def configure_app_context_processors(self, app, context_processors):
        app.app_context_processor(lambda: context_processors)


    def configure_template_filters(self, app, template_filters):
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
        Sets before handlers.
        When called from a blueprint, works on the application level rather than blueprint level.
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
        Sets after handlers.
        When called from a blueprint, works on the application level rather than blueprint level.
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
        for code, fn in error_handlers:
            fn = app.errorhandler(code)(fn)


    def configure_app_error_handlers(self, app, error_handlers):
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
            blueprint_object = import_string("{}:BLUEPRINT".format(blueprint), silent=True)
            if not blueprint_object:
                blueprint_name, blueprint_import_name = blueprint.split('.')[-1], blueprint
                options = dict(static_folder='static', template_folder='templates')
                blueprint_object = Blueprint(blueprint_name, blueprint_import_name, **options)
                blueprint_routes = import_string('{}.urls:routes'.format(blueprint_import_name), silent=True)
                import_string('{}.urls:routes'.format(blueprint_import_name))
                if blueprint_routes:
                    self.app_routes.routes.extend(blueprint_routes)
                    self.app_routes.set_urls(blueprint_object, blueprint_routes)

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


    def app_info(self, *args):
        ''' information about your generated flask application'''
        pp = pprint.PrettyPrinter(indent=4)
        if args:
            info_list = list(args)
        else:
            info_list = []
        config_var_list = []
        for k, v in self.generated_app.config.iteritems():
            config_var_list.append("{}: {}".format(k, v))
        info_list.append(config_var_list)
        url_map_list = []
        for i in self.generated_app.url_map.iter_rules():
            url_map_list.append(i)
        info_list.append(url_map_list)
        for item in info_list:
            if isinstance(item, list):
                pp.pprint(item)
            if isinstance(item, str):
                k = "{}".format(str(item))
                pp.pprint({k: getattr(self.generated_app, k)})
        #pp.pprint(self.app_routes.routes)
        return info_list


class RoutesManager(object):
    def __init__(self):
        self.routes = []

    def set_urls(self, app, routes):
        """
        Connects url patterns to actions for the given wsgi `app`.
        """
        if routes:
            for rule in routes:
                # Set url rule.
                self.routes.append(rule)
                url_rule, endpoint, view_func, opts = self.parse_url_rule(rule)
                app.add_url_rule(url_rule, endpoint=endpoint, view_func=view_func, **opts)


    def parse_url_rule(self, rule):
        """
        Breaks `rule` into `url`, `endpoint`, `view_func` and `opts`
        """
        length = len(rule)
        if length == 4:
            # No processing required.
            return rule
        elif length == 3:
            rule = list(rule)
            endpoint = None
            opts = {}
            if isinstance(rule[2], dict):
                # Options passed.
                opts = rule[2]
                view_func = rule[1]
            else:
                # Endpoint passed.
                endpoint = rule[1]
                view_func = rule[2]
            return (rule[0], endpoint, view_func, opts)
        elif length == 2:
            url_rule, view_func = rule
            return (url_rule, None, view_func, {})
        else:
            raise ValueError('URL rule format not proper {}'.format(rule))


class ExtensionConfig(object):
    """
    A wrapper for extension registry

    defaults to to registering an extension to the app provided by:

        by_class: ExtensionObject(app, *options, **options)

    alternately

        by_init: ExtensionObject.init_app(app, *options, **options)

    Other extension registration methods should subclass and customize this class.

    """
    def __init__(self, extension_class, init_type='by_class', *args, **kwargs):
        self.extension_class = extension_class
        self.init_type = init_type
        self.args = args
        self.kwargs = kwargs

    def initiate(self, app):
        try:
            return getattr(self, self.init_type, None)(app)
        except:
            raise Exception("{}").format(e)

    def by_class(self, app):
        return self.extension_class(app, *self.args, **self.kwargs)

    def by_init(self, app):
        return self.extension_class.init_app(app, *self.args, **self.kwargs)

    def __repr__(self):
        return "<ExtensionConfig object: {}, args: {}, kwargs: {}>".format \
                (self.extension_class.__name__,
                 self.args,
                 self.kwargs)
