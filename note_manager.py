import json, os
import pandas as pd
from datetime import datetime

class NoteManager:
  def __init__(self, local_file='notes.json'):
    self.local_file = local_file
    self.notes = self.load_local_notes()

  def load_local_notes(self):
    if os.path.exists(self.local_file):
      with open(self.local_file, 'r', encoding='utf-8') as file:
        return json.load(file)
    return {}

  def save_local_note(self):
    with open(self.local_file, 'w', encoding='utf-8') as file:
      json.dump(self.notes, file, indent=4, ensure_ascii=False)

  def get_timestamp(self):
    now = datetime.now()
    return f'{now.day}-{now.month}-{now.year} {now.hour}:{now.minute}:{now.second}'
  
  def set_timestamp(self, note_id, timestamp):
    for note in self.notes:
        if note['id'] == note_id:
          note['timestamp'] = timestamp
          return 'ok'
    return 'not_finded'
  
  def create_note(self, title, content):
    note_id = f'note_{len(self.notes) + 1}'
    note = {
        'id': note_id,
        'title': title,
        'content': content,
        'timestamp': self.get_timestamp(),
    }
    self.notes[note_id] = note
    self.save_local_note()
    return note_id

  def show_notes(self):
    if len(self.notes) > 0:
      print('Все заметки:')
      for note in self.notes:
        print(f'Заголовок: {self.notes[note]['title']}, id: {self.notes[note]['id']}')
    else:
      print('Заметки отсутствуют')

  def return_note_by_id(self, note_id):
    if len(self.notes) > 0:
      for note in self.notes:
        if self.notes[note]['id'] == note_id:
          print(f'id: {note_id}')
          print(f'Название: {self.notes[note]['title']}')
          print(f'Содержание: {self.notes[note]['content']}')
          print(f'Последнее изменение: {self.notes[note]['timestamp']}')
          return self.notes[note]
      print('Заметка не найдена')
      return 'not_finded'
    else:
      print('Заметки отсутствуют')

  def change_note(self, note_id, new_title, new_content):
    if len(self.notes) > 0:
      for note in self.notes:
        if self.notes[note]['id'] == note_id:
          self.notes[note]['title'] = new_title
          self.notes[note]['content'] = new_content
          self.notes[note]['timestamp'] = self.get_timestamp()
          print('Заметка изменена')
          return self.notes[note]
      print('Заметка не найдена')
      return 'not_finded'
    else:
      print('Заметки отсутствуют')

  def delete_note(self, note_id):
    if len(self.notes) > 0:
      for note in self.notes:
        if self.notes[note]['id'] == note_id:
          self.notes.remove(note)
          print('Заметка удалена')
          return self.notes[note]
      print('Заметка не найдена')
      return 'not_finded'
    else:
      print('Заметки отсутствуют')

  def import_csv_notes(self, import_file_name):
    if os.path.exists(f'{import_file_name}.csv'):
      with open(f'{import_file_name}.csv', 'r', encoding='utf-8') as import_file:
        importing = pd.read_csv(import_file)
        for note in importing:
            if importing[note][0] != 'id':
                imported_note_id = self.create_note(importing[note][1], importing[note][2])
                self.set_timestamp(imported_note_id, importing[note][3])
    else:
           print(f'Файл {import_file_name}.csv не существует')

  def export_csv_notes(self, export_file_name):
    df = pd.DataFrame(self.notes)
    df.to_csv(f'{export_file_name}.csv', encoding='utf-8')

def start_note_manager():
  def user_input_processing(user_input):
    manager = NoteManager()
    if user_input == '1':
      print('Создание новой заметки')
      title = input('Введите заголовок: ')
      content = input('Введите содержимое: ')
      note_id = manager.create_note(title, content)
      print(f'Сознана заметка с id: {note_id}')
      return True
    elif user_input == '2':
      manager.show_notes()
      return True
    elif user_input == '3':
      note_id = input('Введите id для подробностей: ')
      manager.return_note_by_id(note_id)
      return True
    elif user_input == '4':
      note_id = input('Введите id для подробностей: ')
      title = input('Введите новый заголовок')
      content = input('Введите новое наполнение')
      manager.change_note(note_id, title, content)
      return True
    elif user_input == '5':
      note_id = input('Введите id для удаления: ')
      manager.delete_note(note_id)
      return True
    elif user_input == '6':
      import_file_name = input('Путь до файла импорта: ')
      manager.import_csv_notes(import_file_name)
      return True
    elif user_input == '7':
      export_file_name = input('Название файла для экспорта: ')
      manager.export_csv_notes(export_file_name)
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
1. Создать новую заметку
2. Показать список заметок
3. Просмотр подробностей заметки
4. Редактирование заметки
5. Удаление заметки
6. Импорт заметок
7. Экспорт заметок
8. Вернуться''')

if __name__ == '__main__':
  start_note_manager()

__all__ = ['start_note_manager']