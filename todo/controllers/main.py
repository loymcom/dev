from odoo import http
from odoo.http import request
import json

class Todo(http.Controller):
    @http.route('/todo/todo/', auth='public')
    def index(self, **kw):
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info())
        }
        # todo.index is the xml template that contains
        # main html content 
        return request.render('todo.index', qcontext=context)