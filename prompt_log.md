I mainly used Claude Sonnet 4.6 for this project.

## Learning SQLite
My thinking in for how to get Claude to give me the best rundown possible was to give it all the information. I have it all the project requirememts to teach me.

---

### ME: Hi! Can you give me a quick rundown of databases and SQLite. I have to complete a project with these requirements:

Goal: Build a small app that uses a SQLite database to store, retrieve, update, and delete data. You'll choose something personally interesting to track and build a working app around it using Python and AI tools.
Why This Matters: Almost every real-world application stores data in a database. Understanding how to create tables, insert records, query data, and modify entries is a foundational skill. In this assignment you'll learn to use SQL (Structured Query Language) to manage persistent data, and you'll see how AI tools can help you learn a new technology quickly.
Examples of what you might build:
* A reading log
* A to-do list
* A workoutjournal
* A recipe collection
* A budget tracker
* A course planner
* Or essentially anything else that interests you
Core Requirements (your app must do all of these)
Your app must use a SQLite database with at least one table containing at least 4 columns (including an id column). Your app must support all four CRUD operations:
OPERATIONWHAT IT MEANSEXAMPLECreateAdd a new record to the databaseAdd a new book to my reading logReadRetrieve and display recordsShow all books I've read this yearUpdateModify an existing recordChange a book's rating from 3 to 4 starsDeleteRemove a record from the databaseRemove a book I added by mistake
Your Read functionality must include at least one query that filters or sorts the data based on user input (e.g., "show only 5-star books" or "show entries sorted by date").
Interface
Your app needs some kind of interactive user interface. You have three options, in order from simplest to most ambitious:
1. Command-line interface (CLI): A terminal-based menu where the user types choices and sees text output. This is the simplest option and (because this assignment is focusing on database functionality) this is perfectly sufficient for full credit.
2. Simple web interface: A Flask app with HTML pages for viewing and managing data (similar to HW4). This gives you more practice with web development.
3. Graphical interface: A desktop app using a library like tkinter or PyQt. Only attempt this if you're comfortable or curious.
Strongly recommended: Start with a CLI. It'll be fastest and easiest to get your database logic working and tested if you aren't simultaneously debugging a complex UI. If you finish early and want to add a web or graphical interface, go for it, but get the core database operations working first. Also, if you get the database and CLI working and you unsuccessfully attempt a graphical interface, you should revert your code (and any edits to your README) to a working CLI version before the deadline so that you can still get full credit. Your README should let us know how to run and/or access a working version of your app.



Let me be able to understand enough to complete this project. I have 30mins

---

### CLAUDE:
# Databases & SQLite in 30 Minutes

## What is a Database?

A database is just **organized, persistent storage** — like a spreadsheet that your code can talk to. Instead of saving data to a plain text file, you store it in structured **tables** with rows and columns.

**SQLite** is the simplest flavor: it's just a single `.db` file on your computer. No server, no setup, no passwords. Python has it built-in.

---

## The Core Idea: Tables

Think of a table exactly like a spreadsheet:

| id | title | author | rating |
|----|-------|--------|--------|
| 1 | Dune | Herbert | 5 |
| 2 | 1984 | Orwell | 4 |

- Each **column** is a field you define upfront
- Each **row** is one record
- `id` is always an auto-incrementing number that uniquely identifies each row

---

## SQL: The Language

SQL is how you talk to the database. There are really only **5 commands you need**:

```sql
-- Create the table (run once)
CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, rating INTEGER);

-- CREATE a record
INSERT INTO books (title, author, rating) VALUES ('Dune', 'Herbert', 5);

-- READ records
SELECT * FROM books;
SELECT * FROM books WHERE rating = 5;   -- filtered
SELECT * FROM books ORDER BY rating;    -- sorted

-- UPDATE a record
UPDATE books SET rating = 4 WHERE id = 1;

-- DELETE a record
DELETE FROM books WHERE id = 2;
```

That's literally CRUD — Create, Read, Update, Delete.

---

## Python + SQLite: The 3-Line Pattern

```python
import sqlite3

conn = sqlite3.connect("myapp.db")  # creates the file if it doesn't exist
cursor = conn.cursor()              # cursor is your "query runner"

cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()            # returns a list of tuples

conn.commit()   # SAVE changes (needed after INSERT/UPDATE/DELETE)
conn.close()    # done
```

The `?` placeholder is how you safely pass user input into queries:
```python
cursor.execute("INSERT INTO books (title, rating) VALUES (?, ?)", ("Dune", 5))
#                                                                   ^ tuple of values
```

---

## A Minimal Working App (CLI skeleton)

```python
import sqlite3

def get_conn():
    conn = sqlite3.connect("books.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS books
                    (id INTEGER PRIMARY KEY, title TEXT, author TEXT, rating INTEGER)""")
    conn.commit()
    return conn

def add_book(title, author, rating):
    conn = get_conn()
    conn.execute("INSERT INTO books (title, author, rating) VALUES (?,?,?)", (title, author, rating))
    conn.commit()

def show_books(min_rating=1):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM books WHERE rating >= ? ORDER BY rating DESC", (min_rating,)).fetchall()
    for row in rows:
        print(row)

def update_rating(book_id, new_rating):
    conn = get_conn()
    conn.execute("UPDATE books SET rating=? WHERE id=?", (new_rating, book_id))
    conn.commit()

def delete_book(book_id):
    conn = get_conn()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()

# CLI loop
while True:
    choice = input("\n1) Add  2) View  3) Update  4) Delete  5) Quit\n> ")
    if choice == "1":
        add_book(input("Title: "), input("Author: "), int(input("Rating: ")))
    elif choice == "2":
        show_books(int(input("Min rating (1-5): ")))
    elif choice == "3":
        update_rating(int(input("ID: ")), int(input("New rating: ")))
    elif choice == "4":
        delete_book(int(input("ID: ")))
    elif choice == "5":
        break
```

This skeleton already satisfies **all core requirements**. Swap in your own topic and columns.

---

## Key Takeaways

| Concept | Remember |
|---|---|
| SQLite file | Just a `.db` file, `sqlite3` is built into Python |
| `CREATE TABLE IF NOT EXISTS` | Safe to call every time app starts |
| Always use `?` placeholders | Never f-strings with user input (security) |
| `conn.commit()` | Required to save INSERT/UPDATE/DELETE |
| `fetchall()` vs `fetchone()` | List of all rows vs just the first |

You have everything you need. Pick a topic you like, copy the skeleton, rename the table/columns, and build your CLI menu around it. Good luck!


---

And then I needed to know what kinds of things people use databases for.

---

### ME: 
awesome! combined with the lecture we were given this makes a lot of sense to me. What kinds of things do people do with databases so I can get an idea of a 3hour project I can do?

---

### CLAUDE: Here are some ideas organized by how interesting/manageable they are for 3 hours:

**Easy wins (2hrs of work, polished result)**
- Movie watchlist — track title, genre, rating, watched date. Filter by genre or rating. Very natural CRUD.
- Gym/workout log — exercise, sets, reps, weight. Query "show all bench press PRs" or progress over time.
- Video game backlog — title, platform, status (playing/finished/dropped), hours played.

**A bit more interesting**
- Budget tracker — amount, category, date, note. Queries like "show all spending in 'food' this month" feel genuinely useful.
- Habit tracker — habit name, date completed, streak. You can write a query that calculates your current streak.
- Music log — song, artist, mood, date listened. Filter by mood. Surprisingly fun.

**More ambitious but doable**
- Flashcard/study app — question, answer, difficulty, last reviewed date. You could implement basic spaced repetition logic.
- Recipe box — recipe name, ingredients, prep time, cuisine. Filter by cuisine or time available.

**My honest recommendation for 3 hours:** pick something you'd actually *use*. The project goes faster when you're not making up fake data. If you go to the gym, do the workout log. If you watch a lot of movies, do the watchlist. The SQL is identical across all of them — the only difference is your column names.

What do you actually spend time on? I can help you pick the best fit.

---

### ME: what about storing things that are multiple choice? Say a piece of data has only specific types that I want the user to pick from, what do you think? And I want to store as holding multiple at the same time

---

# CLAUDE: Great question — this is a real database design decision. You have a few options:

## Option 1: Just store a text string (simplest, fine for 3hrs)
```python
# Store comma-separated values in one column
"action, rpg, open-world"
```
Querying it is a bit hacky (`WHERE genres LIKE '%rpg%'`) but totally works for a small project.

## Option 2: Separate lookup table + junction table (the "correct" way)
This is how real apps do it. Say you're tracking games with multiple genres:

```
games table:          genres table:         game_genres table:
id | title            id | name             game_id | genre_id
1  | Elden Ring        1  | RPG              1       | 1
2  | FIFA              2  | Action           1       | 2
                       3  | Sports           2       | 3
```

This is called a **many-to-many relationship**. Clean, queryable, but adds complexity.

---

## My honest take for your 3-hour project

**Go with Option 1** — store a comma-separated string. Here's why:
- The assignment is testing CRUD and SQL basics, not database normalization
- Option 2 adds 2-3 extra tables and significantly more code
- You can still validate choices in Python before saving:

```python
VALID_GENRES = ["action", "rpg", "sports", "puzzle", "horror"]

def pick_multiple(options):
    print("Choose (comma-separated numbers):")
    for i, opt in enumerate(options, 1):
        print(f"  {i}) {opt}")
    picks = input("> ").split(",")
    return ", ".join(options[int(p.strip())-1] for p in picks)

genre_string = pick_multiple(VALID_GENRES)  # returns e.g. "action, rpg"
```

So the user picks from a controlled list, you validate in Python, store as a string. Best of both worlds for a class project.

What's the topic you're leaning toward?


---

And then it was time to start.

## BUILDING MY PROJECT
I created a new chat, sketched out my database and what I wanted to have in my table and how I wanted to read it.

---

### ME: I want to create an SQLite database to track spending. want the database to have these categories:
Revenue or Expense (boolean)
Amount
Description
Category (from a given list)
Date-added (as YYYY-MM-DD)

can you help me write CREATE TABLE and suggest any columns I may be missing

---

### CLAUDE: Here's a `CREATE TABLE` statement for your spending tracker:

```sql
CREATE TABLE transactions (
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
);
```

A few notes on the design choices:

**Included your columns:**
- `is_revenue` for the boolean Revenue/Expense flag
- `amount` as `DECIMAL(10,2)` — supports up to 8 digits before the decimal, 2 after (e.g. `99999999.99`)
- `description` as optional free text
- `category` with a `CHECK` constraint to enforce the allowed list
- `date_added` defaulting to today so you don't have to supply it manually

**Suggested additions:**
- `id` — a standard auto-incrementing primary key, essential for referencing and deleting rows
- `created_at` — the *actual* timestamp the record was inserted, separate from `date_added` which you might set to a past date (e.g. logging a receipt from last week)

**Other columns you might consider:**

| Column | Type | Why |
|---|---|---|
| `payment_method` | TEXT | Track cash vs. card vs. bank transfer |
| `tags` | TEXT | Freeform labels like "tax-deductible" or "reimbursable" |
| `notes` | TEXT | Longer notes beyond a short description |
| `recurring` | BOOLEAN | Flag for subscriptions / regular bills |
| `account` | TEXT | If you have multiple accounts (checking, savings, credit) |

Would you like help writing any `INSERT`, `SELECT`, or reporting queries to go along with this?

---
For the next couple questions, it's just me getting back and forth for each CRUD function

### ME: Show me how to write a Python function that asks the user for amount, description,  category, and date, and inserts a new row into my table using sqlite3. There should be two separate CREATE queries, one for adding revenue, which makes the revenue boolean true, and one for adding expense, making the revenue boolean false. Use parameterized queries to avoid SQL injection.

### ME: Now show me how to write a function to read the database. I want two queries, one to sort by month and one to sort by category. The function should list all the found data, list total revenue, total expenses, and then net costs

### ME: ok. Now I want to add an update function to update entries. users should be able to also look at the listed objects by month before choosing what to update, as to not overwhelm the user with too many ids to choose from

### ME: ok. now please show me how to write a delete function, using the update functions to sort by month before then confirming and deleting

### ME: ok now show me how to write a CLI loop for this. Please show me an example, say with books, so that I can write it myself.

I then write my CLI loop, do some debugging with Claude and Gemini.

---
## BUG FIXES
Writing the code piece by piece left me with some inconsistencies and bugs to remove.

### ME: ok! do a passover for me for any potential bugs or issues? *code attached*

---

### CLAUDE: I can spot a few issues. Here they are from most to least critical:

**Bug 1 — Passing a set instead of two arguments (will crash)**

In your `main()` under option 3:
```python
read_by_month({year, month})   # ❌ this passes a set as the first argument
```
Should be:
```python
read_by_month(year, month)     # ✓ two separate arguments
```

**Bug 2 — Delete confirmation prompt is misleading**

```python
confirm = input("  Type '(y/n)' to confirm: ").strip()
if confirm != "y":
```
The prompt tells the user to type `(y/n)` but the check only accepts `y`. A user who reads the prompt literally and types `y/n` would get "Deletion cancelled." Either clean up the prompt or go back to the explicit `DELETE` confirmation we discussed earlier:
```python
confirm = input("  Type 'DELETE' to confirm: ").strip()
if confirm != "DELETE":
```

**Bug 3 — `print_summary` iterates `rows` twice**

```python
total_revenue  = sum(r["amount"] for r in rows if r["is_revenue"])
total_expenses = sum(r["amount"] for r in rows if not r["is_revenue"])
```
`sqlite3.Row` results from `fetchall()` are a plain list, so iterating twice is fine here — but if you ever switch to a generator or cursor this would silently return 0 on the second pass. Worth converting defensively at the top of `print_summary`:
```python
rows = list(rows)
```

**Minor — `read_by_month` in option 3 duplicates the year/month prompt logic**

You wrote the year/month input loop directly in `main()` before calling `read_by_month(year, month)`. That's fine, but it means the same prompt logic exists in three places now (update, delete, and main). Consider moving it into a small helper to keep things DRY:

```python
def get_month_input():
    while True:
        try:
            year  = int(input("  Year  (e.g. 2026): ").strip())
            month = int(input("  Month (1-12):       ").strip())
            if 1 <= month <= 12:
                return year, month
            print("  Month must be between 1 and 12.")
        except ValueError:
            print("  Please enter valid numbers.")
```

Then everywhere you need it: `year, month = get_month_input()`. That's one place to fix if you ever want to change the prompt.

Bug 1 is the only one that will actually crash the program — the rest are correctness or maintainability issues worth tidying up.

---

I fix bug 1, bug 2 (but not as they suggested), bug 3, and the minort "bug"/aka optimization.

I make final manual changes to pressing 'ENTER' for year and month when you want to choose current year and month.