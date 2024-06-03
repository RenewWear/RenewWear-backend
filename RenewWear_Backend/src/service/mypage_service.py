from model.config import get_db_connection
import base64

def get_sales_list(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # query = """
        # SELECT p.post_id, p.user_id, p.title, p.price, p.created_at, p.status,
        #        GROUP_CONCAT(pi.img) AS image_urls
        # FROM posts p
        # LEFT JOIN post_img pi ON p.post_id = pi.post_id
        # WHERE p.user_id = %s
        # GROUP BY p.post_id
        # """
        query = """
        SELECT p.post_id, p.user_id, p.title, p.price, p.created_at, p.status,
        i.img as image_blob
        FROM posts p 
        LEFT JOIN post_img i ON p.post_id = i.post_id
        WHERE p.user_id = %s
        """
        
        cursor.execute(query, (user_id,))
        sales = cursor.fetchall()

        if sales:
            for sale in sales:
                if sale['image_blob']:
                    image_base64 = base64.b64encode(sale['image_blob']).decode('utf-8')
                    sale['image_blob'] = image_base64
            return sales
        else:
            return []
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()


def get_liked_list(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        query = """
        SELECT l.liked_id, l.user_id, po.post_id, po.title, po.price, po.created_at, po.status,
        i.img as image_blob
        FROM posts po 
        LEFT JOIN post_img i ON po.post_id = i.post_id
        LEFT JOIN liked l ON po.post_id = l.post_id
        WHERE l.user_id = %s
        """
        cursor.execute(query, (user_id,))
        liked = cursor.fetchall()

        if liked:
            for like in liked:
                if like['image_blob']:
                    image_base64 = base64.b64encode(like['image_blob']).decode('utf-8')
                    like['image_blob'] = image_base64
            return liked
        else:
            return []
        
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

