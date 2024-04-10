from flask import Blueprint, render_template, request, session, jsonify
from datetime import datetime
import requests

def displayDriveInfo(data):
    routeSteps =[]
    for directions in data:
        routeSteps.append("In "+ directions[5]+ "\n" +directions[9])
    
    return render_template('route_planner.html', routeSteps=routeSteps)

routePlanBp = Blueprint("routePlanBp",__name__)

@routePlanBp.route("/route_planner", methods=['GET'])
def route_planner():
    return render_template('route_planner.html')

@routePlanBp.route("/route_planner", methods=['POST'])
def cal_route():
    start = request.form['start']
    end = request.form['end']
    routeType = request.form['type']
    
    start_url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={start}&returnGeom=Y&getAddrDetails=Y"
    end_url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={end}&returnGeom=Y&getAddrDetails=Y"

    start_response =requests.request("GET", start_url)
    end_response = requests.request("GET", end_url)
    start_response= start_response.json()
    end_response= end_response.json()

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
    time="20:00:00" #use when past pt time if not comment out

    #to be refreshed on wed 10/4 
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZmFmMmU2ZjQ0NmM5YjVjMmJhMTJiZTA4YTU2NzM4MCIsImlzcyI6Imh0dHA6Ly9pbnRlcm5hbC1hbGItb20tcHJkZXppdC1pdC0xMjIzNjk4OTkyLmFwLXNvdXRoZWFzdC0xLmVsYi5hbWF6b25hd3MuY29tL2FwaS92Mi91c2VyL3Bhc3N3b3JkIiwiaWF0IjoxNzEyNDk1MDE2LCJleHAiOjE3MTI3NTQyMTYsIm5iZiI6MTcxMjQ5NTAxNiwianRpIjoiTDdDTUZhMmt0alFGeElORiIsInVzZXJfaWQiOjI0ODUsImZvcmV2ZXIiOmZhbHNlfQ.ugDXISOtrSnjKatHH4D3IKlAMcGUObUe1s8EYGHsmsw"
    headers = {"Authorization": token}
    if routeType == "pt":
        routing_url =  f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}&date={date}&time={time}&mode={mode}&numItineraries=3"
    else: #for driving/cycling/walking
        routing_url = f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}"
    route_response = requests.request("GET", routing_url, headers=headers).json()
    template=None
    if routeType=="drive":
        #return render_template('route_planner.html', routeData=route_response['route_instructions'])
        template=displayDriveInfo(route_response["route_instructions"])
    
    return jsonify({
        "route_response":route_response,
        "template": template
        })
    
