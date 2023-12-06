import json
import urequests as requests
import codey
import rocky
import time
import event
import ujson

frends_emails = ["YOUR FRIEND EMAIL"]

WIFI_NAME = 'WIFI NAME'
WIFI_PASSWORD = 'WIFI PASSWORD'

base_url = 'YOUR BASE URL'

def connect_to_wifi():
    codey.wifi.start(WIFI_NAME, WIFI_PASSWORD, codey.wifi.STA)
    while True:
        if codey.wifi.is_connected():
            codey.led.show(0, 255, 0)
            codey.emotion.smile()
            return
        else:
            codey.emotion.zzz()
            codey.led.show(255, 0, 0)

@event.greater_than(5 , "timer")
def check_if_any_emails():
    codey.reset_timer()
    request_url = base_url + "/emails/any-unread"
    resp = requests.get(url = request_url)
    print(resp.text)
    print(resp.status_code)
    if resp.status_code < 299:
        print(resp.text)
        result = json.loads(resp.text)
        hasAnyEmails = result["hasEmail"]
        if hasAnyEmails == True:
            subject = result["subject"]
            email_text = result["emailText"]
            if subject.lower == "zadanie domowe":
                schedule_reminder_homework(email_text)
            else:
                ask_ai_email_feeling(subject, email_text)
                email_from_friend = check_email_is_from_friend(result)
                notify_user_about_email(subject, email_from_friend)
        else:
            print("mail box empty")
            codey.emotion.blink()
            return
        print('success')
    else:
        print("error")

def check_email_is_from_friend(result):
    email_from = result["from"]
    email_from_friend = False

    for email in frends_emails:
                if email_from == email:
                    email_from_friend = True

def display(text):
    print(text, end=' ')
    codey.display.show(text, wait=True)

def notify_user_about_email(text, email_from_friend):
    notificiation_text = text
    if email_from_friend == True:
        notificiation_text = "email from friend! text:" + notificiation_text
    codey.emotion.wow()
    codey.emotion.smile()
    display(notificiation_text)
    time.sleep(5)
    codey.display.clear()

@event.button_c_pressed
def mark_as_read():
    print("marking emails as read")
    request_url = base_url + "/emails/mark-as-read"
    resp = requests.delete(url = request_url)
    if resp.status_code < 299:
        codey.emotion.yes()
        print(resp.text)
    else:
         print("error")

def ask_ai_email_feeling(subject, email_text):
    request_url = base_url + "/ai/ask"
    post_data = ujson.dumps({'title': subject, 'emailText': email_text})
    print(post_data)
    resp = requests.post(request_url, headers={'content-type': 'application/json'}, data = post_data)
    if resp.status_code < 299:
        print("checking feelings")
        print(resp.text)
        result = json.loads(resp.text)
        ai_response = result["content"].lower()
        happy = "happy" in ai_response
        angry = "angry" in ai_response
        if happy == True:
            codey.emotion.smile()
        elif angry == True:
            codey.emotion.angry()
        else:
            codey.emotion.sad()
    else:
        print("error")


def schedule_reminder_homework(email_text):
     index = email_text.find("na")
     starting_date_index = index +2
     ending_date_index = starting_date_index +10
     data_as_string = email_text[starting_date_index:ending_date_index]

connect_to_wifi()
