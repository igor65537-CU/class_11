def calc_sum(a, b):
    try:
        return float(a) + float(b)
    except:
        print('Нужно вводить числа')

def calc_dif(a, b):
    try:
        return float(a) - float(b)
    except:
        print('Нужно вводить числа')

def calc_mul(a, b):
    try:
        return float(a) * float(b)
    except:
        print('Нужно вводить числа')

def calc_div(a, b):
    try:
        if float(b) == 0:
            print('Деление на 0')
            return 'Error'
        else:
            return float(a) / float(b)
    except:
        print('Нужно вводить числа')

def dificult_calc(user_input: str):
    supported = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')']
    input_chars = user_input.split()
    for char in input_chars:
        if char not in supported:
            return 'Обнаружены недопустимые символы'
    try:
        return eval(user_input)
    except ZeroDivisionError:
        return 'Деление на 0'

def start_calculator():
    def user_input_processing(user_input):
        if user_input == '1':
            a = input('Число 1:')
            b = input('Число 2:')
            print(calc_sum(a, b))
            return True
        elif user_input == '2':
            a = input('Число 1:')
            b = input('Число 2:')
            print(calc_dif(a, b))
            return True
        elif user_input == '3':
            a = input('Число 1:')
            b = input('Число 2:')
            print(calc_mul(a, b))
            return True
        elif user_input == '4':
            a = input('Число 1:')
            b = input('Число 2:')
            print(calc_div(a, b))
            return True
        elif user_input == '5':
            user_input = input('Введите выражение: ')
            print(dificult_calc(user_input))
        elif user_input == '6':
            return False
  
    working = True
    while working:
        print_menu()
        user_input = input('Действие: ')
        working = user_input_processing(user_input)

def print_menu():
    print('''Выберите действие:
1. Сложение
2. Разность
3. Умножение
4. Деление
5. Выражене
6. Вернуться''')

if __name__ == '__main__':
    start_calculator()

__all__ = ['start_calculator']