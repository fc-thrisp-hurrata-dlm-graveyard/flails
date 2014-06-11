import os
from flask.ext.assets import Environment, Bundle


class Flass(object):
    """Flask asset registration"""

    def __init__(self,
                 flail,
                 **kwargs):
        self.flail = flail
        self.app_asset_env = self.set_env(kwargs.pop('app_asset_env', None))
        self.parse_static_main = kwargs.pop('parse_static_main', True)
        self._exclude_blueprints = ['debugtoolbar', '_uploads', '_themes']
        if kwargs.get('exclude_blueprints', None):
            self._exclude_blueprints.extend(kwargs.pop('exclude_blueprints'))
        self.exclude_files = kwargs.pop('exclude_files', [])
        self.do_log = kwargs.pop('do_log', True)

    def set_env(self, app_asset_env):
        if not app_asset_env:
            app_asset_env = Environment()
        return app_asset_env

    def register_assets(self, app):
        """Registers all css and js assets with application"""

        setattr(self, 'app', app)

        if app is not None:
            self.register_env()

            self.register_env_fleem()

            setattr(self, 'asset_env', self.app.jinja_env.assets_environment)

            setattr(self, 'static_folder', self.app.static_folder)

            self.gather_raw_files

            if self.raw_files:
                self.gather_js(self.raw_files)
                self.gather_css(self.raw_files)

    def register_env(self):
        if self.app_asset_env:
            self.app_asset_env.init_app(self.app)

    def register_env_fleem(self):
        if self.app.extensions.get('fleem_manager'):
            self.app.extensions['fleem_manager'].asset_env = self.app.jinja_env.assets_environment
            self.app.extensions['fleem_manager'].refresh()

    @property
    def gather_raw_files(self):
        raw = {'css': [], 'less': [], 'js': [], 'coffee': []}
        static_raw = self.static_main(raw)
        blueprint_raw = self.static_blueprints(static_raw)
        setattr(self, 'raw_files', blueprint_raw)
        self.log_actions("raw files: {}".format(self.raw_files))

    def static_main(self, raw):
        if self.parse_static_main:
            for k in raw.keys():
                raw[k].extend(self._get_files(self.static_folder, k, k))
        return raw

    def static_blueprints(self, raw):
        for name, bp in self._asset_blueprints.items():
            if bp.static_folder:
                for k in raw.keys():
                    raw[k].extend(self._bp_name(name,
                                                self._get_files(bp.static_folder,
                                                                k, k)))
        return raw

    @property
    def _asset_blueprints(self):
        return {name: bp for name, bp in self.app.blueprints.items()
                if self.app and name not in self._exclude_blueprints}

    def _bp_name(self, name, files):
        return ['{}/{}'.format(name, f) for f in files]

    def _get_files(self, static_folder, folder, extension):
        files_list = []
        for root, dirs, files in os.walk(os.path.join(static_folder, folder)):
            for file in files:
                if file.endswith(".{}".format(extension))\
                        and all(file != s for s in self.exclude_files):
                    path_parts = self._splitall(root)
                    static_index = path_parts.index("static")
                    path_parts = path_parts[static_index + 1:]
                    path_parts.append(file)
                    files_list.append('/'.join(path_parts))
        return files_list

    def _splitall(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path:
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    def gather_js(self, raw_files):
        js_contents = []

        if raw_files['js']:
            js_contents.append(self.make_bundle(raw_files['js']))
        if raw_files['coffee']:
            js_contents.append(self.make_bundle(raw_files['coffee'],
                                                filters='coffeescript',
                                                output='js/coffee_all.js'))

        if js_contents:
            js_all = self.make_bundle(js_contents,
                                      filters='rjsmin',
                                      output='js/application.js')
            self.register_asset('js_all', js_all)
        if self.do_log:
            self.log_actions(self.manifest("js_all",
                                           ".js",
                                           [x.contents for x in js_contents]))

    def gather_css(self, raw_files):
        css_contents = []

        if raw_files['css']:
            css_contents.append(self.make_bundle(raw_files['css']))
        if raw_files['less']:
            css_contents.append(self.make_bundle(raw_files['less'],
                                                 filters='less',
                                                 output='css/less_all.css'))

        if css_contents:
            css_all = self.make_bundle(css_contents,
                                       filters='cssmin',
                                       output='css/application.css')
            self.register_asset('css_all', css_all)
        if self.do_log:
            self.log_actions(self.manifest("css_all",
                                           ".css",
                                           [x.contents for x in css_contents]))

    def make_bundle(self, contents, filters=None, output=None):
        return Bundle(*contents, filters=filters, output=output)

    def register_asset(self, name, bundle):
        self.asset_env.register(name, bundle)

    def manifest(self, name, extension, resources):
        return "{} for {} == {}".format(extension, name, resources)

    def log_actions(self, message):
        self.app.logger.info(message)
