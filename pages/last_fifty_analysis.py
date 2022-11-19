import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

from methods.basic_data_functions import df_graph_top_5_by_rating
from methods.personal_rankings_functions  import last_50_better_analysis, create_personal_ranking_df

# VARIABLES
df = create_personal_ranking_df()

dash.register_page(__name__)

layout = html.Div(children=[
    html.H3(children="PERFORMANCE SUR LES 50 DERNIERS AVIS"),
    html.H3(children="Les avis récents ont-il changé leur note ? La réponse est OUI !"),
    dcc.Graph(figure= px.pie(last_50_better_analysis(), values=last_50_better_analysis().values, names=last_50_better_analysis().index, template='plotly_dark')),

    html.H3(children="Les meilleures pizzerias par arrondissement par avis récent"),
    html.Div(
        dash.dcc.Dropdown(options= df['postal_code'].sort_values().unique(), id="last-district-filter-1", value = df['postal_code'].min())),
        dcc.Graph(id='last-top-5-average-rate-by-district-graph-with-dd'),
])

@callback(
    Output('last-top-5-average-rate-by-district-graph-with-dd', 'figure'),
    Input('last-district-filter-1', 'value')
)

def update_figure_1(selected_district):
    filtered_df = df_graph_top_5_by_rating(df, selected_district)
    
    fig_1 = px.bar(filtered_df, 
                 x='name', y='average_rate', barmode="group", template='plotly_dark'
                 )

    fig_1.update_layout(transition_duration=500, yaxis_range=[filtered_df['average_rate'].min() - 0.2 ,5])
    
    return fig_1
