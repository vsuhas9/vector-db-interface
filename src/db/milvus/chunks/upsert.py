"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from src.logging import get_logger
from src.db.milvus.connection import MilvusAsyncConnection
from src.embeddings import Embeddings

__version__ = "0.0.1"
__all__ = ["MilvusChunkInserter"]


class MilvusChunkInserter(MilvusAsyncConnection):
    """Handles async chunk insertion into Milvus"""

    def __init__(self, body) -> None:
        """Initializes the MilvusChunkInserter with DB context"""
        self.db_name = body.get("db_name")
        self.collection_name = body.get("collection_name")
        self.chunk_list = body.get("chunk_list", [])
        super().__init__(db_name=self.db_name)
        self.embedding = Embeddings(self.embedding_model_name)
        self.logger = get_logger(__name__)

    async def upsert(self) -> tuple[int, dict]:
        """Asynchronously inserts chunks into the given Milvus collection"""
        try:
            data = []
            chunk_id_list = []
            for chunk in self.chunk_list:
                vector = await self.embedding.generate(chunk["content"])
                data.append({
                    "vector": vector,
                    "chunk": chunk["content"],
                    "metadata": chunk["metadata"]
                })

            response = await self.client.insert(
                db_name=self.db_name,
                collection_name=self.collection_name,
                data=data
            )
            for chunk_id in response["ids"]:
                chunk_id_list.append(str(chunk_id))
            self.logger.info("Inserted %d chunks into %s.%s", len(
                self.chunk_list), self.db_name, self.collection_name)
            return True, {
                "description": "Chunks inserted successfully", "ids": chunk_id_list}
        except Exception as e:
            self.logger.error("Insertion error into %s.%s: %s",
                        self.db_name, self.collection_name, e)
            return 400, {"description": f"Insertion failed: {e}"}
        finally:
            await self.client.close()
