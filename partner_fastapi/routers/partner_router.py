# Copyright 2023 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).
"""
The demo router is a router that demonstrates how to use the fastapi
integration with odoo.
"""
from typing import Annotated

from odoo.api import Environment
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError

from odoo.addons.base.models.res_partner import Partner

from fastapi import APIRouter, Depends, HTTPException, status

from odoo.addons.fastapi.dependencies import authenticated_partner, fastapi_endpoint, odoo_env
from odoo.addons.fastapi.models import FastapiEndpoint
from ..schemas import PartnerInfo

import pprint

pp = pprint.PrettyPrinter(indent=4)
router = APIRouter(tags=["partner"])

@router.get("/{version}/res.partner/{id}")
async def read_partner(env: Annotated[Environment, Depends(odoo_env)], version: str, id: int):
    partner = env["res.partner"].browse(id)
    return partner.read()
