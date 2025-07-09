from flask import Flask, render_template, request, redirect, url_for, flash
from services.email_service import send_email
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/send', methods=['GET'])
def send_message():
    return render_template('send_message.html')

@app.route('/send', methods=['POST'])
def send_message_post():
    subject = request.form['subject']
    body = request.form['body']
    recipients = [email.strip() for email in request.form['recipients'].split(',')]
    attachment = request.files.get('attachment')

    # Guarda temporalmente el archivo si hay
    attachment_path = None
    if attachment and attachment.filename:
        attachment_path = os.path.join('temp', attachment.filename)
        os.makedirs('temp', exist_ok=True)
        attachment.save(attachment_path)

    # Llama al servicio de email
    try:
        send_email(subject, body, recipients, attachment_path)
        flash('Mensaje enviado con éxito', 'success')
    except Exception as e:
        print(e)
        flash('Error al enviar el mensaje', 'danger')

    # Limpia el archivo
    if attachment_path and os.path.exists(attachment_path):
        os.remove(attachment_path)

    return redirect(url_for('send_message'))

@app.route('/contacts')
def manage_contacts():
    return render_template('manage_contacts.html')

@app.route('/history')
def view_history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)

