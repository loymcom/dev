See below how to implement. See also website_event_sale_resource_booking.


.. code-block:: python

    from odoo.http import request
    from odoo import models

    class Website(models.Model):
        _inherit = "website"

        def sale_product_domain(self):
            domain = super(Website, self).sale_product_domain()

            def ids(string):
                return [int(num) for num in string.split(",")]

            ids_list = request.httprequest.args.get("your.model")
            if ids_list:
                domain = ["&"] + domain + [("your_model_id", "in", ids(ids_list))]

            return domain


.. code-block:: python

    from odoo.addons.website_sale_filter.controllers.main import WebsiteSaleFilter

    class WebsiteSaleMyController(WebsiteSaleFilter):

        def _get_filters(self, filters=[]):
            # List of (visible_name, model_name, display_type, priority, domain)
            filters.append(
                (
                    "My Model Name",
                    "my.model",
                    "select",   # or "radio"
                    5,          # priority in list of filters
                    [],         # search domain
                )
            )
            return super()._get_filters(filters)