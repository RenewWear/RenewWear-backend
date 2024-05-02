from flask_login import UserMixin
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

# 데이터베이스 연결 함수
def get_db_connection():
    MYSQL_HOST = 'database-1.c90i40424i5z.ap-northeast-2.rds.amazonaws.com'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = 'tjqjxlavmf2024'
    MYSQL_DB = 'serverdb'

    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 사용자 로더 함수
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['email'], user_data['password'])
        else:
            return None
    finally:
        cursor.close()
        conn.close()
