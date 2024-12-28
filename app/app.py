import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_connection import get_connection
from bcrypt import hashpw, gensalt, checkpw


def create_user(username, password):
    password_hash = hashpw(password.encode('utf-8'), gensalt())  # Gera o hash da senha
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash.decode('utf-8')))
        conn.commit()
        print(f"User {username} criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar user: {e}")
    finally:
        cur.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user and checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            print("Login bem-sucedido!")
            return True
        else:
            print("Credenciais inválidas.")
            return False
    except Exception as e:
        print(f"Erro no login: {e}")
        return False
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_user("admin", "admin123")
    is_authenticated = login_user("admin", "admin123")
    print("Login bem-sucedido!" if is_authenticated else "Falha no login")

def save_message(user_id, message):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO messages (user_id, message) VALUES (%s, %s)", (user_id, message))
        conn.commit()
        print("Mensagem salva com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar mensagem: {e}")
    finally:
        cur.close()
        conn.close()

def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM messages ORDER BY created_at DESC")
        messages = cur.fetchall()
        return messages
    except Exception as e:
        print(f"Erro ao buscar mensagens: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def search_books(title=None, author=None, genre=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = "SELECT * FROM books WHERE 1=1"
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
        books = cur.fetchall()
        return books
    except Exception as e:
        print(f"Erro ao buscar livros: {e}")
        return []
    finally:
        cur.close()
        conn.close()