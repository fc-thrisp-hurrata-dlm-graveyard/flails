class Flrm(object):
    """
    A route manager for the flails instance
    """
    def __init__(self):
        self.routes = []


    def configure_urls(self, app, routes):
        """
        Connects url patterns to actions for the given wsgi `app`.
        """
        if routes:
            for rule in routes:
                self.routes.append(rule)
                url_rule, endpoint, view_func, opts = self.parse_url_rule(rule)
                app.add_url_rule(url_rule, endpoint=endpoint, view_func=view_func, **opts)


    def parse_url_rule(self, rule):
        """
        Breaks `rule` into `url`, `endpoint`, `view_func` and `opts`
        """
        length = len(rule)
        if length == 4:
            return rule
        elif length == 3:
            rule = list(rule)
            endpoint = None
            opts = {}
            if isinstance(rule[2], dict):
                opts = rule[2]
                view_func = rule[1]
            else:
                endpoint = rule[1]
                view_func = rule[2]
            return (rule[0], endpoint, view_func, opts)
        elif length == 2:
            url_rule, view_func = rule
            return (url_rule, None, view_func, {})
        else:
            raise ValueError('URL rule format not proper {}'.format(rule))
