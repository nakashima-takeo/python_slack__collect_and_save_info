import time

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
        channels: list[dict] = []
        params: dict = {
            "types": "public_channel",
            "limit": 1000,
        }
        responses = self.__fetchSlackApi(self.__channel_list_url, "get", params=params)
        channels = [channel for response in responses for channel in response["channels"]]
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
        messages: list[dict] = []
        params: dict = {
            "channel": channel_id,
            "limit": 1000,
        }
        if from_unixtime is not None:
            params["oldest"] = from_unixtime
        responses = self.__fetchSlackApi(self.__history_url, "get", params=params)
        messages = [message for response in responses for message in response["messages"]]
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
          指定されたスレッドの履歴。
        """
        messages: list[dict] = []
        params: dict = {
            "channel": channel["id"],
            "ts": original_message["ts"],
        }
        responses = self.__fetchSlackApi(self.__thread_url, "get", params=params)
        messages = [message for response in responses for message in response["messages"]]
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
        params: dict = {
            "channel": channel["id"],
            "text": text,
        }
        if original_message is not None:
            params["thread_ts"] = original_message["thread_ts"]
        responses = self.__fetchSlackApi(self.__post_message_url, "post", params=params)
        return responses[0]["message"]

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

        Raises
        ------
        ValueError
          ユーザーが見つからなかった場合、複数見つかった場合に発生します。
        """
        params: dict = {
            "user": user_id,
        }
        responses = self.__fetchSlackApi(self.__user_info_url, "get", params=params)
        if len(responses) == 0:
            raise ValueError("ユーザーの取得に失敗しました")
        elif len(responses) >= 2:
            raise ValueError("ユーザーが複数見つかりました")
        user_info = responses[0]["user"]
        return user_info

    def __fetchSlackApi(self, url: str, method: str, params: dict) -> list[dict]:
        """
        SlackAPIを叩いてデータを取得する関数。

        Parameters
        ----------
        url : str
          SlackAPIのURL
        method : str
          HTTPメソッド
        params : dict
          SlackAPIに渡すパラメータ

        Returns
        -------
        list[dict]
          SlackAPIのレスポンスのリスト

        Raises
        ------
        Exception
          SlackAPIのレスポンスがエラーの場合に発生する例外
        """
        cursor = None
        responses: list[dict] = []
        # 再帰処理で全てのデータを取得する
        while True:
            if cursor is not None:
                params["cursor"] = cursor

            # SlackAPIを叩く（成功するまで再試行する）
            while True:
                response = requests.request(method=method, url=url, headers=self.__headersAuth, params=params)
                responseJson = response.json()
                if responseJson["ok"] is True:
                    break
                else:
                    if response.status_code == 429:
                        # レートリミットに達した場合、リセットまで待機
                        reset_time = int(response.headers["Retry-After"])
                        print(f"{reset_time}秒待機した後にリトライします。")
                        time.sleep(reset_time)
                    else:
                        raise Exception(f"SlackAPIのレスポンスがエラーです: {responseJson['error']}: {responseJson['response_metadata']}")

            # ページネーションの処理
            if "has_more" in responseJson:
                if responseJson["has_more"] is True:
                    cursor = responseJson["response_metadata"]["next_cursor"]
                else:
                    cursor = None

            responses.append(responseJson)
            if cursor is None:
                break
        return responses
