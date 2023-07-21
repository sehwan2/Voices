from PIL import Image, ImageDraw
import requests

# API 요청 설정
app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"
coord_type = "WGS84GEO"
start_pos = "126.987038,37.565207"
end_pos = "126.996943,37.571253"

# 경로안내 API 호출
url = f"https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={app_key}&startX={start_pos}&startY={start_pos}&endX={end_pos}&endY={end_pos}&reqCoordType={coord_type}"

res = requests.get(url).content()


# 좌표 정보 파싱
path_points = []
for feature in res['features']:
    if 'geometry' in feature and feature['geometry']['type'] == 'LineString':
        path = feature['geometry']['coordinates']
        path_points.extend(path)

start_lon, start_lat = map(float,start_pos.split(","))
end_lon, end_lat = map(float,end_pos.split(","))

width, height = 512, 512 # 이미지 지도 크기
longitude, latitude, zoom = (start_lon + end_lon) / 2, (start_lat + end_lat) / 2, 14 # 지도 중심 좌표 및 확대 배율
line_color, line_width = (0, 0, 255), 4 # 최단 경로 색상 및 두께
marker_color1, marker_size1 = (0, 255, 0), 64 # 출발지 마커 색상 및 크기
marker_color2, marker_size2 = (255, 0, 0), 64 # 도착지 마커 색상 및 크기

# 지도 이미지 다운로드
url = f"https://apis.openapi.sk.com/tmap/staticMap?appKey={app_key}&longitude={longitude}&latitude={latitude}&coordType={coord_type}&zoom={zoom}&format=PNG&width={width}&height={height}&markers={start_pos},{end_pos}"
response = requests.get(url)
image_data = response.content

# 경로 선 그리기
img = Image.open(io.BytesIO(image_data))
draw = ImageDraw.Draw(img)
path_points = [(pt[0] - start_lon, pt[1] - start_lat) for pt in path_points] # 좌표 이동
draw.line(path_points, fill=line_color, width=line_width)

# 출발지 마커
marker_size1 = (marker_size1, marker_size1)
marker_pos1 = (width * (start_lon - longitude) / (2 * zoom) + width / 2, height * (start_lat - latitude) / (2 * zoom) + height / 2)
draw.ellipse((marker_pos1[0] - marker_size1[0] / 2, marker_pos1[1] - marker_size1[1] / 2, marker_pos1[0] + marker_size1[0] / 2, marker_pos1[1] + marker_size1[1] / 2), fill=marker_color1)

# 도착지 마커
marker_size2 = (marker_size2, marker_size2)
marker_pos2 = (width * (end_lon - longitude) / (2 * zoom) + width / 2, height * (end_lat - latitude) / (2 * zoom) + height / 2)
draw.ellipse((marker_pos2[0] - marker_size2[0] / 2, marker_pos2[1] - marker_size2[1] / 2, marker_pos2[0] + marker_size2[0] / 2, marker_pos2[1] + marker_size2[1] / 2), fill=marker_color2)

# 지도 이미지 저장
img.save("map.png")

# 지도 이미지 보기
Image.open("map.png").show()