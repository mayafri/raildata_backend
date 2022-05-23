from peewee import *
from datetime import date

db = SqliteDatabase('viarail.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Stop(BaseModel):
    id = IntegerField(primary_key=True)
    code = CharField(unique=True)
    name = CharField()
    lon = CharField()
    lat = CharField()
    timezone = CharField()

class Route(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    color = CharField()

class Trip(BaseModel):
    id = IntegerField(primary_key=True)
    route = ForeignKeyField(Route)
    train = IntegerField()
    
class Time(BaseModel):
    train = IntegerField()
    record_date = DateField(default=date.today())
    stop = ForeignKeyField(Stop)
    minutes_late = IntegerField()
    scheduled_time_utc = DateTimeField()