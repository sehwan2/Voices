import requests
import xml.etree.ElementTree as ET
import pandas as pd
import urllib.parse

import geocoder

g = geocoder.ip('me')
print(g.latlng)

url = 'http://openapi.seoul.go.kr:8088/4c504c4c73796b6d36344f70466a52/xml/citydata/1/5/' + urllib.parse.quote('경복궁')

response = requests.get(url)
data = response.text

root = ET.fromstring(data)


df = pd.DataFrame({
    '장소명': [root.find('.//AREA_NM').text],
    '장소 코드': [root.find('.//AREA_CD').text],
    '혼잡도 정도': [root.find('.//AREA_CONGEST_LVL').text],
    '위도': [root.find('.//LAT').text],
    '경도': [root.find('.//LNG').text]
})

print(df)