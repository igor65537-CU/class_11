import json, os
import pandas as pd
from datetime import datetime

class TaskManager:
    def __init__(self, local_file='tasks.json'):
        self.local_file = local_file
        self.tasks = self.load_local_tasks()

    def load_local_tasks(self):
        if os.path.exists(self.local_file):
            with open(self.local_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    
    def save_local_tasks(self):
        with open(self.local_file, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)

    def create_task(self, title, description, done=False, priority='', due_date=''):
        task_id = f'task_{len(self.tasks) + 1}'
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'done': done,
            'priority': priority,
            'due_date': due_date,
        }
        self.tasks[task_id] = task
        self.save_local_tasks()
        return task_id
    
    def filter_tasks(self, done='', priority='', due_date=''):
        if done != '':
            self.filtered_tasks = filter(lambda t: done == str(self.tasks[t]['done']), self.tasks)
        else:
           self.filtered_tasks = self.tasks
        if priority != '':
            self.filtered_tasks = filter(lambda t: priority == self.tasks[t]['priority'], self.filtered_tasks)
        if due_date != '':
            self.filtered_tasks = filter(lambda t: due_date == self.tasks[t]['due_date'], self.filtered_tasks)
        self.show_tasks(self, filtered=True)
    
    def show_tasks(self, filtered=False):
        if filtered:
           tasks = self.filtered_tasks
           empty_message = 'Задачи с такими параметрами отсутствуют'
        else:
           tasks = self.tasks
           empty_message = 'Задачи отсутствуют'

        if len(tasks) > 0:
            print('Все задачи:')
            for task in tasks:
                message = f'Заголовок: {tasks[task]['title']}'
                if self.tasks[task]['priority'] != '':
                   message += f', приоритет: {tasks[task]['priority']}'
                if self.tasks[task]['due_date'] != '':
                   message += f', срок: {tasks[task]['due_date']}'
                print(message)
        else:
            print(empty_message)

    def set_task_done(self, task_id):
       if len(self.tasks) > 0:
            for task in self.tasks:
               if self.tasks[task]['id'] == task_id:
                  self.tasks[task]['done'] = True

    def set_priority(self, task_id, priority):
       if len(self.tasks) > 0:
            for task in self.tasks:
               if self.tasks[task]['id'] == task_id:
                  self.tasks[task]['priority'] = priority
       
    def set_due_date(self, task_id, due_date):
       if len(self.tasks) > 0:
            for task in self.tasks:
               if self.tasks[task]['id'] == task_id:
                  self.tasks[task]['due_date'] = due_date

    def change_task(self, task_id, new_title, new_description, is_done, new_priority, due_date):
        if len(self.tasks) > 0:
            for task in self.tasks:
                if self.tasks[task]['id'] == task_id:
                    self.tasks[task]['title'] = new_title
                    self.tasks[task]['description'] = new_description
                    try:
                        self.tasks[task]['done'] = bool(is_done)
                    except:
                       print('СДЕЛАНО: ПОЛЕ БЫЛО ЗАПОЛНЕНО НЕВЕРОНО, ЗНАЧЕНИЕ НЕ ИЗМЕНЕНО')
                    self.tasks[task]['priority'] = new_priority
                    self.tasks[task]['due_date'] = due_date
                    print('Задача изменена')
                    return self.tasks[task]
            print('Задача не найдена')
            return 'not_finded'
        else:
            print('Задачи отсутствуют')

    def delete_task(self, task_id):
        if len(self.tasks) > 0:
            for task in self.tasks:
                if self.tasks[task]['id'] == task_id:
                    self.tasks.remove(task)
                    print('Заметка удалена')
                    return self.tasks[task]
            print('Заметка не найдена')
            return 'not_finded'
        else:
            print('Заметки отсутствуют')

    def import_csv_tasks(self, import_file_name):
        if os.path.exists(f'{import_file_name}.csv'):
            with open(f'{import_file_name}.csv', 'r', encoding='utf-8') as import_file:
                importing = pd.read_csv(import_file)
            for task in importing:
                if importing[task][0] != 'id':
                    title = importing[task][1]
                    description = importing[task][2]
                    done = importing[task][3]
                    priority = importing[task][4]
                    due_date = importing[task][5]
                    self.create_task(title, description, done, priority, due_date)
        else:
           print(f'Файл {import_file_name}.csv не существует')

    def export_csv_tasks(self, export_file_name):
        df = pd.DataFrame(self.tasks)
        df.to_csv(f'{export_file_name}.csv', encoding='utf-8')

def start_task_manager():
  def user_input_processing(user_input):
    manager = TaskManager()
    if user_input == '1':
      print('Создание новой задачи')
      title = input('Введите название задачи: ')
      description = input('Введите описание задачи: ')
      priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
      due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
      task_id = manager.create_task(title, description, priority=priority, due_date=due_date)
      print(f'Сознана задача с id: {task_id}')
      return True
    elif user_input == '2':
      manager.show_tasks()
      return True
    elif user_input == '3':
      print('Фильтры:')
      done = input("Сделано: 'True' или 'False', чтобы пропустить: enter")
      priority = input("Приоритет: 'Высокий', 'Средний', 'Низкий', чтобы пропустить: enter")
      due_date = input("Срок выполнения: 'ДД-ММ-ГГГГ', чтобы пропустить: enter")
      manager.filter_tasks(done, priority, due_date)
      return True
    elif user_input == '4':
      task_id = input('Введите id задачи: ')
      title = input('Название:')
      description = input('Описание: ')
      done = input("Сделано: 'True' или 'False'")
      priority = input("Приоритет: 'Высокий', 'Средний', 'Низкий'")
      due_date = input("Срок выполнения: 'ДД-ММ-ГГГГ'")
      manager.change_task(task_id, title, description, done, priority, due_date)
      return True
    elif user_input == '5':
      task_id = input('Введите id выполненой задачи: ')
      manager.set_task_done(task_id)
      return True
    elif user_input == '6':
      task_id = input('Введите id задачи: ')
      priority = input('Новый приоритет: ')
      manager.set_priority(task_id, priority)
      return True
    elif user_input == '7':
      task_id = input('Введите id задачи: ')
      due_date = input("Новый срок выполнения ('ДД-ММ-ГГГГ'): ")
      manager.set_due_date(task_id, due_date)
      return True
    elif user_input == '8':
      task_id = input('Введите id задачи: ')
      manager.delete_task(task_id)
      return True
    elif user_input == '9':
      import_file = input('Введите файл для импорта: ')
      manager.import_csv_tasks(import_file)
      return True
    elif user_input == '10':
      export_file = input('Введите файл для экспорта: ')
      manager.export_csv_tasks(export_file)
      return True
    elif user_input == '11':
      return False

  print('''Выберите действие:
1. Создать новую задачу
2. Показать список задач
3. Отфильтровать по статусу, приоритету, сроку выполнения
4. Редактировать задачу
5. Отметить задачу выполненой
6. Изменить приоритет
7. Изменить срок задачи
8. Удаление задачи
9. Импорт задач
10. Экспорт задач
11. Вернуться''')
  
  working = True
  while working:
    user_input = input('Действие: ')
    working = user_input_processing(user_input)

if __name__ == '__main__':
  start_task_manager()

__all__ = ['start_task_manager']