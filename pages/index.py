import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import pandas as pd

from methods.basic_data_functions import basic_data_df, \
                                        clean_basic_data_df, \
                                        create_city_and_postal_code_columns, \
                                        df_graph_top_5_by_rating, \
                                        df_graph_top_5_by_nb_reviews, \
                                        top_5_district_by_average_rate, \
                                        top_5_district_by_nb_reviews, \
                                        top_8_by_nb, \
                                        top_20_by_average_rate

df = create_city_and_postal_code_columns(clean_basic_data_df(basic_data_df()))
df_graph = df.drop(['address', 'city'], axis=1)

# -----------------
# STATIC GRAPHS
# -----------------

fig_district_top_5_rate = px.bar(top_5_district_by_average_rate(df_graph), 
    x= top_5_district_by_average_rate(df_graph).index , y= top_5_district_by_average_rate(df_graph).values, barmode="group",labels={"x": "Arrondissement", "y": "Note moyenne"},
    range_y=[top_5_district_by_average_rate(df_graph).min() - 0.2 ,top_5_district_by_average_rate(df_graph).max()+0.2], )

fig_district_top_5_rate.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, font_color="rgb(240,128,128)")
fig_district_top_5_rate.update_traces(marker_color="rgb(240,128,128)")

fig_district_top_5_reviews = px.bar(top_5_district_by_nb_reviews(df_graph), 

    x= top_5_district_by_nb_reviews(df_graph).index , y= top_5_district_by_nb_reviews(df_graph).values, barmode="group", labels={"x": "Arrondissement", "y": "Nombre de commentaires"},
    template='plotly_dark', range_y=[top_5_district_by_nb_reviews(df_graph).min() - 300 ,top_5_district_by_nb_reviews(df_graph).max()+ 300])
fig_district_top_5_reviews.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, font_color="rgb(240,128,128)")
fig_district_top_5_reviews.update_traces(marker_color="rgb(240,128,128)")

fig_pie_chart_top_8_district = figure= px.pie(top_8_by_nb(df_graph), values=top_8_by_nb(df_graph).values, names=top_8_by_nb(df_graph).index,
    color_discrete_sequence=px.colors.sequential.Greys)
fig_pie_chart_top_8_district.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
    font=dict(color="white"))

# -----------------
# STATIC TABS
# -----------------

top_20_tab = dash_table.DataTable(top_20_by_average_rate(df).to_dict('records'), 
    style_table={'overflowY': 'auto', 'height': '500px'},
    style_data={'color': 'white','backgroundColor': 'black'},
    style_header={'color': 'light-blue','backgroundColor': 'black'},
    fixed_rows={'headers': True})

# -----------------
# DISPLAY LAYOUT
# -----------------

dash.register_page(__name__)

layout = html.Div(children=[
    dbc.Row(html.H4(children='Dashboard des pizzerias parisiennes')),
    dbc.Row([
        dbc.Col([
             html.Div([
                html.H6(children="TOP 5 DES RESTAURANTS"),
                html.P(children='Par arrondissement, selon leur note.'),
                html.Div(
                    dash.dcc.Dropdown(options= df_graph['postal_code'].sort_values().unique(), id="district-filter-1", value = df_graph['postal_code'].min())),
                    dcc.Graph(id='top-5-average-rate-by-district-graph-with-dd'),
            ]),
        ], width=3),

        dbc.Col([
            html.Div([
                html.H6(children='TOP 20 DES RESTAURANTS'),
                html.P(children='Selon leur note, avec plus de 100 avis.'),
                html.Div(top_20_tab
                ),
            ])
        ], width=6),

        dbc.Col([
            html.Div([
                html.H6(children='TOP 5 DES ARRONDISSEMENTS'),
                html.P(children='Selon leur note moyenne.'),
                dcc.Graph(
                    figure= fig_district_top_5_rate,
                ),
            ])
        ],width=3),
    
    ], class_name='h-50'),

    html.Div(className='separation_div'),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H6(children="TOP 5 DES RESTAURANTS"),
                html.P(children='Par arrondissement, selon le nombre de commentaires.'),
                html.Div(
                dash.dcc.Dropdown(options= df_graph['postal_code'].sort_values().unique(), id="district-filter-2", value = df_graph['postal_code'].min())),
                dcc.Graph(id='top-5-nb-reviews-by-district-graph-with-dd'),
            ])
        ],width = 3),

        dbc.Col([
            html.Div([
                html.Div([
                html.H6(children='TOP 8 DES ARRONDISSEMENTS'),
                html.P(children='Selon le nombre de restaurants.'),
                dcc.Graph(figure= fig_pie_chart_top_8_district),
            ])
            ])
        ], width=6),

        dbc.Col([
            html.Div([
                html.H6(children='TOP 5 DES ARRONDISSEMENTS'),
                html.P(children='Selon le nombre de commentaires.'),
                dcc.Graph(
                    figure= fig_district_top_5_reviews
                ),
            ])
        ], width=3),
    
    ], class_name='h-50'),
])

# -----------
# CALLBACKS
# -----------s


@callback(
    Output('top-5-average-rate-by-district-graph-with-dd', 'figure'),
    Input('district-filter-1', 'value')
)

def update_figure_1(selected_district):
    filtered_df = df_graph_top_5_by_rating(df_graph, selected_district)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='average_rate', barmode="group",
                 labels={
                     "name": "Nom",
                     "average_rate": "Note moyenne",
                 }
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['average_rate'].min() - 0.2 ,5])
    fig_1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, font_color="rgb(144,238,144)")
    fig_1.update_traces(marker_color="rgb(144,238,144)")
    
    return fig_1

@callback(
    Output('top-5-nb-reviews-by-district-graph-with-dd', 'figure'),
    Input('district-filter-2', 'value')
)

def update_figure_2(selected_district):
    filtered_df = df_graph_top_5_by_nb_reviews(df_graph, selected_district)
    
    fig_2 = px.bar(filtered_df, 
                 x='name', y='nb_of_reviews', barmode="group",
                  labels={
                     "name": "Nom",
                     "nb_of_reviews": "Nombre de commentaires",
                 }
                )

    fig_2.update_layout(transition_duration=500, yaxis_range=[filtered_df['nb_of_reviews'].min()-300  , filtered_df['nb_of_reviews'].max()+300])
    fig_2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',}, font_color="rgb(144,238,144)")
    fig_2.update_traces(marker_color="rgb(144,238,144)")
    return fig_2