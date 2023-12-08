from src.config import settings
from src.config_schema import Environment
from src.modules.user.router import router as router_users
from src.modules.auth.router import router as router_auth
from src.modules.lesson.router import router as router_tests

routers = [router_users, router_auth, router_tests]

if settings.environment == Environment.DEVELOPMENT:
    from src.modules.dev.router import router as router_dev

    routers.append(router_dev)

__all__ = ["routers"]
