import psycopg2
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class DatabaseConnection():
    def __init__(self):
        self.db_name = os.getenv('db_name')
        self.db_host = os.getenv('db_host')
        self.db_user = os.getenv('db_user')
        self.db_password = os.getenv('db_password')
        self.db_port = os.getenv('db_port')
        self.conn = None
        self.cursor = None

    def connection(self):
      try:

        # Connect to PostgreSQL
        self.conn = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port
        )
        self.cursor = self.conn.cursor()
        print('Connection established successfully.')

      except psycopg2.Error as e:
        print('Error connecting to the database:', e)
        
      def query(self, query):
        try:
            if self.cursor:
                self.cursor.execute(query)
                self.conn.commit()  # Commit changes to the database
                print("Query executed successfully.")
        except psycopg2.Error as e:  # Catch psycopg2 database errors
            print("Error executing query:", e)

