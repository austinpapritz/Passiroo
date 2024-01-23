import sqlite3

def create_database():
    # Connect to the SQLite database. If it doesn't exist, it will be created.
    conn = sqlite3.connect('passiroo.db')

    # Create the tables
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_passwords (
                password_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                encrypted_site_name TEXT NOT NULL,
                encrypted_account_name TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        """)

    # Close the connection
    conn.close()

create_database()