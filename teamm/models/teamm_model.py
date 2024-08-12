from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamMModel(models.Model):
    _name = "teamm.model"
    _description = "teamm.model"
    _order = "sequence"

    teamm_id = fields.Many2one("teamm")
    sequence = fields.Integer()
    is_active = fields.Boolean()
    name = fields.Char()
    primary_key = fields.Char()
    values = fields.Char()
