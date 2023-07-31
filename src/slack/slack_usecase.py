from slack_infrastructure import SlackInfrastructure


class SlackUsecase:
    def __init__(self):
        self.slack_infrastructure = SlackInfrastructure()

    # def get_messages(self, channel_name: str, search_words: list[str], search_hours: int) -> list[str]:
    #     channel = self.slack_infrastructure.get_a_channel(channel_name)
    #     if channel is None:
    #         raise ValueError(f"チャンネル「{channel_name}」が見つかりませんでした")
    #     messages = self.slack_infrastructure.get_channel_history(channel["id"])
    #     messages = [message for message in messages if self.__is_within_hours(message, search_hours)]
    #     messages = [message for message in messages if self.__contains_words(message, search_words)]
    #     messages = [message["text"] for message in messages]
    #     return messages
