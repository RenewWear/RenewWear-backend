from model.config import get_db_connection
from model.user_model import User
import bcrypt

def register_user(name, login_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        query = "INSERT INTO users (name, login_id, pw) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, login_id, hashed_pw.decode('utf-8')))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()

def authenticate_user(login_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT * FROM users WHERE login_id = %s"
        cursor.execute(query, (login_id,))
        user_data = cursor.fetchone()
        
        # 디버그 로그 추가
        print("User data fetched:", user_data)

        if user_data:
            # 비밀번호 검증 전에 저장된 해시된 비밀번호 출력
            print("Stored hashed password:", user_data['pw'])
            password_check = bcrypt.checkpw(password.encode('utf-8'), user_data['pw'].encode('utf-8'))
            print("Password check result:", password_check)

            if password_check:
                return User(user_data['user_id'], user_data['name'], user_data['login_id'])
            else:
                return None
        else:
            return None
    except Exception as e:
        print("Exception occurred:", e)
        return None
    finally:
        cursor.close()
        conn.close()