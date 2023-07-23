import requests

url = "https://apis.openapi.sk.com/tmap/routes/pedestrian"
params = {
    "version": "1",
    "appKey": "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0",
    "startX": "126.985302",
    "startY": "37.570841",
    "endX": "126.988205",
    "endY": "37.551135",
    "startName": "출발지",
    "endName": "도착지"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error:", response.status_code)
