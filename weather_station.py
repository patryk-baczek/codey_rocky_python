import codey, event, time
import urequests
import ujson

wifi_name = 'BandwidthTogether'
wifi_password = 'U3xBpfxhZFsAdJDp'

api_key = '156a2adfb1e0d934457cd5a010212213'
lat = 49
lon = 22
request_url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'.format(lat, lon, api_key)
current_temperature = 0
current_weather = 'unknown'

def connect_to_wifi():
    global wifi_name, wifi_password
    codey.wifi.start(wifi_name, wifi_password, codey.wifi.STA)
    while True:
        if codey.wifi.is_connected():
            codey.led.show(0, 255, 0)
            display('connected')
            return
        else:
            codey.led.show(255, 0, 0)


def get_weather():
    global request_url, current_temperature
    resp = urequests.get(request_url)
    if resp.status_code < 299:
        result = resp.json()
        main = result['main']
        weather = result['weather'][0]
        current_temperature = round(main['temp'], 0)
        current_weather = weather['main']
        resp.close()
        codey.led.show(0, 255, 21)
        display(str(current_temperature) + 'C' + ',' + 'weather: ' + current_weather )
    else:
        result = resp.json()
        resp.close()
        codey.led.show(255, 0, 0)
        display(result)


def display(text):
    print(text, end=' ')
    codey.display.show(text, wait=False)


connect_to_wifi()
get_weather()
