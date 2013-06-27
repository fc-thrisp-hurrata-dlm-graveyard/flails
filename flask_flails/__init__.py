__version_info__ = ('0', '0', '3')
__version__ = '.'.join(__version_info__)
from .flails import Flails
from .flex import ExtensionConfig
from flask.ext.classy import FlaskView as FlailsView
from flask.ext.classy import route as route
