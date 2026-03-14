# Simple Budget Tracker

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