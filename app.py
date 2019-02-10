from flask import Flask, render_template, request
import requests
import os
import msg_handler
import time

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>index page</h1>'


@app.route('/<string:string>')
def test(string):
    return(f'test {string}!')


@app.route('/send_msg', methods=['POST', 'GET'])
def send_msg():
    if request.method == 'GET':
        return render_template('msg.html')
    else:
        msg = msg_handler
        if request.form['messenger'] == 'slack':
            SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
            print(SLACK_BOT_TOKEN)
            sender = msg.SlackMsgSender(SLACK_BOT_TOKEN, 'wizard')
        else:
            TELEGRAM_MY_ID = os.getenv('TELEGRAM_MY_ID')
            TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
            sender = msg.TelegramMsgSender(TELEGRAM_BOT_TOKEN, TELEGRAM_MY_ID)
        if sender.send_msg(request.form['msg']):
            ok = '성공'
        else:
            ok = '실패'
        return render_template('msg.html', ok=ok)


if __name__ == '__main__':
    # app.run(debug=True)

    msg = msg_handler
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_SEARCH_TOKEN = os.getenv('SLACK_SEARCH_TOKEN')
    SLACK_GENERAL_ID = os.getenv('SLACK_GENERAL_ID')
    SLACK_WIZARD_ID = os.getenv('SLACK_WIZARD_ID')

    seacher = msg.SlackMsgSearcher(SLACK_SEARCH_TOKEN)
    sender = msg.SlackMsgSender(SLACK_BOT_TOKEN, 'wizard')

    COMMANDS = {'\너굴맨', '\점심', '\날씨'}

    while True:
        # commands = seacher.search_msg(COMMANDS, SLACK_GENERAL_ID)
        commands = seacher.search_msg(COMMANDS, SLACK_WIZARD_ID, is_private=True)
        for command in commands:
            if command == '\너굴맨':
                sender.send_msg('조너굴 바보', 'general')
            if command == '\점심':
                sender.send_msg('점심 메뉴')
            if command == '\날씨':
                sender.send_msg('날씨')