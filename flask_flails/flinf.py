import pprint

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
