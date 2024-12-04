import _ast
from pyflakes.checker import Checker
from flask import Flask, Response, request

application = Flask(__name__)

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


@application.route('/', methods=['POST'])
def check_code():
    code = request.form.get('code')
    return {"errors": pyflakes_check(code)}, 200, {'Access-Control-Allow-Origin':"REPLACE_WITH_REAL_ALLOWED_ORIGIN"}

