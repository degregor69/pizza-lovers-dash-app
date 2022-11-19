import dash
from dash import html, dcc
from dash import html, dcc, callback, Input, Output

import plotly.express as px

from methods.personal_rankings_functions  import top_x_by_score_static_rate, top_x_by_score_dynamic_rate, personal_ranking_df_sorted_by_dynamic_rank

dash.register_page(__name__)

df = personal_ranking_df_sorted_by_dynamic_rank()

layout = html.Div(children=[
    html.H2(children='Nous développons des outils sur mesure !'),
    html.H3(''),
    html.H3(children="Les meilleures pizzerias par arrondissement selon notre algorithme"),
    html.Div(
        dash.dcc.Dropdown(options= df['postal_code'].sort_values().unique(), id="district-filter", value = df['postal_code'].min())),
        dcc.Graph(id='top-5-average-rate-personal-rankings'),

])

@callback(
    Output('top-5-average-rate-personal-rankings', 'figure'),
    Input('district-filter', 'value')
)

def update_figure_1(selected_district):
    filtered_df = top_x_by_score_dynamic_rate(5)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='last_score', barmode="group", template='plotly_dark'
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['last_score'].min() - 100,filtered_df['last_score'].max() +100 ])
    
    return fig_1