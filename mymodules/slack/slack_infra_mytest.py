from .slack_infrastructure import SlackInfrastructure
from .slack_usecase import SlackUsecase


class SlackInfraMyTest:
    """
    SlackInfrastructureのテスト用クラス
    """

    def __init__(self):
        self.__slack = SlackInfrastructure()

    def channel_history(self):
        """
        チャンネルの投稿履歴を取得するメソッド
        """
        channel = self.__slack.get_a_channel("annotation新卒")
        messages = self.__slack.get_channel_history(channel["id"])

        print(messages[0]["text"])

    def post_message(self):
        """
        チャンネルにメッセージを投稿するメソッド
        """
        channel = self.__slack.get_a_channel("annotation新卒")
        print(self.__slack.post_message(channel, "テストメッセージ from python")["text"])

    def get_user_info(self):
        """
        ユーザー情報を取得するメソッド
        """
        channel = self.__slack.get_a_channel("annotation新卒")
        messages = self.__slack.get_channel_history(channel["id"])
        user_info = self.__slack.get_user_info(messages[0]["user"])
        print(user_info["real_name"] + "さんが投稿しました")

    def get_thread_history(self):
        """
        スレッドの投稿履歴を取得するメソッド
        """
        channel = self.__slack.get_a_channel("annotation新卒")
        messages = self.__slack.get_channel_history(channel["id"])
        for message in messages:
            if "thread_ts" in message:
                thread_messages = self.__slack.get_thread_history(channel, message)
                print("スレッド元：" + thread_messages[0]["text"])
                print("スレッド1 :" + thread_messages[1]["text"])
                break


class SlackUsecaseMyTest:
    """
    SlackUsecaseのテスト用クラス
    """

    def __init__(self):
        self.__slack = SlackUsecase()

    def search_messages(self):
        messages = self.__slack.search_messages("annotation新卒", ["こんにちは", "こんばんは", "API"], 10000)
        for message in messages:
            print(message["text"])


# slack_infraの簡易的なテスト
slack_infra_test = SlackInfraMyTest()
print("=================slack_infraの簡易的なテスト=================")
print("新卒チャンネルから最新のメッセージを取得")
slack_infra_test.channel_history()
print("\n" + "ユーザー情報を取得")
slack_infra_test.get_user_info()
# print("\n" + "新卒チャンネルにメッセージを送信")
# slack_infra_test.post_message()
print("\n" + "スレッドのメッセージを取得")
slack_infra_test.get_thread_history()
print("\n" + "=========================================================")

# slack_usecaseの簡易的なテスト
slack_usecase_test = SlackUsecaseMyTest()
print("=================slack_usecaseの簡易的なテスト=================")
print("新卒チャンネルから「こんにちは」「こんばんは」「API」を含むメッセージを取得")
slack_usecase_test.search_messages()
print("\n" + "=========================================================")
