import sqlite3

DB_PATH = 'contacts.db'

def init_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            recipients TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(subject, recipients):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO message_history (subject, recipients) VALUES (?, ?)', (subject, ', '.join(recipients)))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT subject, recipients, sent_at FROM message_history ORDER BY sent_at DESC')
    messages = cursor.fetchall()
    conn.close()
    return messages

