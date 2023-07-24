import geopandas as gpd

# 파일을 불러옵니다.
gdf = gpd.read_file("/Users/kimmo/K_circle/Voices/MINO/대구광역시_신호현시정보(SHP)_20230323/대구광역시_신호현시_20230323.shp")

# 데이터를 출력합니다.
print(gdf)

# DataFrame의 내용을 엑셀 파일로 저장합니다.
gdf.to_excel("output.xlsx")

print("파일이 성공적으로 생성되었습니다.")
