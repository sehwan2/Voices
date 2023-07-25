import folium
import requests

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
    app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"  # 본인의 Tmap API AppKey로 교체해주세요.
    
    start_x = input("출발지의 경도를 입력하세요: ")
    start_y = input("출발지의 위도를 입력하세요: ")
    end_x = input("도착지의 경도를 입력하세요: ")
    end_y = input("도착지의 위도를 입력하세요: ")
    
    route_data = get_tmap_route(start_x, start_y, end_x, end_y, app_key)
    
    if route_data:
        t_distance = route_data[0]["properties"]["totalDistance"] / 1000
        t_time = route_data[0]["properties"]["totalTime"] / 60
        
        print(f"총 거리: {t_distance:.1f}km")
        print(f"총 시간: {t_time:.0f}분")
        
        # 지도 생성 및 중심 좌표 설정
        map_center = [(float(start_y) + float(end_y)) / 2, (float(start_x) + float(end_x)) / 2]
        tmap_map = folium.Map(location=map_center, zoom_start=17)

        # 시작지점과 도착지점 마커 추가
        folium.Marker([float(start_y), float(start_x)], popup="출발지").add_to(tmap_map)
        folium.Marker([float(end_y), float(end_x)], popup="도착지").add_to(tmap_map)

        # 경로 정보를 이용하여 폴리라인 추가
        points = []
        for feature in route_data:
            geometry = feature["geometry"]
            coords = geometry["coordinates"]
            if geometry["type"] == "Point":
                points.append((coords[1], coords[0]))  # 수정된 부분
            elif geometry["type"] == "LineString":
                for coord in coords:
                    points.append((coord[1], coord[0]))  # 수정된 부분
            elif geometry["type"] == "MultiLineString":
                for line in coords:
                    for coord in line:
                        points.append((coord[1], coord[0]))  # 수정된 부분



        if points:
            folium.PolyLine(points, color="red", weight=6, opacity=0.7).add_to(tmap_map)
            print("경로를 지도에 표시하였습니다.")
        else:
            print("경로 정보를 가져올 수 없습니다.")
        
        # 지도를 HTML 파일로 저장
        tmap_map.save("tmap_route_map.html")

        # 지도를 보여주기 위해 웹 브라우저로 실행
        import webbrowser
        webbrowser.open("tmap_route_map.html")
    else:
        print("경로를 가져올 수 없습니다. 올바른 좌표를 입력했는지 확인하세요.")
