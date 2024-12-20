from database.conn import DatabaseConnection
from psycopg2.extras import RealDictCursor
class DormitoryController:
  def __init__(self):
    self.db = DatabaseConnection()

  def index(self) -> list[dict[str, any]]:
    query = '''
      SELECT 
        dormitory.id AS dorm_id,
        dormitory.name AS dorm_name,
        dormitory.price AS dorm_price,
        dormitory.image_path
      FROM dormitory
      INNER JOIN public."user" ON dormitory.user_id = public."user".id;
    '''

    with self.db as db:
      result = db.query(query)

      if result:
        dormitories = db.cursor.fetchall()
        return dormitories
      else: []

  def store(self, request: dict) -> bool:
    query = '''
      INSERT INTO dormitory 
          (dorm_type_id, user_id, name, address, price, total_room, empty_room, image_path)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    '''

    with self.db as db:
      result = db.query(
        query,
        (
          request["dorm_type_id"],
          request["user_id"],
          request["name"],
          request["address"],
          request["price"],
          request["total_room"],
          request["empty_room"],
          request["image_path"]
        )
      )

      return result

  def destroy(self, id: int) -> bool:
    query = '''
      DELETE FROM public."user"
      WHERE id='{id}'
      RETURNING *;
    '''
    
    with self.db as db:
      result = db.query(query)

      if result: 
        return "Success delete dormitories"


    