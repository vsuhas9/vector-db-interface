"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from src.db.milvus.connection import MilvusAsyncConnection
from src.logging import get_logger

__version__ = "0.1.0"
__all__ = [
    "MilvusCollectionCreator"
]


class MilvusCollectionCreator(MilvusAsyncConnection):
    """
    A class that extends MilvusAsyncConnection to support collection creation.
    """

    def __init__(self, body) -> None:
        """
        Initializes the MilvusCollectionCreate with the connection to the Milvus server.
        """
        self.db_name = body.get("db_name", "")
        self.collection_name = body.get("collection_name", "")
        super().__init__(db_name=self.db_name)
        self.logger = get_logger(__name__)
        self.logger.info(
            "MilvusCollectionCreate initialized for DB: %s", self.db_name)

    async def create(self) -> tuple[int, dict]:
        """
        Creates a collection in Milvus and returns (status code, message).

        Args:
            self.collection_name (str): The name of the collection.
        """
        self.logger.info("Attempting to create collection: %s",
                    self.collection_name)
        try:
            await self.client.create_collection(
                collection_name=self.collection_name, dimension=768, auto_id=True)
            self.logger.info(
                "Collection '%s' created successfully.", self.collection_name)
            return 201, {
                "description": f"Collection '{self.collection_name}' created successfully."}
        except Exception as e:
            self.logger.error(
                "Failed to create collection '%s': %s", self.collection_name, e)
            return 400, {
                "description": f"Failed to create collection '{self.collection_name}': {e}"}
        finally:
            await self.client.close()
            self.logger.info("Connection closed after creation attempt.")
