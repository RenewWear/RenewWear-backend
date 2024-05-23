from model.config import get_db_connection

class User:
    def __init__(self, user_id, name, login_id):
        self.id = user_id
        self.name = name
        self.login_id = login_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            return User(user_data['user_id'], user_data['name'], user_data['login_id'])
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()