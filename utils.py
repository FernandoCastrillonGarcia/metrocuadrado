# Data Managment
import sqlite3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


con = sqlite3.connect('data/database.db')
cur = con.cursor()

query = """
SELECT 
    businessType,
    url,
    propertyType,
    builtArea,
    area,
    bathroomsNumber,
    roomsNumber,
    parkingNumber,
    price,
    stratum,
    lat,
    lon
FROM
    Properties
"""
Properties = pd.read_sql_query(query, con)

geometry = [Point(lon, lat) for lon, lat in zip(Properties['lon'], Properties['lat'])]
geoProperties = gpd.GeoDataFrame(Properties, geometry=geometry)

geoProperties.to_pickle('data/geoProperties.pkl')