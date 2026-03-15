# Simple Expense Tracker

This is a simple budget tracker app that looks at all of your money (including revenue and expense) so that it can calculate your net costs. I chose this app because when I was home over break, I told my mom I stopped tracking my expenses because it was too complicated to me to add things into a spreadsheet and then do all the sorting and thinking, and that it was unhelpful without space for added money. So I thought this project was perfect to create something simple to solve this.

---

## The Database

| Column | Type | Notes |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | An incrementing ID of items |
| `is_revenue` | `INTEGER NOT NULL` | A boolean (0 and 1 for SQLite) to determine whether the item is revenue or expense |
| `amount` | `REAL NOT NULL` | The amount of the revenue or expense, a real number to two decimal points |
| `description` | `TEXT NOT NULL` | Adding a short description of what an item is |
| `category` | `TEXT NOT NULL` | A set list of categories for each item |
| `date-added` | `TEXT NOT NULL` | The date the item was added, in YYYY-MM-DD format. Either choose the day or get today from `datetime` library |

---

## HOW TO RUN

1. Clone or download this repo
2. Navigate to project folder in terminal

### To run the CLI Loop:
```bash
python3 main.py
```

### To run the Flask App:
```bash
pip install flask
python backend.py
```
View the ap at http://127.0.0.1:5000

---

## CRUD Operations

### CREATE
There are two create options: to add a revenue or an expense. The database stores is_revenue as a boolean, and then you can fill in the rest of the categories yourself with categories from a set list and date from the datetime library.

### READ
The read query lets you read by month and by category. It makes sure to list all objects, then total revenue, total expenses, and net revenue.

### UPDATE
The update query lets you update any object by letting you select from a specific month, then queries you on each data column what to change. It asks for confirmation to change.

### DELETE
The delete query asks you for a specific month, and then lets you pick an object to delete by id. You also need to confirm this before deleting.

### The menu is as such:
- **1. Add Revenue** — CREATE: log incoming money
- **2. Add Expense** — CREATE: log outgoing money
- **3. View by Month** — READ: browse transactions for a given month (and year)
- **4. View by Category** — READ: browse transactions by category
- **5. Update a Transaction** — UPDATE: edit an existing entry
- **6. Delete a Transaction** — DELETE: permanently delete an entry
- **0. Exit** — quit the program