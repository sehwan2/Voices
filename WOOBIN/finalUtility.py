import requests
import folium
import geopandas as gpd
import matplotlib.pyplot as plt # 데이터 시각화 라이브러리
from IPython.display import IFrame
from shapely.geometry import Point, Polygon
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import urllib.parse
import geocoder
from IPython.core.display import display, HTML

# 카카오 REST API를 호출할 때 사용하는 키 값
api_key = "435c73b9db0f7b7a8400f68b8ca3da0f"

# 주소 검색 API 주소
api_url = "https://dapi.kakao.com/v2/local/search/address.json"

# 호출할 데이터 작성(전범위라는 뜻 -> 특정 범위를 원하면 ''안에 넣기)
data = {'query': ''}

# REST API를 호출하고 응답을 JSON 형태로 파싱
response = requests.get(api_url, headers={'Authorization': f'KakaoAK {api_key}'}, params=data).json()

# 반환된 JSON 결과에서 위도와 경도 값을 추출
#longitude = response['documents'][0]['x']  # 경도
#latitude = response['documents'][0]['y']  # 위도

g = geocoder.ip('me')
print("현재 위치")
print(g.latlng)

# 나중에 현재 위치로 바꿀 것(서울을 갈 수 없어서 수동 변경 -> figure1에서 찾아서 설정하기)
latitude = 37.5695
longitude = 126.8310



# 생성된 HTML의 주소를 인터넷에 입력
# EX) file:///c%3A/Users/%EC%98%A4%EC%9A%B0%EB%B9%88/Desktop/POLIO/%EC%98%A4%EC%9A%B0%EB%B9%88%28aiProject%29/map.html
# 주소가 헷갈리면 HTML을 CHROME에 드래그

# shp 파일을 읽어와서 데이터프레임으로 변환
# https://data.seoul.go.kr/dataList/OA-21285/F/1/datasetView.do
# ㄴ서울시 주요 113장소 영역zip파일 다운
gdf = gpd.read_file('C:/Users/오우빈/Desktop/POLIO/서울시 주요 113장소 영역/서울시 주요 113장소 영역.shp', encoding='utf-8')
#                   ㄴ괄호 안에 폴더 위치 작성
dbf = gdf.set_index('AREA_NM').join(gpd.read_file('C:/Users/오우빈/Desktop/POLIO/서울시 주요 113장소 영역/서울시 주요 113장소 영역.dbf').set_index('AREA_NM'), lsuffix='_gdf', rsuffix='_dbf')
#                                                   ㄴ괄호 안에 폴더 위치 작성

# 지도에 현재 위치 마커 및 GeoJson 레이어 추가, my_map 제작
m = folium.Map(location=[latitude, longitude], zoom_start=12)
folium.Marker([latitude, longitude]).add_to(m)
folium.Marker(g.latlng).add_to(m)
folium.GeoJson(gdf).add_to(m)
m.save('my_map.html')

# 좌표계 WGS84
gdf = gdf.to_crs(epsg=4326)

# 지도 데이터 출력
ax = gdf.plot(figsize=(12, 8), alpha=1, edgecolor='k')
#             ㄴ그래프 크기     ㄴ투명도    ㄴ외곽선 색
# figure1 이름 설정
ax.set(title="Major Areas")

# AREA_NM 값 출력
for x, y, name in zip(gdf.centroid.x, gdf.centroid.y, gdf.index):
    plt.text(x, y, s=name, fontsize=8, color='black', horizontalalignment='center', verticalalignment='center')
    #            ㄴ글자크기       ㄴ글자색   ㄴ글자 가로정렬   ㄴ글자 세로정렬


# 판단 범위의 위도와 경도를 보기 위한 것(마우스 올리면 위도와 경도 확인 가능)
plt.show()

# my_overlayed_map 제작(굳이 없어도 됨)
m = folium.Map(location=[latitude, longitude], zoom_start=12)
folium.GeoJson(gdf).add_to(m)
m.save('my_overlayed_map.html')


# HTML 드래그 하기 아래 파일을 드래그 해야함
IFrame(src='./my_map.html', width=700, height=600)
IFrame(src='./my_overlayed_map.html', width=700, height=600)

# 선택된 영역 내부에 포함되는 데이터인지 확인하기
point = Point(longitude, latitude)
inside = False
for geom in gdf.geometry:
    if point.within(geom):
        inside = True
        break

# area_nm 변수에 POI 번호로 설정
activeMeasure = False
for idx, geom in enumerate(gdf.geometry):
    if point.within(geom):
        inside = True
        activeMeasure = True
        area_nm = gdf.index[idx] + 1
        break
        
# 우리가 판단 가능한 범위인지 판단
if inside:
    activeMeasure = True
    print(area_nm)
else:
    activeMeasure = False
    print("out")

# 판단 가능한 범위면 API 불러오기
if activeMeasure == True :
    url = 'http://openapi.seoul.go.kr:8088/704d4656786f77623831625843516f/xml/citydata/1/5/' + 'POI{:03d}'.format(area_nm)

    response = requests.get(url)
    data = response.text

    root = ET.fromstring(data)
    
    #데이터프레임 구축
    df = pd.DataFrame({
        '장소명': [root.find('.//AREA_NM').text],
        '장소 코드': [root.find('.//AREA_CD').text],
        '혼잡도 정도': [root.find('.//AREA_CONGEST_LVL').text],
    })
    
    # 현재 위치 장소명 및 혼잡도 정보 출력
    print(df)
    
'''
    # 현재 위치 장소명 및 혼잡도 정보 저장
    df_info = df.to_html()

    # my_map.html에 정보 출력
    with open('my_map.html', 'r') as f:
        map_html = f.read()

    map_html = map_html.replace('</body>', '<br>' + df_info + '</body>')

    with open('my_map.html', 'w') as f:
        f.write(map_html)


    # 웹 브라우저 출력
    html_str = f"<div style='float:left;'>{map_html}</div><div style='float:right; width:50%;'>{df_info}</div>"
    display(HTML(html_str))
'''