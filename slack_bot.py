import requests
import os
import msg_handler
import time
from datetime import datetime
from weather import pm_prj
from ssafy_menu import project_ssafy

msg = msg_handler
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SEARCH_TOKEN = os.getenv('SLACK_SEARCH_TOKEN')
SLACK_GENERAL_ID = os.getenv('SLACK_GENERAL_ID')
SLACK_WIZARD_ID = os.getenv('SLACK_WIZARD_ID')
SSAFY_ID = os.getenv('SSAFY_ID')
SSAFY_PW = os.getenv('SSAFY_PW')


seacher = msg.SlackMsgSearcher(SLACK_SEARCH_TOKEN)
sender = msg.SlackMsgSender(SLACK_BOT_TOKEN, 'wizard')

COMMANDS = {'\너굴맨', '\점심', '\날씨'}

while True:
    # commands = seacher.search_msg(COMMANDS, SLACK_GENERAL_ID)
    commands = seacher.search_msg(
        COMMANDS, SLACK_WIZARD_ID, is_private=True)
    print(f'{datetime.now()} - find - {commands}')
    for command in commands:
        if command == '\너굴맨':
            sender.send_msg('조너굴 바보', 'general')
        if command == '\점심':
            menu = project_ssafy.lunch_menu(
                SSAFY_ID, SSAFY_PW, '/usr/lib/chromium-browser/chromedriver')
            sender.send_msg(menu)
        if command == '\날씨':
            weather = pm_prj.temp_and_pm_data('강남구')
            sender.send_msg(weather)
    time.sleep(1)
