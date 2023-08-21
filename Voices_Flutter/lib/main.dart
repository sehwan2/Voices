import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart' as loc;
import 'package:flutter_google_places/flutter_google_places.dart';
import 'package:google_maps_webservice/places.dart' as gmaps;
import 'package:http/http.dart' as http;
import 'package:flutter_polyline_points/flutter_polyline_points.dart'; // 추가

const kGoogleApiKey = "AIzaSyB06bzQkcsSutkjH0sZMEC2JX7hm0IGdjA";
gmaps.GoogleMapsPlaces _places = gmaps.GoogleMapsPlaces(apiKey: kGoogleApiKey);

void main() => runApp(MaterialApp(home: MyApp()));

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  TextEditingController searchController = TextEditingController();
  late GoogleMapController _mapController;
  loc.LocationData? _currentLocation;
  List<gmaps.Prediction> searchResults = [];
  Set<Polyline> _polylines = {}; // Polyline set
  PolylinePoints polylinePoints = PolylinePoints();

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  _getCurrentLocation() async {
    loc.Location location = loc.Location();
    bool _serviceEnabled;
    loc.PermissionStatus _permissionGranted;

    _serviceEnabled = await location.serviceEnabled();
    if (!_serviceEnabled) {
      _serviceEnabled = await location.requestService();
      if (!_serviceEnabled) return;
    }

    _permissionGranted = await location.hasPermission();
    if (_permissionGranted == loc.PermissionStatus.denied) {
      _permissionGranted = await location.requestPermission();
      if (_permissionGranted != loc.PermissionStatus.granted) return;
    }

    loc.LocationData locationData = await location.getLocation();
    setState(() {
      _currentLocation = locationData;
    });
  }

  _searchPlaces(String query) async {
    print("장소 검색 시작: $query");
    var url = Uri.parse(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            "?fields=formatted_address,name,rating,opening_hours,geometry"
            "&input=${Uri.encodeComponent(query)}"
            "&inputtype=textquery"
            "&key=$kGoogleApiKey"
    );

    try {
      var response = await http.get(url);
      var jsonResponse = json.decode(response.body);

      print("API 응답: ${jsonResponse.toString()}");  // 로그 출력

      if (jsonResponse["status"] == "OK") {
        setState(() {
          searchResults = jsonResponse["candidates"]
              .map<gmaps.Prediction>((data) => gmaps.Prediction.fromJson(data))
              .toList();
          print("검색 결과 수: ${searchResults.length}");  // 로그 출력
        });
      } else {
        print("API 오류: ${jsonResponse["status"]}");
      }
    } catch (e) {
      print("검색 중 오류 발생: $e");
    }
  }

    _addPolyline(gmaps.Prediction prediction) async {
    if (_currentLocation == null) return;

    // 장소 상세 정보 가져오기
    gmaps.PlacesDetailsResponse detail = await _places.getDetailsByPlaceId(prediction.placeId!);

    final lat = detail.result.geometry!.location.lat;
    final lng = detail.result.geometry!.location.lng;

    PolylineResult result = await polylinePoints.getRouteBetweenCoordinates(
      kGoogleApiKey,
      PointLatLng(_currentLocation!.latitude!, _currentLocation!.longitude!),
      PointLatLng(lat, lng),
      travelMode: TravelMode.driving,
    );

    if (result.points.isNotEmpty) {
      setState(() {
        _polylines.add(Polyline(
            polylineId: PolylineId(prediction.placeId!),
            points: result.points.map((point) =>
                LatLng(point.latitude, point.longitude)).toList(),
            color: Colors.blue,
            width: 5
        ));
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Voices'),
      ),
      body: GestureDetector(
        onTap: () {
          FocusScope.of(context).requestFocus(new FocusNode()); // 키보드 내리기
        },
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: searchController,
                onChanged: (value) {},
                onSubmitted: (value) {
                  _searchPlaces(value);
                },
                decoration: InputDecoration(
                  labelText: "검색",
                  border: OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(Icons.search),
                    onPressed: () {
                      print("검색 버튼 클림됨!");
                      _searchPlaces(searchController.text);
                    },
                  ),
                ),
              ),
            ),
            Expanded(
              child: _currentLocation == null
                  ? Center(child: CircularProgressIndicator())
                  : GoogleMap(
                onMapCreated: (GoogleMapController controller) {
                  _mapController = controller;
                },
                initialCameraPosition: CameraPosition(
                  target: LatLng(
                      _currentLocation!.latitude!,
                      _currentLocation!.longitude!),
                  zoom: 14.0,
                ),
                markers: {
                  Marker(
                    markerId: MarkerId("current_location"),
                    position: LatLng(
                        _currentLocation!.latitude!,
                        _currentLocation!.longitude!),
                  )
                },
                polylines: _polylines, // Polyline 추가
              ),
            ),
            Container(
              height: 200,
              child: ListView.builder(
                itemCount: searchResults.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(searchResults[index].description ?? ''),
                    onTap: () {
                      _addPolyline(searchResults[index]); // Polyline 그리기 함수 호출
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

