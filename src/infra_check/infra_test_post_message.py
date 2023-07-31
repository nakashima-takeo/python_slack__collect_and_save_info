from slack import SlackInfrastructure

slack = SlackInfrastructure()

# チャンネルにメッセージを送信
channel = slack.get_a_channel("annotation新卒")
slack.post_message(channel, "テストメッセージ from python")
