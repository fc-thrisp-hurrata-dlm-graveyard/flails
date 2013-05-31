from flask import Blueprint
from werkzeug import import_string

class Flab(object):
    def __init__(self, flail):
        self.flail = flail
        self.registrations = flail.app_registrations.blueprint_actions

    def configure_blueprints(self, app, blueprints):
        """
        Registers blueprints with the app.
        If you have a preconfigured/complete blueprint, you can skip past most
        registration steps by naming the exportable blueprint as BLUEPRINT which
        is simply registered on application without further processing
        """
        if getattr(app, 'views_folder', None):
            register_on = self.flail.app_inside_module
            view_blueprint = self.make_blueprint('views', self.flail.app_inside_module)
            #register views
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
                    blueprint_object = self.make_blueprint(blueprint_name, blueprint_import_name)

                    for k,v in self.registrations.iteritems():
                        action = '{}:{}'.format(blueprint, k.capitalize())
                        fn, values = v, import_string(action, silent=True)
                        if values:
                            fn(blueprint_object, values)

                    self.register_blueprint(app, blueprint_object, url_prefix=url_prefix)

    def make_blueprint(self, blueprint_name, blueprint_import_name):
        options = dict(static_folder='static', template_folder='templates')
        try:
            return Blueprint(blueprint_name,
                             blueprint_import_name,
                             **options)
        except:
            #if in the actual application folder, this seems needed, if inelegant
            return Blueprint(blueprint_name,
                             blueprint_import_name.split('.')[-1],
                             **options)

    def register_blueprint(self, app, blueprint_object, url_prefix=None):
        if url_prefix:
            app.register_blueprint(blueprint_object, url_prefix=url_prefix)
        else:
            app.register_blueprint(blueprint_object)
