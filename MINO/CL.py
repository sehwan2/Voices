import pandas as pd
from pyproj import Transformer

def transform_coordinates(x, y, source_epsg, target_epsg):
    transformer = Transformer.from_crs(source_epsg, target_epsg, always_xy=True)
    target_x, target_y = transformer.transform(x, y)
    return target_x, target_y

# 파일 경로
file_path = "/Users/kimmo/K_Circle/Voices/MINO/A077_P_보행자작동신호기/A077_P.xlsx"

# 데이터 읽기
df = pd.read_excel(file_path)

# 좌표 변환
source_epsg = 5186  # GRS80 중부원점
target_epsg = 4326  # WGS84
transformed_coordinates = []

for i, row in df.iterrows():
    x, y = row['XCE'], row['YCE']
    target_x, target_y = transform_coordinates(x, y, source_epsg, target_epsg)
    transformed_coordinates.append((target_x, target_y))

# 변환된 좌표를 DataFrame에 추가
df['WGS84_Longitude'], df['WGS84_Latitude'] = zip(*transformed_coordinates)

# 결과 DataFrame을 새로운 Excel 파일로 저장
df.to_excel("/Users/kimmo/K_Circle/Voices/MINO/A077_P_보행자작동신호기/A077_P_converted.xlsx", index=False)
