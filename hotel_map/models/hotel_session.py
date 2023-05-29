from odoo import api, fields, models

class HotelSession(models.Model):
    _name = "hotel.session"
    _description = "Hotel Session"

    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    days = fields.Integer(compute="_compute_days")

    @api.onchange("start_date","end_date")
    def _compute_days(self):
        for record in self:
            record.days = (record.end_date-record.start_date).days
