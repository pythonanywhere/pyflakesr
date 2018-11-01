import _ast
from pyflakes.checker import Checker
import bottle


def pyflakes_check(code):
    try:
        tree = compile(code, "ignored.py", "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError as syntax_error:
        return [dict(text='Syntax Error', row=syntax_error.lineno - 1, type='error')]
    except ValueError as value_error:
        message = 'Error: {} somewhere in file'.format(value_error.message)
        return [dict(text=message, row=0, type='error')]

    w = Checker(tree, '')
    return [
        dict(text=m.message % m.message_args, row=m.lineno - 1, type='warning')
        for m in w.messages
    ]


ALLOWED_ORIGINS = [
    "https://www.pythonanywhere.com",
    "https://www.pythonanywhere.eu",
    "https://eu.pythonanywhere.com",
    "https://region.pythonanywhere.integration",
    "https://www.pythonanywhere.conrad",
    "https://foo.pythonanywhere.giles",
    "https://www.pythonanywhere.glenn",
    "https://www.pythonanywhere.fjl",
]

@bottle.route('/', method='POST')
def hello_world():
    code = bottle.request.forms.get('code')
    origin = bottle.request.headers.get('Origin', '')
    for allowed_origin in ALLOWED_ORIGINS:
        if origin == allowed_origin:
            bottle.response.headers['Access-Control-Allow-Origin'] = origin
            break

    return dict(errors=pyflakes_check(code))

application = bottle.default_app()
