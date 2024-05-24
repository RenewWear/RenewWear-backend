from flask import request, jsonify, Flask
from model.config import get_db_connection
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#게시글 조회 로직 
def get_post():
    conn = get_db_connection()
    cursor = conn.cursor() 
    try:
        query = """
        SELECT 
        p.post_id, 
        p.user_id, 
        p.title, 
        p.category_id, 
        p.tag, 
        p.price, 
        p.location, 
        p.size,
        p.brand_id, 
        p.used, 
        p.status, 
        p.created_at, 
        p.exchange, 
        p.delivery, 
        GROUP_CONCAT(i.img) as image_urls
        FROM 
        posts p
        LEFT JOIN 
        post_img i ON p.post_id = i.post_id
        GROUP BY 
        p.post_id;
        """
        cursor.execute(query)  # 모든 게시글 & 사진 조회 쿼리 실행
        posts = cursor.fetchall()  # 조회된 모든 게시글을 가져옴

        if posts:
            return posts   
        else:
            return [] 
    
    except Exception as e:
        print(e)
        return None
    
    finally:
        conn.close()  # 데이터베이스 연결 종료

#특정 게시글 조회 로직 
def get_by_post_id(post_id) :
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = """
            SELECT p.post_id, p.user_id, p.title, p.category_id, p.tag, p.price, 
                p.location, p.size, p.brand_id, p.used, p.status, 
                p.created_at, p.exchange, p.delivery, 
                GROUP_CONCAT(i.img) as image_urls
            FROM posts p
            LEFT JOIN post_img i ON p.post_id = i.post_id
            WHERE p.post_id = %s
            GROUP BY p.post_id
            """
            cursor.execute(query,(post_id,))
            post = cursor.fetchone()

            if post :
                return post
            else :
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

#사진 업로드 로직 
def add_img(post_id):
    if 'image' not in request.files :
        return "fail"
    
    file = request.files['image']

    if file :
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            print("Creating upload folder")
            os.makedirs(app.config['UPLOAD_FOLDER'])

        print(f"Saving file to {save_path}")
        file.save(save_path)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            #post_id 가 존재하는지 먼저 확인
            cursor.execute("SELECT * FROM posts WHERE post_id = %s",(post_id))
            img = cursor.fetchone()

            if img is None:
                return "not found"

            query = "INSERT INTO post_img (img,post_id) VALUES (%s,%s)"
            cursor.execute(query,(save_path,post_id))
            conn.commit()

        except Exception as e:
            print(e)
            return "error"
        finally:
            cursor.close()
            conn.close()

        return "success"

    else :
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
    category_id = int(data['category_id'])
    price = int(data['price'])
    location = data['location']
    size = data['size']
    brand_id = int(data['brand_id'])
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
        SET title=%s, user_id=%s, tag=%s, category_id=%s, price=%s, location=%s, size=%s, brand_id=%s, used=%s, body=%s, status=%s, exchange=%s, delivery=%s
        WHERE post_id=%s
        """
        cursor.execute(query, (title, user_id, tag, category_id, price, location, size, brand_id, used, body, status, exchange, delivery, post_id))
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