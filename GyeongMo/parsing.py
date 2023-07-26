import requests

def fetch_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for any errors in the response
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching data:", e)
        return None

def parse_data(data, gps_x, gps_y):
    if not data or not data.get("body") or not data["body"].get("items") or not data["body"]["items"].get("item"):
        print("No data available or invalid data format.")
        return

    item = data["body"]["items"]["item"]
    sig_l_time = item.get("sig_l_time", "미공개")

    if sig_l_time != "미공개":
        print(f"sig_l_time for item ID 142: {sig_l_time}")
    else:
        print("sig_l_time is not available for item ID 142.")

if __name__ == "__main__":
    # Replace the URL with the provided link
    api_url = "https://apis.data.go.kr/6270000/dgSignal/getSignalItem?serviceKey=Kl%2BRNLrUCgC0pfRX8b3sV68604rKks10Ex4oDyGaFkPOr7i7M16DmiPCWVzDyJnM4lwMum%2FvRBl6HcU6vHbUrg%3D%3D&type=json&sigId=142"
    gps_x = 128.631831  # Replace this with your GPS X value
    gps_y = 35.980602  # Replace this with your GPS Y value

    data = fetch_data_from_api(api_url)

    if data:
        parse_data(data, gps_x, gps_y)
    else:
        print("Failed to fetch data from the API.")


if __name__ == "__main__":
    # Replace the URL with the provided link
    api_url = "https://apis.data.go.kr/6270000/dgSignal/getSignalItem?serviceKey=Kl%2BRNLrUCgC0pfRX8b3sV68604rKks10Ex4oDyGaFkPOr7i7M16DmiPCWVzDyJnM4lwMum%2FvRBl6HcU6vHbUrg%3D%3D&type=json&sigId=142"
    gps_x = 128.631831  # Replace this with your GPS X value
    gps_y = 35.980602  # Replace this with your GPS Y value

    data = fetch_data_from_api(api_url)

    if data:
        parse_data(data, gps_x, gps_y)
    else:
        print("Failed to fetch data from the API.")
