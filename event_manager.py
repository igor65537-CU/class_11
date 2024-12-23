class EventManager:
  def __init__(self, local_file='events.json'):
    self.local_file = local_file
    self.events = self.load_local_events()

  def load_local_events(self):
    if os.path.exists(self.local_file):
      with open(self.local_file, 'r', encoding='utf-8') as file:
        return json.load(file)
    return {}

  def save_local_event(self):
    with open(self.local_file, 'w', encoding='utf-8') as file:
      json.dump(self.events, file, indent=4, ensure_ascii=False)

  def create_event(self, name, date, time):
    event_id = f'event_{len(self.events) + 1}'
    event = {
        'event_id': event_id,
        'name': name,
        'date': date,
        'time': time,
        'reminders': []
    }
    self.events[event_id] = event
    self.save_local_event()
    print(f'Событие {name} было создано с ID {event_id}')

  def get_holidays(self, country, year):
    url = f'{self.base_url}/holidays'
    params = {
        'api_key': self.api_key,
        'country': country,
        'year': year
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
      holidays = response.json()['response']['holidays']
      for holiday in holidays:
        name = holiday['name']
        date = holiday['date']['iso']
        self.create_event(name=name, date=date, time='00:00')
      print('Празднии были добавлены')
    else:
      print('Не удалось получить праздники')

  def add_reminder(self, event_id, reminder_time):
    if event_id in self.events:
      self.events[event_id]['reminders'].append(reminder_time)
      self.save_local_event()
      print(f'Напоминание на {reminder_time} для {event_id} было добавлено')
    else:
      print('Событие с таким ID не было найдено')