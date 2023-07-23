import pandas as pd
from pyproj import CRS, Transformer

# Projection definition
epsg5186 = CRS("EPSG:5186") # GRS80, 중부원점
wgs84 = CRS("EPSG:4326") # WGS84

# Define transformer
transformer = Transformer.from_crs(epsg5186, wgs84)

# Read the csv file
df = pd.read_csv('A077_P(보행자작동신호기정보).csv')

# Convert the columns to numeric
df['X좌표'] = pd.to_numeric(df['X좌표'], errors='coerce')
df['Y좌표'] = pd.to_numeric(df['Y좌표'], errors='coerce')

# Remove rows with NaN values
df = df.dropna(subset=['X좌표', 'Y좌표'])

# Convert coordinates
df['lon'], df['lat'] = transformer.transform(df['X좌표'].to_list(), df['Y좌표'].to_list())

# Save the result to a new csv file
df.to_csv('transformed_coordinates.csv', index=False)
