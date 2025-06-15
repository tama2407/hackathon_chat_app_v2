from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user
from sqlalchemy.exc import IntegrityError
from model import User
from database import db_session   # database.pyで定義したセッションを使用
import bcrypt

# 認証ブループリントの作成（auth_bpという名前で、/authから始まるURLを管理する）
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # フォームデータの取得
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')

        # 入力のチェック
        if not all ([name, email, password]):
            flash('すべての項目を入力してください', 'danger')
            return redirect(url_for('auth.signup'))
        
        try:
            # パスワードのハッシュ化
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # 新しいユーザーの作成
            new_user = User(name=name, email=email, password=hashed_pw)
            # データーベースの追加
            db_session.add(new_user)
            db_session.commit()
            flash('アカウント登録が完了しました！', 'success')
            return redirect(url_for('auth.login'))
        
        except IntegrityError:
            db_session.rollback()
            flash('このメールアドレスは、既に登録されています', 'danger')

        except Exception as e:
            db_session.rollback()
            flash('システムエラーが発生しました', 'danger')
        
    # GETリクエスト時やエラー時は、サインアップ画面を表示する
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')

        # ユーザーの検索
        user = db_session.query(User).filter_by(email=email).first()


        # 認証チェック
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            flash('ログインに成功しました！', 'success')
            return redirect(url_for('main.index'))   # メイン画面にリダイレクト
        else:
            flash('メールアドレスまたはパスワードが間違っています', 'danger')
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('ログアウトしました', 'success')
    return redirect(url_for('auth.login'))



