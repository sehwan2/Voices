import requests
#126.98, 37.57
#
#
url = "https://apis.openapi.sk.com/tmap/routes/pedestrian"
params = {
    "version": "1",
    "appKey": "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0",
    "startX": "126.978502",
    "startY": "37.566958",
    "endX": "126.988205",
    "endY": "37.551135",
    "startName": "출발지",
    "endName": "도착지",
    #"resCoordType": "EPSG3857"
}

response = requests.get(url, params=params)

url2 = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xSignalPhaseTimingInformation/1.0"
params2 = {
    "apiKey": "c9c17d9a-f5da-44f5-b9bd-a463306c7db8",
    "type": "json"
}

response2 = requests.get(url2, params2)


# if response.status_code == 200:
#     data = response.json()
#     features = data.get('features', [])
#     for feature in features:
#         geometry = feature.get('geometry', {})
        
#         typeName = geometry.get('type')
#         coordinates = geometry.get('coordinates')
        
        
        
#         properties = feature.get('properties', {})
       
#         turn_type = properties.get('turnType')
#         facility_type = properties.get('facilityType')
        
#         if facility_type != "15":
#             continue
#         if typeName is not None:
#             print(f'typeName: {typeName}')
#         if coordinates is not None:
#             print(f'coordinates: {coordinates}')
#         if turn_type is not None:
#             print(f'turnType: {turn_type}')
#         if facility_type is not None:
#             print(f'facilityType: {facility_type}')
#         print()
# else:
#     print("Error:", response.status_code)
    
if response2.status_code == 200:
    data = response2.json()
    for item in data:
        data_id = item.get('dataId')
        itst_id = item.get('itstId')
        eqmn_id = item.get('eqmnId')
        print(f'dataId: {data_id}, itstId: {itst_id}, eqmnId: {eqmn_id}')
else:
    print("Error:", response2.status_code)
