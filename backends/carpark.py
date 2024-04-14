from flask import Blueprint, render_template
import requests

carparkBp = Blueprint("carparkBp",__name__)

@carparkBp.route("/carpark", methods =['GET'])
def carpark():

    return render_template('carpark-finder.html')

# token =
# headers = {"Authorization": token}

#HDB carpark information
resourceID = 'resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c'

def getInfoByCpAddress(address) :
    carparkInfoResponse = requests.get('https://data.gov.sg/api/action/datastore_search?' + resourceID + '&q=' + '{"address":"' + address + '"}' )
    carparkInfoResponse_json = carparkInfoResponse.json()
    return carparkInfoResponse_json['result']['records']

def getInfoByCpNumber(carpark_number) :
    carparkInfoResponse = requests.get('https://data.gov.sg/api/action/datastore_search?' + resourceID + '&q=' + '{"car_park_no":"' + carpark_number + '"}' )
    carparkInfoResponse_json = carparkInfoResponse.json()
    return carparkInfoResponse_json['result']['records']

# url request to convert coordinates from SVY21 format to WGS84 format
# def convertCoord(x,y):
#     #Longtitude is X coordinate and Latitude is Y coordinate
#     url = 'https://www.onemap.gov.sg/api/common/convert/3414to4326?X=' + str(x) + '&Y=' + str(y)
#     response = requests.request("GET", url, headers=headers)
#     response_json = response.json()
#     coordinates = [response_json['latitude'], response_json['longitude']]
#     return coordinates