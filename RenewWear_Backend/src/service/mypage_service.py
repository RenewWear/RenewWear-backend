from model.config import get_db_connection

def get_purchase_list(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT p.purchase_id, p.user_id, p.post_id, po.title, po.price, po.created_at
        FROM purchase p
        JOIN posts po ON p.post_id = po.post_id
        WHERE p.user_id = %s
        """
        cursor.execute(query, (user_id,))
        purchases = cursor.fetchall()
        return purchases
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()

def get_sales_list(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT s.sales_id, s.user_id, s.post_id, po.title, po.price, po.created_at
        FROM sales s
        JOIN posts po ON s.post_id = po.post_id
        WHERE s.user_id = %s
        """
        cursor.execute(query, (user_id,))
        sales = cursor.fetchall()
        return sales
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
        SELECT l.liked_id, l.user_id, l.post_id, po.title, po.price, po.created_at
        FROM liked l
        JOIN posts po ON l.post_id = po.post_id
        WHERE l.user_id = %s
        """
        cursor.execute(query, (user_id,))
        liked = cursor.fetchall()
        return liked
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        conn.close()
