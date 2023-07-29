import folium
import requests
from shapely import wkt
from geopy.distance import great_circle
import pandas as pd

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # 맥OS 경우

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

if __name__ == "__main__":
    # 데이터 파일 읽어오기
    data = pd.read_excel('/Users/kimmo/K_circle/Voices/MINO/DaeguTrafficLight_InFo.xlsx')

    # 'geometry' 컬럼의 데이터를 WKT(Well-Known Text) 형식으로 파싱
    data['geometry'] = data['geometry'].apply(lambda x: wkt.loads(x))

    # 'id'와 'geometry' 컬럼의 데이터를 튜플로 묶어 리스트로 변환
    locations = [(row['ID'], geom.y, geom.x) if geom.geom_type == 'Point' else (row['id'], geom.centroid.y, geom.centroid.x) for index, row in data.iterrows() for geom in [row['geometry']]]


    # 지도 생성 및 중심 좌표 설정
    map_center = [sum(lat for ID, lat, lng in locations) / len(locations), sum(lng for ID, lat, lng in locations) / len(locations)]
    tmap_map = folium.Map(location=map_center, zoom_start=17)

    # 경로 정보를 이용하여 폴리라인 추가
    start_x = "128.526"
    start_y = "35.8237"
    end_x = "128.535990"
    end_y = "35.836326"
    
    app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"  # 본인의 Tmap API AppKey로 교체해주세요.
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
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open('tmap_route_map_with_traffic_light.html')
