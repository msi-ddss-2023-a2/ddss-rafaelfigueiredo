import unittest
from app.models import create_user, login_user
from app import app
from db_connection import get_connection

class TestModels(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        # Limpa as tabelas antes de cada teste
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM messages")
        cur.execute("DELETE FROM books")
        conn.commit()
        cur.close()
        conn.close()

    def test_create_user(self):
        result = create_user("unique_user", "securepassword")
        self.assertIsNotNone(result)  # Verifica se o user foi criado

    def test_login_user_success(self):
        create_user("test_user", "securepassword")
        result = login_user("test_user", "securepassword")
        self.assertTrue(result)  # Verifica se o login foi bem-sucedido

    def test_login_user_fail(self):
        result = login_user("test_user", "wrongpassword")
        self.assertFalse(result)  # Verifica se o login falhou com senha incorreta
