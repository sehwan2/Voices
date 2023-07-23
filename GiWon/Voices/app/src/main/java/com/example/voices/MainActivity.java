package com.example.voices;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.LinearLayout;

import com.skt.tmap.TMapData;
import com.skt.tmap.TMapPoint;
import com.skt.tmap.TMapView;
import com.skt.tmap.overlay.TMapPolyLine;

public class MainActivity extends AppCompatActivity {

    private static final String TMAP_API_KEY = "PpgbRQ84nYWukHJFfAjA3gFoyXrOfLGazEWmhID0";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /*LinearLayout linearLayoutTmap = (LinearLayout)findViewById(R.id.linearLayoutTmap);
        TMapView tMapView = new TMapView(this);

        tMapView.setSKTMapApiKey( TMAP_API_KEY );
        linearLayoutTmap.addView( tMapView );
*/
        LinearLayout linearLayoutTmap = (LinearLayout)findViewById(R.id.linearLayoutTmap);
        TMapView tMapView = new TMapView(this);

        tMapView.setSKTMapApiKey(TMAP_API_KEY);
        linearLayoutTmap.addView(tMapView);

        // 출발지와 목적지 설정
        TMapPoint startPoint = new TMapPoint(37.570841, 126.985302); // 서울시청
        TMapPoint endPoint = new TMapPoint(37.551135, 126.988205); // 남산타워

        TMapData tmapdata = new TMapData();

        /*tmapdata.findPathDataWithType(TMapData.TMapPathType.PEDESTRIAN_PATH, startPoint, endPoint, new TMapData.FindPathDataListenerCallback() {
            @Override
            public void onFindPathData(TMapPolyLine polyLine) {
                tMapView.addTMapPath(polyLine);
            }
        });*/
    }
}