from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    start_date = fields.Date(inverse="_inverse_start_date")
    end_date = fields.Date(inverse="_inverse_end_date")

    def _inverse_start_date(self):
        for record in self:
            record.start_date = record.start_date

    def _inverse_end_date(self):
        for record in self:
            record.end_date = record.end_date
