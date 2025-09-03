"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
import asyncio
from src.logging import get_logger
from src.db.milvus.connection import MilvusSyncConnection

__version__ = "0.0.1"
__all__ = [
    "MilvusDBDeleter"
]


class MilvusDBDeleter(MilvusSyncConnection):
    """Handles asynchronous Milvus database deletion with status code and message."""

    def __init__(self, body) -> None:
        self.db_name = body.get("db_name", "")
        super().__init__()
        self.logger = get_logger(__name__)
        self.logger.info("MilvusDBDeleter initialized with host: %s", self.milvus_host)

    async def delete(self) -> tuple[int, dict]:
        """Attempts to delete a Milvus database and returns (HTTP status code, message)."""
        try:
            await asyncio.to_thread(self.client.drop_database, db_name=self.db_name)
            self.logger.info("Milvus database deleted: %s", self.db_name)
            return True, {"description": f"Database '{self.db_name}' deleted successfully."}
        except Exception as e:
            self.logger.warning("Could not delete database '%s': %s", self.db_name, e)
            try:
                await asyncio.to_thread(self.client.using_database, db_name=self.db_name)
                collections = await asyncio.to_thread(self.client.list_collections)
                self.logger.warning(
                    "Database not empty. Collections present: %s", collections)
                return 400, {"description": f"Database '{self.db_name}' is not empty."}
            except Exception as inner:
                self.logger.error(
                    "Error listing collections for '%s': %s", self.db_name, inner)
                return 500, {"description": f"Failed to verify collections in '{self.db_name}'."}
        finally:
            await asyncio.to_thread(self.client.close)
            self.logger.info("Connection closed after deletion attempt.")
