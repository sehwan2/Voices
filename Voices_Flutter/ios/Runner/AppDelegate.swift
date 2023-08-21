import UIKit
import Flutter
import GoogleMaps  // <-- 이것을 추가하세요.

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {

        // Google Maps API Key를 여기에 추가하세요.
        GMSServices.provideAPIKey("AIzaSyB06bzQkcsSutkjH0sZMEC2JX7hm0IGdjA")

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
