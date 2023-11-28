# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import warnings
from enum import Enum
from typing import Annotated, Generic, List, Optional, TypeVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, computed_field


class GenericUserInfo(BaseModel):
    name: str
    display_name: str


class GenericEndpointAppInfo(BaseModel):
    id: int
    name: str
    app: str
    auth_method: str = Field(alias="demo_auth_method")
    root_path: str
    model_config = ConfigDict(from_attributes=True)


class GenericExceptionType(str, Enum):
    user_error = "UserError"
    validation_error = "ValidationError"
    access_error = "AccessError"
    missing_error = "MissingError"
    http_exception = "HTTPException"
    bare_exception = "BareException"
