from flask import Blueprint
from werkzeug import import_string

class Flab(object):
    """
    Flails blueprint management
    """
    def __init__(self, flail):
        self.flail = flail
        self.registrations = flail.app_registrations.blueprint_actions

    def configure_blueprints(self, app, blueprints):
        """
        Registers blueprints with the app.
        If you have a preconfigured/complete blueprint, you can skip most
        registration steps by naming the exportable blueprint as BLUEPRINT which
        is simply registered on application without further processing. Otherwise
        you can set up a bluperint with a file structure:

            |my_blueprint
            |------- __init__.py
            |------- views.py
            |-------| static
            |-------|------- css, etc.
            |-------| templates
            |-------|------- templates, etc.

        Place any of:

        before_requests, before_app_requests, after_requests, after_app_requests,
        context_processors, app_context_processors, error_handlers,
        app_error_handlers, view_handlers

        in the __init__ file as ALL_CAP constants.
        """
        if getattr(app, 'views_folder', None):
            register_on = "{}.{}".format(self.flail.app_inside_module, 'views')
            view_blueprint = self.make_blueprint('views', register_on)
            self.register_blueprint_actions(register_on, view_blueprint)
            self.register_blueprint(app, view_blueprint)

        if blueprints:
            for blueprint in blueprints:
                url_prefix = None
                if len(blueprint) == 2:
                    blueprint, url_prefix = blueprint
                has_blueprint = "{}:BLUEPRINT".format(blueprint)
                blueprint_object = import_string(has_blueprint, silent=True)

                if not blueprint_object:
                    blueprint_name = blueprint.split('.')[-1]
                    blueprint_import_name = blueprint
                    blueprint_object = self.make_blueprint(blueprint_name,
                                                           blueprint_import_name)

                    self.register_blueprint_actions(blueprint,
                                                    blueprint_object)

                self.register_blueprint(app, blueprint_object, url_prefix=url_prefix)

    def make_blueprint(self, blueprint_name, blueprint_import_name):
        options = dict(static_folder='static', template_folder='templates')
        return Blueprint(blueprint_name, blueprint_import_name, **options)

    def register_blueprint_actions(self, blueprint, blueprint_object):
        for k,v in self.registrations.iteritems():
            action = '{}:{}'.format(blueprint, k.upper())
            fn, values = v, import_string(action, silent=True)
            if values:
                fn(blueprint_object, values)

    def register_blueprint(self, app, blueprint_object, url_prefix=None):
        if url_prefix:
            app.register_blueprint(blueprint_object, url_prefix=url_prefix)
        else:
            app.register_blueprint(blueprint_object)
