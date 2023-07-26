import datetime
import codey, event, time
import urequests
import ujson

hours_of_day = [0, 3, 6, 9, 12, 15, 18, 21]

wifi_name = 'BandwidthTogether'
wifi_password = 'U3xBpfxhZFsAdJDp'

api_key = '156a2adfb1e0d934457cd5a010212213'
lat = 50.041321
lon = 21.99901
request_url = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric'.format(lat, lon, api_key)
current_temperature = 0
current_weather = 'unknown'

index = 0
selected_hours = 0

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
@event.button_c_pressed
def choose_hours_of_day():
    global index
    selected_hours = hours_of_day[index]
    display(selected_hours)
    next_index = index + 1
    if next_index < len(hours_of_day):
       index = next_index

    else:
        index = 0
@event.button_b_pressed
def get_weather():
    global request_url, current_temperature, selected_hours, current_weather
    resp = urequests.get(request_url)
    if resp.status_code < 299:
        result = resp.json()
        today_date = datetime.date.today()
        year = today_date.year
        month = today_date.month
        day = today_date.day
        weather_date_time = year + '-' + month + '-' + day + ' ' +selected_hours + ':00.00'
        weather_entry = None
        for entry in result['list']:
            if entry['dt_txt'] == weather_date_time:
                weather_entry = entry
                break

        main = weather_entry['main']
        weather = weather_entry['weather'][0]
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

