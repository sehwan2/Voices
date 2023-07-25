import requests
from PIL import Image
from io import BytesIO

static_map_url = "https://apis.openapi.sk.com/tmap/staticmap/image"
static_map_params = {
    "version": "1",
    "appKey": "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0",
    "centerLat": "37.570841",  # 이미지 중심 위도
    "centerLon": "126.985302",  # 이미지 중심 경도
    "zoom": "14",              # 줌 레벨
    "width": "800",            # 이미지 너비
    "height": "600"            # 이미지 높이
}

response = requests.get(static_map_url, params=static_map_params)

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    image.show()
else:
    print("Error: 이미지 로딩 실패", response.status_code)