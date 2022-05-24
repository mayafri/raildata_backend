#!/usr/bin/env python
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
            train_departure_time = str_to_datetime(train_data['times'][0]['scheduled']),
            for stop in train_data['times']:
                real_time = str_to_datetime(stop['estimated'])
                scheduled_time = str_to_datetime(stop['scheduled'])
                minutes_late = get_minutes_late(scheduled_time, real_time)
                Time.get_or_create( # Crée l'entrée si elle n'existe pas, ça évite les doublons
                    train=train_number,
                    record_date=date.today(),
                    train_departure_time_utc=train_departure_time,
                    stop=Stop.get(code=stop['code']),
                    minutes_late=minutes_late,
                    scheduled_time_utc=scheduled_time
                )
