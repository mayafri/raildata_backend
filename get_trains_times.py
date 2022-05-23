import requests, datetime
from models import *

def str_to_datetime(string_utc):
    return datetime.datetime.strptime(string_utc, '%Y-%m-%dT%H:%M:%SZ')

def get_minutes_late(datetime_scheduled, datetime_real):
    diff =  datetime_real - datetime_scheduled
    minutes_late = int(diff.total_seconds()//60)
    return minutes_late if minutes_late > 0 else 0

db.connect()
db.create_tables([Time])

r = requests.get('https://tsimobile.viarail.ca/data/allData.json')
if r.status_code == 200:
    for i in r.json().items():
        train_number = i[0].split()[0]
        train_data = i[1]
        if train_data['arrived']:
            train_dict = {}
            for stop in train_data['times']:
                time_real = str_to_datetime(stop['estimated'])
                time_scheduled = str_to_datetime(stop['scheduled'])
                minutes_late = get_minutes_late(time_scheduled, time_real)
                Time.get_or_create( # Crée l'entrée si elle n'existe pas, ça évite les doublons
                    train=train_number,
                    record_date=date.today(),
                    stop=Stop.get(code=stop['code']),
                    minutes_late=minutes_late,
                    scheduled_time_utc=time_scheduled
                )
