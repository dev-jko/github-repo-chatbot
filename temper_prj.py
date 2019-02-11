def get_weather(input_location):
    from darksky import forecast
    from datetime import datetime
    import os
    
    key= os.getenv('temp_key')

    from geopy.geocoders import Nominatim
    
    geo = Nominatim(user_agent='goo weather app')
    
    l = geo.geocode(input_location)
    lat = round(l.latitude, 3)
    lon = round(l.longitude, 3)
    
    geo_data = (l.latitude, l.longitude)
    
    location = forecast(key, lat, lon)
    temp = round((float(location.currently['temperature']) -32)*5/9, 2)

    return temp

