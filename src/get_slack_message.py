import datetime

from aws.S3 import S3
from slack.slack_usecase import SlackUsecase


def save_slack_messages_to_s3() -> None:
    slack = SlackUsecase()
    source_channel_name: str = "annotation新卒"
    report_channel_name: str = "annotation新卒"
    search_words: list[str] = ["こんにちは", "こんばんは", "API"]
    search_hours: int = 24

    # slackからメッセージを取得する
    messages = slack.search_messages(source_channel_name, search_words, search_hours)
    if len(messages) == 0:
        print("メッセージはありませんでした")
        return

    # メッセージを一つのstringに整える
    messages_text: str = ""
    for message in messages:
        messages_text += datetime.datetime.fromtimestamp(int(message["ts"]) * 1000).strftime("%Y/%m/%d %H:%M:%S") + "\n"
        messages_text += slack.get_user(message["user"])["real_name"] + "\n"
        messages_text += message["text"] + "\n"
        messages_text += "\n"

    # S3にテキストファイルをアップロードする
    s3 = S3()
    s3.write_txt("slack_task_bucket_temp", "slack", messages_text)

    # # Slackにメッセージを投稿する
    slack.post_message(report_channel_name, "メッセージを保存しました")
