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

def main():
    api_url = "https://apis.data.go.kr/6270000/dgSignalOrder/getSignalOrderList"
    service_key = "Kl%2BRNLrUCgC0pfRX8b3sV68604rKks10Ex4oDyGaFkPOr7i7M16DmiPCWVzDyJnM4lwMum%2FvRBl6HcU6vHbUrg%3D%3D"
    type_param = "json"
    num_of_rows = 30
    page_no = 10

    full_url = f"{api_url}?serviceKey={service_key}&type={type_param}&numOfRows={num_of_rows}&pageNo={page_no}"

    data = fetch_data_from_api(full_url)

    if data:
        # Print the data or do any other processing as needed
        print(data)
    else:
        print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
