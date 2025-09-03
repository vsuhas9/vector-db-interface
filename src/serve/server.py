"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import Settings
from src.logging import get_logger, TraceIDMiddleware

from src.models import (
    CreateDBSchema,
    CreateCollectionSchema,
    StoreChunkSchema,
)

from src.config.response_models import (
    CREATE_DB_RESPONSE,
    DELETE_DB_RESPONSE,
    CREATE_COLLECTION_RESPONSE,
    DELETE_COLLECTION_RESPONSE,
    STORE_CHUNK_RESPONSE,
    RETRIEVE_CHUNK_RESPONSE,
    DELETE_CHUNK_RESPONSE,
)

from src.db.milvus import (
    MilvusDBCreator,
    MilvusDBDeleter,
    MilvusCollectionCreator,
    MilvusCollectionDeleter,
    MilvusChunkInserter,
    MilvusChunkRetriever,
    MilvusChunkDeleter,
)
from .response import traced_route

_logger = get_logger(__name__)
__version__ = "0.0.1"


class Serve:
    r"""Class to serve FastAPI"""

    def __init__(self):
        r"""Create an instance of the server"""
        _settings = Settings()

        self.app = FastAPI(
            title="Vector DB Server",
            description="Central DB server for vector storage and retrieval",
            version=__version__,
            servers=None,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            contact={"name": "Vector DB Server"},
            root_path="/db/api/v1",
            openapi_url="/openapi.json"
            if _settings.release in ["dev", "test"]
            else None,
            docs_url="/docs" if _settings.release in ["dev", "test"] else None,
            redoc_url=None,
        )

        # Middlewares
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.add_middleware(TraceIDMiddleware)

        # Routes
        self.register_routes()

    def serve(self, host: str = "0.0.0.0", port: int = 8600):
        r"""Run the FastAPI Server"""
        uvicorn.run(self.app, host=host, port=port)

    def register_routes(self):
        r"""Register FastAPI routes"""
        _logger.info("Registering routes for Vector DB Server")

        # Milvus DB Management
        @self.app.post("/vector/create", responses=CREATE_DB_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def create_db(body: CreateDBSchema = Body(...)):
            r"""Create a vector database"""
            state, message = await MilvusDBCreator(body.model_dump()).create()
            return state, message

        @self.app.delete("/vector/delete", responses=DELETE_DB_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def delete_db(db_name: str = "test"):
            r"""Delete a vector database"""
            body = {"db_name": db_name}
            state, message = await MilvusDBDeleter(body).delete()
            return state, message

        # Milvus Collection Management
        @self.app.post(
            "/collection/create", responses=CREATE_COLLECTION_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def create_collection(body: CreateCollectionSchema = Body(...)):
            r"""Create a vector collection"""
            _logger.info("Received create collection request")
            state, message = await MilvusCollectionCreator(body.model_dump()).create()
            return state, message

        @self.app.delete(
            "/collection/delete", responses=DELETE_COLLECTION_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def delete_collection(
            db_name: str = "test",
            collection_name: str = "test",
        ):
            r"""Delete a vector collection"""
            _logger.info("Received delete collection request")
            body = {
                "db_name": db_name,
                "collection_name": collection_name,
            }
            state, message = await MilvusCollectionDeleter(body).delete()
            return state, message

        # Chunks
        @self.app.post("/chunks/insert", responses=STORE_CHUNK_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def store_chunk(body: StoreChunkSchema = Body(...)):
            r"""Store a chunk in the vector store"""
            state, message = await MilvusChunkInserter(body.model_dump()).upsert()
            return state, message

        @self.app.get("/chunks/get", responses=RETRIEVE_CHUNK_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def get_chunk(
            db: str = "test",
            collection: str = "test",
            query: str = "hello",
            k: int = 1,
        ):
            r"""Retrieve chunks based on an input query"""
            body = {
                "db_name": db,
                "collection_name": collection,
                "query": query,
                "k": k
            }
            state, data = await MilvusChunkRetriever(body).get_chunk()
            return state, data

        @self.app.delete("/chunks/delete", responses=DELETE_CHUNK_RESPONSE, tags=["Vector Store"])
        @traced_route()
        async def delete_chunk(
            db_name: str = "test",
            collection_name: str = "test",
            ids: list[str] | None = None,
        ):
            r"""Delete chunks by id"""
            body = {
                "db_name": db_name,
                "collection_name": collection_name,
                "ids": ids or []
            }
            state, data = await MilvusChunkDeleter(body).delete()
            return state, data
