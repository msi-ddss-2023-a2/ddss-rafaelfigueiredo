from flask import request, jsonify
from app import app
from app.models import create_user, login_user, save_message, get_messages, search_books, get_user_by_id
from db_connection import get_connection


@app.route('/')
def home():
    return "Bem-vindo à aplicação!"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "User e Password são obrigatórios!"}), 400

    try:
        create_user(username, password)
        return jsonify({"message": "User registado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    print(f"Login attempt for user: {username}")

    if not username or not password:
        return jsonify({"error": "User e Password são obrigatórios!"}), 400

    if login_user(username, password):
        print(f"Login successful for user: {username}")
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        print(f"Login failed for user: {username}")
        return jsonify({"error": "User ou Password inválidos!"}), 401

@app.route("/messages", methods=["POST"])
def save_message_route():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({"error": "user_id e mensagem são obrigatórios"}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User não encontrado"}), 400

    try:
        save_message(user_id, message)
        return jsonify({"message": "Mensagem salva com sucesso!"}), 201
    except Exception as e:
        print(f"Erro ao salvar a mensagem: {e}")
        return jsonify({"error": "Erro ao salvar a mensagem"}), 500

@app.route("/messages", methods=["GET"])
def get_messages_route():
    try:
        messages = get_messages()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/books/search", methods=["GET"])
def search_books_route():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")

    try:
        books = search_books(title=title, author=author, genre=genre)
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/vulnerable_login", methods=["POST"])
def vulnerable_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password}'"
    print(f"SQL Query Executed: {query}")  # Adicionado para debug
    cur.execute(query)
    user = cur.fetchone()
    print(f"Query Result: {user}")  # Adicionado para verificar se há resultados
    cur.close()
    conn.close()

    if user:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"error": "User ou Password inválidos!"}), 401


@app.route("/secure_login", methods=["POST"])
def secure_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()

    # Consulta segura com prepared statements
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    cur.execute(query, (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"error": "User ou Password inválidos!"}), 401

# Rota Vulnerável para Envio de Mensagens
@app.route("/vulnerable_messages", methods=["POST"])
def vulnerable_save_message():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    
    # Conexão com o banco de dados
    conn = get_connection()
    cur = conn.cursor()
    
    # Armazena a mensagem sem qualquer sanitização
    cur.execute("INSERT INTO messages (user_id, message) VALUES (%s, %s)", (user_id, message))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Mensagem salva (vulnerável)!"}), 201

# Rota Vulnerável para Exibir Mensagens
@app.route("/vulnerable_display_messages", methods=["GET"])
def vulnerable_display_messages():
    # Conexão com o banco de dados
    conn = get_connection()
    cur = conn.cursor()
    
    # Busca todas as mensagens sem nenhum processamento
    cur.execute("SELECT message FROM messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    
    # Retorna mensagens sem sanitização no lado do servidor
    return jsonify([{"message": msg[0]} for msg in messages])

# Rota Vulnerável para Pesquisa de Pesquisa de Livros
@app.route("/vulnerable_books/search", methods=["GET"])
def vulnerable_search_books():
    title = request.args.get("title", "")
    author = request.args.get("author", "")
    genre = request.args.get("genre", "")
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Consulta SQL direta e insegura
    query = f"SELECT * FROM books WHERE title ILIKE '%{title}%' OR '1'='1' AND author ILIKE '%{author}%' AND genre ILIKE '%{genre}%'"
    print(f"SQL Query Executed: {query}")
    cur.execute(query)
    books = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify([{"title": book[0], "author": book[1], "genre": book[2]} for book in books])
