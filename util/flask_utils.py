from collections import Iterable

import flask
from flask import Flask
from flask import Response
from flask import redirect
from flask import url_for

from default_template_context import get_default_template_context
from template_context import context


def reroute(route_func):
    # type: (callable) -> Response
    """
    Wrap redirect(url_for(...)) for route.func_name.

    :param route_func: the route function to redirect to
    :return: the Response from redirect(url_for(route.func_name))
    """
    return redirect(url_for(route_func.func_name))


_super_route = Flask.route


def route(app, rule, **options):
    def decorator(route_func):
        route_func = _super_route(app, rule, **options)(route_func)

        def url():
            return url_for(route_func.func_name)

        route_func.url = url
        context[route_func.func_name] = route_func
        return route_func

    return decorator


# override
Flask.route = route
del route


def redirect_from(app, rule, **options):
    # type: (Flask, str, dict[str, any]) -> callable
    """
    Redirect the given rule and options to the route it is decorating.

    :param app: this app
    :param rule: rule from @app.route
    :param options: options from @app.route
    :return: a decorator that adds the redirecting logic
    """

    def decorator(func_to_redirect):
        # type: (callable) -> callable
        """
        Decorate a route function to add another route that redirects to this one.

        :param func_to_redirect: the route function to redirect
        :return: the original func_to_redirect
        """

        def redirector():
            # type: () -> Response
            """
            The actual route function that accomplishes the redirecting.

            :return: the redirected Response
            """
            return reroute(func_to_redirect)

        # uniquely modify the redirector name
        # so @app.route will have a unique function name
        # the next time redirect_from is called
        redirector.func_name += '_for_' + func_to_redirect.func_name
        app.route(rule, **options)(redirector)

        return func_to_redirect

    return decorator


# extension method
Flask.redirect_from = redirect_from
del redirect_from

_render_template = flask.render_template

OVERRIDE_RENDER_TEMPLATE = False

if OVERRIDE_RENDER_TEMPLATE:
    def render_template(template_name_or_list, **context):
        # type: (str | Iterable[str], dict[str, any]) -> Response
        """
        Wrap flask.render_template to add default template args.

        :param template_name_or_list: the template name(s)
        :param context: original context
        :return: the Response from flask.render_template
        """
        return _render_template(template_name_or_list, **get_default_template_context(context))


    flask.render_template = render_template
    del render_template
