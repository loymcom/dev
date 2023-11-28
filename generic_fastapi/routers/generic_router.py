# Copyright 2023 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).
"""
The generic router is based on the demo router that demonstrates how to use the fastapi
integration with odoo.
"""
from typing import Annotated

from odoo.api import Environment
from odoo.exceptions import AccessError, MissingError, UserError, ValidationError

from odoo.addons.base.models.res_partner import Partner

from fastapi import APIRouter, Depends, HTTPException, status

from odoo.addons.fastapi.dependencies import authenticated_partner, fastapi_endpoint, odoo_env
from odoo.addons.fastapi.models import FastapiEndpoint
from ..schemas import GenericEndpointAppInfo, GenericExceptionType, GenericUserInfo

router = APIRouter(tags=["generic"])

# DEMO #################################################################################

@router.get("/demo")
async def hello_world():
    """Hello World!"""
    return {"Hello": "World"}


@router.get("/demo/exception")
async def exception(exception_type: GenericExceptionType, error_message: str):
    """Raise an exception

    This method is used in the test suite to check that any exception
    is correctly handled by the fastapi endpoint and that the transaction
    is roll backed.
    """
    exception_classes = {
        GenericExceptionType.user_error: UserError,
        GenericExceptionType.validation_error: ValidationError,
        GenericExceptionType.access_error: AccessError,
        GenericExceptionType.missing_error: MissingError,
        GenericExceptionType.http_exception: HTTPException,
        GenericExceptionType.bare_exception: NotImplementedError,
    }
    exception_cls = exception_classes[exception_type]
    if exception_cls is HTTPException:
        raise exception_cls(status_code=status.HTTP_409_CONFLICT, detail=error_message)
    raise exception_classes[exception_type](error_message)


@router.get("/demo/lang")
async def get_lang(env: Annotated[Environment, Depends(odoo_env)]):
    """Returns the language according to the available languages in Odoo and the
    Accept-Language header.

    This method is used in the test suite to check that the language is correctly
    set in the Odoo environment according to the Accept-Language header
    """
    return env.context.get("lang")


@router.get("/demo/who_ami")
async def who_ami(
    partner: Annotated[Partner, Depends(authenticated_partner)]
) -> GenericUserInfo:
    """Who am I?

    Returns the authenticated partner
    """
    # This method show you how you can rget the authenticated partner without
    # depending on a specific implementation.
    return GenericUserInfo(name=partner.name, display_name=partner.display_name)


@router.get(
    "/demo/endpoint_app_info",
    dependencies=[Depends(authenticated_partner)],
)
async def endpoint_app_info(
    endpoint: Annotated[FastapiEndpoint, Depends(fastapi_endpoint)],
) -> GenericEndpointAppInfo:
    """Returns the current endpoint configuration"""
    # This method show you how to get access to current endpoint configuration
    # It also show you how you can specify a dependency to force the security
    # even if the method doesn't require the authenticated partner as parameter
    return GenericEndpointAppInfo.model_validate(endpoint)
