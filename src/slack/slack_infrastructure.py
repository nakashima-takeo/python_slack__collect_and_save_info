import requests
from typing import List, Dict
# from aws import get_secret

class SlackInfrastructure:
    def __init__(self):
        # slack_api_token = get_secret("slack", "slack_app_token")
        slack_api_token = input("Slack API Token: ")
        if slack_api_token is None:
            raise ValueError("SLACK_API_TOKENが設定されていません")
        self.token = slack_api_token
        self.headersAuth = {
            'Authorization': 'Bearer '+ str(self.token),
        }
        self.history_url = "https://slack.com/api/conversations.history"
        self.channel_list_url = "https://slack.com/api/conversations.list"
        self.post_message_url = "https://slack.com/api/chat.postMessage"
        self.thread_url = "https://slack.com/api/conversations.replies"
        self.user_info_url = "https://slack.com/api/users.info"

    def get_a_channel(self, channel_name: str) -> Dict:
        channels = self.get_all_channels()
        return next((channel for channel in channels if channel["name"] == channel_name), None)

    def get_all_channels(self) -> List[Dict]:
        payload = {
            'types': 'public_channel, private_channel',
            'limit': 1000,
        }
        response = requests.get(self.channel_list_url, headers=self.headersAuth, params=payload)
        response.raise_for_status()
        if not response.json()["ok"]:
            raise ValueError("チャンネルの取得に失敗しました")
        channels = response.json()["channels"]
        return channels

    def get_channel_history(self, channel_id: str) -> List[Dict]:
        payload = {
            'channel': channel_id,
            'limit': 1000,
        }
        response = requests.get(self.history_url, headers=self.headersAuth, params=payload)
        response.raise_for_status()
        messages = response.json()["messages"]
        return messages

    def get_thread_history(self, channel_id: str, thread_ts: str) -> List[Dict]:
        payload = {
            'channel': channel_id,
            'ts': thread_ts,
        }
        response = requests.get(self.thread_url, headers=self.headersAuth, params=payload)
        response.raise_for_status()
        messages = response.json()["messages"]
        return messages

    def post_message(self, channel: Dict, text: str, thread_ts: str = None) -> Dict:
        payload = {
            'channel': channel["id"],
            'text': text,
        }
        if thread_ts is not None:
            payload["thread_ts"] = thread_ts
        response = requests.post(self.post_message_url, headers=self.headersAuth, params=payload)
        response.raise_for_status()
        message = response.json()
        return message

    def get_user_info(self, user_id: str) -> Dict:
        payload = {
            'user': user_id,
        }
        response = requests.get(self.user_info_url, headers=self.headersAuth, params=payload)
        response.raise_for_status()
        user_info = response.json()["user"]
        return user_info
