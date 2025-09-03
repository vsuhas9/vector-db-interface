"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""

BASE_RESPONSES = responses = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "Invalid or malformed request"
                        }
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "Authentication credentials were missing or incorrect"
                        }
                    }
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "You do not have permission to access this resource"
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "The requested resource was not found"
                        }
                    }
                }
            }
        }
    },
    422: {
        "description": "Unprocessable Request",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "Missing entries in the request"
                        }
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Failed"},
                        "description": {
                            "type": "string",
                            "default": "An unexpected error occurred on the server"
                        }
                    }
                }
            }
        }
    }
}

CREATE_DB_RESPONSE = BASE_RESPONSES.copy()
DELETE_DB_RESPONSE = BASE_RESPONSES.copy()

CREATE_COLLECTION_RESPONSE = BASE_RESPONSES.copy()
DELETE_COLLECTION_RESPONSE = BASE_RESPONSES.copy()

STORE_CHUNK_RESPONSE = BASE_RESPONSES.copy()
RETRIEVE_CHUNK_RESPONSE = BASE_RESPONSES.copy()
DELETE_CHUNK_RESPONSE = BASE_RESPONSES.copy()


# Milvus Entries
CREATE_DB_RESPONSE.update({
    200: {
        "description": "Database Created",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Successful"},
                        "description": {"type": "string", "default": "Database Created"},
                    },
                }
            }
        },
    }
})

DELETE_DB_RESPONSE.update({
    200: {
        "description": "Database Deleted",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Successful"},
                        "description": {"type": "string", "default": "Database Deleted"},
                    },
                }
            }
        },
    }
})


STORE_CHUNK_RESPONSE.update({
    200: {
        "description": "Chunk Stored",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Successful"},
                        "description": {"type": "string", "default": "Chunk Stored"},
                    },
                }
            }
        },
    }
})

RETRIEVE_CHUNK_RESPONSE.update({
    200: {
        "description": "Data Retrieved",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "default": "Operation Successful"},
                        "description": {"type": "string", "default": "Data Retrieved"},
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {"type": "string", "example": "Hello how are you doing"},
                                    "metadata": {
                                        "type": "object",
                                        "properties": {
                                            "year": {"type": "integer", "example": 2024},
                                            "description": {"type": "string", "example": "greeting"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            }
        },
    }
})

DELETE_CHUNK_RESPONSE.update({
    200: {
        "description": "Chunks successfully deleted",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "example": "Chunks deleted successfully"
                        },
                        "delete_count": {
                            "type": "integer",
                            "example": 5
                        }
                    },
                    "required": ["description", "delete_count"]
                }
            }
        }
    }
})
