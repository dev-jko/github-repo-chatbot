from flask import Flask, render_template, request
import requests
import os
from msg_handler import msg_handler
import time
from datetime import datetime
from weather import pm_prj, temper_prj

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


@app.route("/payload", methods=['POST'])
def payload():
    data = request.get_json()
    header_data = request.headers.get('X-GitHub-Event')
    msg = header_data+'가 일어났습니다.'
    sender.send_msg(msg, 'wizard')
    return msg


if __name__ == '__main__':
    msg = msg_handler
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_SEARCH_TOKEN = os.getenv('SLACK_SEARCH_TOKEN')
    SLACK_GENERAL_ID = os.getenv('SLACK_GENERAL_ID')
    SLACK_WIZARD_ID = os.getenv('SLACK_WIZARD_ID')

    seacher = msg.SlackMsgSearcher(SLACK_SEARCH_TOKEN)
    sender = msg.SlackMsgSender(SLACK_BOT_TOKEN, 'wizard')

    app.run(host='0.0.0.0', port=5000)
