#!/usr/bin/env python
import csv, requests, zipfile
from io import BytesIO
from models import *

print('Download GTFS zip file from Via Rail')

r = requests.get('https://www.viarail.ca/sites/all/files/gtfs/viarail.zip')
z = zipfile.ZipFile(BytesIO(r.content))
z.extractall('gtfs/')

db = SqliteDatabase('viarail.sqlite')

print('Drop old data')

db.connect()
db.drop_tables([Stop, Route, Trip])
db.create_tables([Stop, Route, Trip])

# Stations

print('Insert stops')

with open('gtfs/stops.txt') as stops_file:
    csv_reader = csv.reader(stops_file, delimiter=',')
    next(csv_reader)
    for stop in csv_reader:
        id = stop[0]
        code = stop[1]
        name = stop[2]
        lon = stop[4]
        lat = stop[5]
        timezone = stop[6]
        Stop.create(id=id, code=code, name=name, lon=lon, lat=lat, timezone=timezone)

# Routes (lignes)

print('Insert routes')

with open('gtfs/routes.txt') as routes_file:
    csv_reader = csv.reader(routes_file, delimiter=',')
    next(csv_reader)
    for route in csv_reader:
        id = route[0]
        name = route[2]
        color = route[4]
        Route.create(id=id, name=name, color=color)

# Trips ~= « trains » la plupart du temps mais parfois il y a plusieurs trips par train,
# par ex. si le train 26 saute une gare le vendredi, il y aura un trip spécial vendredi.

print('Insert trips')

with open('gtfs/trips.txt') as trips_file:
    csv_reader = csv.reader(trips_file, delimiter=',')
    next(csv_reader)
    for trip in csv_reader:
        route = trip[0]
        id = trip[1]
        train = trip[4]
        Trip.create(route=route, id=id, train=train)

print('Done')