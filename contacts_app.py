import sqlite3
import re
# Used to create and interact with the database
# Used for input validation using regular expressions

# DATABASE SETUP
def connect_db():
    conn = sqlite3.connect("contacts.db")
    cur = conn.cursor()

    # Create a table to store contacts (if it doesn't already exist)

    cur.execute("""CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    address TEXT
                )""")
    conn.commit()
    return conn


# For addind contact
def add_contact(conn):
    name = input("Enter full name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email (optional): ")
    address = input("Enter postal address: ")

    # Validation
    if not re.match(r"^\+?\d{7,15}$", phone):
        print("\n❌ Invalid phone number format. Must contain 7-15 digits.\n")
        return

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("\n❌ Invalid email format.\n")
        return

    try:
        conn.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                     (name, phone, email, address))
        conn.commit()
        print("\n✔ Contact added successfully!\n")
    except sqlite3.IntegrityError:
        print("\n⚠ Phone number already exists. Use a different one.\n")


# ----------------- VIEW CONTACTS -----------------
def view_contacts(conn):
    cursor = conn.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    if not data:
        print("\n📭 No contacts found.\n")
        return

    print("\n========== CONTACT LIST ==========")
    for c in data:
        print(f"ID: {c[0]} | Name: {c[1]} | Phone: {c[2]} | Email: {c[3]} | Address: {c[4]}")
    print("==================================\n")


# ----------------- SEARCH CONTACT -----------------
def search_contact(conn):
    key = input("Enter name/phone/email/address to search: ").lower()
    cursor = conn.execute("""
        SELECT * FROM contacts 
        WHERE lower(name) LIKE ? OR phone LIKE ? OR lower(email) LIKE ? OR lower(address) LIKE ?""",
        (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%")
    )
    results = cursor.fetchall()

    if results:
        print("\n🔎 Search Results:")
        for c in results:
            print(f"ID: {c[0]} | Name: {c[1]} | Phone: {c[2]} | Email: {c[3]} | Address: {c[4]}")
        print()
    else:
        print("\n❌ No matching contact found.\n")


# ----------------- UPDATE CONTACT -----------------
def update_contact(conn):
    view_contacts(conn)
    contact_id = input("Enter the contact ID you want to update: ")

    name = input("New name (leave empty to keep current): ")
    phone = input("New phone (optional): ")
    email = input("New email (optional): ")
    address = input("New address (optional): ")

    query = "UPDATE contacts SET "
    values = []
    if name:
        query += "name=?, "
        values.append(name)
    if phone:
        if not re.match(r"^\+?\d{7,15}$", phone):
            print("\n❌ Invalid phone format.\n")
            return
        query += "phone=?, "
        values.append(phone)
    if email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("\n❌ Invalid email.\n")
            return
        query += "email=?, "
        values.append(email)
    if address:
        query += "address=?, "
        values.append(address)

    if not values:
        print("\n⚠ Nothing to update.\n")
        return

    query = query.rstrip(", ") + " WHERE id=?"
    values.append(contact_id)
    conn.execute(query, tuple(values))
    conn.commit()
    print("\n✔ Contact updated successfully!\n")


# ----------------- DELETE CONTACT -----------------
def delete_contact(conn):
    view_contacts(conn)
    contact_id = input("Enter the contact ID to delete: ")

    conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    print("\n🗑 Contact deleted successfully!\n")


# ----------------- MAIN MENU -----------------
def menu():
    conn = connect_db()

    while True:
        print("""
===== CONTACT MANAGEMENT SYSTEM =====
1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Exit
-------------------------------------
""")
        choice = input("Select an option: ")

        if choice == "1": add_contact(conn)
        elif choice == "2": view_contacts(conn)
        elif choice == "3": search_contact(conn)
        elif choice == "4": update_contact(conn)
        elif choice == "5": delete_contact(conn) 
        elif choice == "6":
            print("\nGoodbye! 👋\n")
            conn.close()
            break
        else:
            print("\n❌ Invalid option. Try again.\n")


if __name__ == "__main__":
    menu()
