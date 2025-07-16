import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_with_pdf(pdf_path, receivers):
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    for receiver_email in receivers:
        message = MIMEMultipart()
        message["Subject"] = "Your Daily Newsletter 📬"
        message["From"] = sender_email
        message["To"] = receiver_email

        body = "Hi there,\n\nPlease find your requested newsletter attached.\n\nRegards,\nNewsletter Bot"
        message.attach(MIMEText(body, "plain"))

        with open(pdf_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(pdf_path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
