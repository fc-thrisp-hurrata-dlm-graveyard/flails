import glob
from flask.ext.assets import Environment, Bundle

class Flass(object):
    """
    Flask asset registration
    """
    def __init__(self):
        self.app_asset_env = None
        self.js_files = None
        self.css_files = None


    def register_app_env(self, app):
        self.app_asset_env = Environment(app)


    def register_assets(self, app):
        """
        Registers all css and js assets with application
        """
        if self.app_asset_env is None:
            self.register_app_env(app)

        asset_env = self.app_asset_env

        static_folder = app.static_folder
        css_files = self._get_css_files(static_folder)
        less_files = self._get_less_files(static_folder)
        js_files = self._get_js_files(static_folder)
        coffee_files = self._get_coffee_files(static_folder)

        for name, bp in app.blueprints.iteritems():
            if name == 'debugtoolbar':
                continue
            bp_static_folder = bp.static_folder
            if bp_static_folder:
                css_files.extend(self._append_blueprint_name(name, self._get_css_files(bp_static_folder)))
                less_files.extend(self._append_blueprint_name(name, self._get_less_files(bp_static_folder)))
                js_files.extend(self._append_blueprint_name(name, self._get_js_files(bp_static_folder)))
                coffee_files.extend(self._append_blueprint_name(name, self._get_coffee_files(bp_static_folder)))

        js_contents = []
        if js_files:
            js_contents.append(Bundle(*js_files))
        if coffee_files:
            js_contents.append(Bundle(*coffee_files, filters='coffeescript', output='js/coffee_all.js'))
        if js_contents:
            js_all = Bundle(*js_contents, filters='closure_js', output='js/application.js')
            asset_env.register('js_all', js_all)
            asset_env.register('js_all_compressed', js_all, filters='gzip', output='js/application.js.gz')


        css_contents = []
        if css_files:
            css_contents.append(Bundle(*css_files))
        if less_files:
            css_contents.append(Bundle(*less_files, filters='less', output='css/less_all.css'))
        if css_contents:
            css_all = Bundle(*css_contents,
                             filters='cssmin', output='css/application.css')
            asset_env.register('css_all', css_all)
            asset_env.register('css_all_compressed', css_all, filters='gzip', output='css/application.css.gz')


    def _get_resource_files(self, static_folder, resource_folder, resource_ext):
        return [file[len(static_folder) + 1:] for file in
                glob.glob('{}/{}/*.{}'.format(static_folder, resource_folder, resource_ext))]


    def _get_css_files(self, static_folder):
        return self._get_resource_files(static_folder, 'css', 'css')


    def _get_less_files(self, static_folder):
        return self._get_resource_files(static_folder, 'css', 'less')


    def _get_js_files(self, static_folder):
        return self._get_resource_files(static_folder, 'js', 'js')


    def _get_coffee_files(self, static_folder):
        return self._get_resource_files(static_folder, 'js', 'coffee')


    def _append_blueprint_name(self, name, files):
        return ['{}/{}'.format(name, f) for f in files]
