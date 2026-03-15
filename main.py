import sqlite3
from datetime import datetime

DB_PATH = "expenses.db"

VALID_CATEGORIES = [
    "Housing", "Transportation", "Food & Dining", "Utilities",
    "Healthcare", "Entertainment", "Shopping", "Personal Care",
    "Education", "Savings & Investments", "Income", "Other"
]

con = sqlite3.connect(DB_PATH)
cur = con.cursor()


# ── DATABASE SETUP ────────────────────────────────────────────────────────────

cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_revenue BOOLEAN NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        description TEXT,
        category TEXT NOT NULL CHECK(category IN (
            'Housing',
            'Transportation',
            'Food & Dining',
            'Utilities',
            'Healthcare',
            'Entertainment',
            'Shopping',
            'Personal Care',
            'Education',
            'Savings & Investments',
            'Income',
            'Other'
        )),
        date_added DATE NOT NULL DEFAULT (DATE('now')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
            """)
con.commit()
        

# ── CREATE ───────────────────────────────────────────────────

def get_date_input(prompt):
    while True:
        date_str = input(prompt).strip()
        if date_str == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD, or press Enter for today.")

def get_category_input():
    print("\nCategories:")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Choose a category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(VALID_CATEGORIES):
            return VALID_CATEGORIES[int(choice) - 1]
        print(f"Please enter a number between 1 and {len(VALID_CATEGORIES)}.")

def get_amount_input(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return round(amount, 2)
        except ValueError:
            print("Invalid amount. Please enter a number (e.g. 42.50).")

def insert_transaction(is_revenue: bool):
    label = "Revenue" if is_revenue else "Expense"
    print(f"\n--- Add {label} ---")

    amount      = get_amount_input("Amount: ")
    description = input("Description: ").strip()
    category    = get_category_input()
    date_added  = get_date_input("Date (YYYY-MM-DD, or Enter for today): ")

    sql = """
        INSERT INTO expenses (is_revenue, amount, description, category, date_added)
        VALUES (?, ?, ?, ?, ?)
    """
    params = (is_revenue, amount, description, category, date_added)

    cur.execute(sql, params)
    con.commit()
    print(f"\n✓ {label} of ${amount:.2f} added (id={cur.lastrowid}).")

def add_revenue():
    insert_transaction(is_revenue=True)

def add_expense():
    insert_transaction(is_revenue=False)


# ── READ ───────────────────────────────────────────────────

def format_currency(amount):
    return f"${amount:,.2f}"

def print_summary(rows):
    rows = list(rows)  
    total_revenue = sum(r["amount"] for r in rows if r["is_revenue"])
    total_expenses = sum(r["amount"] for r in rows if not r["is_revenue"])
    net = total_revenue - total_expenses

    print(f"\n{'─' * 40}")
    print(f"  Total Revenue:  {format_currency(total_revenue)}")
    print(f"  Total Expenses: {format_currency(total_expenses)}")
    print(f"  Net:            {format_currency(net)} {'✓' if net >= 0 else '↓'}")
    print(f"{'─' * 40}")

def print_rows(rows):
    if not rows:
        print("  No transactions found.")
        return
    for row in rows:
        tag = "+" if row["is_revenue"] else "-"
        print(f"  [{tag}] {row['date_added']}  {row['category']:<22} {format_currency(row['amount']):<12}  {row['description']}")

def read_by_month(year: int = None, month: int = None):
    """
    Read all transactions for a given month and year.
    Defaults to the current month if no arguments are provided.
    """
    if year is None or month is None:
        today = datetime.today()
        year, month = today.year, today.month

    month_str = f"{year}-{month:02d}"
    print(f"\n{'═' * 40}")
    print(f"  Transactions for {month_str}")
    print(f"{'═' * 40}")

    sql = """
        SELECT id, is_revenue, amount, description, category, date_added
        FROM expenses
        WHERE strftime('%Y-%m', date_added) = ?
        ORDER BY date_added ASC, id ASC
    """


    con.row_factory = sqlite3.Row
    rows = con.execute(sql, (month_str,)).fetchall()

    print_rows(rows)
    print_summary(rows)

def read_by_category(category: str = None):
    """
    Read all transactions for a given category.
    If no category is provided, the user is prompted to choose one.
    """
    if category is None:
        category = get_category_input()

    print(f"\n{'═' * 40}")
    print(f"  transactions for '{category}'")
    print(f"{'═' * 40}")

    sql = """
        SELECT id, is_revenue, amount, description, category, date_added
        FROM expenses
        WHERE category = ?
        ORDER BY date_added ASC, id ASC
    """

    con.row_factory = sqlite3.Row
    rows = con.execute(sql, (category,)).fetchall()

    print_rows(rows)
    print_summary(rows)

# ── UPDATE ───────────────────────────────────────────────────

def get_transaction_by_id(conn, transaction_id: int):
    sql = "SELECT * FROM expenses WHERE id = ?"
    conn.row_factory = sqlite3.Row
    return conn.execute(sql, (transaction_id,)).fetchone()

def prompt_update_fields(existing):
    """
    Show the current values and prompt the user for new ones.
    Press Enter to keep the existing value for any field.
    """
    print("\nLeave a field blank to keep the current value.\n")

    # --- Amount ---
    while True:
        val = input(f"  Amount [{existing['amount']:.2f}]: ").strip()
        if val == "":
            new_amount = existing["amount"]
            break
        try:
            new_amount = round(float(val), 2)
            if new_amount <= 0:
                print("  Amount must be greater than zero.")
            else:
                break
        except ValueError:
            print("  Invalid amount.")

    # --- Description ---
    val = input(f"  Description [{existing['description']}]: ").strip()
    new_description = val if val else existing["description"]

    # --- Category ---
    print(f"  Category [{existing['category']}]: ")
    print("  Choose a new category:")
    val = input("  Change category? (y/n): ").strip().lower()
    new_category = get_category_input() if val == "y" else existing["category"]

    # --- Date ---
    while True:
        val = input(f"  Date [{existing['date_added']}]: ").strip()
        if val == "":
            new_date = existing["date_added"]
            break
        try:
            datetime.strptime(val, "%Y-%m-%d")
            new_date = val
            break
        except ValueError:
            print("  Invalid date format. Use YYYY-MM-DD.")

    # --- Revenue/Expense ---
    current_type = "Revenue" if existing["is_revenue"] else "Expense"
    val = input(f"  Type [{current_type}] — flip to {'Expense' if existing['is_revenue'] else 'Revenue'}? (y/n): ").strip().lower()
    new_is_revenue = (not existing["is_revenue"]) if val == "y" else existing["is_revenue"]

    return {
        "amount":      new_amount,
        "description": new_description,
        "category":    new_category,
        "date_added":  new_date,
        "is_revenue":  new_is_revenue,
    }

def update_transaction():
    # pick month
    print("\n--- Update a Transaction ---")
    print("First, choose a month to browse.\n")
    year, month = choose_month()

    # display that month's transactions
    month_str = f"{year}-{month:02d}"
    sql_fetch = """
        SELECT id, is_revenue, amount, description, category, date_added
        FROM expenses
        WHERE strftime('%Y-%m', date_added) = ?
        ORDER BY date_added ASC, id ASC
    """

    con.row_factory = sqlite3.Row
    rows = con.execute(sql_fetch, (month_str,)).fetchall()

    if not rows:
        print(f"\n  No transactions found for {month_str}.")
        return

    print(f"\n{'═' * 52}")
    print(f"  Transactions for {month_str}")
    print(f"{'═' * 52}")
    for row in rows:
        tag = "+" if row["is_revenue"] else "-"
        print(f"  ID {row['id']:<5} [{tag}] {row['date_added']}  {row['category']:<22} {format_currency(row['amount']):<12}  {row['description']}")
    print(f"{'═' * 52}")

    # pick ID
    valid_ids = {row["id"] for row in rows}
    while True:
        try:
            chosen_id = int(input("\n  Enter the ID to update: ").strip())
            if chosen_id in valid_ids:
                break
            print(f"  ID {chosen_id} is not in the list above. Please choose from the listed IDs.")
        except ValueError:
            print("  Please enter a valid number.")

    # collect updates
    existing = get_transaction_by_id(con, chosen_id)

    print(f"\n  Editing transaction ID {chosen_id}:")
    updated = prompt_update_fields(existing)

    # confirm
    print(f"\n  Summary of changes for ID {chosen_id}:")
    fields = ["is_revenue", "amount", "description", "category", "date_added"]
    any_changes = False
    for field in fields:
        old, new = existing[field], updated[field]
        if old != new:
            print(f"    {field}: {old!r}  →  {new!r}")
            any_changes = True
    if not any_changes:
        print("  No changes made.")
        return

    confirm = input("\n  Save changes? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Update cancelled.")
        return

    # commit
    sql_update = """
        UPDATE expenses
        SET is_revenue  = ?,
            amount      = ?,
            description = ?,
            category    = ?,
            date_added  = ?
        WHERE id = ?
    """
    params = (
        updated["is_revenue"],
        updated["amount"],
        updated["description"],
        updated["category"],
        updated["date_added"],
        chosen_id,
    )

    con.execute(sql_update, params)
    con.commit()

    print(f"\n  ✓ Transaction ID {chosen_id} updated successfully.")

# ── DELETE ───────────────────────────────────────────────────

def delete_transaction():
    # pick a month
    print("\n--- Delete a Transaction ---")
    print("First, choose a month to browse.\n")
    year, month = choose_month()

    # display month
    month_str = f"{year}-{month:02d}"
    sql_fetch = """
        SELECT id, is_revenue, amount, description, category, date_added
        FROM expenses
        WHERE strftime('%Y-%m', date_added) = ?
        ORDER BY date_added ASC, id ASC
    """

    con.row_factory = sqlite3.Row
    rows = con.execute(sql_fetch, (month_str,)).fetchall()

    if not rows:
        print(f"\n  No transactions found for {month_str}.")
        return

    print(f"\n{'═' * 52}")
    print(f"  Transactions for {month_str}")
    print(f"{'═' * 52}")
    for row in rows:
        tag = "+" if row["is_revenue"] else "-"
        print(f"  ID {row['id']:<5} [{tag}] {row['date_added']}  {row['category']:<22} {format_currency(row['amount']):<12}  {row['description']}")
    print(f"{'═' * 52}")

    # pick ID
    valid_ids = {row["id"] for row in rows}
    while True:
        try:
            chosen_id = int(input("\n  Enter the ID to delete: ").strip())
            if chosen_id in valid_ids:
                break
            print(f"  ID {chosen_id} is not in the list above. Please choose from the listed IDs.")
        except ValueError:
            print("  Please enter a valid number.")

    # confirm
    target = next(row for row in rows if row["id"] == chosen_id)
    tag = "+" if target["is_revenue"] else "-"

    print(f"\n  You are about to permanently delete:")
    print(f"  ID {target['id']}  [{tag}]  {target['date_added']}  {target['category']}  {format_currency(target['amount'])}  {target['description']}")
    print(f"\n  This action cannot be undone.")
    print(f"\n  Are you sure?")

    confirm = input("  Type 'YES' to confirm: ").strip()
    if confirm != "YES":
        print("  Deletion cancelled.")
        return

    # delete
    sql_delete = "DELETE FROM expenses WHERE id = ?"

    con.execute(sql_delete, (chosen_id,))
    con.commit()

    print(f"\n  ✓ Transaction ID {chosen_id} deleted successfully.")

# ── HELPER ───────────────────────────────────────────────────

def choose_month():
    today = datetime.today()
    while True:
        try:
            year_input  = input("  Year  (e.g. 2026) or press Enter for current year: ").strip()
            month_input = input("  Month (1-12) or press Enter for current month: ").strip()

            year = year_input if year_input else today.year
            month = month_input if month_input else today.month

            if 1 <= month <= 12:
                break
            print("  Month must be between 1 and 12.")
        except ValueError:
            print("  Please enter valid numbers.")
    
    return year, month

# ── CLI LOOP ───────────────────────────────────────────────────

def main():
    while True:
        print("\n" + "=" * 40)
        print("  Expense Tracker")
        print("=" * 40)
        print("1. Add Revenue")
        print("2. Add Expense")
        print("3. View by Month")
        print("4. View by Category")
        print("5. Update a Transaction")
        print("6. Delete a Transaction")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()
        if choice == "1":
            add_revenue()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            print("Choose a month.\n")
            year, month = choose_month()
            read_by_month(year, month)
        elif choice == "4":
            read_by_category()
        elif choice == "5":
            update_transaction()
        elif choice == "6":
            delete_transaction()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please choose a number from the menu.")

if __name__ == "__main__":
    main()