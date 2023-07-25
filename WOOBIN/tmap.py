# Python3 샘플 코드 #


import requests

url = 'http://api.data.go.kr/openapi/tn_pubr_public_traffic_light_api'
params ={'serviceKey' : 'EQnL7K2jUhuYu4RSZi0Zz0pZry3OerjJopbrTlA8VrQJjoXPIv%2FDJ7N22jOabS57YY5RdRxTjNKnu05hT570jQ%3D%3D', 'pageNo' : '1', 'numOfRows' : '100', 'type' : 'xml', 'ctprvnNm' : '', 'signguNm' : '', 'roadKnd' : '', 'roadRouteNo' : '', 'roadRouteNm' : '', 'roadRouteDrc' : '', 'rdnmadr' : '', 'lnmadr' : '', 'latitude' : '', 'longitude' : '', 'sgngnrInstlMthd' : '', 'roadType' : '', 'priorRoadYn' : '', 'tfclghtManageNo' : '', 'tfclghtSe' : '', 'tfclghtColorKnd' : '', 'sgnaspMthd' : '', 'sgnaspOrdr' : '', 'sgnaspTime' : '', 'sotKnd' : '', 'signlCtrlMthd' : '', 'signlTimeMthdType' : '', 'opratnYn' : '', 'flashingLightOpenHhmm' : '', 'flashingLightCloseHhmm' : '', 'fnctngSgngnrYn' : '', 'remndrIdctYn' : '', 'sondSgngnrYn' : '', 'drcbrdSn' : '', 'institutionNm' : '', 'phoneNumber' : '', 'referenceDate' : '', 'instt_code' : '' }

response = requests.get(url, params=params)
print(response.content)