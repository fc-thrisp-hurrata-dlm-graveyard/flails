from flask.ext.flails import Flails
from config.settings.default_settings import DefaultConfig

f = Flails('test_application', DefaultConfig)
test_application = f.create_app()
