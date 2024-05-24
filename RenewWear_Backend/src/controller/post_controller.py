from flask import request, jsonify,Blueprint
from model.config import get_db_connection
import service.post_service as srv #서비스 로직 함수 import 

post_controller = Blueprint('post_controller', __name__)

#전체 게시글 조회 
@post_controller.route('/getpost',methods=['GET'])
def get_post():
    posts = srv.get_post()
        
    if posts is not None :
        if len(posts) > 0:
            return jsonify(posts),200
        else:
            return "조회할 게시글이 없음",404
    
    else :
        return "서버 내부 오류로 인한 조회 실패 ",500

#특정 게시글 조회 API (파라미터로 post_id 받음)
@post_controller.route('/getpost/<int:post_id>',methods=['GET'])
def get_by_post_id(post_id):
    post = srv.get_by_post_id(post_id)
    if post is not None : 
        if len(post) > 0:
            return jsonify(post),200
        else:
            return "해당 post_id 를 가진 게시글 없음",404
    else:
        return "서버 내부 오류로 인한 조회 실패",500
    
#게시글 작성 버튼을 누르면 호출될 API - post_id 생성 위해 필요 
@post_controller.route('/create_postid',methods=['POST'])
def create_postid():
    post_id = srv.create_postid()

    if post_id != "error":
        return post_id
    else:
        return "서버 내부 오류로 인한 에러",500


#사진 업로드 API 
@post_controller.route('/addimg/<int:post_id>',methods=['POST'])
def upload_img(post_id):
    result = srv.add_img(post_id)

    if result == "success" :
        return "사진 업로드 성공",200
    elif result == "fail" :
        return "사진 업로드 실패",400
    elif result == "not found":
        return "해당 post_id 없음",400
    else :
        return "서버 오류로 사진 업로드 실패",500

#게시글 수정 API 
@post_controller.route('/updatepost/<int:post_id>',methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    result = srv.update_post(post_id,data)

    if result == "success" :
        return "게시글 수정 성공",200
    elif result == "not found" :
        return "해당 post_id 를 가진 게시글이 없음",404
    else:
        return "수정 실패",500

#사진 삭제 API
@post_controller.route('/deleteimg/<int:post_id>',methods=['DELETE'])
def delete_img(post_id):
    result = srv.delete_img(post_id)

    if result == "success":
        return "사진 삭제 성공",200
    
    elif result == "not found":
        return "해당 게시글의 사진 없음",400
    
    elif result == "error":
        return "서버오류로 인한 사진 삭제 실패",500
    

#게시글 삭제 API 
@post_controller.route('/deletepost/<int:post_id>',methods=['DELETE'])
def delete_post(post_id):
    result = srv.delete_post(post_id)

    if result == "success":
        return "게시글 삭제 성공",200
    elif result == "not found":
        return "해당 post_id 를 가진 게시글이 없음",404
    else:
        return "삭제 실패",500

#찜하기 
@post_controller.route('/like',methods=['POST'])
def like_post() :
    data = request.get_json()
    result = srv.like_post(data)

    if result == "success":
        return "찜 성공",200
    elif result == "not found":
        return "해당 post_id 를 가진 게시글이 없음",404
    else:
        return "찜 실패",500