
from slack.slack_usecase import SlackUsecase
from aws.s3 import S3

def main():
  slack_usecase = SlackUsecase()
  source_channel_name :str = "annotation新卒"
  report_channel_name :str = "annotation新卒"
  search_words :list[str] = ["こんにちは", "こんばんは", "API"]
  search_hours :int = 24

  # slackからメッセージを取得する
  messages = slack_usecase.get_messages(source_channel_name, search_words, search_hours)
  if len(messages) == 0:
    print("メッセージはありませんでした")
    return

  # メッセージをテキストファイルに書き出す
  with open("messages.txt", mode="w") as f:
    f.write("\n".join(messages))

  # S3にテキストファイルをアップロードする
  s3 = S3()
  s3.upload_file("messages.txt", "messages.txt")

  # Slackにメッセージを投稿する
  slack_usecase.post_message(report_channel_name, "メッセージを保存しました")
