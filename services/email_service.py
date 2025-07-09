import smtplib
from email.message import EmailMessage
import os

# Configuración SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

def send_email(subject, body, recipients, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ', '.join(recipients)

    # 🛡️ Plantilla HTML base
    html_template = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          
          <h2 style="color: #4A90E2;">💬 Notificación de Mass Messaging</h2>

          <div style="margin-top: 20px; font-size: 16px; color: #333;">
            {body}
          </div>

          <hr style="margin-top: 30px;">
          <footer style="font-size: 12px; color: #777;">
            Este mensaje fue enviado automáticamente desde tu aplicación.<br>
            Mass Messaging App © 2025
          </footer>
        </div>
      </body>
    </html>
    """

    # 🛡️ Mensaje de texto plano (fallback)
    msg.set_content(body)

    # 🛡️ Mensaje HTML principal
    msg.add_alternative(html_template, subtype='html')

    # ✅ Adjuntar archivo si hay
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # ✅ Enviar correo
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
