import smtplib
from email.message import EmailMessage

# Configura tus credenciales SMTP aquí o carga desde config.py
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'misselisavirtual@gmail.com'
SMTP_PASSWORD = 'wfzm dvbg hjng vrru'

def send_email(subject, body, recipients, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    # Adjunta archivo si hay
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = attachment_path.split('/')[-1]
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)

