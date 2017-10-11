def if_else(first, a, b):
    # type: (bool, any, any) -> any
    """
    Functional equivalent of conditional expression.

    :param first: True or False
    :param a: to be returned if first is True
    :param b: to be returned if first is False
    :return: a if first else b
    """
    return a if first else b


def repeat(s, n):
    # type: (str, int) -> str
    return s * n


def br(n):
    # type: (int) -> str
    """
    Concisely create many <br> tags.

    :param n: number of <br> to retur
    :return: n <br> tags
    """
    return repeat('<br>', n)


class TemplateVars(object):
    """
    TODO
    """

    def __init__(self):
        self.vars = {}

    def set(self, **kwargs):
        # type: (dict[str, any]) -> str
        self.vars.update(kwargs)
        return ''

    def get(self, name):
        # type: (str) -> any
        return self.vars[name]

    def get_safe(self, name, default=None):
        # type (str, any) -> any
        return self.vars.get(name, default)


DEFAULT_TEMPLATE_CONTEXT = dict(
    if_else=if_else,
    repeat=repeat,
    br=br,
)


def get_default_template_context(**context):
    # type: (dict[str, any]) -> dict[str, any]
    # TODO
    new_context = DEFAULT_TEMPLATE_CONTEXT.copy()
    new_context.update(context)
    return new_context
