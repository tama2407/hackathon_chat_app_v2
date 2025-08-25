#Docker公式ドキュメントに解説あり

# 元にするベースイメージの取得
FROM python:3.12.11-slim

# Dockerfileコマンドを実行する作業ディレクトリを指定
WORKDIR /app

# イメージにファイルやフォルダを追加
COPY requirements.txt .

# イメージをビルドする時にコマンドを実行
RUN pip install -r requirements.txt

# Flaskアプリのソースコード一式をコンテナに追加する
COPY . .

# コンテナが通信を待ち受けるポートを指定
EXPOSE 5000

# コンテナを起動するときに実行するコマンドを指定
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:create_app()"]