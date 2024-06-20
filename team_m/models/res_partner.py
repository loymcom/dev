from odoo import _, api, fields, models

GENDER = {
    "F": "female",
    "M": "male",
    "": ""
}


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _team_m_search(self, odoo_values):
        """ Return search domain """
        values = odoo_values
        contact_name = values["firstname"] + " " + values["lastname"]
        return [("name", "=", contact_name)]

    @api.model
    def _team_m_to_odoo(self, team_m_values):
        """ Return odoo values """
        Country = self.env["res.country"]
        Partner = self.env["res.partner"]
        PartnerCategory = self.env["res.partner.category"]
        TeamM = self.env["team.m"]

        values = team_m_values
        if values["Country"] == "Norge":
            values["Country"] = "NO"
        birthdate = None
        if values.get('Birth date') != "! Not entered":
            birthdate = TeamM._mdy_date(values['Birth date'])
        category_names = [category.strip() for category in values["Customer Category"].split(",")]
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
