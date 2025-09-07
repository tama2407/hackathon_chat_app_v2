-- （１） 文字コードの設定
SET NAMES utf8mb4;

-- （２） データーベースの作成
--    データーベースの作成（初回のみ、既に存在する場合は何もしない）
CREATE DATABASE IF NOT EXISTS `hackathon_chat_app_v2_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- （３）対象とするデーターベースの選択
USE `hackathon_chat_app_v2_db`;

-- （４）テーブル作成
--    users: アプリのユーザー
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `password` VARCHAR(60) NOT NULL,   -- bcryptハッシュ用（model.pyより）
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_name` (`name`),
  UNIQUE KEY `uq_users_email` (`email`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

--    channels: チャンネル（部屋）
CREATE TABLE IF NOT EXISTS `channels` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `description` TEXT NOT NULL,
  `user_id` INT NOT NULL,  -- 作成者
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_channels_name` (`name`),
  KEY `ix_channels_user_id` (`user_id`),
  CONSTRAINT `fk_channels_user`
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

--    messages: メッセージ
CREATE TABLE IF NOT EXISTS `messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `user_id` INT NOT NULL,
  `channel_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_messages_user_id` (`user_id`),
  KEY `ix_messages_channel_id` (`channel_id`),
  KEY `ix_messages_channel_created` (`channel_id`, `created_at`),
  CONSTRAINT `fk_messages_user`
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
  CONSTRAINT `fk_messages_channel`
    FOREIGN KEY (`channel_id`) REFERENCES `channels`(`id`)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- （５）動作確認用のサンプルデータ
-- model.pyでbcryptハッシュを前提としているため、パスワードは'test123'をハッシュ化
INSERT INTO users(name, email, password)VALUES('テスト', 'test1@gmail.com', '2b$12$LQv3c1yqBwEHq.lNGQJpce7nQsWTOGdE.Xc9ORW.zNxNZeKx3KOke');
INSERT INTO channels(user_id, name, description)VALUES(1, 'ぼっち部屋', 'テストさんの孤独な部屋です');
INSERT INTO messages(user_id, channel_id, content)VALUES(1, 1, '誰かかまってください、、、');
