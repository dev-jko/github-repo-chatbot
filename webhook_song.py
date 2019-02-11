# 'ide.c9.io/'#domain이라고부른다.       ssonggunho/songgunho# 라우트라고 부른다.
from flask import Flask, jsonify, render_template, redirect, request, url_for #sudo pip3 install flask #export FLASK_APP=app.py #flask run -h 0.0.0.0 -p 8080   #export FLASK_ENV=development #python3 app.py
import requests
import random

app = Flask(__name__) 

@app.route("/webhook", methods=['POST']) #index
def index():
    data = request.get_json()
    header_data = request.headers.get('X-GitHub-Event')
    print(header_data)
    MY_CHAT_ID = '692438053' # 대문자는 상수
    BOT_TOKEN = '736162634:AAG4mRZYkCxNcqg9ocIoCpGZCX4wJ_-mVbQ'
    MSG = header_data+'가 일어났습니다.'
    url = 'https://api.hphk.io/telegram/bot{}/sendMessage?chat_id={}&text={}'.format(BOT_TOKEN, MY_CHAT_ID, MSG)
    response = requests.get(url)
    return render_template('index.html')
    print("")
    
    
@app.route("/") #index
def index2():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


    
