from flask.ext.flails import Flails
from config.settings.default_settings import DefaultConfig

flails_instance = Flails('test_application', DefaultConfig)
test_application = flails_instance.create_app()
