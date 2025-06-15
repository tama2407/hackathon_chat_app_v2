from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # 基本設定
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    
    # データベース接続情報（個別環境変数から取得）
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', ''))  # パスワードをエンコード
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    
    # 接続URLの構築
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # 推奨設定
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300
    }
    
    # デバッグ設定（スペルミス修正）
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

