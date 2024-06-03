from flask import request, jsonify, Flask, url_for
from model.config import get_db_connection
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/images/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_post():
    conn = get_db_connection()
    cursor = conn.cursor() 
    try:
        query = """
        SELECT 
        p.post_id, 
        p.user_id, 
        p.title, 
        p.category, 
        p.tag, 
        p.price, 
        p.location, 
        p.size,
        p.brand, 
        p.used, 
        p.status, 
        p.created_at, 
        p.exchange, 
        p.delivery, 
        p.body,
        i.img as image_blob
        FROM 
        posts p
        LEFT JOIN 
        post_img i ON p.post_id = i.post_id
        """
        cursor.execute(query)
        posts = cursor.fetchall()

        if posts:
            # 이미지 데이터를 Base64로 인코딩
            for post in posts:
                if post['image_blob']:
                    # BLOB 데이터를 Base64로 인코딩하고 문자열로 디코딩합니다.
                    image_base64 = base64.b64encode(post['image_blob']).decode('utf-8')
                    post['image_blob'] = image_base64
            return posts   
        else:
            return [] 
    
    except Exception as e:
        print(e)
        return None
    
    finally:
        conn.close()  # 데이터베이스 연결 종료

#특정 게시글 조회 로직 
def get_by_post_id(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT p.post_id, p.user_id, p.title, p.category, p.tag, p.price, 
            p.location, p.size, p.brand, p.used, p.status, 
            p.created_at, p.exchange, p.delivery, p.body,
            i.img as image_blob
        FROM posts p
        LEFT JOIN post_img i ON p.post_id = i.post_id
        WHERE p.post_id = %s
        """
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()

        if post:
            # BLOB 데이터를 Base64로 인코딩
            if post['image_blob']:
                image_base64 = base64.b64encode(post['image_blob']).decode('utf-8')
                post['image_blob'] = image_base64
            return post
        else:
            return []

    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

#create_postid 를 위한 로직 
def create_postid() :
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO posts VALUES ();"
        cursor.execute(query)
        
        # 생성된 post_id 가져오기
        post_id = cursor.lastrowid

        conn.commit()
        return jsonify(post_id)
    
    except Exception as e:
        print(e)
        return "error"
    
    finally:
        cursor.close()
        conn.close()

def add_img(post_id):
    if 'image' not in request.files:
        return "fail"
    
    file = request.files['image']

    if file:
        # 파일 이름을 받아오지만, 저장하지는 않습니다.
        filename = secure_filename(file.filename)
        
        try:
            img_data = file.read()  # 파일을 읽어서 바이너리 데이터로 변환
        except Exception as e:
            print(f"Error reading file: {e}")
            return "error"

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # post_id가 존재하는지 먼저 확인
            cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
            img = cursor.fetchone()

            if img is None:
                return "not found"

            # BLOB 형태로 이미지 데이터와 post_id를 저장합니다.
            query = "INSERT INTO post_img (img, post_id) VALUES (%s, %s)"
            cursor.execute(query, (img_data, post_id))  # img_data를 BLOB으로 데이터베이스에 저장
            conn.commit()

        except Exception as e:
            print(e)
            return "error"
        finally:
            cursor.close()
            conn.close()

        return "success"

    else:
        return "fail"

#사진 삭제 로직
def delete_img(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try : 
        #이미지가 존재하는지 확인 
        cursor.execute("SELECT * FROM post_img WHERE post_id = %s",(post_id))  
        img = cursor.fetchone()

        if img is None :
            return "not found"
        cursor.execute("DELETE FROM post_img WHERE post_id = %s", (post_id,))
        conn.commit()
        return "success"
    
    except Exception as e:
        print(e)
        return "error"
    finally:
        cursor.close()
        conn.close()



#게시글 수정 로직 & 업로드 로직 
def update_post(post_id,data):
    title = data['title']
    user_id = int(data['user_id'])
    tag = data['tag']
    category = data['category']
    price = int(data['price'])
    location = data['location']
    size = data['size']
    brand = data['brand']
    used = data['used']
    body = data['body']
    status = data['status']
    exchange = data['exchange']
    delivery = data['delivery']

    conn = get_db_connection()
    cursor = conn.cursor()

    try : 
        #게시글이 존재하는지 먼저 확인하기 
        cursor.execute("SELECT * FROM posts WHERE post_id = %s",(post_id))  
        post = cursor.fetchone()  
        if post is None :
            return "not found"

        query = """
        UPDATE posts
        SET title=%s, user_id=%s, tag=%s, category=%s, price=%s, location=%s, size=%s, brand=%s, used=%s, body=%s, status=%s, exchange=%s, delivery=%s
        WHERE post_id=%s
        """
        cursor.execute(query, (title, user_id, tag, category, price, location, size, brand, used, body, status, exchange, delivery, post_id))
        conn.commit()
        return "success"
    
    except Exception as e:
         print(e)
         return "error"
    
    finally:
         cursor.close()
         conn.close()

#게시글 삭제 로직 
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor() 
    try:
        #게시글이 존재하는지 먼저 확인하기 
        cursor.execute("SELECT * FROM posts WHERE post_id = %s",(post_id))  
        post = cursor.fetchone()  
        if post is None :
            return "not found" #해당 게시글이 존재하지 않는 경우 
        
        #해당 Post_id 에 해당하는 이미지 데이터 삭제
        cursor.execute("DELETE FROM post_img WHERE post_id = %s", (post_id,))
        
        #게시글 삭제 쿼리
        cursor.execute("DELETE FROM posts WHERE post_id = %s",(post_id))
        conn.commit()
        return "success" 
    
    except Exception as e:
        print(e)
        return "error"
    
    finally:
        conn.close()  # 데이터베이스 연결 종료

#찜 목록 추가하기 
def like_post(data):
    user_id = data['user_id'] 
    post_id = data['post_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #게시글이 존재하는지 먼저 확인하기 
        cursor.execute("SELECT * FROM posts WHERE post_id = %s",(post_id))  
        post = cursor.fetchone()  
        if post is None :
            return "not found" #해당 게시글이 존재하지 않는 경우 
        
        query = "INSERT INTO liked (user_id,post_id) VALUES (%s,%s)"
        cursor.execute(query,(user_id,post_id))
        conn.commit()
        return "success"

    except Exception as e:
        print(e)
        return "error"
    
    finally:
        conn.close() 



# 판매 상태 업데이트 로직
def update_post_status(post_id, user_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 게시글이 존재하는지 및 해당 사용자가 작성자인지 확인
        cursor.execute("SELECT * FROM posts WHERE post_id = %s AND user_id = %s", (post_id, user_id))
        post = cursor.fetchone()

        if post is None:
            return "not found"  # 해당 게시글이 존재하지 않거나 사용자가 작성자가 아닌 경우

        query = "UPDATE posts SET status = %s WHERE post_id = %s AND user_id = %s"
        cursor.execute(query, (status, post_id, user_id))
        conn.commit()
        return "success"

    except Exception as e:
        print(e)
        return "error"

    finally:
        cursor.close()
        conn.close()