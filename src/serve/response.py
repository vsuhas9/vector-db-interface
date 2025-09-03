"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
import json
from functools import wraps
from typing import Callable
from fastapi import Response
from src.models import CreateDBSchema, CreateCollectionSchema, StoreChunkSchema

__version__ = "0.0.1"
__all__ = ["GetResponse"]


class GetResponse:
    R"""Class to generate responses"""

    def __init__(self):
        R"""Initialize the GetResponse class"""

    def _build_response(
            self, status_code: int, description: str, default_status: str, **kwargs) -> Response:
        content = {
            "status": default_status,
            "description": description,
        }
        content.update(kwargs)

        return Response(
            content=json.dumps(content),
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": "true",
                "Content-Type": "application/json",
            },
            status_code=status_code,
        )

    def response_200(self, description: str, **kwargs) -> Response:
        R"""Response for successful operations, such as data retrieval"""
        return self._build_response(200, description, "Operation Successful", **kwargs)

    def response_201(self, description: str, **kwargs) -> Response:
        R"""Response for successful creation operations, such as new resource creation"""
        return self._build_response(201, description, "Resource Created Successfully", **kwargs)

    def response_400(self, description: str, **kwargs) -> Response:
        R"""Response for bad request errors, such as invalid input"""
        return self._build_response(400, description, "Operation Failed", **kwargs)

    def response_403(self, **kwargs) -> Response:
        R"""Response for forbidden errors, such as invalid permissions"""
        return self._build_response(403, "Token Expired", "Operation Failed", **kwargs)

    def response_404(self, description: str, **kwargs) -> Response:
        R"""Response for not found errors, such as missing resources"""
        return self._build_response(404, description, "Operation Failed", **kwargs)

    def response_409(self, description: str, **kwargs) -> Response:
        R"""Response for conflict errors, such as duplicate entries"""
        return self._build_response(409, description, "Operation Failed", **kwargs)

    def response_422(self, **kwargs) -> Response:
        R"""Response for missing entries in the request"""
        return self._build_response(422, "Missing entries in the request", "Operation Failed", **kwargs)

    def response_429(self, **kwargs) -> Response:
        R"""Response for rate limiting or service unavailability"""
        return self._build_response(429, "Service Unavailable", "Operation Failed", **kwargs)


RESPONSE_MAP = {
    True: lambda d: GetResponse().response_200(**(d or {})),
    201: lambda d: GetResponse().response_201(**(d or {})),
    400: lambda d: GetResponse().response_400(**(d or {})),
    403: lambda d: GetResponse().response_403(**(d or {})),
    404: lambda d: GetResponse().response_404(**(d or {})),
    409: lambda d: GetResponse().response_409(**(d or {})),
    422: lambda d: GetResponse().response_422(**(d or {})),
    429: lambda d: GetResponse().response_429(**(d or {})),
}

def traced_route():
    """
    Decorator to trace a route with Langfuse and handle responses.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                status, data = await func(*args, **kwargs)
                response_func = RESPONSE_MAP.get(
                    status, lambda d: GetResponse().response_400(**d)
                )
                response = response_func(data if isinstance(data, dict) else {"data": data})
            except Exception as e:
                response = GetResponse().response_400("Unhandled Exception", error=str(e))
            return response
        return wrapper
    return decorator
