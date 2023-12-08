__all__ = ["router"]

from fastapi import APIRouter
from starlette.responses import HTMLResponse

from src.api.dependencies import Dependencies
from src.api.exceptions import ObjectNotFound
from src.modules.mailing.schemas import RenderedTemplate
from src.modules.user.schemas import UserData
from src.storages.mailing_templates import TemplatesList, MailingTemplate

router = APIRouter(prefix="/mailing", tags=["Mailing"])


@router.get(
    "/visit-callback",
)
async def visit_callback(message_uuid: str) -> None:
    ...


@router.get(
    "/templates/{template_alias}",
    responses={200: {"model": MailingTemplate, "description": "Template found"}, **ObjectNotFound.responses},
)
async def get_template(template_alias: str) -> MailingTemplate:
    templates = Dependencies.get_templates()

    if template_alias in templates.templates:
        return templates[template_alias]

    raise ObjectNotFound()


@router.post(
    "/templates/{template_alias}/render",
    responses={200: {"description": "Template rendered"}, **ObjectNotFound.responses},
)
async def render_template(template_alias: str) -> RenderedTemplate:
    templates = Dependencies.get_templates()

    if template_alias in templates.templates:
        example_user = UserData.example()
        template: MailingTemplate = templates[template_alias]
        return RenderedTemplate(
            html=template.render_html(example_user),
            subject=template.subject,
        )

    raise ObjectNotFound()


@router.get(
    "/templates/{template_alias}/render.html",
    responses={200: {"description": "Template rendered"}, **ObjectNotFound.responses},
    response_class=HTMLResponse,
)
async def render_template_as_html(template_alias: str) -> str:
    templates = Dependencies.get_templates()

    if template_alias in templates.templates:
        example_user = UserData.example()
        template: MailingTemplate = templates[template_alias]
        return template.render_html(example_user)

    raise ObjectNotFound()


@router.get("/templates")
async def get_all_templates() -> TemplatesList:
    templates = Dependencies.get_templates()

    return templates
