# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import warnings
from enum import Enum
from typing import Annotated, Generic, List, Optional, TypeVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, computed_field


class PartnerInfo(BaseModel):
    name: str
    display_name: str

