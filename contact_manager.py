import json, os
import pandas as pd

class ContactManager:
    def __init__(self, local_file='contacts.json'):
        self.local_file = local_file
        self.contacts = self.load_local_contacts()

    def load_local_contacts(self):
        if os.path.exists(self.local_file):
            with open(self.local_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    
    def save_local_contacts(self):
        with open(self.local_file, 'w', encoding='utf-8') as file:
            json.dump(self.contacts, file, indent=4, ensure_ascii=False)

    def create_contact(self, name, phone='', email=''):
        contact_id = f'contact_{len(self.contacts) + 1}'
        contact = {
            'id': contact_id,
            'name': name,
            'phone': phone,
            'email': email,
        }
        self.contacts[contact_id] = contact
        self.save_local_contacts()
        return contact_id
    
    def find_contact(self, name='', phone=''):
        if name == '' and phone == '':
            print('Нет параметров для поиска')
        elif name != '':
           for contact in self.contacts:
              if self.contacts[contact]['name'] == name:
                self.show_contact(contact)
                return 'ok'
           print('Контакт не найден')
        else:
           for contact in self.contacts:
              if self.contacts[contact]['phone'] == phone:
                self.show_contact(contact)
                return 'ok'
           print('Контакт не найден')
    
    def show_contact(self, contact):
        message = f'id: {self.contacts[contact]['id']}, Имя: {self.contacts[contact]['name']}'
        if self.contacts[contact]['phone'] != '':
            message += f', номер телефона: {self.contacts[contact]['phone']}'
        if self.contacts[contact]['email'] != '':
            message += f', email: {self.contacts[contact]['email']}'
        print(message)

    def show_contacts(self):
        if len(self.contacts) > 0:
            print('Все контакты:')
            for contact in self.contacts:
                self.show_contact(contact)
        else:
            print('Контакты отсутствуют')

    def redact_contact(self, contact_id, name='', phone='', email=''):
        if len(self.contacts) > 0:
            for contact in self.contacts:
                if self.contacts[contact]['id'] == contact_id:
                    if name != '':
                        self.contacts[contact]['name'] = name
                    if phone != '':
                        self.contacts[contact]['phone'] = phone
                    if email != '':
                        self.contacts[contact]['email'] = email
                    print('Контакт изменен')
                    return self.contacts[contact]
            print('Контакт не найден')
            return 'not_finded'
        else:
            print('Задачи отсутствуют')

    def delete_contact(self, contact_id):
        if len(self.contacts) > 0:
            for contact in self.contacts:
                if self.contacts[contact]['id'] == contact_id:
                    self.contacts.remove(contact)
                    print('Контакт удален')
                    return self.contacts[contact]
            print('Контакт не найден')
            return 'not_finded'
        else:
            print('Контакты отсутствуют')

    def import_csv_contacts(self, import_file_name):
        if os.path.exists(f'{import_file_name}.csv'):
            with open(f'{import_file_name}.csv', 'r', encoding='utf-8') as import_file:
                importing = pd.read_csv(import_file)
            for contact in importing:
                if importing[contact][0] != 'id':
                    name = importing[contact][1]
                    phone = importing[contact][2]
                    email = importing[contact][3]
                    self.create_contact(name, phone, email)

    def export_csv_contacts(self, export_file_name):
        df = pd.DataFrame(self.contacts)
        df.to_csv(f'{export_file_name}.csv', encoding='utf-8')

def start_contact_manager():
  def user_input_processing(user_input):
    manager = ContactManager()
    if user_input == '1':
      print('Создание нового контакта')
      name = input('Введите имя: ')
      phone = input('Введите телефон(enter чтобы пропустить): ')
      email = input('Введите email(enter чтобы пропустить): ')
      manager.create_contact(name, phone, email)
      return True
    elif user_input == '2':
      manager.show_contacts()
      return True
    elif user_input == '3':
      name = input("Введите имя (чтобы пропустить: enter): ")
      phone = input("Введите телефон (чтобы пропустить: enter): ")
      manager.find_contact(name, phone)
      return True
    elif user_input == '4':
      contact_id = input('Введите id контакта: ')
      name = input('Новое имя (чтобы пропустить: enter): ')
      phone = input('Новый телефон (чтобы пропустить: enter): ')
      email = input("Новый email (чтобы пропустить: enter): ")
      manager.redact_contact(contact_id, name, phone, email)
      return True
    elif user_input == '5':
      contact_id = input('Введите id контакта: ')
      manager.delete_contact(contact_id)
      return True
    elif user_input == '6':
      import_file = input('Введите файл для импорта: ')
      manager.import_csv_contacts(import_file)
      return True
    elif user_input == '7':
      export_file = input('Введите файл для экспорта: ')
      manager.export_csv_contacts(export_file)
      return True
    elif user_input == '8':
      return False

  print('''Выберите действие:
1. Создать новый контакт
2. Показать список контактов
3. Поиск по имени или телефону
4. Редактировать контакт
5. Удалить контакт
6. Импорт контактов
7. Экспорт контактов
8. Вернуться''')
  
  working = True
  while working:
    user_input = input('Действие: ')
    working = user_input_processing(user_input)

if __name__ == '__main__':
  start_contact_manager()

__all__ = ['start_contact_manager']