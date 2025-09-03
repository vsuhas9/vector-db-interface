"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from src.logging import get_logger
from src.db.milvus.connection import MilvusAsyncConnection
from src.embeddings import Embeddings

__version__ = "0.0.1"
__all__ = ["MilvusChunkRetriever"]


class MilvusChunkRetriever(MilvusAsyncConnection):
    """Handles async chunk retrieval from Milvus"""

    def __init__(self, body) -> None:
        """
        Initializes the MilvusChunkRetriever with the database name
        """
        self.db_name = body.get("db_name", "default_db")
        self.collection_name = body.get("collection_name", "")
        self.query = body.get("query", "")
        self.k = body.get("k", 3)
        super().__init__(db_name=self.db_name)
        self.embedding = Embeddings(self.embedding_model_name)
        self.logger = get_logger(__name__)

    async def get_chunk(self) -> tuple[int, dict]:
        """Asynchronously retrieves chunks from Milvus based on a query string."""
        try:
            query_vector = await self.embedding.generate(self.query)
            await self.client.load_collection(
                collection_name=self.collection_name)
            results = await self.client.search(
                db_name=self.db_name,
                collection_name=self.collection_name,
                data=[query_vector],
                output_fields=["id", "chunk", "metadata"],
                k=self.k,
            )

            chunks = []
            for doc in results[0]:
                content = {
                    "id": str(doc["entity"]["id"]),
                    "content": doc["entity"]["chunk"],
                    "metadata": doc["entity"]["metadata"],
                }
                if content not in chunks:
                    chunks.append(content)

            self.logger.info("Retrieved %d chunks from %s.%s",
                            len(chunks), self.db_name, self.collection_name)

            if chunks:
                return True, {"description": "Chunks retrieved", "chunks": chunks[:self.k]}
            else:
                return 404, {"description": "No chunks found"}

        except Exception as e:
            self.logger.error("Retrieval error from %s.%s: %s",
                            self.db_name, self.collection_name, e)
            return 400, {"description": f"Retrieval failed: {e}"}
        finally:
            await self.client.close()
