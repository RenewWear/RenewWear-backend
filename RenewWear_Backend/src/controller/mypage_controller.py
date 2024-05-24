from flask import request, jsonify, Blueprint
import service.mypage_service as mypage_srv  # 서비스 로직 함수 import

mypage_blueprint = Blueprint('mypage', __name__)


@mypage_blueprint.route('/mypage/sales/<int:user_id>', methods=['GET'])
def get_sales_list(user_id):
    sales = mypage_srv.get_sales_list(user_id)
    if sales is not None:
        return jsonify(sales), 200
    else:
        return "서버 내부 오류로 인한 조회 실패", 500

@mypage_blueprint.route('/mypage/liked/<int:user_id>', methods=['GET'])
def get_liked_list(user_id):
    liked = mypage_srv.get_liked_list(user_id)
    if liked is not None:
        return jsonify(liked), 200
    else:
        return "서버 내부 오류로 인한 조회 실패", 500

def mypage_controller(app):
    app.register_blueprint(mypage_blueprint)

