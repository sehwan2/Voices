from shapely import wkt
from flask import Flask, render_template_string
import pandas as pd
import json

# Flask 앱 생성
app = Flask(__name__)

# 데이터 파일 읽어오기
data = pd.read_excel('C:\\Users\\오우빈\\Desktop\\POLIO\\오우빈(aiProject)\\DaeguTrafficLight_InFo.xlsx')

# 'geometry' 컬럼의 데이터를 WKT(Well-Known Text) 형식으로 파싱
data['geometry'] = data['geometry'].apply(lambda x: wkt.loads(x))

# 데이터를 리스트로 변환 (각 원소는 위도와 경도의 튜플)
locations = [(geom.y, geom.x) for geom in data['geometry']]

@app.route("/")
def map():
    # HTML + JavaScript 정의
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Simple Map</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <!-- Tmap JavaScript API를 페이지에 로드 -->
    <script src="https://apis.openapi.sk.com/tmap/jsv2?version=1&appKey=PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"></script>
    <style>
        /* 지도를 표시할 div 요소의 크기를 정의 */
        #map_div {
            width: 100%;
            height: 800px;
        }
    </style>
    <script type="text/javascript">
        var map;
        var markers = [];
        var locations = JSON.parse('{{ locations }}');

        function getUserLocation() {
            // 사용자의 위치를 얻기 위해 Geolocation API 사용
            if(navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    // 사용자의 위도와 경도
                    var lat = position.coords.latitude;
                    var lng = position.coords.longitude;

                    // 사용자 위치를 중심으로 지도 생성
                    map = new Tmapv2.Map("map_div", {
                        center: new Tmapv2.LatLng(lat, lng),
                        width: "100%",
                        height: "800px",
                        zoom: 10
                    });

                    // 사용자 위치에 마커 생성
                    var userMarker = new Tmapv2.Marker({
                        position: new Tmapv2.LatLng(lat, lng),
                        icon: "http://tmapapi.sktelecom.com/upload/tmap/marker/pin_r_m_s.png",
                        map: map
                    });

                    // 각 횡단보도 위치에 마커 생성
                    for (var i = 0; i < locations.length; i++) {
                        var marker = new Tmapv2.Marker({
                            position: new Tmapv2.LatLng(locations[i][0], locations[i][1]),
                            map: map
                        });
                        markers.push(marker);
                    }
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
    </script>
    </head>
    <body onload="getUserLocation()">
        <div id="map_div"></div>
    </body>
    </html>
    """
    # Jinja2 템플릿 엔진을 이용하여 데이터를 JSON 형식으로 변환
    rendered = render_template_string(html, locations=json.dumps(locations))
    return rendered

# 메인 모듈로 실행되면 Flask 앱 실행
if __name__ == "__main__":
    app.run(debug=True, port=5001)
