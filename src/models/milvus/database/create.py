"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from pydantic import BaseModel, Field

__version__ = "0.0.1"
__all__ = ["CreateDBSchema"]


class CreateDBSchema(BaseModel):
    R"""Schema for Managing DBs"""

    db_name: str = Field(...)

    class Config:
        R"""Config Class for 'CreateDBSchema'"""

        json_schema_extra = {
            "example": {
                "db_name": "test",
            }
        }
