import folium
import requests
from shapely import wkt
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd
import geocoder
import webbrowser

# geopy를 사용하여 사용자의 실시간 위치를 받아오는 함수
def get_user_location():
    g = geocoder.ip('me')
    return g.lat, g.lng

# Tmap API를 사용하여 지명(POI) 검색을 통해 주소를 위도와 경도로 변환하는 함수
def get_coordinates_from_POI_search(query, app_key):
    url = "https://apis.openapi.sk.com/tmap/pois"
    params = {
        "version": 1,
        "format": "json",
        "appKey": app_key,
        "searchKeyword": query,
        "resCoordType": "WGS84GEO"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "searchPoiInfo" in data:
            pois = data["searchPoiInfo"]["pois"]["poi"]
            if pois:
                # 사용자가 검색한 지명(POI) 중에서 첫 번째 결과를 선택하여 목적지로 설정
                poi = pois[0]
                return poi["noorLat"], poi["noorLon"]
    return None, None

# 나머지 함수들은 이전과 동일하게 유지됩니다.

if __name__ == "__main__":
    # 데이터 파일 읽어오기 (CSV 형식)
    data = pd.read_csv('/Users/kimmo/K_circle/Voices/MINO/대구광역시_신호등_20230323.csv', encoding='cp949')

    # '신호등관리번호', '위도', '경도' 컬럼의 데이터를 튜플로 묶어 리스트로 변환
    locations = [(row['신호등관리번호'], row['위도'], row['경도']) for index, row in data.iterrows()]

    # 현재 위치 정보 (예시로 대구의 위도와 경도 사용)
    current_latitude, current_longitude = get_user_location()

    # 주소 입력을 통해 도착지의 위도와 경도를 얻어내기 (Tmap API 사용)
    destination_address = input("Please enter your destination: ")
    app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"  # 본인의 Tmap API AppKey로 교체해주세요.
    destination_latitude, destination_longitude = get_coordinates_from_POI_search(destination_address, app_key)

    if destination_latitude is not None and destination_longitude is not None:
        print(f"도착지 주소의 위도: {destination_latitude}, 경도: {destination_longitude}")

        # 지도 생성 및 중심 좌표 설정
        map_center = [current_latitude, current_longitude]
        tmap_map = folium.Map(location=map_center, zoom_start=17)

        # 현재 위치 마커 추가
        folium.Marker(
            [current_latitude, current_longitude],
            icon=folium.CustomIcon('http://tmapapi.sktelecom.com/upload/tmap/marker/pin_r_m_s.png', icon_size=(30, 30))
        ).add_to(tmap_map)

        # ... (이하 생략)

        # 지도를 HTML 파일로 저장
        tmap_map.save("tmap_route_map_with_traffic_light.html")

        print("지도가 tmap_route_map_with_traffic_light.html 파일로 저장되었습니다. 해당 파일을 웹 브라우저로 열어주세요.")
        webbrowser.open("tmap_route_map_with_traffic_light.html")

    else:
        print("주소를 찾을 수 없습니다. 올바른 주소를 입력해주세요.")
