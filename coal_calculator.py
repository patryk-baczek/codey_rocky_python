import codey
import event

price = 1400
number_of_tons = 0

@event.button_c_pressed
def choose_number_of_tons():
    global number_of_tons
    number_of_tons = number_of_tons +1
    display(str(number_of_tons) + ' tons')
@event.button_b_pressed
def calculation():
    if number_of_tons == 0:
        display('first choose how much coal you want to buy')
        return
    else:
        total_price = number_of_tons * price
        display('totalprice ' + str(total_price))

def display(text):
    print(text, end=' ')
    codey.display.show(text, wait=False)