

def lunch_menu(user_id, user_pwd, driver_location):
    import requests
    from bs4 import BeautifulSoup  # pip install bs4
    from selenium import webdriver  # pip install selenium
    import time
    import datetime
    from time import strftime, localtime
    import schedule  # pip install schedule
    # schedule 모듈 document : https://schedule.readthedocs.io/en/stable/
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    weekday = time.localtime().tm_wday
    today = strftime("%m-%d", localtime())
    # weekend일 경우 pass
    if weekday in [5, 6]:
        result = '오늘은 점심이 없는 날입니다'

    else:
        driver = webdriver.Chrome(driver_location, chrome_options=options)

        driver.get('https://edu.ssafy.com/comm/login/SecurityLoginForm.do')

        driver.find_element_by_name('userId').send_keys(user_id)
        driver.find_element_by_name('userPwd').send_keys(user_pwd)
        driver.find_element_by_xpath(
            '//*[@id="wrap"]/div/div/div[4]/form/div/div[2]/div[3]/a').click()

        driver.get('https://edu.ssafy.com/edu/board/notice/list.do')
        A = ''
        B = ''

        # exception week for 3.1
        if today in ["02-25", "02-26", "02-27", "02-28", "03-01"]:
            # 금요일(4)인 경우 pass
            if weekday == 4:
                result = '오늘은 점심이 없는 날입니다'
            else:
                driver.find_element_by_partial_link_text(
                    '2019년 02월 4주차').click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                A_main = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(9) > td:nth-child({weekday + 4})')[0].text.strip()
                B_main = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(17) > td:nth-child({weekday + 2})')[0].text.strip()
                for i in range(10, 15):
                    A += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i}) > td:nth-child({weekday + 1})')[
                        0].text.strip() + ' '
                    B += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i + 8}) > td:nth-child({weekday + 1})')[
                        0].text.strip() + ' '
                drink = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(15) > td:nth-child({weekday + 1})')[0].text.strip()
                result = f'A코스: {A_main} {A}\nB코스: {B_main} {B}\n음료수: {drink}'

        # exception week for 5.5
        # 5월 1주차 or 5월 2주차 / 5월 1주차라는 가정하에
        elif today in ["05-06", "05-07", "05-08", "05-09", "05-10"]:
            # 월요일(0)인 경우 pass
            if weekday == 0:
                result = '오늘은 점심이 없는 날입니다'
            else:
                driver.find_element_by_partial_link_text(
                    '2019년 05월 1주차').click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                # 어린이날 월요일 1일을 기존 weekday 계산에서 빼준다. 단 첫 번째 row 즉 A_main의 경우 어린이날이라는 글자가 있기 때문에 빼지 않는다
                A_main = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(9) > td:nth-child({weekday + 4})')[0].text.strip()
                B_main = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(17) > td:nth-child({weekday + 1})')[0].text.strip()
                for i in range(10, 15):
                    A += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i}) > td:nth-child({weekday})')[
                        0].text.strip() + ' '
                    B += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i + 8}) > td:nth-child({weekday})')[
                        0].text.strip() + ' '
                drink = soup.select(
                    f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(15) > td:nth-child({weekday})')[0].text.strip()
                result = f'A코스: {A_main} {A}\nB코스: {B_main} {B}\n음료수: {drink}'

        # normal week for no holiday
        else:
            driver.find_element_by_partial_link_text('중식').click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            A_main = soup.select(
                f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(9) > td:nth-child({weekday + 4})')[0].text.strip()
            B_main = soup.select(
                f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(17) > td:nth-child({weekday + 2})')[0].text.strip()
            for i in range(10, 15):
                A += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i}) > td:nth-child({weekday + 1})')[
                    0].text.strip() + ' '
                B += soup.select(f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child({i + 8}) > td:nth-child({weekday + 1})')[
                    0].text.strip() + ' '
            drink = soup.select(
                f'#wrap > form > div > div.content > div > div:nth-child(1) > div.datail-content.mb20 > table > tbody > tr:nth-child(15) > td:nth-child({weekday + 1})')[0].text.strip()
            result = f'A코스: {A_main} {A}\nB코스: {B_main} {B}\n음료수: {drink}'

        return result


def check_in_out_alarm(user_id, user_pwd, driver_location):
    driver = webdriver.Chrome(driver_location)
    url = 'https://edu.ssafy.com/comm/login/SecurityLoginForm.do'
    driver.get(url)

    driver.find_element_by_name('userId').send_keys(user_id)
    driver.find_element_by_name('userPwd').send_keys(user_pwd)
    driver.find_element_by_xpath(
        '//*[@id="wrap"]/div/div/div[4]/form/div/div[2]/div[3]/a').click()

    driver.get('https://edu.ssafy.com/edu/mycampus/attendance/attendanceList.do')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    today = time.strftime("%Y-%m-%d")

    check_in_out = soup.select(
        f'a.fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.cate.at01.event-on-{today}')
    early_check_out = soup.select(
        f'a.fc-day-grid-event.fc-h-event.fc-event.fc-start.fc-end.cate.at02.event-on-{today}')
    check = len(check_in_out)
    early = len(early_check_out)
    if check == 0:
        result = '아직 퇴실하지 않으셨습니다'
    if check == 1:
        if early == 1:
            result = f'{early_check_out[0].text}'
    if check == 2:
        if int(check_in_out[1].text[0:2]) < 18:
            result = '18시 이전에 퇴실 버튼을 누르셨습니다!'
        else:
            result = f'{check_in_out[0].text}\n{check_in_out[1].text}'

    return result

# check_in_out_alarm()
# # 11:50 마다 점심 메뉴 알려주기
# schedule.every().day.at("11:50").do()
# # 18:01 마다 퇴실 여부 알려주기
# schedule.every().day.at("18:01").do()

# while 1:
#     #스케줄 모듈을 계속해서 실행하기
#     schedule.run_pending()
#     time.sleep(1)
