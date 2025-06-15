
from flask import Flask
from config import Config
from flask_login import LoginManager
from model import User
from database import init_db, db_session

def create_app():
    # Flaskアプリケーションのインスタンス化
    app = Flask(__name__)

    # Config.pyから設定を読み込む
    app.config.from_object(Config)

    # データーベースの初期化（database.pyの関数）
    init_db(app)

    # Flask-Loginの初期化
    login_manager = LoginManager()
    login_manager.init_app(app)
    # ログインが必要なページを開こうとした時にリダイレクトさせる行き先を指定する
    login_manager.login_view = 'auth.login'

    # ユーザーローダーの設定
    @login_manager.user_loader
    def load_user(user_id):
        return db_session.query(User).get(int(user_id))

    # 認証ブループリントの登録
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # ルートの定義、簡単な動作確認
    @app.route('/')
    def home():
        return "Welcome to Hackathon_Chat_App_v2"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)