# ---------------------------------------------------------
# Contact Management System
# Author: Basana Venkata Karthik
# Week 3 - Functions & Dictionaries (Professional)
# ---------------------------------------------------------

import json
import re
import csv
import os
from datetime import datetime

DATA_FILE = "contacts_data.json"
BACKUP_FILE = "contacts_backup.json"

def load_contacts(path=DATA_FILE):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: contacts file is corrupt. Starting with empty contacts.")
        return {}

def save_contacts(contacts, path=DATA_FILE):
    with open(path, 'w') as f:
        json.dump(contacts, f, indent=4)
    print(f"✅ Contacts saved to {path}")

def backup_contacts(contacts, path=BACKUP_FILE):
    with open(path, 'w') as f:
        json.dump(contacts, f, indent=4)
    print(f"🔁 Backup created at {path}")

def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")
    name = input("Enter contact name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if name in contacts:
        print(f"Contact '{name}' already exists.")
        if input("Update existing? (y/n): ").lower().startswith('y'):
            update_contact(contacts, name)
        return

    phone = input("Enter phone number: ").strip()
    valid, cleaned = validate_phone(phone)
    while not valid:
        print("Invalid phone number. Enter 10-15 digits (you may include + or -).")
        phone = input("Enter phone number: ").strip()
        valid, cleaned = validate_phone(phone)

    email = input("Enter email (optional): ").strip()
    while email and not validate_email(email):
        print("Invalid email format.")
        email = input("Enter email (optional): ").strip()

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other) [Other]: ").strip() or "Other"

    contacts[name] = {
        "phone": cleaned,
        "email": email or None,
        "address": address or None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    save_contacts(contacts)

def search_contacts(contacts, term):
    term = term.lower()
    results = {name: info for name, info in contacts.items() if term in name.lower() or term in (info.get('phone') or '')}
    return results

def display_contact(name, info):
    print("--------------------------------------------------")
    print(f"👤 {name}")
    print(f"   📞 {info.get('phone')}")
    if info.get('email'):
        print(f"   📧 {info.get('email')}")
    if info.get('address'):
        print(f"   📍 {info.get('address')}")
    print(f"   👥 Group: {info.get('group')}")
    print("--------------------------------------------------")

def display_all(contacts):
    if not contacts:
        print("No contacts to show.")
        return
    print(f"\n--- ALL CONTACTS ({len(contacts)}) ---")
    for i, (name, info) in enumerate(sorted(contacts.items()), 1):
        print(f"{i}. {name} - {info.get('phone')} ({info.get('group')})")

def update_contact(contacts, name=None):
    if not name:
        name = input("Enter contact name to update: ").strip()
    if name not in contacts:
        print("Contact not found.")
        return
    info = contacts[name]
    print("Leave blank to keep current value.")
    phone = input(f"Phone [{info.get('phone')}]: ").strip() or info.get('phone')
    valid, cleaned = validate_phone(phone)
    if not valid:
        print("Invalid phone. Update cancelled.")
        return
    email = input(f"Email [{info.get('email') or ''}]: ").strip() or info.get('email')
    if email and not validate_email(email):
        print("Invalid email. Update cancelled.")
        return
    address = input(f"Address [{info.get('address') or ''}]: ").strip() or info.get('address')
    group = input(f"Group [{info.get('group') or 'Other'}]: ").strip() or info.get('group')
    contacts[name] = {
        "phone": cleaned,
        "email": email or None,
        "address": address or None,
        "group": group,
        "created_at": info.get('created_at'),
        "updated_at": datetime.now().isoformat()
    }
    save_contacts(contacts)
    print(f"✅ Contact '{name}' updated.")

def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip()
    if name not in contacts:
        print("Contact not found.")
        return
    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
    if confirm.startswith('y'):
        contacts.pop(name)
        save_contacts(contacts)
        print(f"✅ Contact '{name}' deleted.")

def export_csv(contacts, filename="contacts_export.csv"):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name","phone","email","address","group","created_at","updated_at"])
        for name, info in contacts.items():
            writer.writerow([name, info.get('phone'), info.get('email'), info.get('address'), info.get('group'), info.get('created_at'), info.get('updated_at')])
    print(f"✅ Exported contacts to {filename}")

def stats(contacts):
    total = len(contacts)
    groups = {}
    for info in contacts.values():
        grp = info.get('group') or 'Other'
        groups[grp] = groups.get(grp, 0) + 1
    recent = sorted(contacts.items(), key=lambda x: x[1].get('updated_at') or '', reverse=True)[:5]
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {total}")
    print("\nContacts by Group:")
    for g, c in groups.items():
        print(f"  {g}: {c} contact(s)")
    print("\nRecently Updated:")
    for name, info in recent:
        print(f"  {name} (updated: {info.get('updated_at')})")

def main_menu():
    contacts = load_contacts()
    if not contacts:
        print("✅ No existing contacts file found. Starting fresh.")
    while True:
        print("\n" + "="*30)
        print("      CONTACT MANAGEMENT SYSTEM")
        print("="*30)
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Backup Contacts")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ").strip()
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            q = input("Enter name or phone to search: ").strip()
            if q:
                res = search_contacts(contacts, q)
                if res:
                    for i, (n, info) in enumerate(res.items(),1):
                        print(f"\nResult {i}:")
                        display_contact(n, info)
                else:
                    print("No contacts found.")
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            display_all(contacts)
        elif choice == '6':
            export_csv(contacts)
        elif choice == '7':
            stats(contacts)
        elif choice == '8':
            backup_contacts(contacts)
        elif choice == '9':
            save_contacts(contacts)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-9.")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting gracefully.")