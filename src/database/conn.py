import psycopg2
import psycopg2.extras
import os
from typing import Any, Optional
from dotenv import load_dotenv
from contextlib import contextmanager

class DatabaseConnection():
  def __init__(self):
      load_dotenv()
      self.db_name = os.getenv('db_name')
      self.db_host = os.getenv('db_host')
      self.db_user = os.getenv('db_user')
      self.db_password = os.getenv('db_password')
      self.db_port = os.getenv('db_port')
      self.conn = None
      self.cursor = None

  def connect(self) -> bool:
    """
      Establishes database connection
      Returns: bool indicating if connection was successful
    """
      
    try:
      if not all([
        self.db_name, 
        self.db_host,
        self.db_user, 
        self.db_password, 
        self.db_port
      ]):
        raise ValueError("Missing database configuration. Please check your .env file.")

      # Connect to PostgreSQL
      self.conn = psycopg2.connect(
          database=self.db_name,
          host=self.db_host,
          user=self.db_user,
          password=self.db_password,
          port=self.db_port
      )
      self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      print('Connection established successfully.')
      return True

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return False
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False
      
  def query(self, query: str, params: tuple = None) -> Optional[list]:
    """
      Executes a query with optional parameters
      Args:
          query: SQL query string
          params: Optional tuple of parameters for the query
      Returns:
          List of results for SELECT queries, None for other queries
      """
    try:
      if not self.cursor or not self.conn:
          if not self.connect():
              return False
      
      self.cursor.execute(query, params)
      self.conn.commit()
      return True
    except psycopg2.Error as e:
      print(f"Query execution error: {e}")
      self.conn.rollback()
      return False

  @contextmanager
  def transaction(self):
      """
      Context manager for handling transactions
      Usage:
          with db.transaction():
              db.query("INSERT INTO...")
              db.query("UPDATE...")
      """
      try:
          yield self
          self.conn.commit()
      except Exception as e:
          self.conn.rollback()
          raise e

  def close(self):
    """
    Closes database connection and cursor
    """
    try:
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
    except psycopg2.Error as e:
        print(f"Error closing database connection: {e}")

  def __enter__(self):
        """
        Enables use of 'with' statement
        """
        self.connect()
        return self

  def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures connection is closed when exiting 'with' statement
        """
        self.close()
