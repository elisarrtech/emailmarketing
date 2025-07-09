from flask import Flask, render_template, request, redirect, url_for, flash
from services.email_service import send_email
from models.contact import init_db as init_contacts_db, add_contact, get_all_contacts, delete_contact
from models.message import init_history as init_history_db, save_message, get_all_messages
import os

# Inicializar base de datos
init_contacts_db()
init_history_db()

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'

# Dashboard principal
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ✅ Ruta GET /send → cargar contactos
@app.route('/send', methods=['GET'])
def send_message():
    contacts = get_all_contacts()  # Traemos todos los contactos
    return render_template('send_message.html', contacts=contacts)

# ✅ Ruta POST /send → procesar formulario
@app.route('/send', methods=['POST'])
def send_message_post():
    subject = request.form['subject']
    body = request.form['body']
    recipients = request.form.getlist('recipients')  # ← aquí el cambio
    attachment = request.files.get('attachment')

    # Guardar archivo temporal si hay
    attachment_path = None
    if attachment and attachment.filename:
        os.makedirs('temp', exist_ok=True)
        attachment_path = os.path.join('temp', attachment.filename)
        attachment.save(attachment_path)

    # Enviar correo
    try:
        send_email(subject, body, recipients, attachment_path)
        save_message(subject, recipients)
        flash('Mensaje enviado con éxito', 'success')
    except Exception as e:
        print(e)
        flash('Error al enviar el mensaje', 'danger')

    # Eliminar archivo temporal
    if attachment_path and os.path.exists(attachment_path):
        os.remove(attachment_path)

    return redirect(url_for('send_message'))

# ✅ Gestión de contactos con filtro por etiqueta
@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tag = request.form.get('tag', '')
        add_contact(name, email, tag)
        flash('Contacto agregado con éxito', 'success')
        return redirect(url_for('manage_contacts'))

    # Filtro por etiqueta
    tag_filter = request.args.get('tag')
    contacts = get_all_contacts(tag_filter)
    return render_template('manage_contacts.html', contacts=contacts, tag_filter=tag_filter)

# ✅ Eliminar contacto
@app.route('/contacts/delete/<int:contact_id>')
def delete_contact_route(contact_id):
    delete_contact(contact_id)
    flash('Contacto eliminado', 'warning')
    return redirect(url_for('manage_contacts'))

# ✅ Ver historial
@app.route('/history')
def view_history():
    messages = get_all_messages()
    return render_template('history.html', messages=messages)

# Render: puerto y host externo
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
