# Map Libraries
from branca.element import Figure
import folium as fl
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, GroupedLayerControl

from tqdm import tqdm


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
            <td>{str(data.businessType)}</td>
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

legend_html = """
<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: auto; z-index:9999; font-size:14px;">
<i class="fa fa-home fa-2x" style="color:blue"></i> - Apartamento<br>
<i class="fa fa-home fa-2x" style="color:green"></i> - Casa<br>
<i class="fa fa-home fa-2x" style="color:red"></i> - Oficina<br>
<i class="fa fa-home fa-2x" style="color:purple"></i> - Bodega<br>
<i class="fa fa-home fa-2x" style="color:orange"></i> - Local Comercial<br>
<i class="fa fa-home fa-2x" style="color:gray"></i> - Lote o Casalote<br>
<i class="fa fa-home fa-2x" style="color:cyan"></i> - Edificio de Apartamentos<br>
<i class="fa fa-home fa-2x" style="color:pink"></i> - Consultorio<br>
<i class="fa fa-home fa-2x" style="color:brown"></i> - Edificio de Oficinas<br>
</div>
"""

propertyType_mapping = {
    'Apartamento': 'blue',
    'Casa': 'green',
    'Oficina': 'red',
    'Bodega': 'purple',
    'Local Comercial': 'orange',
    'Lote o Casalote': 'gray',
    'Edificio de Apartamentos': 'cadetblue',
    'Consultorio': 'pink',
    'Edificio de Oficinas': 'beige'
}

def create_map(df):
    businessType_list = df['businessType'].unique().tolist()
    propertyType_list = df['propertyType'].unique().tolist()
    m = fl.Map(
        location = (4.6479362,-74.0868797),
        zoom_start=11,
        control_scale=True,
        zoom_control=False,
        min_lat=4.4697,
        max_lat=4.8529,
        min_lon=-74.2508,
        max_lon=-74.0041)

    cluster = MarkerCluster(control=False).add_to(m)

    layers = {}
    sublayers = {}
    for B in businessType_list:
        layers[B] = FeatureGroupSubGroup(cluster, name = B).add_to(m)
        for P in propertyType_list:
            sublayers[f"{B}_{P}"] = FeatureGroupSubGroup(layers[B], name = P).add_to(m)

    for i in tqdm(df.itertuples()):
        # Get custom settings
        iframe_html = html_creator(i)

        # Add aesthetics to marker
        icon = fl.Icon(icon='house', color = propertyType_mapping[i.propertyType])
        iframe = fl.IFrame(html = iframe_html, width=400, height=600)
        popup = fl.Popup(iframe)
        P = i.propertyType
        B = i.businessType
        
        marker = fl.Marker(location=(i.lat, i.lon),
                    icon=icon, popup=fl.Popup(iframe)).add_to(sublayers[f"{B}_{P}"])

    for B in businessType_list:
        groups = {
            B: [value for k,value in sublayers.items() if f'{B}_' in k]
        }

        GroupedLayerControl(
            groups=groups,
            exclusive_groups=True,
            collapsed=True,
            position = 'topright'
        ).add_to(m)

    GroupedLayerControl(
            groups={'business': list(layers.values())},
            exclusive_groups=True,
            collapsed=True,
            position = 'topleft'
        ).add_to(m)

    m.get_root().html.add_child(fl.Element(legend_html))

    return m