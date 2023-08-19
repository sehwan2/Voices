import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Web Conversion',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  LocationData? _currentLocation;
  late GoogleMapController _mapController;

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  _getCurrentLocation() async {
    final currentLocation = await fetchCurrentLocationFromTmap();
    setState(() {
      _currentLocation = currentLocation;
    });
  }

  Future<LocationData?> fetchCurrentLocationFromTmap() async {
    final url = 'TMAP_API_ENDPOINT';  // Tmap API endpoint를 입력해주세요.
    final response = await http.get(Uri.parse(url), headers: {
      'Authorization': 'PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0',  // 여기에 실제 Tmap API 키를 입력하세요.
    });

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      // API 응답 형식에 따라 적절하게 수정하세요.
      final latitude = data['latitude'];
      final longitude = data['longitude'];

      return LocationData.fromMap({
        'latitude': latitude,
        'longitude': longitude,
      });
    } else {
      print('Failed to fetch data from Tmap: ${response.body}');
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Voices"),
      ),
      body: ListView(
        children: [
          Group69(),
          SizedBox(height: 20),
          Text(
            'Flask로부터 가져온 데이터 또는 로직을 이 부분에 표시',
            textAlign: TextAlign.center,
          ),
          if (_currentLocation != null)
            Container(
              height: 300, // 원하는 높이로 조정
              child: GoogleMap(
                onMapCreated: (GoogleMapController controller) {
                  _mapController = controller;
                },
                initialCameraPosition: CameraPosition(
                  target: LatLng(_currentLocation!.latitude!, _currentLocation!.longitude!),
                  zoom: 14.0,
                ),
                markers: {
                  Marker(
                    markerId: MarkerId("current_location"),
                    position: LatLng(_currentLocation!.latitude!, _currentLocation!.longitude!),
                  )
                },
              ),
            ),
        ],
      ),
    );
  }
}

class Group69 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        Container(
          width: double.infinity, // 원래의 크기, 필요시 조정
          padding: EdgeInsets.all(16.0),
          child: Stack(
            children: [
              // 검색바 부분
              Container(
                width: 880,
                height: 127 / 3,
                padding: EdgeInsets.symmetric(horizontal: 128 / 3),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: TextField(
                  style: TextStyle(
                    fontSize: 50 / 3,
                    fontFamily: 'Noto Sans KR',
                    fontWeight: FontWeight.w300,
                  ),
                  decoration: InputDecoration(
                    hintText: '검색',
                    hintStyle: TextStyle(
                      color: Colors.black.withOpacity(0.5),
                      fontSize: 50 / 3,
                    ),
                    border: InputBorder.none,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

// 가상의 LocationData 클래스
class LocationData {
  final double? latitude;
  final double? longitude;

  LocationData({this.latitude, this.longitude});

  factory LocationData.fromMap(Map<String, dynamic> map) {
    return LocationData(
      latitude: map['latitude'],
      longitude: map['longitude'],
    );
  }
}
