from fastapi import FastAPI, HTTPException
from models import *

app = FastAPI()
db.connect()

@app.get("/routes/")
async def trains_routes():
    routes_list = []
    for route in Route.select():
        routes_list.append(route.__data__)
    for route in routes_list:
        route['trains'] = []
        for trip in Trip.select().where(Trip.route == route['id']):
            if trip.train:
                route['trains'].append(trip.train)
    return {"routes": routes_list}

@app.get("/stops/")
async def trains_stops():
    stops_list = []
    for stop in Stop.select():
        stops_list.append(stop.__data__),
    return {"stops": stops_list}

@app.get("/stops/{stop_id}")
async def trains_stop_by_id(stop_id: int):
    try:
        stop = Stop.get_by_id(stop_id)
    except Stop.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"stops": stop.__data__}

@app.get("/times/{train}")
async def times_by_train(train: int, date_from: str, date_to: str):
    times_list = []
    for time in Time.select().where(
        (Time.record_date >= date_from) & 
        (Time.record_date <= date_to) & 
        (Time.train == train)):
        times_list.append({
            'train': time.train,
            'record_date': time.record_date,
            'stop': time.stop.__data__,
            'minutes_late': time.minutes_late,
            'scheduled_time_utc': time.scheduled_time_utc,
        })
    return {"times": times_list}
