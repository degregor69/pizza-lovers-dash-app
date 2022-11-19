import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import plotly.express as px

from methods.basic_data_functions import basic_data_df, \
                                        clean_basic_data_df, \
                                        create_city_and_postal_code_columns, \
                                        df_graph_top_5_by_rating, \
                                        df_graph_top_5_by_nb_reviews, \
                                        top_5_district_by_average_rate, \
                                        top_5_district_by_nb_reviews, \
                                        top_8_by_nb

df = create_city_and_postal_code_columns(clean_basic_data_df(basic_data_df()))
df_graph = df.drop(['address', 'city'], axis=1)

dash.register_page(__name__)

layout = html.Div(children=[
    dbc.Row(html.H4(children='ANALYSES GÉNÉRALES')),
    dbc.Row([
        dbc.Col([
             html.Div([
                html.H4(children="TOP 5 DES RESTAURANTS"),
                html.H6(children='SELON LEUR NOTE'),
                html.Div(
                    dash.dcc.Dropdown(options= df_graph['postal_code'].sort_values().unique(), id="district-filter-1", value = df_graph['postal_code'].min())),
                    dcc.Graph(id='top-5-average-rate-by-district-graph-with-dd'),
            ]),
        ], width=4),

        dbc.Col([
            html.Div([
                html.H4(children='TOP 8 DES ARRONDISSEMENTS'),
                html.H6(children='SELON LE NOMBRE DE RESTAURANTS'),
                dcc.Graph(figure= px.pie(top_8_by_nb(df_graph), values=top_8_by_nb(df_graph).values, names=top_8_by_nb(df_graph).index, template='plotly_dark')),
            ])
        ], width=4),

        dbc.Col([
            html.Div([
                html.H4(children='TOP 5 DES ARRONDISSEMENTS'),
                html.H6(children='SELON LEUR NOTE'),
                dcc.Graph(
                    figure= px.bar(top_5_district_by_average_rate(df_graph), 
                    x= top_5_district_by_average_rate(df_graph).index , y= top_5_district_by_average_rate(df_graph).values, barmode="group",
                    template='plotly_dark', range_y=[top_5_district_by_average_rate(df_graph).min() - 0.2 ,top_5_district_by_average_rate(df_graph).max()+0.2]),
                ),
            ])
        ],width=4),
    
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4(children="TOP 5"),
                html.H6(children='SELON LE NOMBRE DE COMMENTAIRES'),
                html.Div(
                dash.dcc.Dropdown(options= df_graph['postal_code'].sort_values().unique(), id="district-filter-2", value = df_graph['postal_code'].min())),
                dcc.Graph(id='top-5-nb-reviews-by-district-graph-with-dd'),
            ])
        ],width = 4),

        dbc.Col([
            html.Div([
                html.Div([
                html.H4(children='TOP 8 DES ARRONDISSEMENTS'),
                html.H6(children='SELON LE NOMBRE DE RESTAURANTS'),
                dcc.Graph(figure= px.pie(top_8_by_nb(df_graph), values=top_8_by_nb(df_graph).values, names=top_8_by_nb(df_graph).index, template='plotly_dark')),
            ])
            ])
        ], width=4),

        dbc.Col([
            html.Div([
                html.H4(children='TOP 5 DES ARRONDISSEMENTS'),
                html.H6(children='SELON LE NOMBRE DE COMMENTAIRES'),
                dcc.Graph(
                    figure= px.bar(top_5_district_by_nb_reviews(df_graph), 
                    x= top_5_district_by_nb_reviews(df_graph).index , y= top_5_district_by_nb_reviews(df_graph).values, barmode="group",
                    template='plotly_dark', range_y=[top_5_district_by_nb_reviews(df_graph).min() - 300 ,top_5_district_by_nb_reviews(df_graph).max()+ 300])
                ),
            ])
        ], width=4),
    
    ]),
])

@callback(
    Output('top-5-average-rate-by-district-graph-with-dd', 'figure'),
    Input('district-filter-1', 'value')
)

def update_figure_1(selected_district):
    filtered_df = df_graph_top_5_by_rating(df_graph, selected_district)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='average_rate', barmode="group", template='plotly_dark'
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['average_rate'].min() - 0.2 ,5])
    
    return fig_1

@callback(
    Output('top-5-nb-reviews-by-district-graph-with-dd', 'figure'),
    Input('district-filter-2', 'value')
)

def update_figure_2(selected_district):
    filtered_df = df_graph_top_5_by_nb_reviews(df_graph, selected_district)
    
    fig_2 = px.bar(filtered_df, 
                 x='name', y='nb_of_reviews', barmode="group", template='plotly_dark'
                )

    fig_2.update_layout(transition_duration=500, yaxis_range=[filtered_df['nb_of_reviews'].min()-300  , filtered_df['nb_of_reviews'].max()+300])

    return fig_2