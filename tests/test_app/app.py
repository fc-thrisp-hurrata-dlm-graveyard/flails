from flask.ext.flails import Flails
from config.settings.default_settings import DefaultConfig
import os

local_path = os.path.dirname(__file__)
flails_instance = Flails(app_name='test_application',
                         config_obj=DefaultConfig,
                         requested_info=['jinja_env', 'blueprints', 'asset_env'])
test_application = flails_instance.create_app(static_folder=os.path.join(local_path, 'static'))
