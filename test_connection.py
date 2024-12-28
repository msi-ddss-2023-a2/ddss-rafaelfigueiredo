from db_connection import get_connection
import unittest

try:
    conn = get_connection()
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")


class TestConnection(unittest.TestCase):
    def test_connection(self):
        try:
            conn = get_connection()
            self.assertIsNotNone(conn)
            conn.close()
        except Exception as e:
            self.fail(f"Falha na conexão: {e}")

if __name__ == "__main__":
    unittest.main()