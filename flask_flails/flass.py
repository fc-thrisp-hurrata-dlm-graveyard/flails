import glob
from flask.ext.assets import Environment, Bundle
from time import time
import os
import pprint

class Flass(object):
    """
    Flask asset registration
    """
    def __init__(self, parse_static_main=True,
                       exclude_blueprints=None):
        self.app_asset_env = None
        self.js_content = None
        self.css_content = None
        self.parse_static_main = parse_static_main
        self._exclude_blueprints = ['debugtoolbar', '_uploads', '_themes']
        if exclude_blueprints:
            self._exclude_blueprints.extend(exclude_blueprints)

    def set_env(self):
        #provide support for configuration of the environment
        self.app_asset_env = Environment()

    def register_env(self, app):
        env = self.app_asset_env
        env.init_app(app)

    def register_env_fleem(self, app):
        app.extensions['fleem_manager'].asset_env = app.jinja_env.assets_environment
        app.extensions['fleem_manager'].refresh()

    def manifest(self, where, name, extension, resources):
        filename = "{}.manifest".format(name)
        entry = "{} for {} == {}".format(extension,
                                         name,
                                         resources)

        try:
            f = open(os.path.join(where, filename), 'a')
        except:
            f = open(os.path.join(os.getcwd(), filename), 'a')

        f.write("{}:: {}\n".format(time(), entry))

    def register_assets(self, app):
        """
        Registers all css and js assets with application
        """

        self.register_env(app)

        if app.extensions.get('fleem_manager'):
            self.register_env_fleem(app)

        asset_env = app.jinja_env.assets_environment

        static_folder = app.static_folder

        css_files, less_files, js_files, coffee_files = [],[],[],[]

        if self.parse_static_main:
            css_files.extend(self._get_css(static_folder))
            less_files.extend(self._get_less(static_folder))
            js_files.extend(self._get_js(static_folder))
            coffee_files.extend(self._get_coffee(static_folder))

        if app.blueprints:
            blueprints = {name: bp for name,bp in app.blueprints.iteritems()\
                          if name not in self._exclude_blueprints}

            for name, bp in blueprints.iteritems():
                if bp.static_folder:
                    css_files.extend(self._append_bp_name(name,
                                                          self._get_css(bp.static_folder)))
                    less_files.extend(self._append_bp_name(name,
                                                           self._get_less(bp.static_folder)))
                    js_files.extend(self._append_bp_name(name,
                                                         self._get_js(bp.static_folder)))
                    coffee_files.extend(self._append_bp_name(name,
                                                             self._get_coffee(bp.static_folder)))

        js_contents = []
        if js_files:
            js_contents.append(Bundle(*js_files))
        if coffee_files:
            js_contents.append(Bundle(*coffee_files,
                                      filters='coffeescript',
                                      output='js/coffee_all.js'))
        if js_contents:
            js_all = Bundle(*js_contents,
                            filters='rjsmin',
                            output='js/application.js')
            asset_env.register('js_all',
                               js_all)
            asset_env.register('js_all_compressed',
                               js_all, filters='gzip',
                               output='js/application.js.gz')
        self.js_content = js_contents
        self.manifest(static_folder,
                      "js_all",
                      ".js",
                      [x.contents for x in js_contents])

        css_contents = []
        if css_files:
            css_contents.append(Bundle(*css_files))
        if less_files:
            css_contents.append(Bundle(*less_files,
                                       filters='less',
                                       output='css/less_all.css'))

        if css_contents:
            css_all = Bundle(*css_contents,
                             filters='cssmin',
                             output='css/application.css')
            asset_env.register('css_all',
                               css_all)
            asset_env.register('css_all_compressed',
                               css_all, filters='gzip',
                               output='css/application.css.gz')
        self.css_content = css_contents
        self.manifest(static_folder,
                      "css_all",
                      ".css",
                      [x.contents for x in css_contents])

    def _get_resource_files(self,
                            static_folder,
                            resource_folder,
                            resource_ext):
        return [file[len(static_folder) + 1:] for file in\
                glob.glob('{}/{}/*.{}'.format(static_folder,
                                              resource_folder,
                                              resource_ext))]

    def _get_css(self, static_folder):
        return self._get_resource_files(static_folder, 'css', 'css')

    def _get_less(self, static_folder):
        return self._get_resource_files(static_folder, 'css', 'less')

    def _get_js(self, static_folder):
        return self._get_resource_files(static_folder, 'js', 'js')

    def _get_coffee(self, static_folder):
        return self._get_resource_files(static_folder, 'js', 'coffee')

    def _append_bp_name(self, name, files):
        return ['{}/{}'.format(name, f) for f in files]
