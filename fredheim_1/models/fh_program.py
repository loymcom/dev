from odoo import api, fields, models

class FhProgram(models.Model):
    _name = "fh.program"
    _description = "fh.program"

    name = fields.Char(
    )
    price = fields.Integer(
    )
    location_id = fields.Many2one(
        comodel_name="fh.location",
    )
    session_ids = fields.Many2many(
        comodel_name="fh.session",
        relation="program_session_rel",
    )
