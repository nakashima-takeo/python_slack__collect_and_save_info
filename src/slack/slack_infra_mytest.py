from slack_infrastructure import SlackInfrastructure


class SlackInfraMyTest:
    def __init__(self):
        self.slack = SlackInfrastructure()

    def channel_history(self):
        # チャンネルの文章の取得
        channel = self.slack.get_a_channel("annotation新卒")
        messages = self.slack.get_channel_history(channel["id"])

        print(messages[0]["text"])

    def post_message(self):
        # チャンネルにメッセージを送信
        channel = self.slack.get_a_channel("annotation新卒")
        print(self.slack.post_message(channel, "テストメッセージ from python")["text"])

    def get_user_info(self):
        channel = self.slack.get_a_channel("annotation新卒")
        messages = self.slack.get_channel_history(channel["id"])
        # ユーザー情報の取得
        user_info = self.slack.get_user_info(messages[0]["user"])
        print(user_info["real_name"] + "さんが投稿しました")

    def get_thread_history(self):
        # スレッドの文章の取得
        channel = self.slack.get_a_channel("annotation新卒")
        messages = self.slack.get_channel_history(channel["id"])
        for message in messages:
            if "thread_ts" in message:
                thread_messages = self.slack.get_thread_history(channel, message)
                print("スレッド元：" + thread_messages[0]["text"])
                print("スレッド1 :" + thread_messages[1]["text"])
                break


slack_test = SlackInfraMyTest()
# slack_infraの簡易的なテスト
print("=================slack_infraの簡易的なテスト=================")
print("新卒チャンネルから最新のメッセージを取得")
slack_test.channel_history()
print("\n" + "ユーザー情報を取得")
slack_test.get_user_info()
print("\n" + "新卒チャンネルにメッセージを送信")
slack_test.post_message()
print("\n" + "スレッドのメッセージを取得")
slack_test.get_thread_history()
print("\n" + "=========================================================")
