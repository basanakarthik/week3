contacts = []

def add_contact(name, phone):
    contacts.append({"Name": name, "Phone": phone})
    print("Contact added successfully!\n")

def search_contact(name):
    for contact in contacts:
        if contact["Name"].lower() == name.lower():
            print(f"Name: {contact['Name']}, Phone: {contact['Phone']}\n")
            return
    print("Contact not found.\n")

def display_contacts():
    if not contacts:
        print("No contacts available.\n")
        return
    print("----- Contact List -----")
    for c in contacts:
        print(f"Name: {c['Name']}, Phone: {c['Phone']}")
    print()

while True:
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Display All Contacts")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        add_contact(name, phone)

    elif choice == "2":
        name = input("Enter name to search: ")
        search_contact(name)

    elif choice == "3":
        display_contacts()

    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Try again.\n")
