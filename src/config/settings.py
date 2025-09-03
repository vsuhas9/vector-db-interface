"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
import os
from dotenv import load_dotenv, find_dotenv

__all__ = ["Settings"]


class Settings:
    """Settings class to handle all the data"""

    def __init__(self) -> None:
        # Load only .env (no prefix logic)
        dotenv_path = find_dotenv(".env")
        if dotenv_path:
            load_dotenv(dotenv_path=dotenv_path)

        # Basic Configuration
        self.__name = os.getenv("DB_APPLICATION_NAME", "db")
        self.__version = os.getenv("DB_CODE_VERSION", "0.0.1")
        self.__release = os.getenv("DB_RELEASE", "dev")
        self.__host = os.getenv("DB_HOST", "0.0.0.0")
        self.__port = int(os.getenv("DB_PORT", "8600"))

        # Milvus (default to in-memory backend)
        self.__milvus_host = os.getenv("DB_MILVUS_HOST", "http://localhost:19530")
        self.__milvus_username = os.getenv("DB_MILVUS_USERNAME", "admin")
        self.__milvus_password = os.getenv("DB_MILVUS_PASSWORD", "admin")

        # Embedding Model (Ollama-backed only)
        self.__embedding_model = os.getenv("DB_EMBEDDING_MODEL", "nomic-embed-text")

    # Basic Configuration
    @property
    def name(self):
        R"Application Name"
        return self.__name

    @property
    def release(self):
        R"Application Release"
        return self.__release

    @property
    def version(self):
        R"Application Version"
        return self.__version

    @property
    def host(self):
        R"Application Host"
        return self.__host

    @property
    def port(self):
        "Application Port"
        return self.__port

    # Milvus
    @property
    def milvus_host(self):
        R"Milvus Host"
        return self.__milvus_host

    @property
    def milvus_username(self):
        R"Milvus Username"
        return self.__milvus_username

    @property
    def milvus_password(self):
        R"Milvus Password"
        return self.__milvus_password

    # Embedding
    @property
    def embedding_model(self):
        R"Milvus Embedding Model"
        return self.__embedding_model
