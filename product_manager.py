import random
import time

import codey
import event


class Product:
    def __init__(self, name, location, price):
        self.name = name
        self.location = location
        self.price = price
        self.quantity = 1


available_products = [Product('milk', 'aisle 2', 3.50), Product('eggs', 'aisle 4', 5.50)]
shopping_list = []

shopping_mode = 0
current_displayed_product_index = 0
current_displayed_shopping_product_index = 0


def display_products():
    global available_products
    for product in available_products:
        time.sleep(1)
        display(product.name)


def add_to_shopping_list():
    global shopping_list, current_displayed_product_index, available_products
    selected_product = available_products[current_displayed_product_index - 1]
    shopping_list.append(selected_product)
    print(shopping_list)


def display_shopping_list():
    global shopping_list
    for product in shopping_list:
        display(product.name)
        time.sleep(2)


def get_random_product_of_the_day():
    global shopping_list
    random_product_index = random.randint(0, len(available_products) - 1)
    random_product = available_products[random_product_index]
    random_product_text = "product of the day: " + random_product.name
    display(random_product_text)


def toggle_shopping_mode():
    global shopping_mode

    if shopping_mode == 1:
        display('home mode')
        shopping_mode = 0

    else:
        turn_on_shopping_mode()

@event.button_c_pressed
def turn_on_shopping_mode():
    global shopping_mode
    shopping_mode = 1
    display('shopping mode')
    time.sleep(2)
    shopping_costs = 0
    for product in shopping_list:
        shopping_costs = shopping_costs + product.price

    display('shopping costs: ' + str(shopping_costs) + ' PLN')


@event.button_b_pressed
def when_b_button_pressed():
    if shopping_mode == 0:
        next_product()

    else:
        next_shopping_product()


@event.button_a_pressed
def when_a_button_pressed():
    if shopping_mode == 0:
        add_to_shopping_list()

    else:
        remove_from_shopping_list()


def remove_from_shopping_list():
    selected_product = shopping_list[current_displayed_shopping_product_index - 1]
    shopping_list.remove(selected_product)
    product_count = len(shopping_list)
    if product_count == 0:
        display('all planned products have been purchased')


def next_shopping_product():
    global shopping_list, current_displayed_shopping_product_index
    product_count = len(shopping_list)

    if product_count == 0:
        display('no shopping list, switch to home mode and select products.')
        return

    selected_product = shopping_list[current_displayed_shopping_product_index]
    display(selected_product.name)

    next_index = current_displayed_shopping_product_index + 1
    print(product_count)
    if next_index < product_count:
        current_displayed_shopping_product_index = next_index
    else:
        current_displayed_shopping_product_index = 0


def next_product():
    global available_products, current_displayed_product_index
    selected_product = available_products[current_displayed_product_index]
    display(selected_product.name)

    next_index = current_displayed_product_index + 1
    product_count = len(available_products)
    print(product_count)
    if next_index < product_count:
        current_displayed_product_index = next_index
    else:
        current_displayed_product_index = 0



def increase_quantity():
    global available_products, current_displayed_product_index
    selected_product = available_products[current_displayed_product_index]
    selected_product.quantity = selected_product.quantity + 1
    display('amount of product increased' + str(selected_product.quantity) + ' ' + selected_product.name)


def display(text):
    print(text, end=' ')
    codey.display.show(text, wait=False)


get_random_product_of_the_day()
