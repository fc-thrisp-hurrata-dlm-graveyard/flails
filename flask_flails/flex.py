import re
from operator import attrgetter
from copy import copy
import inspect

MATCH_EXTENSION = re.compile(".*_EXTENSION\Z")

class Flex(object):
    """
    Flask extension registration
    """
    def __init__(self, flail):
        self.flail = flail

    def gather_extensions(self, app_config):
        return [v for k,v in inspect.getmembers(app_config)
            if MATCH_EXTENSION.match(k)]

    def extend_extensions(self, app_config):
        e = app_config.EXTENSIONS
        [e.append(oe) for oe in self.gather_extensions(app_config)]
        return e

    def order_extensions(self, extensions):
        return sorted(extensions, key=attrgetter('precedence'))

    def wrap_extension(self, e):
        if isinstance(e, dict):
            f = copy(e)
            extension_class = f.pop('extension', None)
            args = f.pop('args', None)
            kwargs = f
            if args:
                return ExtensionConfig(extension_class, *args, **kwargs)
            else:
                return ExtensionConfig(extension_class, **kwargs)
        else:
            return e

    def wrap_extensions(self, extensions):
        return [self.wrap_extension(e) for e in extensions]

    def configure_extension(self, app, extension):
        try:
            extension.initiate(app)
        except Exception as e:
            print "CONFIGURE EXTENSION ERROR"
            raise e

    def configure_extensions(self, app, app_config):
        exts = self.extend_extensions(app_config)
        wrapped = self.wrap_extensions(exts)
        ordered = self.order_extensions(wrapped)
        [self.configure_extension(app, extension) for extension in ordered]
        self.extensions = ordered
        print self.extensions


class ExtensionConfig(object):
    """
    A configuration wrapper for extension registry.

    :param init_type: How the extension will be registeres defaults to
                      'by_class' which registers the extension by:

                      ExtensionToBeRegistered(app, *options, **options)

                      by_init registers the extension (Usually a preconfigured
                      instance) by an init_app method:

                      ExtensionToBeRegistered.init_app(app, *options, **options)

    :param precedence: You can gain control over ordering of extension
                       intialization where order is needed by optionally
                       setting precedence as an integer, default is 100.

    Other extension registration methods should subclass and customize this
    class.
    """
    def __init__(self, extension_class, *args, **kwargs):
        self.extension_class = extension_class
        self.init_type = kwargs.pop('init_type', 'by_class')
        self.precedence = kwargs.pop('precedence', 100)
        self.args = args
        self.kwargs = kwargs

    def initiate(self, app):
        try:
            print "initiating....{}".format(self)
            return getattr(self, self.init_type, None)(app)
        except Exception as e:
            raise e

    def by_class(self, app):
        return self.extension_class(app, *self.args, **self.kwargs)

    def by_init(self, app):
        return self.extension_class.init_app(app, *self.args, **self.kwargs)

    def __repr__(self):
        return "<ExtensionConfig for: ({}, args: {}, kwargs: {}, precedence: {})>"\
                .format\
                (self.extension_class,
                 self.args,
                 self.kwargs,
                 self.precedence)
