import sqlite3

DB_PATH = 'contacts.db'

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

def add_contact(name, email, tag=''):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, email, tag) VALUES (?, ?, ?)', (name, email, tag))
    conn.commit()
    conn.close()

def get_all_contacts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, tag FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def delete_contact(contact_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()
