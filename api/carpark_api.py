import json

import requests

CARPARK_NUMBER = 3

response = requests.get('https://api.data.gov.sg/v1/transport/carpark-availability')

response_json = response.json()

timestamp = response_json['items'][0]['timestamp']
carpark_data = response_json['items'][0]['carpark_data']
carpark_info = carpark_data[CARPARK_NUMBER]['carpark_info']
carpark_number = carpark_data[CARPARK_NUMBER]['carpark_number']
carpark_update_datetime = carpark_data[CARPARK_NUMBER]['update_datetime']


# first carpark info
first_carpark = carpark_info[0]
total_lots = first_carpark['total_lots']
lot_type = first_carpark['lot_type']
lots_available = first_carpark['lots_available']

# print(f"Carpark Number: {carpark_number}")
# print(f"Updated Date/Time: {carpark_update_datetime}")
# print(f"Total lots: {total_lots}")
# print(f"Lot Type: {lot_type}")
# print(f"Lots Available: {lots_available}")

def getInfoByCpAddress(address) :
    carparkInfoResponse = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c&q=' + address)
    carparkInfoResponse_json = carparkInfoResponse.json()
    print(carparkInfoResponse_json['result']['records'])

def getInfoByCpNumber(carpark_number) :
    carparkInfoResponse = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c&q=' + carpark_number)
    carparkInfoResponse_json = carparkInfoResponse.json()
    print(carparkInfoResponse_json['result']['records'])
