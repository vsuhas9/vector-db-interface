"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
import asyncio
from langchain_ollama import OllamaEmbeddings
from src.logging import get_logger
from src.config import Settings

__all__ = ["Embeddings"]
__version__ = "0.0.1"


class Embeddings:
    """
    Async-compatible class to configure and generate text embeddings using Ollama.
    """

    def __init__(self, model_name) -> None:
        """Initializes the Embeddings class with OllamaEmbeddings configuration."""
        self.settings = Settings()
        self.logger = get_logger("Embeddings")
        self.embedding = OllamaEmbeddings(
            model=model_name,
            keep_alive=-1,
        )
        self.concurrency_limit = 1
        self._semaphore = asyncio.Semaphore(self.concurrency_limit)

    async def _embed(self, text: str) -> list[float]:
        """Internal method to generate embeddings asynchronously for the given text."""
        self.logger.info("Generating embedding for: %s", text)

        def _embed_sync():
            return self.embedding.embed_query(text)

        async with self._semaphore:
            embedding = await asyncio.to_thread(_embed_sync)
            self.logger.debug("Embedding for '%s': %s...", text, embedding[:3])
            return embedding

    async def generate(self, text: str) -> list[float]:
        """
        Public method to generate embedding for a given text string.

        Args:
            text (str): Input text for which to generate embedding.

        Returns:
            list[float]: Embedding vector.
        """
        return await self._embed(text)
