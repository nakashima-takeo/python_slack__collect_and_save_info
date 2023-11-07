import datetime
import os

from mymodules.aws import S3
from mymodules.slack import Slack


def save_slack_messages_to_s3(event, context) -> None:
    slack = Slack()
    source_channel_name: str = os.environ["SOURCE_CHANNEL_NAME"]
    report_channel_name: str = os.environ["REPORT_CHANNEL_NAME"]
    search_words: list[str] = os.environ["SEARCH_WORDS"].split(",")
    search_hours: int = 10000
    s3_bucket_name: str = "slack-task-temp-bucket-nakashima-takeo"
    s3_file_title_head: str = "slack"

    # slackからメッセージを取得する
    messages = slack.search_messages(source_channel_name, search_words, search_hours)
    if len(messages) == 0:
        print("メッセージはありませんでした")
        return

    # メッセージを一つのstringに整える
    messages_text: str = ""
    for message in messages:
        thread_messages = slack.get_thread_history(source_channel_name, message)
        messages_text += datetime.datetime.fromtimestamp(float(message["ts"])).strftime("%Y/%m/%d %H:%M:%S") + "\n"
        messages_text += slack.get_user(message["user"])["real_name"] + "\n"
        messages_text += message["text"] + "\n"
        for thread_message in thread_messages:
            if thread_message["ts"] == message["ts"]:
                continue
            messages_text += (
                "     " + datetime.datetime.fromtimestamp(float(thread_message["ts"])).strftime("%Y/%m/%d %H:%M:%S") + "\n"
            )
            messages_text += "     " + slack.get_user(thread_message["user"])["real_name"] + "\n"
            messages_text += "     " + thread_message["text"] + "\n"
        messages_text += "\n"

    # S3にテキストファイルをアップロードする
    s3 = S3()
    public_url = s3.write_txt(s3_bucket_name, s3_file_title_head, messages_text)

    # Slackにメッセージを投稿する
    slack_text: str = (
        f"チャンネル: {source_channel_name}\n"
        + f"検索ワード: {search_words}\n"
        + f"{len(messages)}件のスレッドが見つかりました。\n"
        + f"ダウンロードはこちら: {public_url}"
    )
    slack.post_message(report_channel_name, slack_text)
