from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMParam(models.Model):
    _name = "teamm.param"
    _description = "teamm.param"

    key = fields.Char()
    value = fields.Char()
    teamm_id = fields.Many2one("teamm")
