import sqlite3
from datetime import datetime

# 1. Σύνδεση με τη βάση δεδομένων (Το αρχείο expenses.db θα δημιουργηθεί αυτόματα)
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# 2. Δημιουργία του πίνακα 'expenses' αν δεν υπάρχει ήδη
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

def main():
    while True:
        # 3. Το κεντρικό μενού της εφαρμογής
        print("\n--- Διαχειριστής Προσωπικών Εξόδων ---")
        print("1. Προσθήκη νέου εξόδου")
        print("2. Προβολή όλων των εξόδων")
        print("3. Έξοδος")
        
        choice = input("Επίλεξε μια ενέργεια (1-3): ")
        
        if choice == '1':
            print("\n[!] Εδώ θα γράψουμε τον κώδικα για την προσθήκη...")
        elif choice == '2':
            print("\n[!] Εδώ θα γράψουμε τον κώδικα για την προβολή...")
        elif choice == '3':
            print("\nΚλείσιμο προγράμματος. Τα λέμε!")
            # Κλείνουμε τη σύνδεση με τη βάση πριν κλείσει το πρόγραμμα
            conn.close()
            break
        else:
            print("\nΛάθος επιλογή. Πληκτρολόγησε 1, 2 ή 3.")

if __name__ == "__main__":
    main()