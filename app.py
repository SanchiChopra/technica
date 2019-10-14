from math import radians, cos, sin, asin, sqrt
from flask import Flask, request, jsonify, redirect
from flask import g
from cs50 import SQL
import requests
import time
import json

db = SQL("sqlite:///database.db")
app = Flask("__main__")

def haversine(lng1, lat1, lng2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """ 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    # haversine formula 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers: 6371
    km = 6371* c
    return km

@app.route('/add')
def hello_world():
        arr = [{'lat':"12.97298323", 'lng':"79.16381103", 'voltage':"medium"},{'lat':"12.97297611", 'lng':"79.16380391", 'voltage':"medium"}]
        for i in arr:

                db.execute("INSERT INTO pole VALUES(:lat, :lng, :volt)", lat=i["lat"], lng=i["lng"], volt=i["voltage"])
        
        return "Added"

@app.route("/delete")
def del_hello():
        db.execute("DELETE FROM pole")
        return "Deleted!"


@app.route('/api', methods=['POST'])
def add_message():
    content = request.json
    arr = content["boundaries"]
    central = content["central"]
    defaulter={}
    for i in arr:
           j = haversine(central["lat"], central["lng"], i["lat"], i["lng"])
           if j > 1.2/1000:
                   defaulter['lat']=i['lat']
                   defaulter['lng']=i['lng']
                   break
    print(defaulter)
    data = {"lat":str(defaulter["lat"]), "lng":str(defaulter["lng"]), "time": str(time.time()), "id":"1"}
    res = requests.post("http://139.59.23.108:3000/api/v1/client/create", data=json.dumps(data), headers={"Content-Type":"application/json"})
    return str(res.text)
    



@app.route('/view')
def show_hw():
        c = db.execute("select * from pole")
        print(c)
        return str(c)


if __name__ == '__main__':
    app.run(debug=True)
