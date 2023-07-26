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

    items = data["body"]["items"]["item"]
    closest_item = None
    min_distance = float("inf")

    for item in items:
        item_x = float(item["x"])
        item_y = float(item["y"])
        distance = ((gps_x - item_x) ** 2 + (gps_y - item_y) ** 2) ** 0.5

        if distance < min_distance:
            min_distance = distance
            closest_item = item

    if closest_item:
        item_id = closest_item["id"]
        closest_x = closest_item["x"]
        closest_y = closest_item["y"]
        print(f"Closest Item ID: {item_id}")
        print(f"Closest X: {closest_x}")
        print(f"Closest Y: {closest_y}")
    else:
        print("No matching data found.")

if __name__ == "__main__":
    # Replace the URL with the provided link
    api_url = "https://apis.data.go.kr/6270000/dgSignalOrder/getSignalOrderList?serviceKey=Kl%2BRNLrUCgC0pfRX8b3sV68604rKks10Ex4oDyGaFkPOr7i7M16DmiPCWVzDyJnM4lwMum%2FvRBl6HcU6vHbUrg%3D%3D&type=json&numOfRows=30&pageNo=10"
    gps_x = 128.631831  # Replace this with your GPS X value
    gps_y = 35.980602  # Replace this with your GPS Y value

    data = fetch_data_from_api(api_url)

    if data:
        parse_data(data, gps_x, gps_y)
    else:
        print("Failed to fetch data from the API.")
