from flask import Flask
from flask_login import LoginManager
from controller.post_controller import post_controller
from controller.auth_controller import auth_controller
from model.config import get_db_connection
from model.user_model import load_user


app = Flask(__name__)
app.secret_key = 'secret-key-here'  # 세션 관리용 비밀 키

# Flask-Login 설정
login_manager = LoginManager(app)
login_manager.user_loader(load_user)  # 사용자 로더 함수 설정
login_manager.login_view = 'auth_controller.login'  # 로그인 페이지 지정

post_controller(app)
app.register_blueprint(auth_controller, url_prefix='/auth')  # 인증 관련 경로

if __name__ == '__main__' :
    app.run(debug=True,port=8080)
