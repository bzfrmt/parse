from pprint import pprint
import requests
import json
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
location_link='http://dataservice.accuweather.com/locations/v1/cities/search'
main_link = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'

city = 'orenburg'
appid = 'Ag2DEnAGOHNOr4uJFgCcuIbE3PKPp8MF'
params = {'q':city,
          'apikey':appid}
#response = requests.get(main_link,headers=header,params=params)
response = requests.get(location_link,headers=header,params=params)
print (response)
if response.ok:
    location_data = json.loads(response.text)
    #print(location_data)
    for city in location_data:
        print(city['Key'],city['LocalizedName'])
        params_forecast = {'apikey':appid}
        response_forecast = requests.get(main_link+city['Key'],headers=header,params=params_forecast)
        #print (response)
        if response.ok:
                forecast_data = json.loads(response_forecast.text)
                #print(forecast_data)
                with open('task2.json', 'w', encoding='utf-8') as f:
                    json.dump(forecast_data, f, ensure_ascii=False)
                print(forecast_data['DailyForecasts'])


#print(f"В городе {data['name']} температура {round(data['main']['temp'] - 273.15,2)} градусов")









# with open('file.pdf','wb') as f:
#     f.write(response.content)
