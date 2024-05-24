from flask import request, jsonify, Flask,session
from model.config import get_db_connection
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO,emit,join_room,leave_room
import os
import json

def socketio_init(socketio) :

    #사용자가 채팅방에 입장됐을 때 호출됨 
    @socketio.on('joined',namespace='/chat')
    def joined(message):
        # room = session.get('room') 
        room = message['room']
        join_room(room)  #사용자를 해당 방에 입장 시킴 

        #기존 채팅 기록 불러오기 
        conn = get_db_connection()
        cursor = conn.cursor() 

        query = """
        SELECT user,content
        FROM message
        WHERE room_id = %s
        ORDER BY send_time ASC
        """
        
        cursor.execute(query,(room,))
        chat_history = cursor.fetchall()

        # 기존 채팅 기록 전송
        for chat in chat_history:
            name=chat['user']
            content=chat['content']
            if content is not None:
                emit('message', {'name': name, 'msg': content}, to=request.sid)
                # return chat

        cursor.close()
        conn.close()

    #사용자가 메세지를 전송했을 때 호출됨
    @socketio.on('text',namespace='/chat')
    def text(message):
        print("Received message:", json.dumps(message))  # 로깅 추가
        room = message['room']
        name = message['name']
        msg = message['msg']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO message (room_id,user,content) VALUES (%s,%s,%s)
        """

        cursor.execute(query,(room,name,msg))

        update_query = """
        UPDATE chatroom
        SET last_message = %s
        WHERE room_id = %s
        """
        cursor.execute(update_query, (msg, room))
        conn.commit()
        
        emit('message',{'name':name,'msg':msg},room=room)

    #사용자가 퇴장했을 때 호출됨
    @socketio.on('left',namespace='/chat')
    def left(message):
        room = message['room']
        name = message['name']
        leave_room(room) #사용자를 방에서 제거 

        leave_message = f"{name}님이 퇴장하셨습니다."
        emit('message', {'msg': leave_message, 'name': '알림'}, room=room)
        
        #퇴장 시 db에 메세지 기록 삭제 
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        DELETE FROM message
        WHERE room_id = %s 
        """
        
        cursor.execute(query,(room))
        conn.commit()

        exitquery = """
        DELETE FROM chatroom
        WHERE room_id = %s
        """

        cursor.execute(exitquery,(room))
        conn.commit()        

        cursor.close()
        conn.close()







