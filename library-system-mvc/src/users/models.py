from src.database import get_db_connection

def insert_user(name: str, email: str) -> int:
    """Inserts a new user into the database and returns the generated ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email),
    )
    conn.commit()
    user_id: int = cursor.lastrowid
    conn.close()
    return user_id

def get_user_by_id(user_id: int):
    """Retrieves a user by their ID. Returns None if not found."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users() -> list:
    """Retrieves all users from the database ordered by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()
    return users