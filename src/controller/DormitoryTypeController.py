from database.conn import DatabaseConnection
from psycopg2.extras import RealDictCursor

class DormitoryTypeController:
  def __init__(self):
    self.db = DatabaseConnection()

  def index(self) -> list[dict[str, any]]:
    query = '''
      SELECT * FROM public.dorm_type;
    '''

    with self.db as db:
      result = db.query(query)

      if result:
        dormitory_types = db.cursor.fetchall()
        return dormitory_types
      else: []
