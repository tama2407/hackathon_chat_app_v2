
from flask import Flask,render_template, redirect, url_for
from config import Config
from flask_login import LoginManager, current_user
from model import User
import database
from database import init_db

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
        return database.db_session.query(User).get(int(user_id))

    # 認証ブループリントの登録
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 部屋関係のブループリントの登録
    from routes.channels import channels_bp
    app.register_blueprint(channels_bp)

    # メッセージブループリント
    from routes.messages import messages_bp
    app.register_blueprint(messages_bp)

    # ルートの定義、アプリ用
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            # ログイン済み → 部屋一覧ページにジャンプ
            return redirect(url_for('channels.index'))
        else:
            # ログインしていない → ログインページにジャンプ
            return redirect(url_for('auth.login'))

    # # ルートの定義、簡単な動作確認
    # @app.route('/')
    # def home():
    #     return "Welcome to Hackathon_Chat_App_v2"
    
    # 404エラー
    @app.errorhandler(404)
    def show_error404(error):
        return render_template('error/404.html'), 404
    
    # 500エラー
    @app.errorhandler(500)
    def show_error500(error):
        return render_template('error/500.html'), 500

    # Docker用のヘルスチェックエンドポイント
    @app.route('/health')
    def health():
        try:
            from database import db_session
            db_session.execute('SELECT 1')
            return {"status": "healthy", "database": "connected"}, 200
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}, 503

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)