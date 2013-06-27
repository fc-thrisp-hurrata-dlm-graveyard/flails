import re
from operator import attrgetter

MATCH_EXTENSION = re.compile(".*_EXTENSION\Z")

class Flex(object):
    """
    Flask extension registration
    """
    def __init__(self, flail, **kwargs):
        self.flail = flail
        if kwargs:
            self.initialize_extensions(kwargs)

    def extend_extensions(self, app_config):
        other_extensions = (x for x in dir(app_config)
                            if not x.startswith('_')
                            and MATCH_EXTENSION.match(x))
        for oe in other_extensions:
            app_config.EXTENSIONS.append(getattr(app_config, oe))

    def order_extensions(self, extensions):
        return sorted(extensions, key=attrgetter('precedence'))

    def initialize_extensions(self, extensions):
        self.extensions = extensions
        if self.extensions:
            for e in self.extensions:
                if not isinstance(e, ExtensionConfig):
                    if isinstance(e, dict):
                        extension_class = e['extension']
                        args = e['args']
                        kwargs = e['kwargs']
                        e = ExtensionConfig(extension_class, *args, **kwargs)

    def configure_extensions(self, app, app_config):
        self.extend_extensions(app_config)
        extensions = self.order_extensions(app_config.EXTENSIONS)
        if extensions:
            self.initialize_extensions(extensions)
        for extension in self.extensions:
            try:
                extension.initiate(app)
            except Exception as e:
               raise e


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
            return getattr(self, self.init_type, None)(app)
        except Exception as e:
            raise

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
