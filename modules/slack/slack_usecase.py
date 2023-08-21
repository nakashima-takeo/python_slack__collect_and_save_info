from datetime import datetime, timedelta
from typing import Dict

from .slack_infrastructure import SlackInfrastructure


class SlackUsecase:
    def __init__(self):
        self.users = []
        self.slack_infrastructure = SlackInfrastructure()

    def search_messages(self, channel_name: str, search_words: list[str], search_hours: int) -> list[Dict]:
        channel = self.slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        # search_hours時間前のunixtimeを計算する
        from_unixtime = int((datetime.now() - timedelta(hours=search_hours)).timestamp())
        messages = self.slack_infrastructure.get_channel_history(channel["id"], from_unixtime)
        messages = [message for message in messages if any(word in message["text"] for word in search_words)]
        return messages

    def get_thread_history(self, channel_name: str, original_message: Dict) -> list[Dict]:
        channel = self.slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        messages = self.slack_infrastructure.get_thread_history(channel, original_message)
        return messages

    def get_user(self, user_id: str) -> Dict:
        # 既に取得済みのユーザー情報を取得
        user = next((user for user in self.users if user["id"] == user_id), None)
        if user is not None:
            return user
        # 取得済みでない場合はAPIを叩いて取得
        new_user = self.slack_infrastructure.get_user_info(user_id)
        self.users.append(new_user)
        return new_user

    def post_message(self, channel_name: str, message: str) -> None:
        channel = self.slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        self.slack_infrastructure.post_message(channel, message)
