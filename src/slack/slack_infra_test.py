from slack_infrastructure import SlackInfrastructure


class SlackInfraTest:
    def __init__(self):
        self.slack = SlackInfrastructure()

    def channel_history(self):
        # チャンネルの文章の取得
        channel = self.slack.get_a_channel("annotation新卒")
        messages = self.slack.get_channel_history(channel["id"])

        print(messages[0]["text"])

        # for message in messages:
        #     print(message["text"] + "\n")

    def post_message(self):
        # チャンネルにメッセージを送信
        channel = self.slack.get_a_channel("annotation新卒")
        print(self.slack.post_message(channel, "テストメッセージ from python")["message"]["text"])

    def get_user_info(self):
        channel = self.slack.get_a_channel("annotation新卒")
        messages = self.slack.get_channel_history(channel["id"])
        # ユーザー情報の取得
        user_info = self.slack.get_user_info(messages[0]["user"])
        print(user_info["real_name"] + "さんが投稿しました")


slack_test = SlackInfraTest()
# slack_infraの簡易的なテスト
print("=================slack_infraの簡易的なテスト=================")
print("新卒チャンネルから最新のメッセージを取得")
slack_test.channel_history()
print("\n" + "ユーザー情報を取得")
slack_test.get_user_info()
print("\n" + "新卒チャンネルにメッセージを送信")
slack_test.post_message()
