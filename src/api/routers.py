from src.config import settings
from src.config_schema import Environment
from src.modules.user.router import router as router_users
from src.modules.auth.router import router as router_auth
from src.modules.personal_account.router import router as router_personal_account
from src.modules.lesson.router import router as router_tests
from src.modules.consultation.router import router as router_consultation
from src.modules.report.router import router as router_report
from src.modules.phishing.router import router as router_phishing

routers = [
    router_users,
    router_auth,
    router_tests,
    router_personal_account,
    router_consultation,
    router_report,
    router_phishing,
]

if settings.environment == Environment.DEVELOPMENT:
    from src.modules.dev.router import router as router_dev

    routers.append(router_dev)

__all__ = ["routers"]
