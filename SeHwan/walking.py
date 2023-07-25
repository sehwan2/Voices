from tmapy.pedestrian import TmapPedestrianPathfinder

api_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"
startpoint = (37.570840, 126.985301) # 예시 출발지 좌표
endpoint = (37.551135, 126.988205)   # 예시 도착지 좌표
start_name = "서울역"   # 예시 출발지 이름
end_name = "시청"      # 예시 도착지 이름

pathfinder = TmapPedestrianPathfinder(api_key)
pathfinder.set_start(startpoint, name=start_name)
pathfinder.set_end(endpoint, name=end_name)

path_data = pathfinder.find()

if path_data is not None:
    features = path_data['features']

    # 지나치는 신호등 확인
    for feature in features:
        props = feature["properties"]
        if "S_" in props.get("description", ""):
            print("신호등 위치:", feature["geometry"]["coordinates"])
            print("신호등 인덱스:", props["pointIndex"])
else:
    print("경로 검색 실패")