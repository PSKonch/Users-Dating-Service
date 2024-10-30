import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config import settings

def send_email(to_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()  
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")