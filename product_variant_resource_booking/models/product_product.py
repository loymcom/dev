from datetime import datetime

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_dates(self):
        date_start = None
        date_end = None

        context = self.env.context
        date_format = self.env["res.lang"].search([("code", "=", context["lang"])]).date_format

        domain = context.get("domain") or []
        for d in domain:
            if isinstance(d, list) or isinstance(d, tuple):
                if isinstance(d[0], str) and d[0] == "date_start":
                    date_start = d[2]
                if isinstance(d[0], str) and d[0] == "date_end":
                    date_end = d[2]
        if date_start:
            date_start = datetime.strptime(date_start, date_format)
        if date_end:
            date_end = datetime.strptime(date_end, date_format)

        for record in self:
            record.date_start = date_start
            record.date_end = date_end

    def _compute_partner_id(self):
        partner_id = self.env.context.get("partner_id")
        for record in self:
            record.partner_id = partner_id

    date_range_id = fields.Many2one("date.range", string="Date Range")
    date_start = fields.Date(string="Start date", compute="_compute_dates")
    date_end = fields.Date(string="End date", compute="_compute_dates")
    partner_id = fields.Many2one("res.partner", string="Contact", compute="_compute_partner_id")

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        self = self.with_context(domain=domain)
        return super().web_search_read(domain, fields, offset, limit, order, count_limit)
