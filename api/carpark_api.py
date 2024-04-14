import requests

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
def convertCoord(x,y):
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmZmFmMmU2ZjQ0NmM5YjVjMmJhMTJiZTA4YTU2NzM4MCIsImlzcyI6Imh0dHA6Ly9pbnRlcm5hbC1hbGItb20tcHJkZXppdC1pdC0xMjIzNjk4OTkyLmFwLXNvdXRoZWFzdC0xLmVsYi5hbWF6b25hd3MuY29tL2FwaS92Mi91c2VyL3Bhc3N3b3JkIiwiaWF0IjoxNzEyODI1NzU3LCJleHAiOjE3MTMwODQ5NTcsIm5iZiI6MTcxMjgyNTc1NywianRpIjoiMkx6WGZxMHl4NWI2RWd4aCIsInVzZXJfaWQiOjI0ODUsImZvcmV2ZXIiOmZhbHNlfQ.lMaDzogTANdmo4JiMtXuMleBdJVD6OsDT8DAhFuQu18"
    headers = {"Authorization": token}

    #Longtitude is X coordinate and Latitude is Y coordinate
    url = 'https://www.onemap.gov.sg/api/common/convert/3414to4326?X=' + str(x) + '&Y=' + str(y)
    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    coordinates = [response_json['latitude'], response_json['longitude']]
    return coordinates

# CARPARK_NUMBER = 3
# response = requests.get('https://api.data.gov.sg/v1/transport/carpark-availability')
# response_json = response.json()
#
# timestamp = response_json['items'][0]['timestamp']
# carpark_data = response_json['items'][0]['carpark_data']
# carpark_info = carpark_data[CARPARK_NUMBER]['carpark_info']
# carpark_number = carpark_data[CARPARK_NUMBER]['carpark_number']
# carpark_update_datetime = carpark_data[CARPARK_NUMBER]['update_datetime']
#
# # first carpark info
# first_carpark = carpark_info[0]
# total_lots = first_carpark['total_lots']
# lot_type = first_carpark['lot_type']
# lots_available = first_carpark['lots_available']
#
# # print(f"Carpark Number: {carpark_number}")
# # print(f"Updated Date/Time: {carpark_update_datetime}")
# # print(f"Total lots: {total_lots}")
# # print(f"Lot Type: {lot_type}")
# # print(f"Lots Available: {lots_available}")


# # test calls
# testResult1 = getInfoByCpAddress("BLK 272A SENGKANG CENTRAL")
# print(testResult1)
# testResult2 = getInfoByCpNumber("sk1k")
# print(testResult2)
# coordinates = convertCoord(testResult1[0]['x_coord'], testResult1[0]['y_coord'])
# print(coordinates)

# Results from test call
# [{'_id': 1467, 'car_park_no': 'SK1K', 'address': 'BLK 272A SENGKANG CENTRAL', 'x_coord': '34678.7297', 'y_coord': '40731.1214', 'car_park_type': 'SURFACE CAR PARK', 'type_of_parking_system': 'COUPON PARKING', 'short_term_parking': 'WHOLE DAY', 'free_parking': 'NO', 'night_parking': 'YES', 'car_park_decks': '0', 'gantry_height': '0.00', 'car_park_basement': 'N', 'rank address': 0.46362185, '_full_count': '1'}]
# [{'_id': 1467, 'car_park_no': 'SK1K', 'address': 'BLK 272A SENGKANG CENTRAL', 'x_coord': '34678.7297', 'y_coord': '40731.1214', 'car_park_type': 'SURFACE CAR PARK', 'type_of_parking_system': 'COUPON PARKING', 'short_term_parking': 'WHOLE DAY', 'free_parking': 'NO', 'night_parking': 'YES', 'car_park_decks': '0', 'gantry_height': '0.00', 'car_park_basement': 'N', 'rank car_park_no': 0.06079271, '_full_count': '1'}]
# [1.3846315451169153, 103.8933320236058]
