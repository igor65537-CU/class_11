from note_manager import *

def start():
    print('''Добро пожаловать в Персональный помощник!
Выберите действие:
1. Управление заметками
2. Управление задачами
3. Управление контактами
4. Управление финансовыми записями
5. Калькулятор
6. Выход''')
    working = True
    while working:
        user_input = input('Действие: ')
        working = input_processing(user_input)

def input_processing(user_input):
    if user_input == '1':
        start_note_manager()
        return True
    elif user_input == '2':
        return True
    elif user_input == '3':
        return True
    elif user_input == '4':
        return True
    elif user_input == '5':
        return True
    elif user_input == '6':
        return False

if __name__ == '__main__':
    start()