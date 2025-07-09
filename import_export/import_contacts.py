import csv
from models.contact import add_contact

def import_contacts_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            tag = row.get('tag', '').strip()
            if name and email:
                add_contact(name, email, tag)
