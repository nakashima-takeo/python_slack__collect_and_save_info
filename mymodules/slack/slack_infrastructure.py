import requests


class SlackInfrastructure:
    """
    Slack APIを利用するためのインフラストラクチャを提供するクラスです。
    """

    def __init__(self, slack_token: str):
        if slack_token is None:
            raise ValueError("SLACK_API_TOKENが設定されていません")
        self.__token = slack_token
        self.__headersAuth = {
            "Authorization": "Bearer " + str(self.__token),
        }

        self.__history_url = "https://slack.com/api/conversations.history"
        self.__channel_list_url = "https://slack.com/api/conversations.list"
        self.__post_message_url = "https://slack.com/api/chat.postMessage"
        self.__thread_url = "https://slack.com/api/conversations.replies"
        self.__user_info_url = "https://slack.com/api/users.info"

    def get_a_channel(self, channel_name: str) -> dict | None:
        """
        指定されたチャンネル名に一致するチャンネルを取得します。

        Parameters
        ----------
        channel_name : str
          取得したいチャンネル名

        Returns
        -------
        dict or None
          指定されたチャンネル名に一致するチャンネルの情報。見つからなかった場合はNone。
        """
        channels = self.get_all_channels()
        return next(
            (channel for channel in channels if channel["name"] == channel_name),
        )

    def get_all_channels(self) -> list[dict]:
        """
        全てのチャンネルの情報を取得します。

        Returns
        -------
        list[dict]
          全てのチャンネルの情報を含むリスト。
        """
        payload: dict = {
            "types": "public_channel, private_channel",
            "limit": 1000,
        }
        response = requests.get(self.__channel_list_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        if not response.json()["ok"]:
            raise ValueError("チャンネルの取得に失敗しました")
        channels = response.json()["channels"]
        return channels

    def get_channel_history(self, channel_id: str, from_unixtime: int | None = None) -> list[dict]:
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
        list[dict]
          指定されたチャンネルの履歴を含むリスト。
        """
        payload: dict = {
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

    def get_thread_history(self, channel: dict, original_message: dict) -> list[dict]:
        """
        指定されたスレッドの履歴を取得します。

        Parameters
        ----------
        channel : dict
          スレッドが存在するチャンネルの情報
        original_message : dict
          スレッドの親メッセージ

        Returns
        -------
        list[dict]
          指定されたスレッドの履歴を含むリスト。
        """
        payload: dict = {
            "channel": channel["id"],
            "ts": original_message["ts"],
        }
        response = requests.get(self.__thread_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        messages = response.json()["messages"]
        return messages

    def post_message(self, channel: dict, text: str, original_message: dict | None = None) -> dict:
        """
        指定されたチャンネルにメッセージを投稿します。

        Parameters
        ----------
        channel : dict
          メッセージを投稿するチャンネルの情報
        text : str
          投稿するメッセージの本文
        original_message : dict or None
          返信するメッセージの情報。指定しない場合はNone。

        Returns
        -------
        dict
          投稿されたメッセージの情報。
        """
        payload: dict = {
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

    def get_user_info(self, user_id: str) -> dict:
        """
        指定されたユーザーの情報を取得します。

        Parameters
        ----------
        user_id : str
          取得したいユーザーのID

        Returns
        -------
        dict
          指定されたユーザーの情報。
        """
        payload: dict = {
            "user": user_id,
        }
        response = requests.get(self.__user_info_url, headers=self.__headersAuth, params=payload)
        response.raise_for_status()
        user_info = response.json()["user"]
        return user_info
