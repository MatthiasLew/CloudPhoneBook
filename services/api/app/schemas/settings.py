"""User settings schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class SettingsUpdate(BaseModel):
    theme: str = Field(default="dark", pattern="^(dark|light|system)$")
    table_layout_json: dict[str, Any] = Field(default_factory=dict)


class SettingsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    theme: str
    table_layout_json: dict[str, Any]
    updated_at: datetime | None = None
