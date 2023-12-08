__all__ = ["SMTPRepository"]

import contextlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_validator import validate_email, EmailNotValidError

from src.config import settings
from src.modules.smtp.schemas import MailingTemplate


class SMTPRepository:
    _server: smtplib.SMTP

    def __init__(self):
        self._server = smtplib.SMTP(settings.smtp.server, settings.smtp.port)

    @contextlib.contextmanager
    def _context(self):
        self._server.connect(settings.smtp.server, settings.smtp.port)
        self._server.starttls()
        self._server.login(settings.smtp.username, settings.smtp.password.get_secret_value())
        yield
        self._server.quit()

    def render_message(self, template: "MailingTemplate", target_email: str, **environment) -> str:
        mail = MIMEMultipart("related")
        html = template.render_html(**environment)
        msg_html = MIMEText(html, "html")
        mail.attach(msg_html)

        mail["Subject"] = template.subject
        mail["From"] = settings.smtp.username
        mail["To"] = target_email

        return mail.as_string()

    def send(self, message: str, to: str):
        try:
            valid = validate_email(to)
            to = valid.normalized
        except EmailNotValidError as e:
            raise ValueError(e)
        with self._context():
            self._server.sendmail(settings.smtp.username, to, message)

    # def send_connect_email(self, email: str, auth_code: str):
    #     mail = MIMEMultipart("related")
    #     # Jinja2 for html template
    #     main = Template(
    #         """
    #         <html>
    #             <body>
    #                 <p>Hi!</p>
    #                 <p>Here is your temporary code for registration: {{ code }}</p>
    #             </body>
    #         </html>
    #         """,
    #         autoescape=True,
    #     )
    #
    #     html = main.render(code=auth_code)
    #     msgHtml = MIMEText(html, "html")
    #     mail.attach(msgHtml)
    #
    #     mail["Subject"] = "Registration in Monitoring Service"
    #     mail["From"] = settings.smtp.username
    #     mail["To"] = email
    #
    #     with self._context():
    #         self._server.sendmail(settings.smtp.username, email, mail.as_string())
