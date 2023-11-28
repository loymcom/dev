# Copyright 2022 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).
from typing import Annotated, Any, List

from odoo import _, api, fields, models
from odoo.api import Environment
from odoo.exceptions import ValidationError

from odoo.addons.base.models.res_partner import Partner

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from odoo.addons.fastapi.dependencies import (
    authenticated_partner_from_basic_auth_user,
    authenticated_partner_impl,
    odoo_env,
)
from ..routers import partner_router, partner_router_doc


class GenericFastAPI(models.AbstractModel):

    _inherit = "generic.fastapi"


class FastapiEndpoint(models.Model):

    _inherit = "fastapi.endpoint"

    def _get_fastapi_routers(self) -> List[APIRouter]:
        routers = super()._get_fastapi_routers()
        routers.append(partner_router)
        return routers

    def _prepare_fastapi_app_params(self) -> dict[str, Any]:
        params = super()._prepare_fastapi_app_params()
        if self.app == "generic":
            tags_metadata = params.get("openapi_tags", []) or []
            tags_metadata.append({"name": "partner", "description": partner_router_doc})
            params["openapi_tags"] = tags_metadata
        return params
