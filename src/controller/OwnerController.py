from database.conn import DatabaseConnection
from psycopg2.extras import RealDictCursor
class OwnerController:
  def __init__(self):
    self.db = DatabaseConnection()

  def dormitories(self) -> list[dict[str, any]]:
    query = '''
      SELECT 
        dormitory.name,
        dorm_type."name" AS dormitory_type,
        dormitory.address,
        dormitory.total_room,
        dormitory.empty_room
      FROM dormitory
      INNER JOIN public."user" 
          ON dormitory.user_id = public."user".id
      INNER JOIN dorm_type 
          ON dormitory.dorm_type_id = dorm_type.id
      WHERE public."user".id = 1;
      '''

    with self.db as db:
      result = db.query(query)

      if result:
        dormitories = db.cursor.fetchall()
        return dormitories
      else: []