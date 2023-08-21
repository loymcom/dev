from odoo import fields, models
from odoo.exceptions import UserError

def mod10(kidnummer):
    """
    kidnummer: uten kontroll-siffer
    return: kidnummer med kontroll-siffer
    """
    tverrsum = 0
    faktor = 2 
    # Gå gjennom tallene i KID-nummeret i motsatt rekkefølge
    for siffer in reversed(str(kidnummer)):
        # Legg til bidraget av siffer ganget med faktor i tverrsummen
        tverrsum += sum(int(j) for j in str(int(siffer) * faktor))
        # Regn ut ny faktor. Rekkefølgen er 2, 1, 2, 1, 2, 1, ...
        faktor = faktor % 2 + 1
    return "{}{}".format(kidnummer, (10 - tverrsum % 10) % 10)

def mod11(a):
    """
    a: kidnummer uten kontrollsiffer
    return: kidnummer med kontrollsiffer
    """
    cross = sum([int(val)*[2,3,4,5,6,7][idx%6] for idx,val in enumerate(list(str(a))[::-1])]) 
    return "%s%s" % (a,cross % 11 == 10 and '-' or 11-(cross % 11))

# print(mod10(234567))
# print(mod11(1234567890))


class AccountMove(models.Model):
    _inherit = "account.move"

    def create(self, values):
        return UserError(values)
        # return super().create(values)
        # records = super().create(values)
        # for record in records:
        #     mod = record.journal_id.l10n_no_kid_mod
        #     if mod:
        #         pdg = record.journal_id.l10n_no_kid_partner_digits
        #         mdg = record.journal_id.l10n_no_kid_move_digits
        #         partner_kid = str(record.partner_id.id).zfill(pdg) if pdg else ""
        #         move_kid = str(record.id).zfill(mdg)
        #         if mod == "mod10":
        #             record.payment_reference = mod10(partner_kid + move_kid)
        #         if mod == "mod11":
        #             record.payment_reference = mod11(partner_kid + move_kid)
        # return records
