from datetime import datetime
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Toilet(BaseModel):
    room: str
    available: int

client = MongoClient('mongodb://localhost', 27017)
db = client["toilet"]

app = FastAPI()

@app.get("/")
def start():
    return {"status": "OK"}

# @app.post('/toilet/testpost')
# def update_1(toilet: Toilet):
#     t = jsonable_encoder(toilet)
#     if t['available'] == 1:
#         db[t['room']].insert_one("room":t['room'],
#                 {"time":datetime.now()}, "totaltime":0, "")

@app.put('/toilet')
def update_1(toilet: Toilet):
    t = jsonable_encoder(toilet)
    if t['available'] == 1:
        db[t['room']].update_one({"room":t['room']},{"$set":{"time":datetime.now()}})
        return {'status':'Done1'}    
    
    r = db[t['room']].find_one()
    a = r['amount']
    time = (datetime.now() - r['time']).total_seconds()
    if t['available'] == 0:
        db[t['room']].update_one({"room":t['room']},{"$set":{"amount":a+1,"totaltime":r['totaltime']+time}})
        return {'status':'Done0'}

@app.get('/estimate')
def get_estimate():
    # return {}
    ans = {
        '1': 0,
        '2': 0,
        '3': 0
    }
    for i in range(1,4):
        r = db[str(i)].find_one()
        if r['amount'] == 0:
            continue
        else :
            ans[str(i)] = r['totaltime']/r['amount']
    return {'estimate': ans}
    



    