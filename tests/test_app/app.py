from flask.ext.flails import Flails
from config.settings.default_settings import DefaultConfig

flails_instance = Flails(app_name='test_application',
                         config_obj=DefaultConfig,
                         requested_info=['jinja_env', 'blueprints'])
test_application = flails_instance.create_app()
