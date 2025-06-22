
### 概要
- Flask、SQLAlchemy、MariaDBを使用したチャットアプリケーションです。
- ユーザー認証、チャンネル作成、メッセージ投稿機能を実装しています。


### 技術スタック
- Backend: Flask, SQLAlchemy
- Database: MariaDB
- Authentication: Flask-Login, bcrypt
- Frontend: HTML, CSS
- Deployment: AWS EC2, Docker


### 機能
- ユーザー認証（新規登録・ログイン・ログアウト）
- チャンネル作成・管理
- メッセージ投稿・表示


### 環境構築
- Python 3.8以上
- MariaDB または MySQL


### インストール手順
1. リポジトリのクローン
2. 仮想環境の作成と有効化
3. 依存関係のインストール
4. 環境変数の設定（.envファイルの作成）
5. データベースの初期化


### 使用方法
1. アプリケーションを起動 （python app.py）
2. ブラウザで http://localhost:5000 にアクセス
3. アカウントを新規作成 または ログイン
4. ログイン後、チャンネルを作成してメッセージを投稿