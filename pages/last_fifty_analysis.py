import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

from methods.last_50_functions import have_changed_share, show_repartition, top_20_by_average_rate, create_last_50_df, top_5_district_by_comment_rate, top_5_restaurant_by_comment_rate
# VARIABLES
df = create_last_50_df()

# -----------------
# STATIC GRAPHS
# -----------------

fig_district_top_5_comment_rate = px.bar(top_5_district_by_comment_rate(df), 
    x= top_5_district_by_comment_rate(df).index , y= top_5_district_by_comment_rate(df).values, barmode="group",labels={"x": "Arrondissement", "y": "Note moyenne"},
    range_y=[top_5_district_by_comment_rate(df).min() - 0.2 ,top_5_district_by_comment_rate(df).max()+0.2], )

fig_district_top_5_comment_rate.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, font_color="rgb(240,128,128)")
fig_district_top_5_comment_rate.update_traces(marker_color="rgb(240,128,128)")

# -----------------
# LAYOUT
# -----------------


dash.register_page(__name__,
    name = 'Analyses récentes')

layout = html.Div(children=[
    html.H6(children="Nous analysons les derniers avis pour être au courant des dernières tendances grâce à notre algorithme spécial."),
    html.Div([
        html.P(children=["Les avis récents ont-il changé leur note ? La réponse est OUI !"], style= {'margin-right': '5px'}),
        html.P(children=[str(have_changed_share()) + "% " + "ont changé de note avec leurs 50 derniers commentaires."], style= {'margin-right': '5px'}),
        html.P(children=[str(show_repartition("Better")) + "% " + "ont une meilleure note, " +  str(show_repartition("Worse")) + "% " + "en ont une moins bonne."],style= {'margin-right': '5px'}),
    ],className="d-flex flex-row"),
    dbc.Row([
        dbc.Col([
                html.Div([
                html.H6(children="TOP 5 DES RESTAURANTS"),
                html.P(children='Par arrondissement, selon leur dernière note moyenne.'),
                html.Div(
                    dash.dcc.Dropdown(options= df['postal_code'].sort_values().unique(), id="last-50-district-filter-1", value = df['postal_code'].min())),
                    dcc.Graph(id='top-5-average-rate-last-50'),
            ]),
        ], width=3),

        dbc.Col([
            html.Div([
                html.H6(children='TOP 20 DES RESTAURANTS'),
                html.P(children='Selon leur dernière note moyenne.'),
                dash_table.DataTable(top_20_by_average_rate().to_dict('records'), 
                    style_table={'overflowY': 'auto', 'height': '500px'},
                    style_data={'color': 'white','backgroundColor': 'black'},
                    style_header={'color': 'light-blue','backgroundColor': 'black'},
                    fixed_rows={'headers': True})
            ])
        ], width=6),

        dbc.Col([
            html.Div([
                html.H6(children='TOP 5 DES ARRONDISSEMENTS'),
                html.P(children='Selon leur dernière note moyenne.'),
                dcc.Graph(
                    figure= fig_district_top_5_comment_rate,
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
    filtered_df = top_5_restaurant_by_comment_rate(df, selected_district)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='comment_rate', barmode="group",
                 labels={
                     "name": "Nom",
                     "average_rate": "Note moyenne",
                 }
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['average_rate'].min() - 0.2 ,5])
    fig_1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, font_color="rgb(144,238,144)")
    fig_1.update_traces(marker_color="rgb(144,238,144)")
    
    return fig_1