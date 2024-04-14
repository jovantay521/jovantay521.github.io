from flask import Flask, render_template, request, jsonify
from backends.login import loginBp
from backends.signup import signupBp
from backends.busExplorer import busExplorerBp
import secrets
from datetime import datetime
import requests

app = Flask(__name__)

#Register each page of the website as blueprint
app.register_blueprint(loginBp)
app.register_blueprint(signupBp)
app.register_blueprint(busExplorerBp)

@app.route("/", methods =['GET'])
@app.route("/route-planner", methods=['GET'])
def home():
    app.secret_key = secrets.token_hex(16) #Creates a session key.
    return render_template('route-planner.html')


def displayDriveInfo(data):
    routeSteps = [[], [], []]
    counter=0
    for routeData in data:
        for directions in routeData:
            routeSteps[counter].append("In "+ directions[5]+ "\n" +directions[9])
        counter+=1

    return render_template('route-planner.html', route1Steps=routeSteps[0], route2Steps=routeSteps[1], route3Steps=routeSteps[2]) #rendering an empty array will not have any effect

def displayPTInfo(data):
    routeSteps=[[], [], []]
    counter =0
    for itenary in data: #each itenary is an object containing 1 route data
        route = itenary["legs"] # list of steps for the route
        for routeData in route: #for each step of the route
            if routeData["mode"] == "WALK":
                for step in routeData["steps"]:
                    routeSteps[counter].append(f"Head {step['absoluteDirection']} {step['distance']}m to {routeData['to']['name']}")
                continue
            elif routeData["mode"] == "BUS" or routeData["mode"] == "SUBWAY":
                routeSteps[counter].append(f"Board {routeData['routeLongName']} from {routeData['from']['name']} for {routeData['to']['stopSequence']-routeData['from']['stopSequence']} stops to {routeData['to']['name']}")
                continue
        counter+=1
    return render_template("route-planner.html", route1Steps=routeSteps[0], route2Steps=routeSteps[1], route3Steps=routeSteps[2])

@app.route("/route-planner", methods=['POST'])
def cal_route():
    start = request.form['start']
    end = request.form['end']
    routeType = request.form['type']

    start_url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={start}&returnGeom=Y&getAddrDetails=Y"
    end_url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={end}&returnGeom=Y&getAddrDetails=Y"

    start_response = requests.request("GET", start_url)
    end_response = requests.request("GET", end_url)
    start_response = start_response.json()
    end_response = end_response.json()

    start_lat = start_response['results'][0]['LATITUDE']
    start_long = start_response['results'][0]['LONGITUDE']

    end_lat = end_response['results'][0]['LATITUDE']
    end_long = end_response['results'][0]['LONGITUDE']

    #routeType = "pt" #to be changed later when receive input from form
    mode = "TRANSIT" #to be in caps as per required by api

    now =datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    datetime_list =now.split(" ")
    date = datetime_list[0]
    time= datetime_list[1]
    if time[:5]>"00:00" and time[:5]<"06:00":
        routeType = "drive"

    #to be refreshed on wed 17/4
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vaW50ZXJuYWwtYWxiLW9tLXByZGV6aXQtaXQtMTIyMzY5ODk5Mi5hcC1zb3V0aGVhc3QtMS5lbGIuYW1hem9uYXdzLmNvbS9hcGkvdjIvdXNlci9wYXNzd29yZCIsImlhdCI6MTcxMzA3MzkzMiwiZXhwIjoxNzEzMzMzMTMyLCJuYmYiOjE3MTMwNzM5MzIsImp0aSI6Iko0aUR6VmtIMXVadjdub3IiLCJzdWIiOiJmZmFmMmU2ZjQ0NmM5YjVjMmJhMTJiZTA4YTU2NzM4MCIsInVzZXJfaWQiOjI0ODUsImZvcmV2ZXIiOmZhbHNlfQ.3CnAVoe1hcalNu8wEUyPUprGxvwcXxLleXSGwk1MwwA"
    headers = {"Authorization": token}
    if routeType == "pt":
        routing_url =  f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}&date={date}&time={time}&mode={mode}&numItineraries=3"
    else: #for driving/cycling/walking
        routing_url = f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}"
    route_response = requests.request("GET", routing_url, headers=headers).json()
    template=None
    if routeType == "pt":
        template = displayPTInfo(route_response["plan"]["itineraries"])
    else:
        #return render_template('route-planner.html', routeData=route_response['route_instructions'])
        data = []
        data.append(route_response["route_instructions"])
        try:
            data.append(route_response["phyroute"]["route_instructions"])
        except KeyError:
            pass
        try:
            data.append(route_response["alternativeroute"][0]["route_instructions"])
        except KeyError:
            pass
        template = displayDriveInfo(data)

    return jsonify({
        "route_response": route_response,
        "template": template
    })

@app.route("/", methods=['POST'])
def saveRoute():
    import json
    src= request.form['source']
    dst= request.form['destination']
    routeType = request.form['routeType']
    encodedRoute = json.loads(request.form['encodedRoute'])
    routeInfo = json.loads(request.form['routeInfo'])

    print(src)
    print(dst)
    print(routeType)
    print(encodedRoute)
    print(routeInfo)

    return "success"
if __name__ == '__main__':
    app.run(debug=True, port=8000)
