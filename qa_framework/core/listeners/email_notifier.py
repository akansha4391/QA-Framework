import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from qa_framework.core.logger import get_logger

logger = get_logger("email_notifier")

class EmailNotifier:
    """
    Simple Email Notifier.
    """
    def __init__(self, smtp_server: str, port: int, sender_email: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, recipient: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.sender_email, self.password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient, text)
            server.quit()
            logger.info(f"Email sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
