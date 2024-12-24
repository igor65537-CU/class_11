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

def start_calculator():
    print('''Выберите действие:
1. Сложение
2. Разность
3. Умножение
4. Деление
5. Вернуться''')
    
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
            return False
  
    working = True
    while working:
        user_input = input('Действие: ')
        working = user_input_processing(user_input)

if __name__ == '__main__':
    start_calculator()

__all__ = ['start_calculator']