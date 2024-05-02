from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, logout_user, login_required
from model.user_model import User, get_db_connection  # 사용자 모델과 DB 연결 함수
from werkzeug.security import check_password_hash, generate_password_hash

auth_controller = Blueprint('auth_controller', __name__)  # 블루프린트 생성

@auth_controller.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 비밀번호 해싱
        hashed_password = generate_password_hash(password, method='sha256')

        # 데이터베이스에 사용자 추가
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            conn.commit()
            flash('회원가입 성공!', 'success')
            return redirect('/auth/login')  # 로그인 페이지로 리디렉션
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')  # 회원가입 페이지 렌더링

@auth_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # 사용자 정보 조회
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()

            if user_data and check_password_hash(user_data['password'], password):
                user = User(user_data['id'], user_data['username'], user_data['email'], user_data['password'])
                login_user(user)
                flash('로그인 성공!', 'success')
                return redirect('/')
            else:
                flash('잘못된 이메일 또는 비밀번호', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')  # 로그인 페이지 렌더링

@auth_controller.route('/logout')
@login_required  # 로그아웃은 로그인한 사용자만 가능
def logout():
    logout_user()
    flash('로그아웃 성공!', 'success')
    return redirect('/')
