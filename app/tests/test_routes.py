import unittest
from app import app
from db_connection import get_connection
from app.models import create_user, save_message, login_user, get_user_by_username


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        # Limpa as tabelas antes de cada teste
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM messages")
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM books")
        conn.commit()
        cur.close()
        conn.close()

    def test_login_user_success(self):
        create_user("test_user", "securepassword")
        result = login_user("test_user", "securepassword")
        self.assertTrue(result)

    def test_register_missing_fields(self):
        response = self.client.post('/register', json={
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('User e password são obrigatórios!', response.get_json().get('error'))

    def test_login_success(self):
        self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login bem-sucedido!', response.get_json().get('message'))

    def test_login_invalid_credentials(self):
        response = self.client.post('/login', json={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Usuário ou senha inválidos!', response.get_json().get('error'))

    def test_save_message_success(self):
        create_user("messageuser", "messagepassword")
        user = get_user_by_username("messageuser")
        response = self.client.post('/messages', json={
            'user_id': user['id'],
            'message': 'Minha mensagem de teste'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Mensagem salva com sucesso!', response.get_json()['message'])

    def test_get_messages(self):
        # Criação do user antes de salvar a mensagem
        create_user("messageuser", "password123")
        user = get_user_by_username("messageuser")
        save_message(user['id'], "Minha mensagem de teste")  # Use o ID correto do usuário

        response = self.client.get('/messages')
        self.assertTrue(len(response.get_json()) > 0)  # Certifique-se de que há mensagens

    def test_search_books_by_title(self):
        # Adicione um livro ao banco antes de fazer a busca
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", 
                    ("Harry Potter", "J.K. Rowling", "Fantasy"))
        conn.commit()
        cur.close()
        conn.close()

        response = self.client.get('/books/search?title=Harry')
        self.assertEqual(response.status_code, 200)

        books = response.get_json()
        self.assertTrue(any(book['title'] == 'Harry Potter' for book in books))

    def test_search_books_no_results(self):
        response = self.client.get('/books/search?title=Unknown')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)