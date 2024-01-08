# Map Libraries
from branca.element import Figure
import folium as fl
from folium.plugins import MarkerCluster
from folium.features import CustomIcon

# Data Managment
import sqlite3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

scale = {'width':500, 'height':1000}
fig = Figure()
m = fl.Map(location = (4.6479362,-74.0868797), zoom_start=11)
fig.add_child(m)

con = sqlite3.connect('database.db')
df = pd.read_sql_query('select * from inmuebles', con)
geometry = [Point(lon, lat) for lon, lat in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

marker_cluster = MarkerCluster().add_to(m)


def html_creator(data):
    bathrooms = data.bathroomsNumber
    if data.bathroomsNumber < 1:
        bathrooms = 'N/A'
    html_str = f"""
    <p>Precio para: {str(data.rentType)} </p>
    <p>Precio: $ {data.price:,} </p>
    <p>Area: {str(data.area)} mt2</p>
    <p>Estrato: {str(data.stratum)} </p>
    <p>Numero de alcobas: {str(data.roomsNumber)} </p>
    <p>Numero de baños: {bathrooms} </p>
    <p>Numero de Parqueaderos: {str(data.parkingNumber)} </p>
    <p>Tipo de Propiedad: {str(data.propertyType)} </p>
    <p>URL: {str(data.url)} </p>
    """
    return html_str


for i in gdf.itertuples():
    iconMongo = CustomIcon('../img/mogus.png', icon_size=(15,15))
    iframe_html = html_creator(i)
    iframe = fl.IFrame(html = iframe_html, width=300, height=200)
    fl.Marker(location=(i.lat, i.lon),
              icon=iconMongo, popup=fl.Popup(iframe)).add_to(marker_cluster)

m.save('Inmuebles.html')
m.render()
