from db_connection import get_connection
from bcrypt import hashpw, gensalt, checkpw

def create_user(username, password):
    try:
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        print(f"Creating user: {username} with password hash: {hashed_password}")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()
        print("User created successfully!")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def login_user(username, password):
    user = get_user_by_username(username)
    if user and checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return True
    return False

def save_message(user_id, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (user_id, message) VALUES (%s, %s)", (user_id, message))
    conn.commit()
    cur.close()
    conn.close()

def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, message, created_at FROM messages ORDER BY created_at DESC")
    rows = cur.fetchall()
    messages = [{"id": row[0], "user_id": row[1], "message": row[2], "created_at": row[3]} for row in rows]
    cur.close()
    conn.close()
    return messages

def search_books(title=None, author=None, genre=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = "SELECT title, author, genre FROM books WHERE 1=1"
        params = []
        if title:
            query += " AND title ILIKE %s"
            params.append(f"%{title}%")
        if author:
            query += " AND author ILIKE %s"
            params.append(f"%{author}%")
        if genre:
            query += " AND genre ILIKE %s"
            params.append(f"%{genre}%")
        cur.execute(query, params)
        rows = cur.fetchall()
        # Retorne como uma lista de dicionários
        return [{"title": row[0], "author": row[1], "genre": row[2]} for row in rows]
    finally:
        cur.close()
        conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return {'id': user[0], 'username': user[1], 'password_hash': user[2]} if user else None