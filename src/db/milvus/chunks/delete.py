"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from src.logging import get_logger
from src.db.milvus.connection import MilvusAsyncConnection

__version__ = "0.0.1"
__all__ = ["MilvusChunkDeleter"]


class MilvusChunkDeleter(MilvusAsyncConnection):
    """Handles async chunk deletion from Milvus"""

    def __init__(self, body) -> None:
        """
        Initializes the MilvusChunkRemover with the database name
        """
        self.db_name = body.get("db_name", "")
        self.collection_name = body.get("collection_name", "")
        self.ids = body.get("ids", "")
        super().__init__(db_name=self.db_name)
        self.logger = get_logger(__name__)

    async def delete(self) -> tuple[int, dict]:
        """Asynchronously deletes chunks from Milvus based on provided IDs."""
        try:
            if not self.ids:
                return 400, {"description": "No IDs provided for deletion"}
            response = await self.client.delete(
                collection_name=self.collection_name,
                filter=f"id in {self.ids}"
            )

            self.logger.info("Deleted %d chunks from %s.%s",
                            len(self.ids), self.db_name, self.collection_name)
            return True, {
                "description": "Chunks deleted successfully", 
                "delete_count": response["delete_count"]}

        except Exception as e:
            self.logger.error("Deletion error from %s.%s: %s",
                            self.db_name, self.collection_name, e)
            return 500, {"description": f"Deletion failed: {e}"}
        finally:
            await self.client.close()
