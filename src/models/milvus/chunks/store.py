"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from pydantic import BaseModel, Field


__version__ = "0.0.1"
__all__ = ["StoreChunkSchema"]


class StoreChunkSchema(BaseModel):
    """
    Schema for storing a chunk in the database.
    """
    chunk_list: list[dict] = Field(...)
    collection_name: str = Field(...)
    db_name: str = Field(...)

    class Config:
        """
        Pydantic configuration for the StoreChunkSchema.
        """
        json_schema_extra = {
            "example": {
                "chunk_list": [
                    {
                        "content": "Hello world",
                        "metadata": {
                            "source": "document_123",
                            "timestamp": "2025-06-20T12:00:00Z"
                        },
                    }
                ],
                "collection_name": "test",
                "db_name": "test",
            }
        }
