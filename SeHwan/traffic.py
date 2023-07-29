import folium
import requests
from shapely import wkt
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd

def get_tmap_route(start_x, start_y, end_x, end_y, app_key):
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian"
    params = {
        "version": 1,
        "format": "json",
        "appKey": app_key,
        "startX": start_x,
        "startY": start_y,
        "endX": end_x,
        "endY": end_y,
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": "출발지",
        "endName": "도착지"
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        data = response.json()
        if "features" in data:
            result_data = data["features"]
            return result_data
    return None

def get_coordinates_from_address_using_tmap_api(address, app_key):
    url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeo"
    params = {
        "version": 1,
        "format": "json",
        "appKey": app_key,
        "coordType": "WGS84GEO",
        "fullAddr": address
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "coordinateInfo" in data:
            coordinate = data["coordinateInfo"]["coordinate"][0]  # Use index 0 to access the first coordinate
            return coordinate["lat"], coordinate["lon"]
    return None, None

if __name__ == "__main__":
    # 데이터 파일 읽어오기 (CSV 형식)
    data = pd.read_csv('C:\\Users\\user\\OneDrive\\바탕 화면\\Sehwan\\대구광역시_신호등_20230323.csv', encoding='cp949')

    # '신호등관리번호', '위도', '경도' 컬럼의 데이터를 튜플로 묶어 리스트로 변환
    locations = [(row['신호등관리번호'], row['위도'], row['경도']) for index, row in data.iterrows()]

    # 현재 위치 정보 (예시로 대구의 위도와 경도 사용)
    current_latitude = 35.8714
    current_longitude = 128.6014

    # 주소 입력을 통해 도착지의 위도와 경도를 얻어내기 (Tmap API 사용)
    destination_address = "대구광역시 달서구 본동"
    app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"  # 본인의 Tmap API AppKey로 교체해주세요.
    destination_latitude, destination_longitude = get_coordinates_from_address_using_tmap_api(destination_address, app_key)

    if destination_latitude is not None and destination_longitude is not None:
        print(f"도착지 주소의 위도: {destination_latitude}, 경도: {destination_longitude}")

        # 지도 생성 및 중심 좌표 설정
        map_center = [current_latitude, current_longitude]
        tmap_map = folium.Map(location=map_center, zoom_start=17)

        # 경로 정보를 이용하여 폴리라인 추가
        start_x = str(current_longitude)
        start_y = str(current_latitude)
        end_x = str(destination_longitude)
        end_y = str(destination_latitude)

        route_data = get_tmap_route(start_x, start_y, end_x, end_y, app_key)

        if route_data:
            points = []
            for feature in route_data:
                geometry = feature["geometry"]
                coords = geometry["coordinates"]
                if geometry["type"] == "Point":
                    points.append((coords[1], coords[0]))
                elif geometry["type"] == "LineString":
                    for coord in coords:
                        points.append((coord[1], coord[0]))
                elif geometry["type"] == "MultiLineString":
                    for line in coords:
                        for coord in line:
                            points.append((coord[1], coord[0]))

            if points:
                # 횡단보도 위치에 마커 추가
                for ID, lat, lng in locations:
                    for point in points:
                        if great_circle(point, (lat, lng)).meters < 40:  # 거리 임계값은 적절히 조절
                            folium.Marker([lat, lng], popup=f"신호등 ID: {ID}").add_to(tmap_map)
                            break

                folium.PolyLine(points, color="red", weight=6, opacity=0.7).add_to(tmap_map)
                print("경로와 근접한 마커를 지도에 표시하였습니다.")
            else:
                print("경로 정보를 가져올 수 없습니다.")
        else:
            print("경로를 가져올 수 없습니다. 올바른 좌표를 입력했는지 확인하세요.")

        # 지도를 HTML 파일로 저장
        tmap_map.save("tmap_route_map_with_traffic_light.html")

        # 지도를 보여주기 위해 웹 브라우저로 실행
        import webbrowser
        webbrowser.open("tmap_route_map_with_traffic_light.html")

    else:
        print("주소를 찾을 수 없습니다. 올바른 주소를 입력해주세요.")