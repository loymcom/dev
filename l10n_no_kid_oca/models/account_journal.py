from odoo import fields, models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_no_kid_partner_digits = fields.Integer(
        "KID partner digits",
        help="Set 0 or sufficient digits for any partner id.",
    )
    l10n_no_kid_move_digits = fields.Integer(
        "KID account move digits",
        help="Set sufficient digits for any account move id.",
    )
    l10n_no_kid_mod = fields.Selection(
        [("mod10", "MOD10"), ("mod11", "MOD11")],
        string="KID MOD",
        help="Algorithm to compute the KID control number",
    )
