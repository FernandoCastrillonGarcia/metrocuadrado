# %% 
# Map Libraries
from branca.element import Figure
import folium as fl
from folium.plugins import MarkerCluster

# Data Managment
import sqlite3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

scale = {'width':500, 'height':1000}
fig = Figure()
m = fl.Map(location = (4.6479362,-74.0868797), zoom_start=11)
fig.add_child(m)

con = sqlite3.connect('scrapper/results/database.db')
df = pd.read_sql_query('select * from inmuebles', con)
geometry = [Point(lon, lat) for lon, lat in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

marker_cluster = MarkerCluster().add_to(m)

for i in gdf.itertuples():
    iframe_html = f"""
    <p>Arriendo: $ {i.price:,} </p>
    <p>Area: {str(i.area)} mt2</p>
    <p>Estrato: {str(i.stratum)} </p>
    <p>Numero de alcobas: {str(i.roomsNumber)} </p>
    <p>Numero de baños: {i.bathroomsNumber} </p>
    <p>Numero de Parqueaderos: {str(i.parkingNumber)} </p>
    <p>Tipo de Propiedad: {str(i.propertyType)} </p>
    """
    XD = "<strong>XD</strong>"
    iframe = fl.IFrame(html = iframe_html, width=300, height=200)
    fl.Marker(location=(i.lat, i.lon),
              icon=fl.Icon(color='red'), popup=fl.Popup(iframe)).add_to(marker_cluster)

m.save('Inmuebles.html')

m
# %%
