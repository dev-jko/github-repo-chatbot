def get_weather(input_location):
    from darksky import forecast
    from datetime import datetime
    
    API_KEY = '00ebc1052d5ab59784ec9067f1763825'
    
    # import darkskylib
    from geopy.geocoders import Nominatim
    
    geo = Nominatim(user_agent='goo weather app')
    
    
    
    l = geo.geocode(input_location)
    lat = round(l.latitude, 3)
    lon = round(l.longitude, 3)
    
    geo_data = (l.latitude, l.longitude)
    
    location = forecast(API_KEY, lat, lon)
    temp = round((float(location.currently['temperature']) -32)*5/9, 2)
    # summary = location.currently['summary']
    # t = datetime.utcfromtimestamp(location.time)

    # return f'{input_location}의 온도는 \'{temp}\'도입니다.'
    return temp

# print(get_weather('강남구'))