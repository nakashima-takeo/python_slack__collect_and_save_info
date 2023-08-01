from datetime import datetime, timedelta
from typing import Dict

from slack_infrastructure import SlackInfrastructure


class SlackUsecase:
    def __init__(self):
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
