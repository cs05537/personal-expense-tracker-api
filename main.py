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

# ΝΕΑ ΣΥΝΑΡΤΗΣΗ: Προσθήκη Εξόδου
def add_expense():
    print("\n--- Νέα Καταχώρηση ---")
    try:
        # Ζητάμε το ποσό και το μετατρέπουμε σε δεκαδικό αριθμό (float)
        amount = float(input("Δώσε ποσό σε ευρώ (π.χ. 3.50): "))
    except ValueError:
        print("[!] Λάθος: Πρέπει να γράψεις αριθμό. Δοκίμασε ξανά.")
        return

    category = input("Κατηγορία (π.χ. Καφές, Supermarket, Βενζίνη): ")
    description = input("Περιγραφή (προαιρετικά, πάτα Enter για κενό): ")
    
    # Παίρνουμε την τωρινή ημερομηνία και ώρα αυτόματα
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Εισαγωγή των δεδομένων στη βάση (SQL) με ασφαλή τρόπο χρησιμοποιώντας τα '?'
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, current_date))
    
    conn.commit()
    print(f"\n[+] Επιτυχία! Το έξοδο καταχωρήθηκε: {amount}€ για '{category}'.")


def main():
    while True:
        print("\n--- Διαχειριστής Προσωπικών Εξόδων ---")
        print("1. Προσθήκη νέου εξόδου")
        print("2. Προβολή όλων των εξόδων")
        print("3. Έξοδος")
        
        choice = input("Επίλεξε μια ενέργεια (1-3): ")
        
        if choice == '1':
            add_expense() # Καλεί τη νέα μας συνάρτηση!
        elif choice == '2':
            print("\n[!] Εδώ θα γράψουμε τον κώδικα για την προβολή...")
        elif choice == '3':
            print("\nΚλείσιμο προγράμματος. Τα λέμε!")
            conn.close()
            break
        else:
            print("\nΛάθος επιλογή. Πληκτρολόγησε 1, 2 ή 3.")

if __name__ == "__main__":
    main()