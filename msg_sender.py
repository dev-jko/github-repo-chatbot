import requests
import os
import datetime
import time


class MsgSearcher:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.timestamp = time.time()
        # self.timestamp = datetime.datetime.now()


# class TelegramMsgSearcher(MsgSearcher):
#     def read_msg(self, msg):
#         if receive_user is None:
#             receive_user = self.receive_user
#         url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={receive_user}&text={msg}'
#         response = requests.post(url).json()
#         return response['ok']


class SlackMsgSearcher(MsgSearcher):
    def search_msg2(self, msg):
        url = f'https://slack.com/api/search.messages?token={self.bot_token}&query={msg}'
        response = requests.get(url).json()
        if response['ok']:
            messages = response['messages']['matches']
            result_set = []
            temp_timestamp = self.timestamp
            for message in messages:
                message_time = float(message['ts'])
                if message_time > self.timestamp:
                    if msg in message['text']:
                        temp_timestamp = message_time
                        result = {}
                        result['channel'] = message['channel']['name']
                        result['channel_id'] = message['channel']['id']
                        result_set.append(result)
            self.timestamp = temp_timestamp
            return result_set
        else:
            return None

    def search_msg(self, msg_set, channel_id):
        url = f'https://slack.com/api/channels.history?token={self.bot_token}&channel={channel_id}&count=5'
        response = requests.get(url).json()
        if response['ok']:
            messages = response['messages']
            temp_timestamp = self.timestamp
            result = set({})
            for message in messages:
                message_time = float(message['ts'])
                if message_time > self.timestamp:
                    for msg in msg_set:
                        if msg in message['text']:
                            result.add(msg)
                            temp_timestamp = message_time
                            self.timestamp = temp_timestamp
            self.timestamp = temp_timestamp
            return result
        return None


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
