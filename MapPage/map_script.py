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

con = sqlite3.connect('../MapPage/assets/db/database.db')
df = pd.read_sql_query('select * from inmuebles', con)
geometry = [Point(lon, lat) for lon, lat in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

marker_cluster = MarkerCluster().add_to(m)


def html_creator(data):
    bathrooms = data.bathroomsNumber
    rooms = data.roomsNumber
    parking = data.parkingNumber

    if data.bathroomsNumber < 1:
        bathrooms = 'N/A'
    if data.roomsNumber < 1:
        rooms = 'N/A'
    if data.parkingNumber < 1:
        parking = 'N/A'
    html_str = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Property Information</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background-color: #f2f2f2;
            }}

            td.url {{
                background-color: #e6f7ff; /* Light blue for URLs */
            }}
        </style>
    </head>
    <body>

    <!-- Create a table to organize property information -->
    <table>
        <tr>
            <th>Attribute</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Precio para</td>
            <td>{str(data.rentType)}</td>
        </tr>
        <tr>
            <td>Precio</td>
            <td>$ {data.price:,}</td>
        </tr>
        <tr>
            <td>Area</td>
            <td>{str(data.area)} mt2</td>
        </tr>
        <tr>
            <td>Estrato</td>
            <td>{str(data.stratum)}</td>
        </tr>
        <tr>
            <td>Numero de alcobas</td>
            <td>{str(rooms)}</td>
        </tr>
        <tr>
            <td>Numero de baños</td>
            <td>{str(bathrooms)}</td>
        </tr>
        <tr>
            <td>Numero de Parqueaderos</td>
            <td>{str(parking)}</td>
        </tr>
        <tr>
            <td>Tipo de Propiedad</td>
            <td>{str(data.propertyType)}</td>
        </tr>
        <tr>
            <td class="url">URL</td>
            <td class="url"><a href="{str(data.url)}">Enlace</a></td>
        </tr>
    </table>

    </body>
    </html>
    """
    return html_str


for i in gdf.itertuples():
    color = 'red'
    if i.rentType == 'Venta':
        color = 'blue'
    iframe_html = html_creator(i)
    iframe = fl.IFrame(html = iframe_html, width=400, height=600)
    fl.Marker(location=(i.lat, i.lon),
              icon=fl.Icon(icon='house', prefix = 'fa', color = color), popup=fl.Popup(iframe)).add_to(marker_cluster)

m.save('pages/Iframe.html')
m.render()
