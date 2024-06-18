from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamM(models.Model):
    _name = "team.m"

    name = fields.Char()
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_team_m(self):
        raise UserError("Test Error")
