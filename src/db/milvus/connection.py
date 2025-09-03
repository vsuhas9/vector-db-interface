"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
# -*- coding: utf-8 -*-
from __future__ import annotations
from pymilvus import MilvusClient, AsyncMilvusClient
from src.config.settings import Settings

__version__ = "0.1.0"
__all__ = [
    "MilvusSyncConnection",
    "MilvusAsyncConnection"
]


class MilvusSyncConnection:
    """ A class to manage the synchronous connection to a Milvus database using the MilvusClient."""
    def __init__(self):
        """ Initializes the MilvusConnection with the host and token from the Settings.
        """
        _settings = Settings()
        self.milvus_host = _settings.milvus_host
        self.milvus_token = f"{_settings.milvus_username}:{_settings.milvus_password}"
        self.client = MilvusClient(uri=self.milvus_host, token=self.milvus_token)


class MilvusAsyncConnection:
    """
    A class to manage the connection to a Milvus database using the MilvusClient.
    This class initializes a connection to the Milvus server using the host and token
    specified in the Settings configuration.a712aaf17a6f
    Attributes:
        milvus_host (str): The host address of the Milvus server.
        milvus_token (str): The authentication token for the Milvus server.
        client (MilvusClient): The MilvusClient instance for interacting with the Milvus server.
    """
    def __init__(self, db_name) -> None:
        """
        Initializes the MilvusConnection with the host and token from the Settings.
        Raises:
            ValueError: If the host or token is not set in the Settings.
        """
        _settings = Settings()
        self.milvus_host = _settings.milvus_host
        self.embedding_model_name = _settings.embedding_model
        self.milvus_token = f"{_settings.milvus_username}:{_settings.milvus_password}"
        self.client = AsyncMilvusClient(
            uri=self.milvus_host, token=self.milvus_token, db_name=db_name
        )
