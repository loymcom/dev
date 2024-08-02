import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.addons.sale.controllers import portal
from odoo.osv import expression
from odoo.tools import lazy
from odoo.tools.json import scriptsafe as json_scriptsafe

_logger = logging.getLogger(__name__)

from odoo.addons.website_sale_product_variant.controllers.main import WebsiteSaleProductVariant
from odoo.addons.website_sale.controllers.main import TableCompute


class WebsiteSaleBooking(WebsiteSaleProductVariant):

    def _tmpl_ids(self, search_product, website):
        if website.shop_model == "shop.product":
            return search_product.product_tmpl_id.ids

        return super()._tmpl_ids(search_product, website)
