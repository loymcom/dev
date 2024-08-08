from odoo import api, fields, models
from odoo.exceptions import UserError


class TeammAlias(models.Model):
    _name = "teamm.alias"
    _order = "name"

    name = fields.Char()
    aliases = fields.Char(help="comma-separated string")
    teamm_id = fields.Many2one("teamm")
