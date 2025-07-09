import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

def send_email(subject, body, recipients, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(recipients)

    # ✅ Configura el mensaje como HTML
    msg.set_content(body)  # Texto plano como respaldo
    msg.add_alternative(f"""\
    <html>
        <body>
            {body}
        </body>
    </html>
    """, subtype='html')

    # ✅ Adjuntar archivo si hay
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # ✅ Enviar email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
