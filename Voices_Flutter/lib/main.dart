import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';

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
    final userLocation = await _getUserLocation();
    if (userLocation != null) {
      setState(() {
        _currentLocation = userLocation;
      });
    } else {
      print("Failed to get user's location.");
    }
  }

  Future<LocationData?> _getUserLocation() async {
    Location location = new Location();
    bool _serviceEnabled;
    PermissionStatus _permissionGranted;
    LocationData _locationData;

    _serviceEnabled = await location.serviceEnabled();
    if (!_serviceEnabled) {
      _serviceEnabled = await location.requestService();
      if (!_serviceEnabled) {
        return null;
      }
    }

    _permissionGranted = await location.hasPermission();
    if (_permissionGranted == PermissionStatus.denied) {
      _permissionGranted = await location.requestPermission();
      if (_permissionGranted != PermissionStatus.granted) {
        return null;
      }
    }

    _locationData = await location.getLocation();
    return _locationData;
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
              height: 300,
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
          width: double.infinity,
          padding: EdgeInsets.all(16.0),
          child: Stack(
            children: [
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
