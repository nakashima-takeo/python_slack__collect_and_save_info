from datetime import datetime, timedelta
from typing import Dict

from .slack_infrastructure import SlackInfrastructure


class SlackUsecase:
    """
    Slackの機能を利用するためのユースケースクラスです。
    """

    def __init__(self):
        self.__users = []
        self.__slack_infrastructure = SlackInfrastructure()

    def search_messages(self, channel_name: str, search_words: list[str], search_hours: int) -> list[Dict]:
        """
        指定したチャンネル内のメッセージを検索します。

        Parameters
        ----------
        channel_name : str
          チャンネル名
        search_words : list[str]
          検索する単語のリスト
        search_hours : int
          検索する時間範囲（何時間前まで検索するか）

        Returns
        -------
        list[Dict]
          検索結果のメッセージのリスト
        """
        channel = self.__slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        # search_hours時間前のunixtimeを計算する
        from_unixtime = int((datetime.now() - timedelta(hours=search_hours)).timestamp())
        messages = self.__slack_infrastructure.get_channel_history(channel["id"], from_unixtime)
        messages = [message for message in messages if any(word in message["text"] for word in search_words)]
        return messages

    def get_thread_history(self, channel_name: str, original_message: Dict) -> list[Dict]:
        """
        指定したチャンネル内のスレッドの履歴を取得します。

        Parameters
        ----------
        channel_name : str
          チャンネル名
        original_message : Dict
          スレッドの親メッセージ

        Returns
        -------
        list[Dict]
          スレッドの履歴のリスト
        """
        channel = self.__slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        messages = self.__slack_infrastructure.get_thread_history(channel, original_message)
        return messages

    def get_user(self, user_id: str) -> Dict:
        """
        指定したユーザーの情報を取得します。

        Parameters
        ----------
        user_id : str
          ユーザーID

        Returns
        -------
        Dict
          ユーザー情報
        """
        # 既に取得済みのユーザー情報を取得
        user = next((user for user in self.__users if user["id"] == user_id), None)
        if user is not None:
            return user
        # 取得済みでない場合はAPIを叩いて取得
        new_user = self.__slack_infrastructure.get_user_info(user_id)
        self.__users.append(new_user)
        return new_user

    def post_message(self, channel_name: str, message: str) -> None:
        """
        指定したチャンネルにメッセージを投稿します。

        Parameters
        ----------
        channel_name : str
          チャンネル名
        message : str
          投稿するメッセージ
        """
        channel = self.__slack_infrastructure.get_a_channel(channel_name)
        if channel is None:
            raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
        self.__slack_infrastructure.post_message(channel, message)
