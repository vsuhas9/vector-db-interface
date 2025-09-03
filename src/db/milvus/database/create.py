"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
import asyncio
from src.logging import get_logger
from src.db.milvus.connection import MilvusSyncConnection

__version__ = "0.1.0"
__all__ = [
    "MilvusDBCreator"
]


class MilvusDBCreator(MilvusSyncConnection):
    """Handles asynchronous Milvus database creation with status code and message."""

    def __init__(self, body) -> None:
        self.db_name = body.get("db_name", "")
        super().__init__()
        self.logger = get_logger(__name__)
        self.logger.info("MilvusDBCreator initialized with host: %s", self.milvus_host)

    async def create(self) -> tuple[int, dict]:
        """Attempts to create a Milvus database and returns (HTTP status code, message)."""
        try:
            await asyncio.to_thread(self.client.create_database, db_name=self.db_name)
            self.logger.info("Milvus database created: %s", self.db_name)
            return 201, {"description": f"Database '{self.db_name}' created successfully."}
        except Exception as e:
            self.logger.error("Error creating database '%s': %s", self.db_name, e)
            return 400, {"description": f"Failed to create database '{self.db_name}': {e}"}
        finally:
            await asyncio.to_thread(self.client.close)
            self.logger.info("Connection closed after creation attempt.")
