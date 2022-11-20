import dash
import plotly.graph_objects as go
import os

from dash import html, dcc
from dash import html, dcc, callback, Input, Output
from methods.personal_ranking_functions  import personal_ranking_df_sorted_by_dynamic_rank, add_long_lat_to_df
from dotenv import load_dotenv

dash.register_page(__name__,
    name = 'La solution LOVERS')

df = personal_ranking_df_sorted_by_dynamic_rank()
load_dotenv()
geo_df = add_long_lat_to_df()
load_dotenv()

# ------------------------
# CONFIGURATION OF THE MAP
# ------------------------

mapbox_access_token = os.getenv('MAPBOX_TOKEN')

fig = go.Figure(go.Scattermapbox(
    lat = geo_df['long'],
    lon = geo_df['lat'],
    text = geo_df['name'],
    mode = 'markers',
    marker=go.scattermapbox.Marker(
            size=15,
            color = ['rgb(240,128,128)',"rgb(144,238,144)", 'rgba(218,216,213,255)'] * 7
    ),
))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=48.866667,
            lon=2.333333
        ),
        pitch=0,
        zoom=11.5,
        style = 'mapbox://styles/mapbox/dark-v10',
    ),
    margin={"r":0,"t":0,"l":0,"b":0}
)

# ----------------
# LAYOUT
# ----------------


layout = html.Div(children=[
    html.H6("Les 20 meilleures pizzerias, selon notre propre algorithme."),
    html.P("Le tout, sur une carte."),
    dcc.Graph(
        figure= fig,
        className='graph-background'
    )
], className='graph_background')


