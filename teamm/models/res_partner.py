from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        # url = self.env.context["teamm_url"]
        # if url[-12:] == "/orders/list":
        #     partner_name = values["mainGuest"]["firstName"] + " " + values["mainGuest"]["lastName"]
        # else:
        #     partner_name = values["first name"] + " " + values["last name"]
        # domain = [("name", "=", partner_name)]
        domain = [("ref", "=", values["hubspot contact"])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Country = self.env["res.country"]
        PartnerCategory = self.env["res.partner.category"]
        TeamM = self.env["teamm"]

        values = teamm_values
        odoo_values = {}
        url = self.env.context["teamm_url"]

        if url and url[-12:] == "/orders/list":
            odoo_values = {
                "firstname": values["mainGuest"]["firstName"],
                "lastname": values["mainGuest"]["lastName"],
            }
        # elif teamm_values.get("sale.order"):
        #     odoo_values = {
        #         "firstname": values["first name"],
        #         "lastname": values["last name"],
        #         "ref": values["hubspot contact"],
        #     }
        else:
            if values["country"] == "Norge":
                values["country"] = "NO"
            try:
                birthdate = TeamM._get_date(values.get("birth date"))
            except:
                birthdate = False               
            category_names = [
                category.strip() for category in values["customer category"].split(",")
            ]
            categories = PartnerCategory.search([("name", "in", category_names)])
            odoo_values = {
                # "name": values["name"],
                "birthdate_date": birthdate,
                "ref": values["hubspot contact"],
                "category_id": [(6, 0, categories.ids)],
                # "x_new_guest_year": values["new guest year"],
                "firstname": values["first name"],
                "gender": TeamM.GENDER.get(values["gender"]),
                "lastname": values["last name"],
                "country_id": Country.search([("code", "=", values["country"])]).id,
                "city": values["city"],
                "zip": values["zip"],
                "email": values["email"],
                "street": values["street"],
                "phone": values["phone"],
            }
        return odoo_values
