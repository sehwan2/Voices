from flask import Flask, render_template_string
import pandas as pd
import json

# Flask 앱 생성
app = Flask(__name__)

# 데이터 파일 읽어오기
data = pd.read_csv('C:\\Users\\user\\OneDrive\\바탕 화면\\Sehwan\\대구광역시_신호등_20230323.csv', encoding='cp949')


# 데이터를 리스트로 변환 (각 원소는 위도와 경도의 튜플)
locations = list(zip(data['위도'], data['경도']))

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
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
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

                    // 각 신호등 위치에 마커 생성
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

        function searchPOI() {
            var searchKeyword = $('#searchKeyword').val();
            var headers = {}; 
            headers["appKey"]="PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0";

            $.ajax({
                method:"GET",
                headers : headers,
                url:"https://apis.openapi.sk.com/tmap/pois?version=1&format=json",
                async:false,
                data:{
                    "searchKeyword" : searchKeyword,
                    "resCoordType" : "EPSG3857",
                    "reqCoordType" : "WGS84GEO",
                    "count" : 1
                },
                success:function(response){
                    console.log(response);
                    if (response.searchPoiInfo.pois !== undefined) {
                        var resultpoisData = response.searchPoiInfo.pois.poi[0];
                        var lat = Number(resultpoisData.noorLat);
                        var lon = Number(resultpoisData.noorLon);

                        console.log("code: " + request.status);
                        console.log("lat: ", lat);
                        console.log("lon: ", lon);

                        // 새로운 위치에 마커 생성
                        var newMarker = new Tmapv2.Marker({
                            position: new Tmapv2.LatLng(lat, lon),
                            map: map
                        });
                        markers.push(newMarker);
                        // 기존 경로 제거 후 새로운 경로 그리기
                        drawRoute(lat, lon);
                    }
                },
                error:function(request,status,error){
                    console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                }
            });
        }

        function drawRoute(destLat, destLon) {
            var headers = {}; 
            headers["appKey"] = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0";

            var startX = markers[0].getPosition()._lng;
            var startY = markers[0].getPosition()._lat;

            var endX = destLon;
            var endY = destLat;

            var paramOption = "car";
                
            $.ajax({
                method:"POST",
                headers : headers,
                url:"https://apis.openapi.sk.com/tmap/routes?version=1&format=html",
                async:false,
                data:{
                    "startX" : startX,
                    "startY" : startY,
                    "endX" : endX,
                    "endY" : endY,
                    "reqCoordType" : "WGS84GEO",
                    "resCoordType" : "EPSG3857",
                    "searchOption" : paramOption
                },
                success:function(response){
                    var resultData = response.features;

                    var tmap = new Tmapv2.Map("map_div", {
                        center: new Tmapv2.LatLng(startY, startX),
                        width: "100%",
                        height: "400px",
                        zoom: 15
                    });

                    var routeLayer = new Tmapv2.Graphics.Layer({name:"routeLayer"});
                    tmap.addLayer(routeLayer);
                        
                    var markerStartLayer = new Tmapv2.Graphics.Layer({name: "markerStartLayer"});
                    tmap.addLayer(markerStartLayer);

                    var size = new Tmapv2.base.Size(24, 38);
                    var offset = new Tmapv2.base.Pixel(-(size.w / 2), -size.h);
                    var icon = new Tmapv2.base.Icon('https://api2.sktelecom.com/tmap/images/start.png', size, offset);
                    var lonlat = new Tmapv2.base.LonLat(startX, startY).transform("EPSG4326_TO_EPSG3857");
                    var markerStart = new Tmapv2.Marker({position: new Tmapv2.LatLng(lonlat.lat, lonlat.lon), icon: icon});
                    markerStartLayer.addMarker(markerStart);

                    var markerEndLayer = new Tmapv2.Graphics.Layer({name: "markerEndLayer"});
                    tmap.addLayer(markerEndLayer);
                    var icon = new Tmapv2.base.Icon('https://api2.sktelecom.com/tmap/images/end.png', size, offset);
                    var lonlat = new Tmapv2.base.LonLat(endX, endY).transform("EPSG4326_TO_EPSG3857");
                    var markerEnd = new Tmapv2.Marker({position: new Tmapv2.LatLng(lonlat.lat, lonlat.lon), icon: icon});
                    markerEndLayer.addMarker(markerEnd);

                    var routeLineStyle = new Tmapv2.Graphics.LineStyle({strokeColor: "#dd00dd", strokeWeight: 6, strokeDashstyle: "solid", fill: true, fillColor: "#dd00dd", fillOpacity: 0.2});
                    var routeLayer = new Tmapv2.Graphics.Layer({name:"routeLine"});
                    tmap.addLayer(routeLayer);

                    for(var i in resultData){
                        var geometry = resultData[i].geometry;
                        var properties = resultData[i].properties;

                        if(geometry.type == "LineString"){
                            for(var j in geometry.coordinates){
                                var section = [];
                                var lineString = new Tmapv2.base.Geometry.LineString();

                                section[j] = geometry.coordinates[j];

                                var entry = new Tmapv2.base.Entry();
                                entry.totalDistance = properties.totalDistance;

                                for(var k in section){
                                    var order = section[k][0];
                                    var lon = section[k][1];
                                    var lat = section[k][2];

                                    var transform = new Tmapv2.Projection.convertEPSG3857ToWGS84GEO(new Tmapv2.base.Point(lon,lat));
                                    lineString.addPoint(new Tmapv2.base.Geometry.Point(transform._lon, transform._lat));

                                    entry.lon = transform._lon;
                                    entry.lat = transform._lat;
                                    entry.distance = properties.distance[k];

                                    lineString.entry = [];
                                    lineString.entry.push(entry);
                                    lineString.style = routeLineStyle;
                                }
                                routeLayer.addLine(lineString);
                            }
                        }
                    }
                },
                error:function(request,status,error){
                    console.log("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                }
            });
        }

        $(document).ready(function() {
            getUserLocation();
            $('#searchPOI').click(function() {
                searchPOI();
            });
        });

    </script>
    </head>
    <body>
        <div>
            <input type="text" id="searchKeyword" name="searchKeyword" value="">    
            <button id="searchPOI">적용하기</button>
        </div>
        <div id="map_div"></div>
    </body>
    </html>
    """
    # Jinja2 템플릿 엔진을 이용하여 데이터를 JSON 형식으로 변환
    rendered = render_template_string(html, locations=json.dumps(locations))
    return rendered

# 메인 모듈로 실행될 때 Flask 서버 구동
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
