from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/times/{trains}")
async def times_by_train(trains: str, departure_time_from: str, departure_time_to: str):
    # On peut donner un n° train ou plusieurs séparés par virgules
    times_list = []
    for time in Time.select().where(
        (Time.train_departure_time_utc >= departure_time_from) & 
        (Time.train_departure_time_utc <= departure_time_to) & 
        (Time.train.in_(trains.split(',')))):
        times_list.append({
            'train': time.train,
            'train_departure_time_utc': time.train_departure_time_utc,
            'stop': time.stop.__data__,
            'minutes_late': time.minutes_late,
            'scheduled_time_utc': time.scheduled_time_utc,
        })
    return {"times": times_list}

async def get_trips_for_train(trains_list):
    trips_ids_list = []
    for trip in Trip.select().where(Trip.train.in_(trains_list)):
        trips_ids_list.append(trip.id)
    return trips_ids_list

@app.get("/shapes/{trains}")
async def shapes_by_train(trains: str):
    trips = await get_trips_for_train(trains.split(','))
    shapes_list = []
    for shape in Shape.select().where(Shape.trip.in_(trips)):
        shapes_list.append(shape.__data__)
    return {"shapes": shapes_list}

@app.get("/schedules/{trains}")
async def schedules_by_train(trains: str):
    trips = await get_trips_for_train(trains.split(','))
    schedules_list = []
    for schedule in Schedule.select().where(Schedule.trip.in_(trips)):
        schedules_list.append(schedule.__data__)
    return {"shapes": schedules_list}
