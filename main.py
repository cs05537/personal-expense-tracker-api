import sqlite3
from datetime import datetime

# Σύνδεση με τη βάση δεδομένων
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Δημιουργία του πίνακα 'expenses'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL
    )
''')
conn.commit()


def add_expense():
    print("\n--- Νέα Καταχώρηση ---")
    try:
        amount = float(input("Δώσε ποσό σε ευρώ (π.χ. 3.50): "))
    except ValueError:
        print("[!] Λάθος: Πρέπει να γράψεις αριθμό. Δοκίμασε ξανά.")
        return

    category = input("Κατηγορία (π.χ. Καφές, Supermarket, Βενζίνη): ")
    description = input("Περιγραφή (προαιρετικά, πάτα Enter για κενό): ")
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, current_date))
    
    conn.commit()
    print(f"\n[+] Επιτυχία! Το έξοδο καταχωρήθηκε: {amount}€ για '{category}'.")


# ΝΕΑ ΣΥΝΑΡΤΗΣΗ: Προβολή Εξόδων
def view_expenses():
    print("\n--- Λίστα Εξόδων ---")
    
    # Παίρνουμε όλα τα δεδομένα από τον πίνακα expenses
    cursor.execute("SELECT id, amount, category, description, date FROM expenses")
    rows = cursor.fetchall() # Το fetchall() επιστρέφει μια λίστα με όλες τις γραμμές
    
    if not rows:
        print("[!] Δεν υπάρχουν καταχωρημένα έξοδα ακόμα.")
        return

    total_spend = 0.0
    
    # Εμφανίζουμε κάθε έξοδο σε γραμμές
    for row in rows:
        expense_id = row[0]
        amount = row[1]
        category = row[2]
        description = row[3] if row[3] else "-" # Αν δεν έχει περιγραφή, βάλε μια παύλα
        date = row[4]
        
        print(f"[{expense_id}] {date} | {category}: {amount}€ ({description})")
        total_spend += amount # Προσθέτουμε το ποσό στο σύνολο

    print("-" * 40)
    print(f"ΣΥΝΟΛΙΚΑ ΕΞΟΔΑ: {total_spend:.2f}€")


def main():
    while True:
        print("\n--- Διαχειριστής Προσωπικών Εξόδων ---")
        print("1. Προσθήκη νέου εξόδου")
        print("2. Προβολή όλων των εξόδων")
        print("3. Έξοδος")
        
        choice = input("Επίλεξε μια ενέργεια (1-3): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses() # Καλεί τη νέα μας συνάρτηση!
        elif choice == '3':
            print("\nΚλείσιμο προγράμματος. Τα λέμε!")
            conn.close()
            break
        else:
            print("\nΛάθος επιλογή. Πληκτρολόγησε 1, 2 ή 3.")

if __name__ == "__main__":
    main()