from slack_infrastructure import SlackInfrastructure

slack = SlackInfrastructure()

# チャンネルの文章の取得
channel = slack.get_a_channel("annotation新卒")
messages = slack.get_channel_history(channel["id"])

for message in messages:
    print(message["text"] + "\n")
