from flask import Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from database import db_session
from model import Message, Channel
from sqlalchemy.exc import SQLAlchemyError

# メッセージ関係のブループリントを作成（messages_bpという名前で、/messagesから始まるURLを管理する）
messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

# メッセージの投稿
@messages_bp.route('/create', methods=['POST'])
@login_required
def create():
    channel_id = request.form.get('channel_id')
    content = request.form.get('content','').strip()

    # メッセージ内容が空でないか、入力をチェックする
    if not content:
        flash('メッセージを入力してください', 'danger')
        return redirect(url_for('channels.view', channel_id=channel_id))
    
    # チャンネルが存在することを確認する
    channel = db_session.get(Channel, channel_id)
    if channel is None:
        # 存在しない場合は404エラーを返す
        abort(404)

    # 新しいMessageインスタンスを作成して保存する
    try:
        new_message = Message(content=content, user_id=current_user.id, channel_id=channel_id)
        db_session.add(new_message)
        db_session.commit()
        flash('メッセージを送信しました！', 'success')
    except SQLAlchemyError:
        db_session.rollback()
        flash('メッセージの送信に失敗しました...', 'danger')

    return redirect(url_for('channels.view', channel_id=channel_id))
