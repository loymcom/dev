from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMModel(models.Model):
    _name = "teamm.model"

    sequence = fields.Integer()
    is_active = fields.Boolean()
    name = fields.Char()
    teamm_id = fields.Many2one("teamm")
