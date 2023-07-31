from slack_infrastructure import SlackInfrastructure

def test_preparation() -> SlackInfrastructure:
  return SlackInfrastructure()

def channel_history():
    slack = test_preparation()
    # チャンネルの文章の取得
    channel = slack.get_a_channel("annotation新卒")
    messages = slack.get_channel_history(channel["id"])

    for message in messages:
        print(message["text"] + "\n")

def post_message():
    slack = test_preparation()
    # チャンネルにメッセージを送信
    channel = slack.get_a_channel("annotation新卒")
    slack.post_message(channel, "テストメッセージ from python")
