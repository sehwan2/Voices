# Flask 및 기타 필요한 라이브러리 import
from flask import Flask, render_template_string, request

# Flask 앱 생성
app = Flask(__name__)

# 기본 라우트 정의. 해당 라우트는 메인 페이지를 반환
@app.route("/")
def map():
    # HTML + JavaScript 정의
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Simple Map</title>
    <!-- Tmap JavaScript API를 페이지에 로드 -->
    <script src="https://apis.openapi.sk.com/tmap/jsv2?version=1&appKey=PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0"></script>  <!-- Tmap JavaScript API를 로드. 사용자의 APP Key로 교체함. -->
    <style>
        /* 지도를 표시할 div 요소의 크기를 정의 */
        #map_div {
            width: 100%;
            height: 800px;
        }
    </style>
    <script type="text/javascript">
    /* 전역 변수 정의 */
    var map;
    var marker;

    /* 페이지가 로드될 때 실행되는 함수 정의 */
    function initTmap() {
        /* 지도 객체 생성 */
        map = new Tmapv2.Map("map_div", {
            /* 기본 중심좌표: 서울 */
            center: new Tmapv2.LatLng(37.566681, 126.978453),
            width: "100%",
            height: "800px",
            zoom: 16
        });

        /* Geolocation API를 사용하여 사용자의 현재 위치 정보를 얻음 */
        navigator.geolocation.getCurrentPosition(onSuccessGeolocation, onErrorGeolocation);
    }

    /* Geolocation 성공 시 실행되는 함수 정의 */
    function onSuccessGeolocation(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        /* 지도의 중심을 사용자의 현재 위치로 이동 */
        map.setCenter(new Tmapv2.LatLng(lat, lon));

        /* 사용자의 현재 위치에 특별한 아이콘으로 표시된 마커를 생성 */
        marker = new Tmapv2.Marker({
            position: new Tmapv2.LatLng(lat, lon),
            icon: "http://tmapapi.sktelecom.com/upload/tmap/marker/pin_r_m_s.png",
            map: map
        });
    }

    /* Geolocation 실패 시 실행되는 함수 정의 */
    function onErrorGeolocation() {
        alert("Geolocation failed. Please enable location services.");
    }

    /* 목적지 검색 함수 정의 */
    function searchPlace() {
        /* 텍스트 필드에서 목적지 정보를 가져옴 */
        var place = document.getElementById('place').value;

        /* 검색어를 URL 인코딩 */
        var encodedPlace = encodeURIComponent(place);

        /* Tmap POI 검색 API를 사용하여 목적지 검색 */
        var searchPoi = new Tmapv2.extension.Search({
            appKey: "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0",  // 사용자의 APP Key로 교체함.
            coord: new Tmapv2.LatLng(map.getCenter().lat(), map.getCenter().lng())
        });
        searchPoi.searchPOI(encodedPlace, function(res) {
            /* 검색 요청 및 응답을 콘솔에 출력 */
            console.log("Request: ", searchPoi);
            console.log("Response: ", res);
            /* 검색 결과 중 첫 번째 위치를 지도의 중심으로 설정하고 해당 위치에 마커를 생성 */
            if (res.poi) {
                var poi = res.poi[0];
                var latlon = new Tmapv2.LatLng(poi.noorLat, poi.noorLon);
                map.setCenter(latlon);
                if (!marker) {
                    marker = new Tmapv2.Marker({
                    position: latlon,
                    map: map
                    });
                } else {
                    marker.setPosition(latlon);
                }
            } else {
                alert("No results found.");
            }
        }, function(error) {
            /* 에러 핸들링: API 요청 자체에 문제가 생겼을 때 */
            console.error("Error occurred: ", error);
            alert("Error occurred while searching. Please try again.");
        });
    }

    </script>
    </head>
    <body onload="initTmap()">
        <div id="map_div"></div>
        <!-- 목적지 검색을 위한 텍스트 필드 및 검색 버튼 -->
        <div>
            <input type="text" id="place">
            <button onclick="searchPlace()">Search</button>
        </div>
    </body>
    </html>
    """
    # HTML 코드 반환
    return render_template_string(html)

# 메인 모듈로 실행되면 Flask 앱 실행
if __name__ == "__main__":
    app.run(debug=True)
