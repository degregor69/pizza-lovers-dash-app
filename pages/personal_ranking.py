import dash
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import os

from dash import html, dcc
from dash import html, dcc, callback, Input, Output
from methods.personal_ranking_functions  import personal_ranking_df_sorted_by_dynamic_rank, add_long_lat_to_df
from dotenv import load_dotenv

dash.register_page(__name__)

df = personal_ranking_df_sorted_by_dynamic_rank()
load_dotenv()
geo_df = add_long_lat_to_df()
load_dotenv()

px.set_mapbox_access_token(os.getenv('MAPBOX_TOKEN'))

fig = px.scatter_mapbox(geo_df, lat='long', lon='lat', zoom=11)


layout = html.Div(children=[
    html.H2(children='Nous développons des outils sur mesure !'),
    html.H3(''),
    html.H3(children="Les meilleures pizzerias par arrondissement selon notre algorithme"),
    html.Div([
            dcc.Graph(id="graph", figure=fig)
    ], className= "mw-50")
])


