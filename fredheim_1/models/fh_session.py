from odoo import api, fields, models

class FhSession(models.Model):
    _name = "fh.session"
    _description = "fh.session"

    date_start = fields.Date(
    )
    date_end = fields.Date(
    )
    program_ids = fields.Many2many(
        comodel_name="fh.program",
        relation="program_session_rel",
    )
