import sqlite3

DB_PATH = 'contacts.db'

# ⚙️ Inicializar tabla
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            tag TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ➕ Agregar un contacto
def add_contact(name, email, tag=''):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, email, tag) VALUES (?, ?, ?)', (name, email, tag))
    conn.commit()
    conn.close()

# 🔍 Traer contactos con filtro opcional
def get_all_contacts(tag_filter=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if tag_filter:
        cursor.execute('SELECT id, name, email, tag FROM contacts WHERE tag LIKE ?', ('%' + tag_filter + '%',))
    else:
        cursor.execute('SELECT id, name, email, tag FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

# ❌ Eliminar contacto
def delete_contact(contact_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()
