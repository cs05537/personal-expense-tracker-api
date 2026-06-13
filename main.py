from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

# 1. Αρχικοποίηση της εφαρμογής (Το "γκαρσόνι" μας)
app = FastAPI(title="Personal Expense Tracker API")

# 2. Σύνδεση με τη βάση
# Το check_same_thread=False είναι απαραίτητο για web εφαρμογές με SQLite
conn = sqlite3.connect('expenses.db', check_same_thread=False)
cursor = conn.cursor()

# Δημιουργία πίνακα (παραμένει ίδιο)
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

# 3. Μοντέλο Δεδομένων: Πώς περιμένουμε να έρχονται τα νέα έξοδα
class Expense(BaseModel):
    amount: float
    category: str
    description: str = "" # Προαιρετικό, αν δεν μπει θα είναι κενό

# 4. GET Endpoint (Αντικαθιστά το "Προβολή όλων των εξόδων")
@app.get("/expenses")
def get_expenses():
    cursor.execute("SELECT id, amount, category, description, date FROM expenses")
    rows = cursor.fetchall()
    
    expenses_list = []
    total = 0.0
    
    for row in rows:
        expenses_list.append({
            "id": row[0],
            "amount": row[1],
            "category": row[2],
            "description": row[3],
            "date": row[4]
        })
        total += row[1]
        
    # Το API επιστρέφει πάντα δεδομένα σε μορφή JSON (λεξικό της Python)
    return {"total_spent": round(total, 2), "expenses": expenses_list}

# 5. POST Endpoint (Αντικαθιστά το "Προσθήκη νέου εξόδου")
@app.post("/expenses")
def add_expense(expense: Expense):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (expense.amount, expense.category, expense.description, current_date))
    conn.commit()
    
    return {
        "message": "Το έξοδο καταχωρήθηκε επιτυχώς!", 
        "category": expense.category,
        "amount": expense.amount
    }