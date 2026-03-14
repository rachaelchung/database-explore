from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))

DB_PATH = "expenses.db"

VALID_CATEGORIES = [
    "Housing", "Transportation", "Food & Dining", "Utilities",
    "Healthcare", "Entertainment", "Shopping", "Personal Care",
    "Education", "Savings & Investments", "Income", "Other"
]


# ── DATABASE SETUP ────────────────────────────────────────────────────────────

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_revenue BOOLEAN NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT,
            category TEXT NOT NULL CHECK(category IN (
                'Housing','Transportation','Food & Dining','Utilities',
                'Healthcare','Entertainment','Shopping','Personal Care',
                'Education','Savings & Investments','Income','Other'
            )),
            date_added DATE NOT NULL DEFAULT (DATE('now')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    return con


def row_to_dict(row):
    return {
        "id": row["id"],
        "is_revenue": bool(row["is_revenue"]),
        "amount": float(row["amount"]),
        "description": row["description"],
        "category": row["category"],
        "date_added": row["date_added"],
    }


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "static"), "index.html")


@app.route("/api/categories", methods=["GET"])
def get_categories():
    return jsonify(VALID_CATEGORIES)


@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    month = request.args.get("month")   # YYYY-MM
    category = request.args.get("category")

    con = get_db()
    if month:
        rows = con.execute("""
            SELECT id, is_revenue, amount, description, category, date_added
            FROM expenses
            WHERE strftime('%Y-%m', date_added) = ?
            ORDER BY date_added ASC, id ASC
        """, (month,)).fetchall()
    elif category:
        rows = con.execute("""
            SELECT id, is_revenue, amount, description, category, date_added
            FROM expenses
            WHERE category = ?
            ORDER BY date_added ASC, id ASC
        """, (category,)).fetchall()
    else:
        rows = con.execute("""
            SELECT id, is_revenue, amount, description, category, date_added
            FROM expenses
            ORDER BY date_added DESC, id DESC
            LIMIT 100
        """).fetchall()
    con.close()
    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    is_revenue = data.get("is_revenue", False)
    amount = data.get("amount")
    description = data.get("description", "")
    category = data.get("category")
    date_added = data.get("date_added") or datetime.today().strftime("%Y-%m-%d")

    if not amount or amount <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400
    if category not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400
    try:
        datetime.strptime(date_added, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    con = get_db()
    cur = con.execute("""
        INSERT INTO expenses (is_revenue, amount, description, category, date_added)
        VALUES (?, ?, ?, ?, ?)
    """, (is_revenue, round(float(amount), 2), description, category, date_added))
    con.commit()
    new_id = cur.lastrowid
    row = con.execute("SELECT * FROM expenses WHERE id = ?", (new_id,)).fetchone()
    con.close()
    return jsonify(row_to_dict(row)), 201


@app.route("/api/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    data = request.json
    con = get_db()
    existing = con.execute("SELECT * FROM expenses WHERE id = ?", (transaction_id,)).fetchone()
    if not existing:
        con.close()
        return jsonify({"error": "Transaction not found"}), 404

    amount = data.get("amount", existing["amount"])
    description = data.get("description", existing["description"])
    category = data.get("category", existing["category"])
    date_added = data.get("date_added", existing["date_added"])
    is_revenue = data.get("is_revenue", existing["is_revenue"])

    if float(amount) <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400
    if category not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    con.execute("""
        UPDATE expenses
        SET is_revenue=?, amount=?, description=?, category=?, date_added=?
        WHERE id=?
    """, (is_revenue, round(float(amount), 2), description, category, date_added, transaction_id))
    con.commit()
    row = con.execute("SELECT * FROM expenses WHERE id = ?", (transaction_id,)).fetchone()
    con.close()
    return jsonify(row_to_dict(row))


@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    con = get_db()
    existing = con.execute("SELECT * FROM expenses WHERE id = ?", (transaction_id,)).fetchone()
    if not existing:
        con.close()
        return jsonify({"error": "Transaction not found"}), 404
    con.execute("DELETE FROM expenses WHERE id = ?", (transaction_id,))
    con.commit()
    con.close()
    return jsonify({"deleted": transaction_id})


@app.route("/api/summary", methods=["GET"])
def get_summary():
    month = request.args.get("month")
    con = get_db()
    if month:
        rows = con.execute("""
            SELECT is_revenue, SUM(amount) as total
            FROM expenses
            WHERE strftime('%Y-%m', date_added) = ?
            GROUP BY is_revenue
        """, (month,)).fetchall()
    else:
        rows = con.execute("""
            SELECT is_revenue, SUM(amount) as total
            FROM expenses
            GROUP BY is_revenue
        """).fetchall()
    con.close()

    revenue = 0.0
    expenses = 0.0
    for row in rows:
        if row["is_revenue"]:
            revenue = float(row["total"])
        else:
            expenses = float(row["total"])

    return jsonify({
        "revenue": revenue,
        "expenses": expenses,
        "net": revenue - expenses
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)