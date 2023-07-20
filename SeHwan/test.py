import requests

def get_data_from_api():
    url = "https://apis.openapi.sk.com/tmap/routes"
    params = {
        "version": "1",
        "format": "json",
        "callback": "result",
        "appKey": "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    api_data = get_data_from_api()
    if api_data:
        print(api_data)