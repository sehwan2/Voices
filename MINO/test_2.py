import folium
import requests
from shapely import wkt
from geopy.distance import great_circle
import pandas as pd
from flask import Flask, render_template, request
import time

app = Flask(__name__)
app.config['TEMPLATE_FORDER'] = '/Users/kimmo/K_circle/Voices/MINO/templates'

def get_api_response(keyword):
    base_url = 'https://apis.openapi.sk.com/tmap/pois'  # 여기에 실제 API 주소를 입력하세요
    params = {
        'keyword': keyword,
        'count': '100',  # 원하는 결과 개수를 입력하세요
    }
    response = requests.get(base_url, params=params)
    return response

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
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        if "coordinateInfo" in data:
            coordinate = data["coordinateInfo"]["coordinate"]
            if coordinate and coordinate[0]["newLat"] and coordinate[0]["newLon"]:
                lat = float(coordinate[0]["newLat"])
                lon = float(coordinate[0]["newLon"])
                return lat, lon
    return None, None

def get_places_from_keyword_using_tmap_api(keyword, app_key):
    # 추가된 함수: 키워드를 검색하여 연관된 장소 리스트를 얻어내는 함수
    url = "https://apis.openapi.sk.com/tmap/pois"
    params = {
        "version": 1,
        "format": "json",
        "appKey": app_key,
        "searchKeyword": keyword
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "searchPoiInfo" in data:
            places = []
            for place in data["searchPoiInfo"]["pois"]["poi"]:
                places.append((place["name"], float(place["noorLat"]), float(place["noorLon"])))
            return places
    return None

def search_places(keyword, app_key):
    url = "https://apis.openapi.sk.com/tmap/pois"
    params = {
        "version": 1,
        "format": "json",
        "appKey": app_key,
        "searchKeyword": keyword,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "searchPoiInfo" in data:
            places = data["searchPoiInfo"]["pois"]["poi"]
            return places
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 사용자로부터 입력된 도착지 주소 받기
        destination_address = request.form['destination_address']

        # 주소 입력을 통해 도착지의 위도와 경도를 얻어내기 (Tmap API 사용)
        app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"  # 본인의 Tmap API AppKey로 교체해주세요.
        destination_latitude, destination_longitude = get_coordinates_from_address_using_tmap_api(destination_address, app_key)

        if destination_latitude is not None and destination_longitude is not None:
            # 지도 생성 및 중심 좌표 설정
            map_center = [destination_latitude, destination_longitude]
            tmap_map = folium.Map(location=map_center, zoom_start=17)

            # 실시간 위치 정보를 얻어옴 (Geolocation API 사용)
            user_latitude = request.form.get('user_latitude')
            user_longitude = request.form.get('user_longitude')

            if user_latitude and user_longitude:
                # 경로 정보를 이용하여 폴리라인 추가
                start_x = str(user_longitude)
                start_y = str(user_latitude)
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
            else:
                print("사용자의 위치 정보를 얻을 수 없습니다. 브라우저에서 위치 정보 제공에 동의해주세요.")

            # 대기 시간 설정 (예시로 2초로 설정)
            time.sleep(2)

            # 지도를 HTML 파일로 저장
            tmap_map.save("templates/tmap_route_map_with_traffic_light.html")

            # 렌더링된 템플릿 반환
            return render_template('tmap_route_map_with_traffic_light.html')

        else:
            return render_template('index.html', map_exists=False)

    return render_template('index.html', map_exists=False)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        page = request.args.get('page', default=1, type=int)

        # 페이지당 결과 개수를 설정합니다.
        results_per_page = 10

        # 검색 API 호출 및 결과 받아오기
        places = search_places(keyword, app_key="PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0")

        # 페이징 처리를 위해 결과를 현재 페이지에 맞게 자릅니다.
        start_index = (page - 1) * results_per_page
        end_index = start_index + results_per_page
        paginated_places = places[start_index:end_index]

        return render_template('search_results.html', keyword=keyword, places=paginated_places, page=page)

    return render_template('search_results.html', places=[], keyword="")


if __name__ == "__main__":
    # 데이터 파일 읽어오기 (CSV 형식)
    data = pd.read_csv('/Users/kimmo/K_circle/Voices/MINO/대구광역시_신호등_20230323.csv', encoding='cp949')

    # '신호등관리번호', '위도', '경도' 컬럼의 데이터를 튜플로 묶어 리스트로 변환
    locations = [(row['신호등관리번호'], row['위도'], row['경도']) for index, row in data.iterrows()]

    # 현재 위치 정보 (예시로 대구의 위도와 경도 사용)
    current_latitude = 35.8714
    current_longitude = 128.6014

    app.run(host="0.0.0.0", port=8080, debug=True)