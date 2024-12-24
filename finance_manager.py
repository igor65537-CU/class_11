import json, os
import pandas as pd
from datetime import datetime

class FinanceManager:
    def __init__(self, local_file='finance.json'):
        self.local_file = local_file
        self.records = self.load_local_records()

    def load_local_records(self):
        if os.path.exists(self.local_file):
            with open(self.local_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    
    def save_local_records(self):
        with open(self.local_file, 'w', encoding='utf-8') as file:
            json.dump(self.records, file, indent=4, ensure_ascii=False)

    def create_record(self, amount, category='', date='', description=''):
        record_id = f'record_{len(self.records) + 1}'
        contact = {
            'id': record_id,
            'amount': amount,
            'category': category,
            'date': date,
            'description': description,
        }
        self.records[record_id] = contact
        self.save_local_records()
        return record_id

    def show_records(self, date_filter='', category_filter=''):
        self.filter_records(date_filter, category_filter)
        if len(self.records) > 0:
            print('Все операции после фильтрации:')
            records = self.filtered_records
            if len(records) > 0:
                for record in records:
                    self.show_record(record)
            else:
               print('Операции с заданными параметрами отсутствуют')
        else:
            print('Операции отсутствуют')

    def filter_records(self, date_filter='', category_filter=''):
        if date_filter != '':
            self.filtered_records = filter(lambda r: date_filter == self.records[r]['date'], self.records)
        else:
           self.filtered_records = self.records
        if category_filter != '':
            self.filtered_records = filter(lambda r: category_filter == self.records[r]['category'], self.filtered_records)

    def create_report(self, start_date, end_date):
        income = []
        income_categoty = []
        expense = []
        expense_categoty = []
        start_stamp = datetime.strptime(start_date, "%d-%m-%Y").timestamp()
        end_stamp = datetime.strptime(end_date, "%d-%m-%Y").timestamp()
        for record in self.records:
            record_date = self.records[record]['date']
            record_stamp = datetime.strptime(record_date, "%d-%m-%Y").timestamp()
            if (record_stamp >= start_stamp) and (record_stamp <= end_stamp):
                if self.records[record]['amount'] > 0:
                   income.append(self.records[record]['amount'])
                   income_categoty.append(self.records[record]['category'])
                else:
                   expense.append(self.records[record]['amount'] * -1)
                   expense_categoty.append(self.records[record]['category'])
        report_file = f'report_{start_date}_{end_date}.csv'
        with open(report_file, 'w') as f:
           report = pd.DataFrame({'income': income,
                                  'income_category': income_categoty,
                                  'expense': expense,
                                  'expence_category': expense_categoty})
           report.to_csv(f, encoding='utf-8')
        print(f'Финансовый отчёт за период с {start_date} по {end_date}:')
        print(f'- Общий доход: {sum(income)} руб.')
        print(f'- Общие расходы: {sum(expense)} руб.')
        print(f'- Баланс: {sum(income) - sum(expense)} руб.')
        print(f'Подробная информация сохранена в файле {report_file}')

    def summary_balance(self):
        balance = 0
        for record in self.records:
            balance += self.records[record]['amount']
        print(f'Общий баланс: {balance}')
    
    def show_record(self, record):
       print(f'id: {self.records[record]['id']}, сумма: {self.records[record]['amount']}')

    def group_finance(self, category):
       print(f'Группировка по категории {category}')
       for record in self.records:
          if self.records[record]['category'] == category:
             self.show_record(record)

    def import_csv_records(self, import_file_name):
        if os.path.exists(f'{import_file_name}.csv'):
            with open(f'{import_file_name}.csv', 'r', encoding='utf-8') as import_file:
                importing = pd.read_csv(import_file)
            for record in importing:
                if importing[record][0] != 'id':
                    amount = importing[record][1]
                    category = importing[record][2]
                    date = importing[record][3]
                    description = importing[record][4]
                    self.create_record(amount, category, date, description)
        else:
           print(f'Файл {import_file_name}.csv не существует')

    def export_csv_records(self, export_file_name):
        df = pd.DataFrame(self.records)
        df.to_csv(f'{export_file_name}.csv', encoding='utf-8')

def start_finance_manager():
  def user_input_processing(user_input):
    manager = FinanceManager()
    if user_input == '1':
      print('Создание новой записи')
      amount = float(input('Введити сумму операции (положительное число для доходов, отрицательное для расходов):'))
      category = input('Введите категорию операции: ')
      date = input('Введите дату операции(ДД-ММ-ГГГГ): ')
      description = input('Введите описание(enter, чтобы пропустить): ')
      manager.create_record(amount, category, date, description)
      return True
    elif user_input == '2':
      date_filter = input('Введите дату для фильтрации(enter, чтобы пропустить): ')
      category_filter = input('Введите категорию для фильтрации(enter, чтобы пропустить): ')
      manager.show_records(date_filter, category_filter)
      return True
    elif user_input == '3':
      start_date = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
      end_date = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
      manager.create_report(start_date, end_date)
      return True
    elif user_input == '4':
      manager.summary_balance()
      return True
    elif user_input == '5':
      category = input('Введите категорию для группировки: ')
      manager.group_finance(category)
      return True
    elif user_input == '6':
      import_file_name = input('Файл для импорта: ')
      manager.import_csv_records(import_file_name)
      return True
    elif user_input == '7':
      export_file_name = input('Файл для экспорта: ')
      manager.export_csv_records(export_file_name)
      return True
    elif user_input == '8':
      return False
  
  working = True
  while working:
    print_menu()
    user_input = input('Действие: ')
    working = user_input_processing(user_input)

def print_menu():
   print('''Выберите действие:
1. Создать новую финансовую запись
2. Показать список финансовых записей
3. Сгенирировать отчет
4. Подсчет общего баланса
5. Группировка расходов и доходов по категориям
6. Импорт финансовых записей
7. Экспорт финансовых записей
8. Вернуться''')

if __name__ == '__main__':
  start_finance_manager()

__all__ = ['start_finance_manager']