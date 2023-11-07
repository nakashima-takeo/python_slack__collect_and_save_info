from typing import Dict, List

import requests

from mymodules.aws import SecretsManager


class SlackInfrastructure:
    """
    Slack APIを利用するためのインフラストラクチャを提供するクラスです。
    """

    def __init__(self):
        __secrets_manager = SecretsManager()
        __slack_api_token = __secrets_manager.get_secret("slack", "slack_app_token")
        # __slack_api_token = input("Slack API Token: ")
        if __slack_api_token is None:
            raise ValueError("SLACK_API_TOKENが設定されていません")
        self.__token = __slack_api_token
        self.__headersAuth = {
            "Authorization": "Bearer " + str(self.__token),
        }

        self.__history_url = "https://slack.com/api/conversations.history"
        self.__channel_list_url = "https://slack.com/api/conversations.list"
        self.__post_message_url = "https://slack.com/api/chat.postMessage"
        self.__thread_url = "https://slack.com/api/conversations.replies"
        self.__user_info_url = "https://slack.com/api/users.info"

    def get_a_channel(self, channel_name: str) -> Dict | None:
        """
        指定されたチャンネル名に一致するチャンネルを取得します。

        Parameters
        ----------
        channel_name : str
          取得したいチャンネル名

        Returns
        -------
        Dict or None
          指定されたチャンネル名に一致するチャンネルの情報。見つからなかった場合はNone。
        """
        channels = self.get_all_channels()
        return next(
            (channel for channel in channels if channel["name"] == channel_name),
        )

    def get_all_channels(self) -> List[Dict]:
        """
        全てのチャンネルの情報を取得します。

        Returns
        -------
        List[Dict]
          全てのチャンネルの情報を含むリスト。
        """
        payload: Dict = {
            "types": "public_channel, private_channel",
            "limit": 1000,
        }
        response = requests.get(self.__channel_list_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        if not response.json()["ok"]:
            raise ValueError("チャンネルの取得に失敗しました")
        channels = response.json()["channels"]
        return channels

    def get_channel_history(self, channel_id: str, from_unixtime: int | None = None) -> List[Dict]:
        """
        指定されたチャンネルの履歴を取得します。

        Parameters
        ----------
        channel_id : str
          取得したいチャンネルのID
        from_unixtime : int or None
          取得するメッセージの最古のUNIX時間。指定しない場合はNone。

        Returns
        -------
        List[Dict]
          指定されたチャンネルの履歴を含むリスト。
        """
        payload: Dict = {
            "channel": channel_id,
            "limit": 1000,
        }
        if from_unixtime is not None:
            payload["oldest"] = from_unixtime
        response = requests.get(self.__history_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        if not response.json()["ok"]:
            raise ValueError("チャンネルの取得に失敗しました")
        messages = response.json()["messages"]
        return messages

    def get_thread_history(self, channel: Dict, original_message: Dict) -> List[Dict]:
        """
        指定されたスレッドの履歴を取得します。

        Parameters
        ----------
        channel : Dict
          スレッドが存在するチャンネルの情報
        original_message : Dict
          スレッドの親メッセージ

        Returns
        -------
        List[Dict]
          指定されたスレッドの履歴を含むリスト。
        """
        payload: Dict = {
            "channel": channel["id"],
            "ts": original_message["ts"],
        }
        response = requests.get(self.__thread_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        messages = response.json()["messages"]
        return messages

    def post_message(self, channel: Dict, text: str, original_message: Dict | None = None) -> Dict:
        """
        指定されたチャンネルにメッセージを投稿します。

        Parameters
        ----------
        channel : Dict
          メッセージを投稿するチャンネルの情報
        text : str
          投稿するメッセージの本文
        original_message : Dict or None
          返信するメッセージの情報。指定しない場合はNone。

        Returns
        -------
        Dict
          投稿されたメッセージの情報。
        """
        payload: Dict = {
            "channel": channel["id"],
            "text": text,
        }
        if original_message is not None:
            payload["thread_ts"] = original_message["thread_ts"]
        response = requests.post(self.__post_message_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        message = response.json()
        if not message["ok"]:
            raise ValueError("メッセージの送信に失敗しました")
        return message["message"]

    def get_user_info(self, user_id: str) -> Dict:
        """
        指定されたユーザーの情報を取得します。

        Parameters
        ----------
        user_id : str
          取得したいユーザーのID

        Returns
        -------
        Dict
          指定されたユーザーの情報。
        """
        payload: Dict = {
            "user": user_id,
        }
        response = requests.get(self.__user_info_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        user_info = response.json()["user"]
        return user_info
