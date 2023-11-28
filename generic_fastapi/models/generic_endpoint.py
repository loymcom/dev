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
from ..routers import generic_router, generic_router_doc


class GenericFastAPI(models.AbstractModel):

    _name = "generic.fastapi"
    _description = "Generic Abstract FastAPI"


class FastapiEndpoint(models.Model):

    _inherit = "fastapi.endpoint"

    app: str = fields.Selection(
        selection_add=[("generic", "Generic Endpoint")], ondelete={"generic": "cascade"}
    )
    generic_auth_method = fields.Selection(
        selection=[("http_basic", "HTTP Basic")],
        string="Authenciation method",
    )

    def _get_fastapi_routers(self) -> List[APIRouter]:
        routers = super()._get_fastapi_routers()
        routers.append(generic_router)
        return routers

    @api.constrains("app", "generic_auth_method")
    def _valdiate_generic_auth_method(self):
        for rec in self:
            if rec.app == "generic" and not rec.generic_auth_method:
                raise ValidationError(
                    _(
                        "The authentication method is required for app %(app)s",
                        app=rec.app,
                    )
                )

    @api.model
    def _fastapi_app_fields(self) -> List[str]:
        fields = super()._fastapi_app_fields()
        fields.append("generic_auth_method")
        return fields

    def _get_app(self):
        app = super()._get_app()
        if self.app == "generic":
            # Here we add the overrides to the authenticated_partner_impl method
            # according to the authentication method configured on the generic app
            if self.generic_auth_method == "http_basic":
                authenticated_partner_impl_override = (
                    authenticated_partner_from_basic_auth_user
                )
            else:
                pass
            app.dependency_overrides[
                authenticated_partner_impl
            ] = authenticated_partner_impl_override
        return app

    def _prepare_fastapi_app_params(self) -> dict[str, Any]:
        params = super()._prepare_fastapi_app_params()
        if self.app == "generic":
            tags_metadata = params.get("openapi_tags", []) or []
            tags_metadata.append({"name": "generic", "description": generic_router_doc})
            params["openapi_tags"] = tags_metadata
        return params
