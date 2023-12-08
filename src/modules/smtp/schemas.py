from pydantic import Field, BaseModel


class MailingTemplate(BaseModel):
    subject: str = Field("Авторизация в Кибер.Базе", description="Subject of the email")
    file: str = Field("auth-code.jinja2", description="Path to the template file (relative to static folder)")

    def render_html(self, **environment) -> str:
        from src.api.dependencies import Dependencies

        main = Dependencies.get_jinja2_env().get_template(self.file)

        html = main.render(**environment)
        return html
