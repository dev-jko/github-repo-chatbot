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

    seacher = msg.SlackMsgSearcher(SLACK_SEARCH_TOKEN)
    sender = msg.SlackMsgSender(SLACK_BOT_TOKEN, 'wizard')
    while True:
        if seacher.search_msg('\너굴맨', SLACK_GENERAL_ID):
            sender.send_msg('조너굴 바보', 'general')
        # result_set = seacher.search_msg2('\너굴맨', slackgene)
        # if result_set:
        #     for result in result_set:
        #         sender.send_msg('조너굴 바보', result['channel'])
