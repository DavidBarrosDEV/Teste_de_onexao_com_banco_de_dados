import psycopg2
import unittest

class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(
            host='192.168.1.5',
            port='5432',
            user='systock',
            password='sys2017tock',
            database='systock'
        )

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.rollback()
        self.cursor.close()

    def test_connection(self):
        self.assertFalse(self.conn.closed, "A conexão com o banco de dados está fechada.")

    def test_create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY, name varchar);")
        self.conn.commit()
        self.cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='test_table');")
        result = self.cursor.fetchone()[0]
        self.assertTrue(result, "A tabela de teste não foi criada.")

    # Outros testes...

if __name__ == '__main__':
    unittest.main()
