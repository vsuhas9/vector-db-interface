"""
 * Authors: Suhas V
 * Created on: 11-12-2024-14h-10m
"""
from __future__ import annotations
from src import Settings, Serve

__version__ = "0.0.1"
__all__ = ["DB"]


class DB:
    r"""Simple DB Server"""

    def __init__(self) -> None:
        r"""Create the DB service instance"""
        self.settings = Settings()
        self.server = Serve()
        self.server.serve(
            host=self.settings.host,
            port=self.settings.port   
        )


if __name__ == "__main__":
    DB()
