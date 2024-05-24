from flask import request, jsonify, Blueprint, session, render_template, redirect, url_for
from model.config import get_db_connection
import service.chat_events as srv #서비스 로직 함수 import 

def chat_controller(app):

    #구매자 채팅방 입장 api 
    @app.route('/chat', methods=['GET'])
    def chat(): 
        #파라미터로 post_id , 구매자의 user_id 받음 
        post_id = request.args.get('post_id') # 채팅을 요청한 게시글
        sender_id = request.args.get('sender_id') # 구매자 user_id (pk)

        conn = get_db_connection()
        cursor = conn.cursor()

        # receiver_id(=판매자 user_id (pk)) 가져오기 (room id 가져오기 위함)
        cursor.execute("SELECT user_id FROM posts WHERE post_id = %s", (post_id,))
        receiver_id_result = cursor.fetchone()
        receiver_id = receiver_id_result['user_id'] if receiver_id_result else None

        # chatroom 에서 room_id 가져오기
        query = """
        SELECT room_id FROM chatroom WHERE post_id = %s AND sender_id = %s AND receiver_id = %s
        """
        cursor.execute(query, (post_id, sender_id, receiver_id))
        chatroom_data = cursor.fetchone()

        # chatroom 테이블에서 sender_id, receiver_id 로 room_id 찾아오기 
        if chatroom_data is None:
            cursor.execute('INSERT INTO chatroom (post_id, sender_id, receiver_id) VALUES (%s, %s, %s)', (post_id, sender_id, receiver_id))
            conn.commit()
            room = cursor.lastrowid
        else:
            room = chatroom_data['room_id']

        # 구매자 login_id (닉네임) 찾기 
        cursor.execute('SELECT login_id FROM users WHERE user_id = %s', (sender_id,))
        sender_name_result = cursor.fetchone()
        # sender_name = sender_name_result['login_id']
        name = sender_name_result['login_id'] 

        cursor.close()
        conn.close()

        session['room'] = room # 세션에 방 이름 저장 
        session['name'] = name
        
        # return render_template('chat.html',room=room,name=name)
        return jsonify({
            'room':room,
            'name':name
        })

    #판매자 채팅방 입장 api 
    @app.route('/chat/<int:room_id>', methods=['GET'])
    def chatroom(room_id):

        # 채팅방에 접속하는 라우트
        conn = get_db_connection()
        cursor = conn.cursor()

        # room_id로 채팅방 정보 가져오기
        cursor.execute('SELECT * FROM chatroom WHERE room_id = %s', (room_id,))
        chatroom_data = cursor.fetchone()

        if not chatroom_data:
            return "채팅방을 찾을 수 없습니다.", 404

        post_id = chatroom_data['post_id'] 
        receiver_id = chatroom_data['receiver_id'] #구매자 id 

        cursor.execute('SELECT login_id FROM users WHERE user_id = %s', (receiver_id,))
        receiver_name_result = cursor.fetchone()
        name = receiver_name_result['login_id'] if receiver_name_result else None        

        cursor.close()
        conn.close()

        session['room'] = room_id # 세션에 방 id 저장 
        session['name'] = name #세션에 구매자 login_id 저장 

        # return render_template('chat.html',room=room_id,name=name)
        return jsonify({
            'room':room_id,
            'name':name
        })
    
    @app.route('/chat/list/<int:user_id>', methods=['GET'])
    def chat_list(user_id):
        # 채팅방에 접속하는 라우트
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM chatroom WHERE sender_id = %s OR receiver_id = %s', (user_id, user_id))
        chatroom_data = cursor.fetchall()

        chat_list = []
        for row in chatroom_data :
            cursor.execute('SELECT login_id FROM users WHERE user_id = %s', (row['sender_id'],))
            sender_name_result = cursor.fetchone()
            sender_name = sender_name_result['login_id'] if sender_name_result else None

            cursor.execute('SELECT login_id FROM users WHERE user_id = %s', (row['receiver_id'],))
            receiver_name_result = cursor.fetchone()
            receiver_name = receiver_name_result['login_id'] if receiver_name_result else None


            chat_list.append({
                'room_id' : row['room_id'],
                'sender_id' : row['sender_id'],
                'sender_name': sender_name,
                'receiver_id' : row['receiver_id'],
                'receiver_name': receiver_name,
                'post_id': row['post_id'],
                'last_message': row['last_message']
            })
            
        return jsonify(chat_list)


        