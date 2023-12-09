__all__ = ["init_app"]

import logging

from fastapi import FastAPI
from sqladmin import Admin

# noinspection PyProtectedMember
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from src.modules.admin.auth import authentication_backend
from src.modules.admin.views import models


class CustomAdmin(Admin):
    ...


def init_app(app: FastAPI, engine: Engine | AsyncEngine):
    admin = CustomAdmin(
        app,
        engine,
        authentication_backend=authentication_backend,
        templates_dir="src/modules/admin/templates",
    )

    for model in models:
        admin.add_view(model)

    logging.info(r"Admin panel is configured at /admin")
