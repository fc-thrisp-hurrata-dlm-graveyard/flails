class Flap(object):
    """Common registration methods for applications & blueprints"""
    def __init__(self, flail):
        self.flail = flail

    def configure_context_processors(self, app, context_processors):
        """Sets app wide context processors."""
        app.context_processor(lambda: context_processors)

    def configure_app_context_processors(self, app, context_processors):
        """Sets app wide context processors from a blueprint."""
        app.app_context_processor(lambda: context_processors)

    def configure_jinja_globals(self, app, jinja_globals):
        for k, v in jinja_globals.items():
            app.jinja_env.globals[k] = v

    def configure_template_filters(self, app, template_filters):
        """Sets template filters on the jinja2 environment."""
        for filter_name, filter_fn in template_filters:
            app.jinja_env.filters[filter_name] = filter_fn

    def configure_before_handlers(self, app, before_handlers):
        """Sets before handlers."""
        for before in before_handlers:
            before = app.before_request(before)

    def configure_before_app_handlers(self, app, before_handlers):
        """Sets app wide before handlers from a blueprint."""
        for before in before_handlers:
            before = app.before_app_request(before)

    def configure_after_handlers(self, app, after_handlers):
        """Sets after handlers."""
        for after in after_handlers:
            after = app.after_request(after)

    def configure_after_app_handlers(self, app, after_handlers):
        """Sets app wide after handlers from a blueprint."""
        for after in after_handlers:
            after = app.after_app_request(after)

    def configure_log_handlers(self, app, log_handlers):
        """Sets log handlers for the app."""
        for handler in log_handlers:
            app.logger.addHandler(handler)

    def configure_error_handlers(self, app, error_handlers):
        """Sets custom error handlers."""
        for code, fn in error_handlers:
            fn = app.errorhandler(code)(fn)

    def configure_app_error_handlers(self, app, error_handlers):
        """Sets app wide custom error handlers from a blueprint."""
        for code, fn in error_handlers:
            fn = app.app_errorhandler(code)(fn)

    def configure_views(self, app, views):
        for v in views:
            try:
                getattr(v, 'register')(app)
            except Exception as e:
                Exception(e)

    def configure_middlewares(self, app, middlewares):
        """Adds middlewares to the app."""
        if middlewares:
            for m in middlewares:
                if isinstance(m, list) or isinstance(m, tuple):
                    if len(m) == 3:
                        mware, args, kwargs = m
                        new_mware = mware(app.wsgi_app, *args, **kwargs)
                    elif len(m) == 2:
                        mware, args = m
                        if isinstance(args, dict):
                            new_mware = mware(app.wsgi_app, **args)
                        elif isinstance(args, list) or isinstance(args, tuple):
                            new_mware = mware(app.wsgi_app, *args)
                        else:
                            new_mware = mware(app.wsgi_app, args)
                else:
                    new_mware = m(app.wsgi_app)
                app.wsgi_app = new_mware

    @property
    def app_actions(self):
        return {'before_requests': self.configure_before_handlers,
                'after_requests': self.configure_after_handlers,
                'context_processors': self.configure_context_processors,
                'jinja_globals': self.configure_jinja_globals,
                'template_filters': self.configure_template_filters,
                'error_handlers': self.configure_error_handlers,
                'log_handlers': self.configure_log_handlers,
                'middleware': self.configure_middlewares}

    @property
    def blueprint_actions(self):
        return {'before_requests': self.configure_before_handlers,
                'before_app_requests': self.configure_before_app_handlers,
                'after_requests': self.configure_after_handlers,
                'after_app_requests': self.configure_after_app_handlers,
                'context_processors': self.configure_context_processors,
                'app_context_processors': self.configure_app_context_processors,
                'error_handlers': self.configure_error_handlers,
                'app_error_handlers': self.configure_app_error_handlers,
                'view_handlers': self.configure_views}
