import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader


class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, template_dir: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_email(self, to: List[str], subject: str, template_name: str, variables: Dict[str, str]) -> None:
        # Carregar e renderizar o template
        template = self.env.get_template(template_name)
        body = template.render(variables)

        # Criar a mensagem
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Conectar ao servidor SMTP e enviar o e-mail
        with smtplib.SMTP(host=self.smtp_server, port=self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            print("E-mail enviado com sucesso!")
