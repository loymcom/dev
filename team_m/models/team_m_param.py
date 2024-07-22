from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMParam(models.Model):
    _name = "team.m.param"

    key = fields.Char()
    value = fields.Char()
    team_m_id = fields.Many2one("team.m")
