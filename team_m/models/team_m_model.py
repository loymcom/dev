from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMModel(models.Model):
    _name = "team.m.model"

    sequence = fields.Integer()
    is_active = fields.Boolean()
    name = fields.Char()
    team_m_id = fields.Many2one("team.m")
