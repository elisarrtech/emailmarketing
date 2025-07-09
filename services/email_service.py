import smtplib
from email.message import EmailMessage
import os

# Configuración SMTP desde variables de entorno
SMTP_SERVER = 'smtp.gmail.com'  # Podrías moverlo a config.py o variable de entorno si después quieres más flexibilidad
SMTP_PORT = 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

def send_email(subject, body, recipients, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    # Adjuntar archivo si lo hay
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Conexión y envío
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
