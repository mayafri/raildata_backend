from peewee import *

db = SqliteDatabase('viarail.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Stop(BaseModel):
    id = IntegerField(primary_key=True)
    code = CharField(unique=True)
    name = CharField()
    lat = CharField()
    lon = CharField()
    timezone = CharField()

class Route(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    color = CharField()

class Trip(BaseModel):
    id = IntegerField(primary_key=True)
    route = ForeignKeyField(Route)
    train = CharField()
    
class Time(BaseModel):
    train = CharField()
    train_departure_time_utc = DateTimeField()
    stop = ForeignKeyField(Stop)
    minutes_late = IntegerField()
    scheduled_time_utc = DateTimeField()

class Shape(BaseModel):
    trip = ForeignKeyField(Trip)
    lat = CharField()
    lon = CharField()

class Schedule(BaseModel):
    trip = ForeignKeyField(Trip)
    arrival_time = TimeField()
    departure_time = TimeField()
    stop = ForeignKeyField(Stop)
    sequence = IntegerField()
