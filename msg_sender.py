import requests
import os


class MsgSender:
    def __init__(self, bot_token):
        self.bot_token = bot_token


class TelegramMsgSender(MsgSender):
    def __init__(self, bot_token, receive_user):
        super().__init__(bot_token)
        self.receive_user = receive_user

    def send_msg(self, msg, receive_user=None):
        if receive_user is None:
            receive_user = self.receive_user
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={receive_user}&text={msg}'
        response = requests.post(url).json()
        return response['ok']


class SlackMsgSender(MsgSender):
    def __init__(self, bot_token, channel):
        super().__init__(bot_token)
        self.channel = channel

    def send_msg(self, msg, channel=None):
        if channel is None:
            channel = self.channel
        url = f'https://slack.com/api/chat.postMessage?token={self.bot_token}&channel={channel}&text={msg}&pretty=1'
        response = requests.post(url).json()
        return response['ok']
