from flask import Blueprint, render_template, request, session, jsonify
from datetime import datetime
import requests


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
    time="08:00:00" #use when past pt time if not comment out

    #to be refreshed on sat 6/4 
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZmFmMmU2ZjQ0NmM5YjVjMmJhMTJiZTA4YTU2NzM4MCIsImlzcyI6Imh0dHA6Ly9pbnRlcm5hbC1hbGItb20tcHJkZXppdC1pdC0xMjIzNjk4OTkyLmFwLXNvdXRoZWFzdC0xLmVsYi5hbWF6b25hd3MuY29tL2FwaS92Mi91c2VyL3Bhc3N3b3JkIiwiaWF0IjoxNzEyMTU1ODQwLCJleHAiOjE3MTI0MTUwNDAsIm5iZiI6MTcxMjE1NTg0MCwianRpIjoiQzJGa3BxdHdiQkl2R3dpMyIsInVzZXJfaWQiOjI0ODUsImZvcmV2ZXIiOmZhbHNlfQ.gJXWqfcFCeELFK13YsxLrXcDteNy6r_95aUFa1LIC9g"
    headers = {"Authorization": token}
    if routeType == "pt":
        routing_url =  f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}&date={date}&time={time}&mode={mode}&numItineraries=2"
    else: #for driving/cycling/walking
        routing_url = f"https://www.onemap.gov.sg/api/public/routingsvc/route?start={start_lat}%2C{start_long}&end={end_lat}%2C{end_long}&routeType={routeType}"
    route_response = requests.request("GET", routing_url, headers=headers).json()

    return jsonify(route_response)