from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# 基本設定
Base = declarative_base()
engine = None
db_session = None

def init_db(app):
    global engine, db_session
    
    # エンジンの作成
    engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )
    
    # セッションの設定
    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )
    
    # テーブルの作成
    from model import User, Channel, Message    # 明示的なインポート
    Base.metadata.create_all(bind=engine)
    
    # アプリ終了時のセッションクローズ
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
