
import requests

url = 'http://api.data.go.kr/openapi/tn_pubr_public_crosswalk_api'
params ={
    'serviceKey' : 'vmN5SKYoq9qo7bloIS5rz16%2FBXO6wNUYd%2FPf%2FS1a64Z2rA3thWklP0cSPpdivNN2KwVRfRE2p2ZjSIiK86jEBA%3D%3D',
    'pageNo' : '1',
    'numOfRows' : '100',
    'type' : 'json',
    'ctprvnNm' : '',
    'signguNm' : '',
    'roadNm' : '',
    'rdnmadr' : '',
    'lnmadr' : '',
    'crslkManageNo' : '',
    'crslkKnd' : '',
    'bcyclCrslkCmbnatYn' : '',
    'highlandYn' : '',
    'latitude' : '',
    'longitude' : '',
    'cartrkCo' : '',
    'bt' : '',
    'et' : '',
    'tfclghtYn' : '',
    'fnctngSgngnrYn' : '',
    'sondSgngnrYn' : '',
    'greenSgngnrTime' : '',
    'redSgngnrTime' : '',
    'tfcilndYn' : '',
    'ftpthLowerYn' : '',
    'brllBlckYn' : '',
    'cnctrLghtFcltyYn' : '',
    'institutionNm' : '',
    'phoneNumber' : '',
    'referenceDate' : '',
    'instt_code' : '' }

response = requests.get(url, params=params)

print(response.text)

if response.status_code == 200:
    try:
        data = response.json()
        if isinstance(data, dict):
            for item in data.get('body', {}).get('items', []):
                crslkManageNo = item.get('crslkManageNo')
                latitude = item.get('latitude')
                longitude = item.get('longitude')
                print(f'crslkManageNo: {crslkManageNo}, latitude: {latitude}, longitude: {longitude}')
        else:
            print("Error: Invalid JSON data")
    except ValueError as e:
        print("Error: Failed to parse JSON data -", str(e))
else:
    print("Error:", response.status_code)