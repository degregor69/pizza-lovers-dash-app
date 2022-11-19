import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

from methods.basic_data_functions import df_graph_top_5_by_rating
from methods.last_50_functions import have_changed_share, show_repartition, top_20_by_average_rate, create_last_50_df, top_5_district_by_comment_rate

# VARIABLES
df = create_last_50_df()
dash.register_page(__name__)

layout = html.Div(children=[
    html.H5(children="Nous analysons les derniers avis pour être au courant des dernières tendances."),
    html.H6(children="Les avis récents ont-il changé leur note ? La réponse est OUI !"),
    html.H6(children=[str(have_changed_share()) + "% " + "ont changé de note avec leurs 50 derniers commentaires."]),
    html.H6(children=[str(show_repartition("Better")) + "% " + "ont une meilleure note, " +  str(show_repartition("Worse")) + "% " + "en ont une moins bonne."]),

    dbc.Row([
        dbc.Col([
                html.Div([
                html.H4(children="TOP 5 DES RESTAURANTS"),
                html.H6(children='SELON LEUR NOTE'),
                html.Div(
                    dash.dcc.Dropdown(options= df['postal_code'].sort_values().unique(), id="last-50-district-filter-1", value = df['postal_code'].min())),
                    dcc.Graph(id='top-5-average-rate-last-50'),
            ]),
        ], width=3),

        dbc.Col([
            html.Div([
                html.H4(children='TOP 20 DES RESTAURANTS :'),
                html.H6(children='SELON LEUR NOTE'),
                dash_table.DataTable(top_20_by_average_rate().to_dict('records'), 
                    style_table={'overflowY': 'auto', 'height': '500px'},
                    style_data={'color': 'white','backgroundColor': 'black'},
                    style_header={'color': 'light-blue','backgroundColor': 'black'},
                    fixed_rows={'headers': True})
            ])
        ], width=6),

        dbc.Col([
            html.Div([
                html.H4(children='TOP 5 DES ARRONDISSEMENTS'),
                html.H6(children='SELON LEUR NOTE'),
                dcc.Graph(
                    figure= px.bar(top_5_district_by_comment_rate(df), 
                    x= top_5_district_by_comment_rate(df).index , y= top_5_district_by_comment_rate(df).values, barmode="group",
                    template='plotly_dark', range_y=[top_5_district_by_comment_rate(df).min() - 0.2 ,top_5_district_by_comment_rate(df).max()+0.2]),
                ),
            ])
        ],width=3),
        
    ])
])

@callback(
    Output('top-5-average-rate-last-50', 'figure'),
    Input('last-50-district-filter-1', 'value')
)

def update_figure_1(selected_district):
    filtered_df = df_graph_top_5_by_rating(df, selected_district)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='average_rate', barmode="group", template='plotly_dark'
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['average_rate'].min() - 0.2 ,5])
    
    return fig_1
