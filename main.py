from flask import Flask, render_template, request, jsonify, session, redirect
from backends.login import loginBp
from backends.signup import signupBp
# from backends.busExplorer import busExplorerBp
from backends.reset import resetBp
from database.dbSaveRoute import dbSaveRoute
from database.dbAccOperation import dbAccOp
import secrets
from datetime import datetime
import requests
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) #Creates a session key.

#Register each page of the website as blueprint
app.register_blueprint(loginBp)
app.register_blueprint(resetBp)
app.register_blueprint(signupBp)
# app.register_blueprint(busExplorerBp)

@app.route("/", methods =['GET'])
@app.route("/route-planner", methods=['GET'])
def home():
    user_email = session.get('user_email')
    return render_template('route-planner.html', user_email=user_email)

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

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('token', None)
    session.pop('uid', None)
    return render_template("route-planner.html")

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
    # Open the file in read mode
    with open('api-key.txt', 'r') as file:
        # Read the entire contents of the file into a string
        token = file.read()
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
    name= request.form['name']
    src= request.form['source']
    dst= request.form['destination']
    routeType = request.form['routeType']
    encodedRoute = json.loads(request.form['encodedRoute'])
    routeInfo = json.loads(request.form['routeInfo'])

    data = {"source": src, "destination": dst, "routeType": routeType, "encodedRoute": encodedRoute, "routeInfo": routeInfo}
    result = dbSaveRoute.saveRoute(data, name)
    if (result == 1):
        return "Success"
    elif (result == 2):
        return "Duplicate"
    elif (result == 3):
        return "Limit"
    else:
        return "Failure"

@app.route("/getRoute", methods=['GET'])
def getRoute():
    allSavedRoutes = {"routes" : []}
    savedRoutes=dbSaveRoute.retrieveSaveRoute()
    if savedRoutes is not None:
        for route in savedRoutes.each():
            name = route.key()
            source = route.val()['source']
            destination = route.val()['destination']
            routeType = route.val()['routeType']
            encodedRoute = route.val()['encodedRoute']
            routeInfo = route.val()['routeInfo']
            data = {"name": name,"source": source, "destination": destination, "routeType": routeType, "encodedRoute": encodedRoute, "routeInfo": routeInfo}
            allSavedRoutes['routes'].append(data)

    return jsonify(allSavedRoutes)


@app.route("/delRoute", methods=["POST"])
def delRoute():
    name = request.form["name"]
    result = dbSaveRoute.deleteSaveRotue(name)
    if (result == 1):
        return "success"
    else:
        return "fail"

if __name__ == '__main__':
    app.run(debug=True, port=8000)

