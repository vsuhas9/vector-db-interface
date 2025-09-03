"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from pydantic import BaseModel, Field

__version__ = "0.0.1"
__all__ = ["CreateCollectionSchema"]


class CreateCollectionSchema(BaseModel):
    R"""Schema for Managing Collections"""

    db_name: str = Field(...)
    collection_name: str = Field(...)
    class Config:
        R"""Config Class for 'CreateCollectionSchema'"""

        json_schema_extra = {
            "example": {
                "db_name": "test",
                "collection_name": "test",
            }
        }
