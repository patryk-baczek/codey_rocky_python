import codey
import event

list_grades = []
selected_grades = 1


@event.button_c_pressed
def input_grades():
    global selected_grades
    selected_grades = selected_grades + 1
    reset_grades()
    print(str(selected_grades))


@event.button_a_pressed
def add_to_final_grades():
    global selected_grades
    codey.display.show(selected_grades)
    list_grades.append(selected_grades)
    selected_grades = 1


@event.button_b_pressed
def final_result():
    operation = len(list_grades)
    sum = 0
    for grades in list_grades:
       sum = sum + grades
    result = sum / operation
    display('your avg:'+str(result))


def reset_grades():
    global selected_grades
    if selected_grades == 7:
        selected_grades = 0


def display(text):
    print(text, end=' ')
    codey.display.show(text, wait=False)

