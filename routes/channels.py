from flask import (Blueprint, render_template, redirect,url_for, request, flash, abort)
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from database import db_session
from model import Channel, Message

# 部屋関係のブループリントを作成（channels_bpという名前で、/channelsから始まるURLを管理する）
channels_bp = Blueprint('channels', __name__, url_prefix='/channels')

# 部屋一覧ページ
@channels_bp.route('/', methods=['GET'])
@login_required
def index():
    channels = db_session.query(Channel).order_by(Channel.created_at.desc()).all()
    return render_template('channels/index.html',channels=channels)

# 部屋の詳細ページ
@channels_bp.route('/<int:channel_id>', methods=['GET'])
@login_required
def view(channel_id):
    channel = db_session.query(Channel).get_or_404(channel_id)
    messages = (db_session.query(Message).filter_by(channel_id=channel_id).order_by(Message.created_at.asc()).all())
    return render_template('channels/detail.html',channel=channel,messages=messages)

# 新しい部屋の作成
@channels_bp.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()

    if not name or not description:
        flash('チャンネル名と説明は必須です。', 'danger')
        return redirect(url_for('channels.index'))
    
    if db_session.query(Channel).filter_by(name=name).first():
        flash('同じ名前のチャンネルがすでに存在します。', 'danger')
        return redirect(url_for('channels.index'))

    try:
        new_channel = Channel(name=name,description=description,user_id=current_user.id)
        db_session.add(new_channel)
        db_session.commit()
        flash('チャンネルを作成しました！', 'success')

    except SQLAlchemyError:
        db_session.rollback()
        flash('チャンネルの作成に失敗しました。', 'danger')

    return redirect(url_for('channels.index'))

# 部屋の削除
@channels_bp.route('/delete/<int:channel_id>', methods=['POST'])
@login_required
def delete(channel_id):
    channel = db_session.query(Channel).get_or_404(channel_id)

    # 作成者以外は削除できないようにする
    if channel.user_id != current_user.id:
        abort(403)  # 権限なし

    try:
        db_session.delete(channel)
        db_session.commit()
        flash(f'「{channel.name}」を削除しました。', 'success')
    except SQLAlchemyError:
        db_session.rollback()
        flash('削除に失敗しました。', 'danger')

    return redirect(url_for('channels.index'))
