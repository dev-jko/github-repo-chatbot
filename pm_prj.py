import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from temper_prj import get_weather



# PM 10 좋음 0~30 보통 ~ 80 나쁨 ~150 매우나쁨 150~
# PM 25 좋음 0~ 15 보통 ~ 35 나쁨 ~75 매우나쁨 76~

def temp_and_pm_data(location):
    air_key = 'FKCdgbAO7HrrHnLRueGT45kJ46LSeQZ3W6DH4cDlHj7fYP1G4a9lt5rk54MXSc9sTiobJcdfb8LZG7u1XSnPig%3D%3D'
    url = f'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&pageNo=2&numOfRows=20&ServiceKey={air_key}'

    raw_data = requests.get(url)

    data = BeautifulSoup(raw_data.text, 'html.parser')

    city = data.find_all("cityname")
    pm10value = data.find_all("pm10value")
    pm25value = data.find_all("pm25value")
    datatime = data.find_all('datatime')
    for idx, i in enumerate(city):
        if location in i:
            idx= idx
            break
    else:
        return f'서울시에 있는 \'구\'를 입력해주세요 ex)강남구'
    pm10 = int(str(pm10value[idx])[11:-12])
    pm25 = int(str(pm25value[idx])[11:-12])
    datatime = str(data.find_all('datatime')[idx])[21:26]

    

    if pm10 > 150:
        pm10_condition = '매우 나쁨'
    elif pm10 > 80:
        pm10_condition = '나쁨'
    elif pm10 > 30:
        pm10_condition = '보통'
    else:
        pm10_condition = '좋음'
    
    

    if pm25 > 75:
        pm25_condition = '매우 나쁨'
    elif pm25 > 35:
        pm25_condition = '나쁨'
    elif pm25 > 15:
        pm25_condition = '보통'
    else:
        pm25_condition = '좋음'

    temperature = get_weather(location)

    return f'{location}의 {datatime}시 측정 미세먼지 수치는 {pm10}, \'{pm10_condition}\'입니다. 초미세먼지 수치는 {pm25}, \'{pm25_condition}\'입니다. 현재 기온은 {temperature}도입니다.'


# 서울시 25개구 검색 가능. 기온은 geopy로 검색하기 때문에 전국이 다 가능하지만
# 서울만 검색 가능한 미세먼지 API를 신청함. 하루 500건 접속 가능한 걸로 앎.
# 용산구 은평구 종로구 중구 중랑구 강남구 강동구 강북구 강서구 관악구 광진구
# 구로구 금천구 노원구 도봉구 동대문구 동작구 마포구 서대문구 서초구 가능

    
# temp_and_pm_data(location) 에 구 입력하면 미세먼지와 기온 return함.


print(temp_and_pm_data('강남구'))