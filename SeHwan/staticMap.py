import requests
from PIL import Image

# 파라미터 설정
app_key = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"
longitude = 126.987038
latitude = 37.565207
coord_type = "WGS84GEO"
zoom = 14
markers = "126.987038,37.565207"
width = 512
height = 512

# API 호출 URL 설정
url = f"https://apis.openapi.sk.com/tmap/staticMap?appKey={app_key}&longitude={longitude}&latitude={latitude}&coordType={coord_type}&zoom={zoom}&markers={markers}&format=PNG&width={width}&height={height}"

# 지도 이미지 다운로드
response = requests.get(url)
image_data = response.content

# 지도 이미지 저장
with open("map.png", "wb") as f:
    f.write(image_data)

# 지도 이미지 보기
Image.open("map.png").show()