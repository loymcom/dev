from odoo import _, api, fields, models

GENDER = {
    "F": "female",
    "M": "male",
    "": ""
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        """ Return search domain """
        values = team_m_values
        url = self.env.context["team_m_url"]
        if url[-12:] == "/orders/list":
            partner_name = values["mainGuest"]["firstName"] + " " + values["mainGuest"]["lastName"]
        else:
            partner_name = values["First name"] + " " + values["Last name"]
        domain = [("name", "=", partner_name)]
        return self.search(domain)

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        """ Return odoo values """
        Country = self.env["res.country"]
        PartnerCategory = self.env["res.partner.category"]
        TeamM = self.env["team.m"]

        values = team_m_values
        odoo_values = {}
        url = self.env.context["team_m_url"]

        if url[-12:] == "/orders/list":
            odoo_values = {
                'firstname': values["mainGuest"]['firstName'],
                'lastname': values["mainGuest"]['lastName'],
            }
        else:
            if values["Country"] == "Norge":
                values["Country"] = "NO"
            birthdate = None
            if values.get('Birth date') != "! Not entered":
                birthdate = TeamM._mdy_date(values['Birth date'])
            category_names = [
                category.strip() for category in values["Customer Category"].split(",")
            ]
            categories = PartnerCategory.search([('name', 'in', category_names)])
            odoo_values = {
                'name': values['Name'],
                'birthdate_date': birthdate,
                'ref': values['Record ID - Contact - Hubspot'],
                'category_id': [(6, 0, categories.ids)],
                'x_new_guest_year': values['New guest year'],
                'firstname': values['First name'],
                'gender': GENDER[values['Gender']],
                'lastname': values['Last name'],
                'country_id': Country.search([("code", "=", values["Country"])]).id,
                'city': values['City'],
                'zip': values['Zip'],
                'email': values['Email'],
                'street': values['Street'],
                'phone': values['Phone'],
            }
        return odoo_values
