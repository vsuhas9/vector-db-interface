"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
# -*- coding: utf-8 -*-
import logging
import sys
import json
import contextvars
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

__version__ = "0.0.1"
__all__ = [
    "TraceIDFilter",
    "JsonFormatter",
    "TraceIDMiddleware",
    "set_trace_id",
    "get_logger"
]

trace_id_var = contextvars.ContextVar("trace_id", default="no-trace-id")


class TraceIDFilter(logging.Filter):
    """
    A logging filter that adds the trace_id to each log record.
    This allows logs to be correlated with a specific request or operation.
    """
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True


class JsonFormatter(logging.Formatter):
    """
    A custom JSON formatter for logging.
    This formatter outputs log records in JSON format, which is useful for structured logging.
    """
    def format(self, record):
        """
        Format the log record as a JSON object.
        This method overrides the default format method to output a JSON string.
        """
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "trace_id": getattr(record, "trace_id", "no-trace-id"),
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


class TraceIDMiddleware(BaseHTTPMiddleware):
    R"""
    Middleware to automatically generate and set a trace_id for each request.
    This middleware generates a new trace_id for each incoming request and sets it in the context.
    It also logs the trace_id at the start of each request and includes it in the response headers.
    """
    async def dispatch(self, request: Request, call_next):
        R"""
        Dispatch method that is called for each request.
        It generates a new trace_id, sets it in the context, logs the request,
        and then calls the next middleware or route handler.
        Args:
            request (Request): The incoming request object.
            call_next: The next middleware or route handler to call.
        Returns:
            Response: The response object returned by the next middleware or route handler.
        """
        trace_id = str(uuid.uuid4())
        set_trace_id(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response


def set_trace_id(trace_id: str):
    """
    Set the trace_id for the current context.
    This function should be called at the start of each request or operation
    to ensure that logs can be correlated with the trace.
    """
    trace_id_var.set(trace_id)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    If the logger does not already have handlers, it will be configured with a StreamHandler
    that outputs to stdout and includes a trace_id in the log records.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] [%(trace_id)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(TraceIDFilter())

        logger.addHandler(stream_handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
